"""Annotate paper.pdf with highlights from VERIFICATION.md flagged claims.

    python3 src/highlight_paper.py reviews/foo

Reads:
- reviews/<slug>/paper/paper.pdf
- reviews/<slug>/phase1/outputs/CLAIMS.md
- reviews/<slug>/phase2/outputs/VERIFICATION.md

Writes:
- reviews/<slug>/phase3/outputs/paper.highlighted.pdf

Highlight color encodes the most severe flagged error category per
`conventions/error_categories.md`:

  blue   (#4285F4) — unreferenced
  amber  (#FFBF00) — ambiguous
  orange (#FF6D00) — internal_contradiction
  red    (#D32F2F) — literature_collision
  purple (#7B1FA2) — domain_violation

Sentences with all CLEAR or no checker verdict get no highlight. Each highlight
carries a clickable annotation with the claim id, every flagged category, and
each checker's reasoning.

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

def parse_claims_md(path: Path) -> dict[str, dict]:
    """Return {claim_id: {sentence, page, line, type, hedged, confidence}}.

    CLAIMS.md is a markdown table; format per methodology/05-artifacts.md:
        | claim_id | type | sentence | hedged | confidence | page | line | section | provenance |
    """
    text = path.read_text()
    rows: dict[str, dict] = {}
    header = None
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(c.startswith("---") or set(c) <= set("- ") for c in cells if c):
            continue
        if header is None:
            header = [c.lower() for c in cells]
            continue
        row = dict(zip(header, cells))
        cid = row.get("claim_id", "").strip()
        if not cid or not cid.upper().startswith("C"):
            continue
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
    """Reduce per-category verdicts to a single per-claim verdict:
    FLAGGED > INCONCLUSIVE > CLEAR > NOT_CHECKED."""
    if not claim_record:
        return "NOT_CHECKED"
    verdicts = {c.get("verdict") for c in claim_record.values()}
    if "FLAGGED" in verdicts:
        return "FLAGGED"
    if "INCONCLUSIVE" in verdicts:
        return "INCONCLUSIVE"
    if "CLEAR" in verdicts:
        return "CLEAR"
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
        "skipped_no_flag": 0,    # all CLEAR or no checker verdict
        "skipped_no_match": 0,
        "skipped_no_page": 0,
    }

    for cid, claim in claims.items():
        record = verdicts.get(cid, {})
        category = most_severe_flagged(record)
        if category is None:
            counts["skipped_no_flag"] += 1
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

    claims = parse_claims_md(claims_md)
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
