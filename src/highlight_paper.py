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
            "hedged": row.get("hedged", "").lower() == "true",
            "confidence": row.get("confidence", "").lower(),
        }
    return rows


def parse_verification_md(path: Path) -> dict[str, dict]:
    """Return {claim_id: {verdict, confidence, method, reason, reasoning}}.

    Section format per methodology/05-artifacts.md:

        ## C001 — VERDICT: FAIL — confidence: medium
        - method: numerical_recheck
        - reason: out_of_scope          (only on INCONCLUSIVE)
        - evidence:
          - paper.txt:142
        - reasoning: prose explaining the verdict; may span multiple lines.

    Returns empty dict if the file does not exist.
    """
    if not path.exists():
        return {}
    text = path.read_text()
    out: dict[str, dict] = {}

    header_re = re.compile(
        r"^##\s+(C\d+)\s*[—–-]\s*VERDICT:\s*(\w+)(?:\s*[—–-]\s*confidence:\s*(\w+))?",
        re.MULTILINE,
    )
    headers = list(header_re.finditer(text))
    for i, m in enumerate(headers):
        cid = m.group(1)
        verdict = m.group(2).upper()
        confidence = (m.group(3) or "").lower()
        body_start = m.end()
        body_end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[body_start:body_end]

        method_m = re.search(r"^-\s*method\s*:\s*([\w_]+)", body, re.MULTILINE)
        reason_m = re.search(r"^-\s*reason\s*:\s*([\w_:.\-]+)", body, re.MULTILINE)
        # Reasoning is prose, may span multiple lines until the next list item
        # or the next section header.
        reasoning_m = re.search(
            r"^-\s*reasoning\s*:\s*(.+?)(?=\n-\s|\n##\s|\Z)",
            body, re.MULTILINE | re.DOTALL,
        )

        reasoning = ""
        if reasoning_m:
            # Collapse continuation indents and trim trailing blank lines.
            raw = reasoning_m.group(1)
            reasoning = "\n".join(line.strip() for line in raw.splitlines()).strip()

        out[cid] = {
            "verdict": verdict,
            "confidence": confidence,
            "method": (method_m.group(1) if method_m else "").strip(),
            "reason": (reason_m.group(1) if reason_m else "").strip(),
            "reasoning": reasoning,
        }
    return out


# Canonical palette (graph_schema.md). Used for trust-score badging.
TRUST_COLORS = {
    "high":   "#2ECC71",
    "medium": "#F1C40F",
    "low":    "#E74C3C",
    "none":   "#95A5A6",
}


def trust_score(verdicts: dict) -> dict:
    """Compute the trust score from a dict of {claim_id: verdict_record}.

    Weighting:
      PASS         → 1.0
      INCONCLUSIVE → 0.5  (could be paywalled or ambiguous; partial credit)
      FAIL         → 0.0

    NOT_CHECKED claims are excluded from the denominator (no opinion).

    Buckets (pinned to the canonical palette):
      ≥ 85  →  high   (green)
      ≥ 60  →  medium (yellow)
      < 60  →  low    (red)
      no attempts → "none" (gray)

    Returns {score, bucket, color, passed, failed, inconclusive, attempted}.
    """
    passed = sum(1 for v in verdicts.values() if v.get("verdict") == "PASS")
    failed = sum(1 for v in verdicts.values() if v.get("verdict") == "FAIL")
    inconclusive = sum(1 for v in verdicts.values() if v.get("verdict") == "INCONCLUSIVE")
    attempted = passed + failed + inconclusive

    if attempted == 0:
        bucket = "none"
        score = None
    else:
        score = round(100 * (passed + 0.5 * inconclusive) / attempted)
        if score >= 85:
            bucket = "high"
        elif score >= 60:
            bucket = "medium"
        else:
            bucket = "low"

    return {
        "score": score,
        "bucket": bucket,
        "color": TRUST_COLORS[bucket],
        "passed": passed,
        "failed": failed,
        "inconclusive": inconclusive,
        "attempted": attempted,
    }


