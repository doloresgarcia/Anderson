"""Annotate paper.pdf with highlights from VERIFICATION.md findings.

    python3 src/highlight_paper.py reviews/foo

Reads:
- reviews/<slug>/paper/paper.pdf
- reviews/<slug>/phase1/outputs/CLAIMS.md
- reviews/<slug>/phase2/outputs/VERIFICATION.md

Writes:
- reviews/<slug>/phase3/outputs/paper.highlighted.pdf

Highlight color encodes the most severe flagged error category, or yellow when
the aggregate claim verdict is INCONCLUSIVE with no flagged category:

  blue   (#4285F4) — unreferenced
  amber  (#FFBF00) — ambiguous
  orange (#FF6D00) — internal_contradiction
  red    (#D32F2F) — literature_collision
  purple (#7B1FA2) — domain_violation
  yellow (#F1C40F) — INCONCLUSIVE

Sentences with all CLEAR or no checker verdict get no highlight. Each highlight
carries a clickable annotation with the claim id, every flagged/inconclusive
category, and each checker's reasoning.

Requires PyMuPDF: `pip install pymupdf`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Error categories — single source of truth in conventions/error_categories.md.
# Replicated here for the renderer; if you edit one, edit the other.
# ---------------------------------------------------------------------------

CATEGORIES = (
    "unreferenced",
    "ambiguous",
    "internal_contradiction",
    "literature_collision",
    "domain_violation",
)

# Severity ordered highest → lowest. The most-severe flagged category determines
# the highlight color when a claim is flagged in multiple categories.
SEVERITY = (
    "domain_violation",
    "literature_collision",
    "internal_contradiction",
    "ambiguous",
    "unreferenced",
)

CATEGORY_HEX = {
    "unreferenced":           "#4285F4",
    "ambiguous":              "#FFBF00",
    "internal_contradiction": "#FF6D00",
    "literature_collision":   "#D32F2F",
    "domain_violation":       "#7B1FA2",
}


def _hex_to_rgb01(hex_color: str) -> tuple[float, float, float]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


CATEGORY_RGB = {cat: _hex_to_rgb01(hx) for cat, hx in CATEGORY_HEX.items()}
CATEGORY_RGB["INCONCLUSIVE"] = _hex_to_rgb01("#F1C40F")


# Trust-score buckets, pinned to the older 4-color palette since they describe
# overall paper trust, not error categories.
TRUST_COLORS = {
    "high":   "#2ECC71",
    "medium": "#F1C40F",
    "low":    "#E74C3C",
    "none":   "#95A5A6",
}


# ---------------------------------------------------------------------------
# Parsers — CLAIMS.md (markdown table) and VERIFICATION.md (5-category sections).
# ---------------------------------------------------------------------------

class ClaimsParseError(ValueError):
    """Raised when CLAIMS.md cannot be parsed without risking bad columns."""


_CLAIM_ID_RE = re.compile(r"^C\d+$", re.IGNORECASE)


def _is_escaped(s: str, idx: int) -> bool:
    """True if s[idx] is preceded by an odd-length backslash run."""
    n = 0
    j = idx - 1
    while j >= 0 and s[j] == "\\":
        n += 1
        j -= 1
    return n % 2 == 1


def _split_markdown_table_row(line: str) -> list[str]:
    """Split one markdown table row without treating math/code pipes as cells.

    Literal pipes can be written as `\\|`. Unescaped pipes inside `$...$`,
    `$$...$$`, or backtick code spans are treated as cell content. Unescaped
    pipes in ordinary text remain separators; the fixed CLAIMS.md schema can
    then repair extra separators inside the free-text sentence column.
    """
    row = line.strip()
    if not row.startswith("|"):
        raise ClaimsParseError(f"not a markdown table row: {line!r}")

    start = 1
    end = len(row)
    if end > start and row.endswith("|") and not _is_escaped(row, end - 1):
        end -= 1

    cells: list[str] = []
    buf: list[str] = []
    math_delim: str | None = None
    code_ticks = 0
    i = start
    while i < end:
        ch = row[i]

        if ch == "\\" and i + 1 < end:
            nxt = row[i + 1]
            if nxt == "|":
                buf.append("|")
                i += 2
                continue
            if nxt in "$`":
                buf.append(ch)
                buf.append(nxt)
                i += 2
                continue
            buf.append(ch)
            i += 1
            continue

        if ch == "`" and math_delim is None:
            j = i
            while j < end and row[j] == "`":
                j += 1
            run = j - i
            if code_ticks == 0:
                code_ticks = run
            elif run == code_ticks:
                code_ticks = 0
            buf.append(row[i:j])
            i = j
            continue

        if ch == "$" and code_ticks == 0:
            delim = "$$" if i + 1 < end and row[i + 1] == "$" else "$"
            if math_delim is None:
                math_delim = delim
            elif math_delim == delim:
                math_delim = None
            buf.append(delim)
            i += len(delim)
            continue

        if ch == "|" and code_ticks == 0 and math_delim is None:
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue

        buf.append(ch)
        i += 1

    cells.append("".join(buf).strip())
    return cells


def _is_separator_row(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells if c)


def _claim_cells_from_schema(
    cells: list[str],
    header: list[str],
    path: Path,
    line_no: int,
) -> list[str]:
    """Return cells aligned to header or raise a visible parse error.

    CLAIMS.md has one known free-text column, `sentence`. If a row has extra
    cells, treat the extras as unescaped literal pipes in that column and keep
    the stable columns on either side. Rows that still do not look like claim
    rows after repair fail rather than silently shifting data.
    """
    expected = len(header)
    if len(cells) == expected:
        return cells

    if "sentence" in header and len(cells) > expected:
        sentence_idx = header.index("sentence")
        after = expected - sentence_idx - 1
        if len(cells) >= sentence_idx + 1 + after:
            tail_start = len(cells) - after if after else len(cells)
            repaired = [
                *cells[:sentence_idx],
                " | ".join(cells[sentence_idx:tail_start]).strip(),
                *cells[tail_start:],
            ]
            row = dict(zip(header, repaired))
            if (
                len(repaired) == expected
                and _CLAIM_ID_RE.match(row.get("claim_id", "").strip())
                and row.get("hedged", "").strip().lower() in {"true", "false"}
                and row.get("confidence", "").strip().lower() in {"high", "medium", "low"}
            ):
                return repaired

    raise ClaimsParseError(
        f"{path}:{line_no}: malformed CLAIMS.md row has {len(cells)} cells; "
        f"expected {expected}. Escape literal pipes as \\| or keep math pipes "
        "inside $...$."
    )

def parse_claims_md(path: Path) -> dict[str, dict]:
    """Return {claim_id: {sentence, page, line, type, hedged, confidence}}.

    CLAIMS.md is a markdown table; format per methodology/05-artifacts.md:
        | claim_id | type | sentence | hedged | confidence | page | line | section | provenance |
    """
    text = path.read_text()
    rows: dict[str, dict] = {}
    seen: dict[str, int] = {}
    header = None
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = _split_markdown_table_row(stripped)
        if _is_separator_row(cells):
            continue
        if header is None:
            header = [c.lower() for c in cells]
            missing = {"claim_id", "sentence"} - set(header)
            if missing:
                raise ClaimsParseError(
                    f"{path}:{line_no}: CLAIMS.md header missing columns: "
                    f"{', '.join(sorted(missing))}"
                )
            continue
        cells = _claim_cells_from_schema(cells, header, path, line_no)
        row = dict(zip(header, cells))
        cid = row.get("claim_id", "").strip().upper()
        if not cid or not cid.startswith("C"):
            continue
        if cid in rows:
            raise ClaimsParseError(
                f"{path}:{line_no}: duplicate claim_id {cid} "
                f"(first seen on line {seen[cid]})"
            )
        seen[cid] = line_no
        sentence = row.get("sentence", "").strip().strip('"').strip("'")
        try:
            page = int(row.get("page", "")) if row.get("page") else None
        except ValueError:
            page = None
        rows[cid] = {
            "sentence": sentence,
            "page": page,
            "line": row.get("line", ""),
            "type": row.get("type", ""),
            "hedged": row.get("hedged", "").lower() == "true",
            "confidence": row.get("confidence", "").lower(),
            "section": row.get("section", ""),
            "provenance": row.get("provenance", ""),
        }
    return rows


# Subsection header inside a category section:
#   ### C001 — FLAGGED — confidence: high
_SUBSECTION_RE = re.compile(
    r"^###\s+(C\d+)\s*[—–-]\s*(\w+)(?:\s*[—–-]\s*confidence:\s*(\w+))?",
    re.MULTILINE,
)
# Top-level section header (category):
#   ## unreferenced
_SECTION_RE = re.compile(r"^##\s+([\w_]+)\s*$", re.MULTILINE)


def _extract_field(body: str, key: str) -> str:
    """Pull a `- key: value` field out of a subsection body. value may span
    multiple lines (continuation indent or wrapped prose) until the next
    `- ` at column 0 (top-level list item) or end of body."""
    pattern = rf"^-\s*{re.escape(key)}\s*:\s*(.*?)(?=\n-\s\w|\Z)"
    m = re.search(pattern, body, re.MULTILINE | re.DOTALL)
    if not m:
        return ""
    val = m.group(1)
    if key in ("reasoning", "reason", "violated_principle", "canonical_source"):
        # prose: collapse continuation indents, strip
        return "\n".join(line.strip() for line in val.splitlines()).strip()
    return val.strip()


def parse_verification_md(path: Path) -> dict[str, dict[str, dict]]:
    """Return {claim_id: {category: {verdict, confidence, evidence, reasoning, …}}}.

    Sections are organized by category (per methodology/05-artifacts.md):

        ## unreferenced
        ### C001 — FLAGGED — confidence: high
        - evidence: paper.txt:42-44
        - reasoning: …

        ### C003 — CLEAR — confidence: high

        ## ambiguous
        ### C001 — INCONCLUSIVE — confidence: low
        - reason: ambiguous_wording
        - reasoning: …

    Returns empty dict if the file does not exist.
    """
    if not path.exists():
        return {}
    text = path.read_text()
    out: dict[str, dict[str, dict]] = {}

    sections = list(_SECTION_RE.finditer(text))
    for i, sec in enumerate(sections):
        category = sec.group(1).strip()
        if category not in CATEGORIES:
            continue
        body_start = sec.end()
        body_end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
        section_body = text[body_start:body_end]

        subs = list(_SUBSECTION_RE.finditer(section_body))
        for j, sub in enumerate(subs):
            cid = sub.group(1)
            verdict = sub.group(2).upper()
            confidence = (sub.group(3) or "").lower()
            sub_body_start = sub.end()
            sub_body_end = subs[j + 1].start() if j + 1 < len(subs) else len(section_body)
            sub_body = section_body[sub_body_start:sub_body_end]

            entry: dict = {"verdict": verdict, "confidence": confidence}
            for k in ("evidence", "reasoning", "reason",
                      "violated_principle", "canonical_source", "interpretations"):
                v = _extract_field(sub_body, k)
                if v:
                    entry[k] = v
            out.setdefault(cid, {})[category] = entry

    return out


# ---------------------------------------------------------------------------
# Per-claim aggregation helpers.
# ---------------------------------------------------------------------------

def claim_aggregate_verdict(claim_record: dict) -> str:
    """Reduce per-category verdicts to a single per-claim verdict.

    Precedence: FLAGGED > INCONCLUSIVE > CLEAR > NOT_CHECKED.

    A claim is only `CLEAR` if **all five checker categories** examined it
    and none flagged it. Partial coverage (e.g. only `unreferenced` ran
    and reported CLEAR while the other four categories never ran) yields
    `INCONCLUSIVE`, never `CLEAR` — the trust score is meant to require
    real verification, not "no checker objected because no checker ran."
    """
    if not claim_record:
        return "NOT_CHECKED"
    verdicts = {c.get("verdict") for c in claim_record.values()}
    if "FLAGGED" in verdicts:
        return "FLAGGED"
    if "INCONCLUSIVE" in verdicts:
        return "INCONCLUSIVE"
    if "CLEAR" in verdicts:
        # Only CLEAR if every category was examined and reported CLEAR.
        # Otherwise demote to INCONCLUSIVE — partial coverage never gets to
        # claim CLEAR (would inflate the trust score).
        examined = set(claim_record.keys())
        if examined >= set(CATEGORIES):
            return "CLEAR"
        return "INCONCLUSIVE"
    return "NOT_CHECKED"


def flagged_categories(claim_record: dict) -> list[str]:
    """Return the categories where this claim is FLAGGED, in severity order
    (highest severity first)."""
    flagged = [c for c, e in claim_record.items() if e.get("verdict") == "FLAGGED"]
    return sorted(flagged, key=lambda c: SEVERITY.index(c) if c in SEVERITY else 99)


def most_severe_flagged(claim_record: dict) -> str | None:
    """Return the most severe category where this claim is FLAGGED, or None."""
    cats = flagged_categories(claim_record)
    return cats[0] if cats else None


# ---------------------------------------------------------------------------
# Trust score.
# ---------------------------------------------------------------------------

def trust_score(verdicts: dict) -> dict:
    """Compute the trust score from per-claim verdict records.

    `verdicts` is the return value of `parse_verification_md`:
    `{claim_id: {category: {...}}}`.

    Per-claim aggregate (FLAGGED > INCONCLUSIVE > CLEAR > NOT_CHECKED) is
    weighted CLEAR=1.0, INCONCLUSIVE=0.5, FLAGGED=0.0; NOT_CHECKED is excluded.

    Buckets: ≥85 high (green), ≥60 medium (yellow), <60 low (red),
    no attempts → "none" (gray).
    """
    aggregates = {cid: claim_aggregate_verdict(rec) for cid, rec in verdicts.items()}
    clear        = sum(1 for v in aggregates.values() if v == "CLEAR")
    flagged      = sum(1 for v in aggregates.values() if v == "FLAGGED")
    inconclusive = sum(1 for v in aggregates.values() if v == "INCONCLUSIVE")
    not_checked  = sum(1 for v in aggregates.values() if v == "NOT_CHECKED")
    attempted = clear + flagged + inconclusive

    if attempted == 0:
        bucket = "none"
        score = None
    else:
        score = round(100 * (clear + 0.5 * inconclusive) / attempted)
        bucket = "high" if score >= 85 else ("medium" if score >= 60 else "low")

    return {
        "score": score,
        "bucket": bucket,
        "color": TRUST_COLORS[bucket],
        "clear": clear,
        "flagged": flagged,
        "inconclusive": inconclusive,
        "not_checked": not_checked,
        "attempted": attempted,
        "aggregates": aggregates,
    }


# ---------------------------------------------------------------------------
# Annotation text — the comment shown on a clicked highlight.
# ---------------------------------------------------------------------------

def build_annotation_text(cid: str, claim_record: dict) -> str:
    """Compose the comment shown when a reader clicks a highlighted sentence.

    Lists every flagged and inconclusive category with confidence and the
    checker's reasoning. CLEAR categories are not listed (no problem to
    describe).
    """
    flagged = [(c, claim_record[c]) for c in flagged_categories(claim_record)]
    inconclusive = [
        (c, claim_record[c])
        for c in CATEGORIES
        if claim_record.get(c, {}).get("verdict") == "INCONCLUSIVE"
    ]
    parts: list[str] = [cid]
    if flagged:
        parts.append("FLAGGED: " + ", ".join(c for c, _ in flagged))
    if inconclusive:
        parts.append("INCONCLUSIVE: " + ", ".join(c for c, _ in inconclusive))

    for cat, entry in flagged + inconclusive:
        parts.append("")
        header = f"[{cat}]"
        if entry.get("confidence"):
            header += f" confidence: {entry['confidence']}"
        parts.append(header)
        if entry.get("reasoning"):
            parts.append(entry["reasoning"])
        if entry.get("reason"):
            parts.append(f"reason: {entry['reason']}")
        if cat == "domain_violation" and entry.get("violated_principle"):
            parts.append(f"violated principle: {entry['violated_principle']}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# PDF synthesis: trust-score cover page + highlights on the original PDF.
# ---------------------------------------------------------------------------

def insert_trust_cover_page(doc, slug: str, t: dict) -> None:
    """Prepend a one-page trust-score cover to an open fitz document."""
    import fitz
    PAGE_W, PAGE_H = 595, 842
    page = doc.new_page(pno=0, width=PAGE_W, height=PAGE_H)

    page.insert_text(fitz.Point(60, 90),  "ANDERSON",
                     fontname="hebo", fontsize=14, color=(0.3, 0.3, 0.3))
    page.insert_text(fitz.Point(60, 110), "automated paper claim review",
                     fontname="helv", fontsize=10, color=(0.55, 0.55, 0.55))

    page.insert_text(fitz.Point(60, 170), slug,
                     fontname="hebo", fontsize=22, color=(0.1, 0.1, 0.1))

    score_str = f"{t['score']}" if t["score"] is not None else "-"
    label = {
        "high":   "HIGH TRUST",
        "medium": "MEDIUM TRUST",
        "low":    "LOW TRUST",
        "none":   "NOT YET CHECKED",
    }[t["bucket"]]
    color_rgb = _hex_to_rgb01(t["color"])

    band = fitz.Rect(60, 230, 535, 360)
    page.draw_rect(band, color=None, fill=color_rgb, fill_opacity=0.18)
    page.draw_rect(band, color=color_rgb, width=2)

    page.insert_text(fitz.Point(80, 285), score_str,
                     fontname="hebo", fontsize=68, color=color_rgb)
    page.insert_text(
        fitz.Point(80 + (180 if t["score"] is not None else 100), 285),
        "/ 100" if t["score"] is not None else "",
        fontname="helv", fontsize=20, color=(0.4, 0.4, 0.4),
    )
    page.insert_text(fitz.Point(80, 330), label,
                     fontname="hebo", fontsize=14, color=color_rgb)

    page.insert_text(
        fitz.Point(60, 400),
        f"{t['clear']} clear | {t['flagged']} flagged | {t['inconclusive']} inconclusive",
        fontname="helv", fontsize=12, color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        fitz.Point(60, 422),
        f"out of {t['attempted']} attempted checker verdicts",
        fontname="helv", fontsize=10, color=(0.5, 0.5, 0.5),
    )

    note = (
        "Trust score weighting: CLEAR = 1.0, INCONCLUSIVE = 0.5, FLAGGED = 0.0.\n"
        "NOT_CHECKED claims are excluded from the denominator.\n"
        "Buckets: 85+ high, 60+ medium, <60 low.\n"
        "\n"
        "Highlighted claims on the following pages - color encodes the most\n"
        "severe error category found by the five checker agents:\n"
        "    blue   - unreferenced (needs a citation)\n"
        "    amber  - ambiguous (unclear or underspecified)\n"
        "    orange - internal_contradiction (paper contradicts itself)\n"
        "    red    - literature_collision (conflicts with published work)\n"
        "    purple - domain_violation (conflicts with established knowledge)\n"
        "\n"
        "Click any highlight for the full per-category reasoning."
    )
    rect = fitz.Rect(60, 480, 535, 760)
    page.insert_textbox(rect, note, fontname="helv", fontsize=10,
                        color=(0.3, 0.3, 0.3), align=0)


def find_sentence_quads(page, sentence: str):
    """Return rectangles where the sentence appears on the page."""
    sentence = sentence.strip()
    if not sentence:
        return []
    rects = page.search_for(sentence, quads=False)
    if rects:
        return rects
    head = sentence[:50].rsplit(" ", 1)[0] if len(sentence) > 50 else sentence
    if head and head != sentence:
        rects = page.search_for(head, quads=False)
        if rects:
            return rects
    return []


def annotate_pdf(
    pdf_in: Path,
    pdf_out: Path,
    claims: dict[str, dict],
    verdicts: dict[str, dict],
    slug: str = "",
) -> dict:
    """Add highlights to pdf_in, write to pdf_out. Returns counts."""
    import fitz

    doc = fitz.open(pdf_in)
    counts = {
        "highlighted": 0,
        "skipped_no_finding": 0,  # all CLEAR or no checker verdict
        "skipped_no_match": 0,
        "skipped_no_page": 0,
    }

    for cid, claim in claims.items():
        record = verdicts.get(cid, {})
        category = most_severe_flagged(record)
        if category is None:
            if claim_aggregate_verdict(record) == "INCONCLUSIVE":
                category = "INCONCLUSIVE"
            else:
                counts["skipped_no_finding"] += 1
                continue
        page_num = claim.get("page")
        if page_num is None or page_num < 1 or page_num > len(doc):
            counts["skipped_no_page"] += 1
            continue
        page = doc[page_num - 1]
        rects = find_sentence_quads(page, claim["sentence"])
        if not rects:
            counts["skipped_no_match"] += 1
            continue
        annot = page.add_highlight_annot(rects)
        annot.set_colors(stroke=CATEGORY_RGB[category])
        annot.set_info(title="Anderson", content=build_annotation_text(cid, record))
        annot.update()
        counts["highlighted"] += 1

    # Cover page LAST so claim page numbers (referring to the original PDF)
    # remain valid while highlights are added.
    t = trust_score(verdicts)
    insert_trust_cover_page(doc, slug or "review", t)
    counts["trust_score"] = t["score"]
    counts["trust_bucket"] = t["bucket"]

    pdf_out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(pdf_out)
    doc.close()
    return counts


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("review_dir", type=Path, help="path to reviews/<slug>/")
    p.add_argument("--claims", type=Path, help="override CLAIMS.md path")
    p.add_argument("--verification", type=Path, help="override VERIFICATION.md path")
    p.add_argument("--pdf", type=Path, help="override input PDF path")
    p.add_argument("--out", type=Path, help="override output PDF path")
    args = p.parse_args()

    review = args.review_dir
    if not review.is_dir():
        print(f"error: {review} is not a directory", file=sys.stderr)
        return 2

    pdf_in = args.pdf or (review / "paper" / "paper.pdf")
    claims_md = args.claims or (review / "phase1" / "outputs" / "CLAIMS.md")
    verification_md = args.verification or (review / "phase2" / "outputs" / "VERIFICATION.md")
    pdf_out = args.out or (review / "phase3" / "outputs" / "paper.highlighted.pdf")

    for required, label in [(pdf_in, "PDF"), (claims_md, "CLAIMS.md")]:
        if not required.exists():
            print(f"error: {label} not found at {required}", file=sys.stderr)
            return 2

    try:
        claims = parse_claims_md(claims_md)
    except ClaimsParseError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    verdicts = parse_verification_md(verification_md)
    if not verdicts:
        print(f"warning: no verdicts found in {verification_md}; "
              f"highlights will be empty", file=sys.stderr)

    counts = annotate_pdf(pdf_in, pdf_out, claims, verdicts, slug=review.name)
    print(f"wrote {pdf_out}")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
