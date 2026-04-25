"""Annotate paper.pdf with highlights from VERIFICATION.md verdicts.

    python3 src/highlight_paper.py reviews/foo

Reads:
- reviews/<slug>/paper/paper.pdf
- reviews/<slug>/phase1/outputs/CLAIMS.md     (claim_id → sentence + page)
- reviews/<slug>/phase2/outputs/VERIFICATION.md (claim_id → verdict)

Writes:
- reviews/<slug>/phase3/outputs/paper.highlighted.pdf

Color palette is the canonical one from conventions/graph_schema.md:
  red    (#E74C3C) — FAIL
  yellow (#F1C40F) — INCONCLUSIVE
PASS and NOT_CHECKED produce no highlight (would be visual noise).

Each highlight carries a margin annotation pointing to the claim id and the
verdict, so the reader can cross-reference VERIFICATION.md.

Requires PyMuPDF: `pip install pymupdf`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Canonical palette (graph_schema.md). PyMuPDF wants RGB floats in [0, 1].
HIGHLIGHT_COLOR_RGB = {
    "FAIL":         (0.906, 0.298, 0.235),  # #E74C3C
    "INCONCLUSIVE": (0.945, 0.769, 0.059),  # #F1C40F
}


def parse_claims_md(path: Path) -> dict[str, dict]:
    """Return {claim_id: {sentence, page, line, type}} from CLAIMS.md.

    CLAIMS.md is a markdown table. Format per methodology/05-artifacts.md:
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
        }
    return rows


def parse_verification_md(path: Path) -> dict[str, dict]:
    """Return {claim_id: {verdict, reason}} from VERIFICATION.md.

    VERIFICATION.md has one section per claim, header format:
        ## C001 — VERDICT: FAIL — confidence: medium
    """
    if not path.exists():
        return {}
    text = path.read_text()
    out: dict[str, dict] = {}
    pattern = re.compile(
        r"^##\s+(C\d+)\s*[—–-]\s*VERDICT:\s*(\w+)(?:\s*[—–-]\s*confidence:\s*(\w+))?",
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        cid = m.group(1)
        verdict = m.group(2).upper()
        confidence = (m.group(3) or "").lower()
        out[cid] = {"verdict": verdict, "confidence": confidence}
    return out


def find_sentence_quads(page, sentence: str):
    """Return rectangles where the sentence appears on the page.

    PyMuPDF's `search_for` handles soft hyphens and many line-break edge cases,
    but not all. Falls back to a head-of-sentence search if the full match
    fails.
    """
    sentence = sentence.strip()
    if not sentence:
        return []
    rects = page.search_for(sentence, quads=False)
    if rects:
        return rects
    # Fallback: try the first ~50 chars (handles wrapping that breaks exact match).
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
) -> dict:
    """Add highlights to pdf_in, write to pdf_out. Returns counts."""
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_in)
    counts = {"highlighted": 0, "skipped_no_match": 0, "skipped_no_verdict": 0,
              "skipped_pass": 0, "skipped_no_page": 0}

    for cid, claim in claims.items():
        v = verdicts.get(cid)
        if v is None:
            counts["skipped_no_verdict"] += 1
            continue
        verdict = v["verdict"]
        if verdict not in HIGHLIGHT_COLOR_RGB:
            counts["skipped_pass"] += 1  # PASS or NOT_CHECKED
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
        r, g, b = HIGHLIGHT_COLOR_RGB[verdict]
        annot.set_colors(stroke=(r, g, b))
        annot.set_info(
            title="Anderson",
            content=f"{cid} — {verdict}" + (f" ({v['confidence']})" if v["confidence"] else ""),
        )
        annot.update()
        counts["highlighted"] += 1

    pdf_out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(pdf_out)
    doc.close()
    return counts


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("review_dir", type=Path,
                   help="path to reviews/<slug>/")
    p.add_argument("--claims", type=Path,
                   help="override CLAIMS.md path (default: <review>/phase1/outputs/CLAIMS.md)")
    p.add_argument("--verification", type=Path,
                   help="override VERIFICATION.md path (default: <review>/phase2/outputs/VERIFICATION.md)")
    p.add_argument("--pdf", type=Path,
                   help="override input PDF path (default: <review>/paper/paper.pdf)")
    p.add_argument("--out", type=Path,
                   help="override output PDF path (default: <review>/phase3/outputs/paper.highlighted.pdf)")
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
        print(f"warning: no verdicts found in {verification_md} "
              f"(file missing or no parsable sections); nothing to highlight",
              file=sys.stderr)

    counts = annotate_pdf(pdf_in, pdf_out, claims, verdicts)
    print(f"wrote {pdf_out}")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