def build_annotation_text(cid: str, v: dict) -> str:
    """Compose the comment shown when a reader clicks a highlight.

    Layered: header line first (cid + verdict + confidence), then mechanical
    fields (method, reason), then the prose reasoning. Skips empty fields.
    """
    parts = [f"{cid} — VERDICT: {v.get('verdict', '')}"]
    if v.get("confidence"):
        parts[-1] += f" (confidence: {v['confidence']})"
    if v.get("method"):
        parts.append(f"method: {v['method']}")
    if v.get("reason"):
        parts.append(f"reason: {v['reason']}")
    if v.get("reasoning"):
        parts.append("")
        parts.append(v["reasoning"])
    return "\n".join(parts)


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


def _hex_to_rgb01(hex_color: str) -> tuple[float, float, float]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def insert_trust_cover_page(doc, slug: str, t: dict) -> None:
    """Prepend a one-page trust-score cover to an open fitz document."""
    import fitz
    PAGE_W, PAGE_H = 595, 842
    page = doc.new_page(pno=0, width=PAGE_W, height=PAGE_H)

    # Header strip
    page.insert_text(
        fitz.Point(60, 90),
        "ANDERSON",
        fontname="hebo", fontsize=14, color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        fitz.Point(60, 110),
        "automated paper claim review",
        fontname="helv", fontsize=10, color=(0.55, 0.55, 0.55),
    )

    # Big slug
    page.insert_text(
        fitz.Point(60, 170),
        slug,
        fontname="hebo", fontsize=22, color=(0.1, 0.1, 0.1),
    )

    # Big trust score
    score_str = f"{t['score']}" if t["score"] is not None else "—"
    label = {
        "high":   "HIGH TRUST",
        "medium": "MEDIUM TRUST",
        "low":    "LOW TRUST",
        "none":   "NOT YET CHECKED",
    }[t["bucket"]]
    color_rgb = _hex_to_rgb01(t["color"])

    # Colored score band.
    band = fitz.Rect(60, 230, 535, 360)
    page.draw_rect(band, color=None, fill=color_rgb, fill_opacity=0.18)
    page.draw_rect(band, color=color_rgb, width=2)

    page.insert_text(
        fitz.Point(80, 285),
        f"{score_str}",
        fontname="hebo", fontsize=68, color=color_rgb,
    )
    page.insert_text(
        fitz.Point(80 + (180 if t["score"] is not None else 100), 285),
        "/ 100" if t["score"] is not None else "",
        fontname="helv", fontsize=20, color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        fitz.Point(80, 330),
        label,
        fontname="hebo", fontsize=14, color=color_rgb,
    )

    # Breakdown lines.
    y = 400
    page.insert_text(
        fitz.Point(60, y),
        f"{t['passed']} pass | {t['failed']} fail | {t['inconclusive']} inconclusive",
        fontname="helv", fontsize=12, color=(0.2, 0.2, 0.2),
    )
    page.insert_text(
        fitz.Point(60, y + 22),
        f"out of {t['attempted']} attempted verifications",
        fontname="helv", fontsize=10, color=(0.5, 0.5, 0.5),
    )

    # Methodology note. ASCII-only to render reliably in all PDF viewers.
    note = (
        "Trust score weighting: PASS = 1.0, INCONCLUSIVE = 0.5, FAIL = 0.0.\n"
        "NOT_CHECKED claims are excluded from the denominator.\n"
        "Buckets: 85+ high, 60+ medium, <60 low.\n"
        "\n"
        "Highlighted claims on the following pages:\n"
        "    red    - verified FAIL (paper contradicts itself or external evidence)\n"
        "    yellow - INCONCLUSIVE (could not be decisively verified)\n"
        "Click any highlight for the verdict and the verifier's reasoning."
    )
    rect = fitz.Rect(60, 480, 535, 720)
    page.insert_textbox(
        rect, note, fontname="helv", fontsize=10,
        color=(0.3, 0.3, 0.3), align=0,
    )


def annotate_pdf(
    pdf_in: Path,
    pdf_out: Path,
    claims: dict[str, dict],
    verdicts: dict[str, dict],
    slug: str = "",
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
        annot.set_info(title="Anderson", content=build_annotation_text(cid, v))
        annot.update()
        counts["highlighted"] += 1

    # Prepend the trust-score cover page LAST so claim page numbers (which
    # refer to the original PDF) stay valid while we add highlights above.
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

    counts = annotate_pdf(pdf_in, pdf_out, claims, verdicts, slug=review.name)
    print(f"wrote {pdf_out}")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
