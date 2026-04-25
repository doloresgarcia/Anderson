#!/usr/bin/env python3
"""extract_claims.py — deterministic claim extraction from a LaTeX paper.

Pipeline:
    1. Parse with pylatexenc (AST, no macro expansion).
    2. Walk AST: emit structural claims (equations, captions, table cells,
       red-highlight markers); accumulate prose into paragraph buffers.
    3. For each prose paragraph: scispaCy sentence segmentation, lexical
       feature tagging, transition/roadmap filtering, dependency-tree
       compound-clause splitting, then emit prose claims.
    4. Output JSONL on stdout (or to -o path).

Usage:
    python extract_claims.py paper_highlighted_mistakes.tex > claims.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import spacy
from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.latexwalker import (
    LatexCharsNode,
    LatexEnvironmentNode,
    LatexGroupNode,
    LatexMacroNode,
    LatexMathNode,
    LatexNode,
    LatexWalker,
)


# ---------- Lexical patterns ----------

HEDGE_TERMS = {
    "may", "might", "could", "suggest", "suggests", "suggesting",
    "indicate", "indicates", "appear", "appears", "seem", "seems",
    "possibly", "likely", "perhaps", "plausibly", "presumably", "arguably",
}

FIRST_PERSON = {"we", "our", "ours", "us"}

# Words that, when leading a coordinated clause, signal the clause is
# semantically dependent on the main clause and shouldn't be split off.
SUBORDINATORS = {
    "so", "thus", "hence", "therefore", "consequently",
    "because", "although", "while", "since", "though",
    "whereas", "as", "if", "that",
}

TRANSITION_PAT = re.compile(
    r"^(in section|in this section|we now|recall|first[,]|second[,]|"
    r"third[,]|finally[,]|note that)\b",
    re.IGNORECASE,
)
ROADMAP_PAT = re.compile(
    r"\b(in this paper|the rest of this paper|the remainder of this paper|"
    r"we will discuss|we will present|the structure of this paper)\b",
    re.IGNORECASE,
)
DEFINITION_PAT = re.compile(
    r"\b(let .+ denote|let .+ be|we define|is defined as|we call)\b",
    re.IGNORECASE,
)
CONDITIONAL_START = re.compile(
    r"^(if|when|whenever|suppose|given that|assuming)\b",
    re.IGNORECASE,
)
NUMERIC_PAT = re.compile(r"\b\d[\d.,]*\s*%?")
CITE_TOKEN_PAT = re.compile(r"\[CITE:([^\]]+)\]")

SECTION_MACROS = {
    "section": 1, "section*": 1,
    "subsection": 2, "subsection*": 2,
    "subsubsection": 3, "subsubsection*": 3,
}

EQUATION_ENVS = {
    "align", "align*", "equation", "equation*",
    "gather", "gather*", "multline", "multline*",
}

CITE_MACROS = {"cite", "citep", "citet", "citealp", "citealt",
               "citeauthor", "citeyear", "citeyearpar"}

# Cross-reference macros: emit a generic <ref> placeholder so sentences
# don't fragment into "In Tab., we see..." when the ref is dropped.
REF_MACROS = {"ref", "eqref", "pageref", "autoref", "Cref", "cref",
              "nameref"}

# Macros to silently drop. Value = number of {arg} groups to consume
# from siblings (when pylatexenc didn't parse them via macro spec).
# Optional [opt] args are not counted; those are usually parsed correctly.
DROP_MACROS: dict[str, int] = {
    # Spacing / breaks
    "par": 0, "noindent": 0, "newline": 0, "linebreak": 0, "newpage": 0,
    "smallskip": 0, "medskip": 0, "bigskip": 0, "clearpage": 0,
    "vspace": 1, "hspace": 1,
    "qquad": 0, "qqquad": 0, "qqqquad": 0, "quad": 0, "dz": 0,
    "ding": 1, "checkmark": 0,
    # Layout
    "centering": 0, "raggedright": 0, "raggedleft": 0,
    "hline": 0, "toprule": 0, "midrule": 0, "bottomrule": 0, "cline": 1,
    "pagestyle": 1, "thispagestyle": 1,
    "fancyhead": 1, "fancyfoot": 1, "fancyhf": 1,
    "headrulewidth": 0, "footrulewidth": 0,
    # Sizing
    "footnotesize": 0, "small": 0, "normalsize": 0,
    "large": 0, "Large": 0, "LARGE": 0, "huge": 0, "Huge": 0, "tiny": 0,
    "scriptsize": 0,
    # Setup / preamble
    "graphicspath": 1, "bibliography": 1, "bibliographystyle": 1,
    "appendix": 0, "maketitle": 0, "tableofcontents": 0,
    "documentclass": 1, "usepackage": 1,
    "newcommand": 2, "renewcommand": 2, "providecommand": 2,
    "DeclareMathOperator": 2, "renewenvironment": 3, "newenvironment": 3,
    "setlength": 2, "addtolength": 2, "settowidth": 2,
    "pdfoutput": 0, "relax": 0, "protect": 0,
    "thanks": 1,
    # Counters / formatting
    "arabic": 1, "roman": 1, "Roman": 1, "alph": 1, "Alph": 1,
    # Cross-references in label/multi-file form (label IS dropped; ref is
    # handled separately via REF_MACROS to emit a placeholder)
    "label": 1, "input": 1, "include": 1, "subimport": 1,
    "author": 1, "title": 1, "date": 1, "affiliation": 1, "email": 1,
}

# Macros that wrap content we want passed through
PASSTHROUGH_MACROS = {
    "textbf", "textit", "emph", "underline", "texttt", "textsc",
    "textrm", "textsf", "textsl", "uppercase", "lowercase",
    "url", "href",  # treat as opaque text
}


# ---------- AST helpers ----------

_CONVERTER = LatexNodes2Text(strict_latex_spaces=False, keep_comments=False)


def line_for_pos(source: str, pos: int) -> int:
    return source.count("\n", 0, pos) + 1


def render_text(nodes: list[LatexNode]) -> str:
    if not nodes:
        return ""
    try:
        return _CONVERTER.nodelist_to_text(nodes)
    except Exception:
        return ""


def group_text(group: LatexNode | None) -> str:
    if group is None:
        return ""
    if isinstance(group, LatexGroupNode):
        return render_text(group.nodelist)
    return render_text([group])


def get_macro_args(node: LatexMacroNode, siblings: list[LatexNode],
                   idx: int, n_args: int,
                   prefer_groups: bool = False) -> tuple[list[LatexNode | None], int]:
    """Return (args, n_sibling_positions_consumed).

    pylatexenc parses args based on the macro spec; for macros it doesn't know
    about, args are absent and the {...} groups appear as separate sibling
    nodes. Some macros (\\section, \\subsection, ...) include star/optional
    flags in argnlist before the mandatory group — pass prefer_groups=True to
    pull only LatexGroupNode args (skipping star markers etc.).
    """
    args: list[LatexNode | None] = []
    if node.nodeargd and getattr(node.nodeargd, "argnlist", None):
        for a in node.nodeargd.argnlist:
            if a is None:
                continue
            if prefer_groups and not isinstance(a, LatexGroupNode):
                continue
            args.append(a)
        if len(args) >= n_args:
            return args[:n_args], 0

    j = idx + 1
    consumed = 0
    while j < len(siblings) and len(args) < n_args:
        sib = siblings[j]
        if isinstance(sib, LatexGroupNode):
            args.append(sib)
            j += 1
            consumed += 1
        elif isinstance(sib, LatexCharsNode) and sib.chars.strip() == "":
            j += 1
            consumed += 1
        else:
            break
    return args, consumed


# ---------- Walker ----------

class ClaimWalker:
    def __init__(self, source: str, source_path: str) -> None:
        self.source = source
        self.source_path = source_path
        self.section_stack: list[tuple[int, str]] = []
        self.claims: list[dict[str, Any]] = []
        self._next_id = 0
        self._para_chunks: list[str] = []
        self._para_start_pos: int | None = None
        self._nlp = None

    def nlp(self):
        if self._nlp is None:
            self._nlp = spacy.load("en_core_sci_sm")
        return self._nlp

    def claim_id(self) -> str:
        self._next_id += 1
        return f"claim-{self._next_id:04d}"

    @property
    def section_path(self) -> list[str]:
        return [t for _, t in self.section_stack]

    def update_section(self, level: int, title: str) -> None:
        while self.section_stack and self.section_stack[-1][0] >= level:
            self.section_stack.pop()
        self.section_stack.append((level, title))

    def emit(self, **fields: Any) -> None:
        """Append a claim record. Caller passes only the fields relevant to
        the claim's type — empty/false defaults are skipped at write time."""
        rec: dict[str, Any] = {
            "id": self.claim_id(),
            "section_path": list(self.section_path),
            **fields,
        }
        self.claims.append(rec)

    # ----- Main walk -----

    def walk(self, nodes: list[LatexNode]) -> None:
        i = 0
        while i < len(nodes):
            extra = self.handle_node(nodes, i)
            i += 1 + extra
        self.flush_paragraph()

    def handle_node(self, siblings: list[LatexNode], i: int) -> int:
        node = siblings[i]
        if isinstance(node, LatexCharsNode):
            return self._handle_chars(node)
        if isinstance(node, LatexMacroNode):
            return self._handle_macro(node, siblings, i)
        if isinstance(node, LatexEnvironmentNode):
            return self._handle_env(node)
        if isinstance(node, LatexMathNode):
            self._append_text(self.source[node.pos:node.pos + node.len], node.pos)
            return 0
        if isinstance(node, LatexGroupNode):
            self._walk_inline(node.nodelist)
            return 0
        return 0

    def _walk_inline(self, nodes: list[LatexNode]) -> None:
        i = 0
        while i < len(nodes):
            extra = self.handle_node(nodes, i)
            i += 1 + extra

    def _handle_chars(self, node: LatexCharsNode) -> int:
        chars = node.chars
        if "\n\n" in chars or re.search(r"\n\s*\n", chars):
            parts = re.split(r"\n\s*\n", chars)
            for k, part in enumerate(parts):
                self._append_text(part, node.pos)
                if k < len(parts) - 1:
                    self.flush_paragraph()
        else:
            self._append_text(chars, node.pos)
        return 0

    def _handle_macro(self, node: LatexMacroNode, siblings: list[LatexNode], i: int) -> int:
        name = node.macroname

        if name in SECTION_MACROS:
            args, consumed = get_macro_args(node, siblings, i, 1, prefer_groups=True)
            title = group_text(args[0] if args else None).strip()
            self.flush_paragraph()
            self.update_section(SECTION_MACROS[name], title)
            return consumed

        if name in CITE_MACROS:
            args, consumed = get_macro_args(node, siblings, i, 1)
            keys = group_text(args[0] if args else None) if args else ""
            for k in (k.strip() for k in keys.split(",")):
                if k:
                    self._append_text(f" [CITE:{k}] ", node.pos)
            return consumed

        if name in REF_MACROS:
            # Drop the ref arg but emit a placeholder so the host sentence
            # ("In Tab.~\ref{X}, we see…") flows correctly through the
            # sentence segmenter.
            _, consumed = get_macro_args(node, siblings, i, 1)
            self._append_text("<ref>", node.pos)
            return consumed

        if name == "footnote":
            # Treat the footnote as one prose unit. Render its content,
            # process through the prose pipeline as a separate paragraph,
            # but tag every claim with is_footnote=True. Don't poison the
            # surrounding paragraph buffer.
            args, consumed = get_macro_args(node, siblings, i, 1)
            if args and isinstance(args[0], LatexGroupNode):
                fn_text = self._render_footnote(args[0])
                if fn_text.strip():
                    self._process_paragraph(fn_text, node.pos, is_footnote=True)
            return consumed

        if name == "textcolor":
            # Pass content through; the color arg is ignored. Real papers
            # don't carry meaningful color semantics.
            args, consumed = get_macro_args(node, siblings, i, 2)
            content = args[1] if len(args) >= 2 else None
            if isinstance(content, LatexGroupNode):
                self._walk_inline(content.nodelist)
            elif content is not None:
                self._append_text(group_text(content), node.pos)
            return consumed

        if name in ("result", "bestresult"):
            args, consumed = get_macro_args(node, siblings, i, 2)
            val = group_text(args[0] if len(args) >= 1 else None).strip()
            err = group_text(args[1] if len(args) >= 2 else None).strip()
            text = f"{val} ± {err}" if err else val
            pos = node.pos
            end = node.pos + node.len + sum(
                getattr(s, "len", 0)
                for s in siblings[i + 1:i + 1 + consumed]
                if isinstance(s, LatexGroupNode)
            )
            rec = {
                "type": "table_cell",
                "text": text,
                "line": line_for_pos(self.source, pos),
                "value": val,
                "best": name == "bestresult",
            }
            if err:
                rec["error"] = err
            self.emit(**rec)
            self._append_text(f" {text} ", pos)
            return consumed

        if name == "caption":
            # captions inside figure/table envs are handled at env level;
            # if we hit one outside (rare), emit it
            args, consumed = get_macro_args(node, siblings, i, 1)
            cap_text = group_text(args[0] if args else None).strip()
            if cap_text:
                self.emit(
                    type="caption",
                    text=cap_text,
                    line=line_for_pos(self.source, node.pos),
                )
            return consumed

        if name in PASSTHROUGH_MACROS:
            args, consumed = get_macro_args(node, siblings, i, 1)
            if args and isinstance(args[0], LatexGroupNode):
                self._walk_inline(args[0].nodelist)
            elif args:
                self._append_text(group_text(args[0]), node.pos)
            return consumed

        if name in DROP_MACROS:
            n_args = DROP_MACROS[name]
            if n_args:
                _, consumed = get_macro_args(node, siblings, i, n_args)
                return consumed
            return 0

        # Unknown macro: try to render via latex2text, otherwise pass empty
        try:
            rendered = _CONVERTER.nodelist_to_text([node])
        except Exception:
            rendered = ""
        if rendered.strip():
            self._append_text(rendered, node.pos)
        return 0

    def _handle_env(self, node: LatexEnvironmentNode) -> int:
        env = node.environmentname
        pos = node.pos
        end = node.pos + node.len
        line = line_for_pos(self.source, pos)
        raw = self.source[pos:end]

        if env in EQUATION_ENVS:
            self.flush_paragraph()
            self.emit(
                type="equation",
                text=self.source[pos:end].strip(),
                line=line,
                env=env,
            )
            return 0

        if env in ("figure", "figure*"):
            self.flush_paragraph()
            cap = self._extract_caption(node.nodelist)
            if cap is not None:
                cap_text, cap_pos, _ = cap
                self.emit(
                    type="caption",
                    text=cap_text,
                    line=line_for_pos(self.source, cap_pos),
                    env=env,
                )
            return 0

        if env in ("table", "table*", "tabular"):
            self.flush_paragraph()
            cap = self._extract_caption(node.nodelist)
            if cap is not None:
                cap_text, cap_pos, _ = cap
                self.emit(
                    type="caption",
                    text=cap_text,
                    line=line_for_pos(self.source, cap_pos),
                    env=env,
                )
            # walk children for table_cell extraction, but skip the caption
            # macro itself to avoid double-emit
            children = [n for n in node.nodelist
                        if not (isinstance(n, LatexMacroNode) and n.macroname == "caption")]
            self._walk_inline(children)
            self.flush_paragraph()
            return 0

        if env in ("itemize", "enumerate", "description"):
            self.flush_paragraph()
            self._walk_inline(node.nodelist)
            self.flush_paragraph()
            return 0

        if env in ("abstract",):
            self.flush_paragraph()
            saved_section = list(self.section_stack)
            self.update_section(1, "Abstract")
            self._walk_inline(node.nodelist)
            self.flush_paragraph()
            self.section_stack = saved_section
            return 0

        # default: treat as inline content
        self._walk_inline(node.nodelist)
        return 0

    def _extract_caption(self, nodes: list[LatexNode]) -> tuple[str, int, int] | None:
        for idx, n in enumerate(nodes):
            if isinstance(n, LatexMacroNode) and n.macroname == "caption":
                args, _ = get_macro_args(n, nodes, idx, 1)
                if args:
                    cap = args[0]
                    text = group_text(cap).strip()
                    if isinstance(cap, LatexGroupNode):
                        return text, cap.pos, cap.pos + cap.len
                    return text, n.pos, n.pos + n.len
        return None

    def _render_footnote(self, group: LatexGroupNode) -> str:
        """Render footnote content to plain text with cite tokens preserved."""
        parts: list[str] = []
        for child in group.nodelist:
            if isinstance(child, LatexCharsNode):
                parts.append(child.chars)
            elif isinstance(child, LatexMacroNode):
                if child.macroname in CITE_MACROS:
                    args, _ = get_macro_args(child, group.nodelist,
                                             group.nodelist.index(child), 1)
                    keys = group_text(args[0] if args else None) if args else ""
                    for k in (k.strip() for k in keys.split(",")):
                        if k:
                            parts.append(f" [CITE:{k}] ")
                elif child.macroname in REF_MACROS:
                    parts.append("<ref>")
                elif child.macroname in DROP_MACROS:
                    pass
                else:
                    try:
                        parts.append(_CONVERTER.nodelist_to_text([child]))
                    except Exception:
                        pass
            elif isinstance(child, LatexMathNode):
                parts.append(self.source[child.pos:child.pos + child.len])
            elif isinstance(child, LatexGroupNode):
                parts.append(self._render_footnote(child))
        return "".join(parts)

    # ----- Paragraph buffer -----

    def _append_text(self, text: str, pos: int) -> None:
        if not text:
            return
        if self._para_start_pos is None:
            self._para_start_pos = pos
        self._para_chunks.append(text)

    def flush_paragraph(self) -> None:
        if not self._para_chunks:
            self._para_start_pos = None
            return
        full = "".join(self._para_chunks)
        base_pos = self._para_start_pos or 0
        self._para_chunks = []
        self._para_start_pos = None
        parts = re.split(r"\n\s*\n", full)
        cursor_in_full = 0
        for part in parts:
            stripped = part.strip()
            if stripped and len(stripped.split()) >= 3:
                self._process_paragraph(part, base_pos + cursor_in_full)
            cursor_in_full += len(part) + 2

    def _process_paragraph(self, raw: str, approx_pos: int,
                           is_footnote: bool = False) -> None:
        text_with_cites = re.sub(r"\s+", " ", raw).strip()
        if not text_with_cites:
            return
        nlp_text = CITE_TOKEN_PAT.sub("", text_with_cites)
        nlp_text = re.sub(r"\s+", " ", nlp_text).strip()
        if not nlp_text:
            return
        try:
            doc = self.nlp()(nlp_text)
        except Exception as e:
            print(f"  spacy error: {e}", file=sys.stderr)
            return
        emitted_texts: set[str] = set()
        for sent in doc.sents:
            self._process_sentence(sent, text_with_cites, approx_pos,
                                   is_footnote, emitted_texts)

    def _process_sentence(self, sent, full_para_with_cites: str,
                          approx_para_pos: int,
                          is_footnote: bool,
                          emitted_texts: set[str]) -> None:
        sent_text = sent.text.strip()
        if not sent_text or len(sent_text.split()) < 4:
            return

        lower = sent_text.lower()
        words = set(re.findall(r"[a-zA-Z']+", lower))

        # Filter transitions / roadmaps before doing more work.
        if TRANSITION_PAT.match(sent_text) or ROADMAP_PAT.search(sent_text):
            return

        has_hedge = bool(words & HEDGE_TERMS) or "suggest that" in lower or \
                    "appears to" in lower or "seems to" in lower
        is_definition = bool(DEFINITION_PAT.search(sent_text))

        if has_hedge:
            epistemic = "hedged"
        elif CONDITIONAL_START.match(sent_text):
            epistemic = "conditional"
        else:
            epistemic = "asserted"

        cite_keys = self._cites_for_sentence(sent_text, full_para_with_cites)
        is_first_person = bool(words & FIRST_PERSON)
        is_numeric = bool(NUMERIC_PAT.search(sent_text))

        sent_pos = approx_para_pos + sent.start_char
        line = line_for_pos(self.source, sent_pos) if sent_pos < len(self.source) else \
               line_for_pos(self.source, approx_para_pos)

        clauses = self._split_compound(sent)
        for clause in clauses:
            key = re.sub(r"\s+", " ", clause).strip().lower()
            if not key or key in emitted_texts:
                continue
            emitted_texts.add(key)
            self.emit(
                type="prose",
                text=clause,
                line=line,
                cite_keys=cite_keys,
                is_first_person=is_first_person,
                is_numeric=is_numeric,
                is_footnote=is_footnote,
                is_definition=is_definition,
                epistemic=epistemic,
            )

    def _cites_for_sentence(self, sent_text: str,
                            full_para_with_cites: str) -> list[str]:
        keys: list[str] = []
        for m in CITE_TOKEN_PAT.finditer(full_para_with_cites):
            window_start = max(0, m.start() - 80)
            window = full_para_with_cites[window_start:m.start()]
            window_clean = CITE_TOKEN_PAT.sub("", window).strip()
            tail = window_clean[-40:] if len(window_clean) >= 40 else window_clean
            if tail and tail in sent_text:
                for k in m.group(1).split(","):
                    k = k.strip()
                    if k and k not in keys:
                        keys.append(k)
        return keys

    def _split_compound(self, sent) -> list[str]:
        """Conservative split: break on top-level 'conj' deps whose head is a
        verb in the main clause and whose own subtree includes a subject."""
        sent_text = sent.text.strip()
        splits: list[Any] = []
        for tok in sent:
            if tok.dep_ != "conj":
                continue
            if tok.head.pos_ not in ("VERB", "AUX"):
                continue
            # Only split top-level coordination. Nested conj (X and Y and Z)
            # has Z's head=Y, which means head.dep_ == "conj", not ROOT.
            # Restricting to ROOT prevents overlapping subtree extraction.
            if tok.head.dep_ != "ROOT":
                continue
            has_subj = any(c.dep_ in ("nsubj", "nsubjpass", "csubj", "csubjpass")
                           for c in tok.subtree)
            if not has_subj:
                continue
            # Don't split off clauses that start with subordinators
            # ("so we stick to this term", "because X", "thus Y") — those
            # depend on the main clause for meaning.
            sub_tokens = [t for t in tok.subtree if t.dep_ != "cc"]
            if not sub_tokens:
                continue
            first_word = sub_tokens[0].text.lower()
            if first_word in SUBORDINATORS:
                continue
            splits.append(tok)

        if not splits:
            return [sent_text]

        conj_ids = {t.i for sp in splits for t in sp.subtree}
        base_tokens = [t for t in sent if t.i not in conj_ids]
        clauses: list[str] = []
        base_text = "".join(t.text_with_ws for t in base_tokens).strip(" ,;:.")
        # Splitting off a conj subtree often leaves a stranded coordinator
        # at the end of the base ("X, Y, and."). Strip it.
        base_text = re.sub(r"[\s,;:]+(and|or|but|nor|yet)\s*$", "",
                           base_text, flags=re.IGNORECASE).strip(" ,;:.")
        if base_text and len(base_text.split()) >= 5:
            clauses.append(base_text + ".")
        for sp in splits:
            sub_text = "".join(t.text_with_ws for t in sp.subtree).strip(" ,;:.")
            sub_text = re.sub(r"^(and|or|but|nor|yet)\s+", "",
                              sub_text, flags=re.IGNORECASE).strip(" ,;:.")
            if sub_text and len(sub_text.split()) >= 5:
                clauses.append(sub_text + ".")

        # If filtering left us with nothing or just one clause, fall back
        # to the unsplit sentence rather than emit nothing.
        return clauses if len(clauses) >= 2 else [sent_text]


# ---------- Entry point ----------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="Path to .tex file")
    ap.add_argument("-o", "--output", default="-",
                    help="Output JSONL path (default: stdout)")
    args = ap.parse_args()

    src_path = Path(args.source)
    source = src_path.read_text(encoding="utf-8")

    walker = LatexWalker(source, tolerant_parsing=True)
    nodes, _, _ = walker.get_latex_nodes()

    cw = ClaimWalker(source=source, source_path=src_path.name)
    cw.walk(nodes)

    out_stream = sys.stdout if args.output == "-" else open(args.output, "w", encoding="utf-8")
    try:
        for c in cw.claims:
            out_stream.write(json.dumps(c, ensure_ascii=False) + "\n")
    finally:
        if out_stream is not sys.stdout:
            out_stream.close()

    by_type: dict[str, int] = {}
    for c in cw.claims:
        by_type[c["type"]] = by_type.get(c["type"], 0) + 1
    print(f"Total claims: {len(cw.claims)}", file=sys.stderr)
    for t, n in sorted(by_type.items()):
        print(f"  {t}: {n}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
