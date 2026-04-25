"""Annotate paper.txt with highlights from VERIFICATION.md verdicts.

Plain-text counterpart to highlight_paper.py. Use when the paper was provided
as a .txt file (no PDF to annotate).

    python3 src/highlight_text.py reviews/foo

Reads:
- reviews/<slug>/paper/paper.txt
- reviews/<slug>/phase1/outputs/CLAIMS.md
- reviews/<slug>/phase2/outputs/VERIFICATION.md

Writes:
- reviews/<slug>/phase3/outputs/paper.highlighted.html
- reviews/<slug>/phase3/outputs/paper.highlighted.pdf  (if PyMuPDF available)

Color palette is the canonical one from conventions/graph_schema.md:
  red    (#E74C3C) — FAIL
  yellow (#F1C40F) — INCONCLUSIVE
PASS and NOT_CHECKED produce no highlight.

The HTML is self-contained (no JS, no CDN) — `<mark>` spans for the highlights,
anchor ids `claim-<id>`, and hover tooltips with the verdict.

The PDF is synthesized from paper.txt with PyMuPDF — A4, single column,
line-level highlight bands behind any line that contains a FAIL/INCONCLUSIVE
sentence. Line-level (not character-level) is intentional: with a plain-text
input we have no original layout to preserve, so coloring whole lines is both
robust and visually clearer than mid-line highlights in a synthesized PDF.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Reuse the parsers from highlight_paper.py (same CLAIMS.md / VERIFICATION.md
# format). Importing rather than duplicating keeps both renderers in sync.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from highlight_paper import (  # noqa: E402
    parse_claims_md,
    parse_verification_md,
    build_annotation_text,
    insert_trust_cover_page,
    trust_score,
)

# Canonical palette (graph_schema.md).
HIGHLIGHT_COLORS = {
    "FAIL":         "#E74C3C",
    "INCONCLUSIVE": "#F1C40F",
}


def find_ranges(text: str, claims: dict, verdicts: dict) -> list[tuple]:
    """Return [(start, end, claim_id, verdict, confidence), ...] sorted by
    start, with overlaps resolved by keeping the earlier-start range.

    Tries an exact literal match first; falls back to a whitespace-tolerant
    regex match (each whitespace run in the sentence allows any whitespace
    in the text, so soft-wrapped paragraphs match too).
    """
    ranges: list[tuple] = []
    for cid, claim in claims.items():
        v = verdicts.get(cid)
        if not v or v["verdict"] not in HIGHLIGHT_COLORS:
            continue
        sentence = (claim.get("sentence") or "").strip()
        if not sentence:
            continue

        idx = 0
        found = False
        while True:
            pos = text.find(sentence, idx)
            if pos == -1:
                break
            ranges.append((pos, pos + len(sentence), cid, v["verdict"], v.get("confidence", "")))
            idx = pos + len(sentence)
            found = True
        if found:
            continue

        # Whitespace-tolerant fallback for soft-wrapped sentences.
        words = sentence.split()
        if len(words) < 2:
            continue
        pattern = r"\s+".join(re.escape(w) for w in words)
        for m in re.finditer(pattern, text):
            ranges.append((m.start(), m.end(), cid, v["verdict"], v.get("confidence", "")))

    ranges.sort()
    merged: list[tuple] = []
    for r in ranges:
        if merged and r[0] < merged[-1][1]:
            continue  # overlap; keep the earlier one
        merged.append(r)
    return merged


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def char_range_to_lines(text: str, start: int, end: int) -> tuple[int, int]:
    """Return (start_line, end_line), 1-indexed, for a character range."""
    return text.count("\n", 0, start) + 1, text.count("\n", 0, end) + 1


def line_verdict_map(text: str, ranges: list[tuple]) -> dict[int, str]:
    """{line_number: verdict} for any line that intersects a highlight range.
    Lines spanning a FAIL keep FAIL even if also overlapped by INCONCLUSIVE."""
    out: dict[int, str] = {}
    for start, end, _cid, verdict, _conf in ranges:
        sl, el = char_range_to_lines(text, start, end)
        for ln in range(sl, el + 1):
            if out.get(ln) == "FAIL":
                continue
            out[ln] = verdict
    return out


def _wrap_line(line: str, max_chars: int) -> list[str]:
    """Soft-wrap a line at the last space before `max_chars`. Preserves
    leading whitespace by keeping wrapped continuations starting at column 0."""
    if len(line) <= max_chars:
        return [line]
    out: list[str] = []
    cursor = 0
    while cursor < len(line):
        if len(line) - cursor <= max_chars:
            out.append(line[cursor:])
            break
        idx = line.rfind(" ", cursor, cursor + max_chars + 1)
        if idx > cursor:
            out.append(line[cursor:idx])
            cursor = idx + 1
        else:
            out.append(line[cursor:cursor + max_chars])
            cursor += max_chars
    return out


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Anderson — highlighted paper: {slug}</title>
<style>
  body {{
    font-family: Georgia, serif;
    font-size: 15px; line-height: 1.55;
    max-width: 880px; margin: 40px auto 80px; padding: 0 24px;
    color: #1a1a1a;
  }}
  h1 {{ font-size: 18px; color: #555; margin-bottom: 4px; }}
  .meta {{ color: #888; font-size: 12px; margin-bottom: 24px; }}
  pre {{
    white-space: pre-wrap;
    font-family: Georgia, serif;
    font-size: 15px; line-height: 1.55;
    margin: 0;
  }}
  mark {{
    border-radius: 2px;
    padding: 1px 2px;
    color: #1a1a1a;
    text-decoration: none;
  }}
  mark.fail         {{ background-color: #E74C3C; color: #fff; }}
  mark.inconclusive {{ background-color: #F1C40F; color: #1a1a1a; }}
  mark sup {{
    font-size: 9px; font-weight: bold;
    margin-left: 2px; opacity: 0.85;
  }}
  #legend {{
    position: fixed; top: 20px; right: 20px;
    background: white; padding: 8px 12px;
    border: 1px solid #d0d0d0; border-radius: 4px;
    font-family: system-ui, sans-serif; font-size: 11px;
    box-shadow: 0 2px 6px rgba(0,0,0,.08);
  }}
  #legend .swatch {{ display: inline-block; width: 12px; height: 12px;
    vertical-align: middle; margin-right: 4px; border-radius: 2px; }}
  #legend .row {{ margin: 2px 0; }}
</style>
</head>
<body>
<h1>{slug}</h1>
<div class="meta">{count_fail} FAIL · {count_inconclusive} INCONCLUSIVE highlighted. Hover for verdict.</div>
<div id="legend">
  <div class="row"><span class="swatch" style="background:#E74C3C"></span>FAIL</div>
  <div class="row"><span class="swatch" style="background:#F1C40F"></span>INCONCLUSIVE</div>
</div>
<pre>{body}</pre>
</body>
</html>
"""


# Canonical palette as PyMuPDF RGB floats in [0, 1].
_PDF_RGB = {
    "FAIL":         (0.906, 0.298, 0.235),  # #E74C3C
    "INCONCLUSIVE": (0.945, 0.769, 0.059),  # #F1C40F
}


def synthesize_pdf(
    text: str,
    ranges: list[tuple],
    verdicts: dict,
    out_path: Path,
    slug: str,
) -> dict:
    """Synthesize a PDF from paper.txt with line-level highlight bands and a
    margin sticky-note per highlighted claim describing the verdict.

    Layout is intentionally minimal: A4, single column, Helvetica 10pt, lines
    wrapped at ~85 characters. Any line that intersects a FAIL or
    INCONCLUSIVE highlight range gets a colored band; the first line of each
    flagged claim also gets a clickable sticky-note annotation whose content
    is the full verdict + reasoning from VERIFICATION.md (built by
    `build_annotation_text`).
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise RuntimeError(
            "PyMuPDF not installed; cannot produce PDF. "
            "Install with: pip install pymupdf"
        )

    PAGE_W, PAGE_H = 595, 842        # A4 in points
    MARGIN = 60
    FONT_NAME = "helv"
    FONT_SIZE = 10
    LINE_H = 13
    MAX_CHARS = 85

    line_verdicts = line_verdict_map(text, ranges)

    # First line per claim_id, for sticky-note placement.
    first_line_per_cid: dict[str, int] = {}
    for start, end, cid, _verdict, _conf in ranges:
        sl, _ = char_range_to_lines(text, start, end)
        first_line_per_cid.setdefault(cid, sl)

    counts = {
        "FAIL":              sum(1 for v in line_verdicts.values() if v == "FAIL"),
        "INCONCLUSIVE":      sum(1 for v in line_verdicts.values() if v == "INCONCLUSIVE"),
        "highlighted_lines": len(line_verdicts),
        "annotations":       len(first_line_per_cid),
    }

    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = MARGIN

    # Header
    page.insert_text(
        fitz.Point(MARGIN, y),
        f"Anderson — highlighted paper: {slug}",
        fontname=FONT_NAME, fontsize=12, color=(0.3, 0.3, 0.3),
    )
    y += LINE_H * 2

    # We need to know which claims attach to which original line, so we emit
    # the sticky note exactly once per claim at its first occurrence.
    line_to_cids: dict[int, list[str]] = {}
    for cid, ln in first_line_per_cid.items():
        line_to_cids.setdefault(ln, []).append(cid)

    placed_annots: set[str] = set()

    for orig_no, raw_line in enumerate(text.splitlines(), start=1):
        verdict = line_verdicts.get(orig_no)
        wrapped_lines = _wrap_line(raw_line if raw_line else " ", MAX_CHARS)
        for sub_idx, wrapped in enumerate(wrapped_lines):
            if y + LINE_H > PAGE_H - MARGIN:
                page = doc.new_page(width=PAGE_W, height=PAGE_H)
                y = MARGIN

            if verdict:
                rgb = _PDF_RGB[verdict]
                rect = fitz.Rect(
                    MARGIN - 3, y - LINE_H + 3,
                    PAGE_W - MARGIN + 3, y + 4,
                )
                page.draw_rect(rect, color=None, fill=rgb, fill_opacity=0.35)

            page.insert_text(
                fitz.Point(MARGIN, y),
                wrapped,
                fontname=FONT_NAME, fontsize=FONT_SIZE,
            )

            # Place sticky notes on the first wrapped sub-line of the original
            # line that owns the claim's first occurrence.
            if sub_idx == 0 and orig_no in line_to_cids:
                for cid in line_to_cids[orig_no]:
                    if cid in placed_annots:
                        continue
                    placed_annots.add(cid)
                    v = verdicts.get(cid, {})
                    note_point = fitz.Point(PAGE_W - MARGIN + 8, y - 4)
                    annot = page.add_text_annot(note_point, build_annotation_text(cid, v))
                    annot.set_info(title=f"Anderson · {cid}")
                    rgb = _PDF_RGB.get(v.get("verdict", ""), (0.6, 0.6, 0.6))
                    annot.set_colors(stroke=rgb)
                    annot.update()

            y += LINE_H

    # Prepend the trust-score cover page (last so we can reuse the existing
    # text-emission loop without juggling page indices).
    t = trust_score(verdicts)
    insert_trust_cover_page(doc, slug, t)
    counts["trust_score"] = t["score"]
    counts["trust_bucket"] = t["bucket"]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)
    doc.close()
    return counts


def render(text: str, ranges: list[tuple], slug: str) -> tuple[str, dict]:
    parts: list[str] = []
    cursor = 0
    counts = {"FAIL": 0, "INCONCLUSIVE": 0}
    for start, end, cid, verdict, confidence in ranges:
        parts.append(html_escape(text[cursor:start]))
        snippet = html_escape(text[start:end])
        css_class = verdict.lower()
        title = f"{cid} — {verdict}" + (f" ({confidence})" if confidence else "")
        parts.append(
            f'<mark class="{css_class}" id="claim-{cid}" title="{html_escape(title)}">'
            f'{snippet}<sup>{cid}</sup></mark>'
        )
        cursor = end
        counts[verdict] = counts.get(verdict, 0) + 1
    parts.append(html_escape(text[cursor:]))
    body = "".join(parts)
    html = HTML_TEMPLATE.format(
        slug=html_escape(slug),
        body=body,
        count_fail=counts["FAIL"],
        count_inconclusive=counts["INCONCLUSIVE"],
    )
    return html, counts


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("review_dir", type=Path,
                   help="path to reviews/<slug>/")
    p.add_argument("--text", type=Path,
                   help="override paper.txt path (default: <review>/paper/paper.txt)")
    p.add_argument("--claims", type=Path,
                   help="override CLAIMS.md path")
    p.add_argument("--verification", type=Path,
                   help="override VERIFICATION.md path")
    p.add_argument("--html-out", type=Path,
                   help="override HTML output path")
    p.add_argument("--pdf-out", type=Path,
                   help="override PDF output path")
    p.add_argument("--no-pdf", action="store_true",
                   help="skip PDF synthesis (HTML only)")
    p.add_argument("--no-html", action="store_true",
                   help="skip HTML output (PDF only)")
    args = p.parse_args()

    review = args.review_dir
    if not review.is_dir():
        print(f"error: {review} is not a directory", file=sys.stderr)
        return 2

    text_path = args.text or (review / "paper" / "paper.txt")
    claims_md = args.claims or (review / "phase1" / "outputs" / "CLAIMS.md")
    verification_md = args.verification or (review / "phase2" / "outputs" / "VERIFICATION.md")
    html_out = args.html_out or (review / "phase3" / "outputs" / "paper.highlighted.html")
    pdf_out  = args.pdf_out  or (review / "phase3" / "outputs" / "paper.highlighted.pdf")

    for required, label in [(text_path, "paper.txt"), (claims_md, "CLAIMS.md")]:
        if not required.exists():
            print(f"error: {label} not found at {required}", file=sys.stderr)
            return 2

    text = text_path.read_text(errors="replace")
    claims = parse_claims_md(claims_md)
    verdicts = parse_verification_md(verification_md)

    if not verdicts:
        print(f"warning: no verdicts found in {verification_md} "
              f"(file missing or no parsable sections); nothing to highlight",
              file=sys.stderr)

    ranges = find_ranges(text, claims, verdicts)

    # Track sentences we couldn't locate, for reviewer follow-up.
    matched_ids = {r[2] for r in ranges}
    expected_ids = {
        cid for cid, v in verdicts.items()
        if v["verdict"] in HIGHLIGHT_COLORS and claims.get(cid, {}).get("sentence")
    }
    unmatched = sorted(expected_ids - matched_ids)

    slug = review.name

    if not args.no_html:
        html, html_counts = render(text, ranges, slug)
        html_out.parent.mkdir(parents=True, exist_ok=True)
        html_out.write_text(html)
        print(f"wrote {html_out}")
        print(f"  highlights: {html_counts}")

    if not args.no_pdf:
        try:
            pdf_counts = synthesize_pdf(text, ranges, verdicts, pdf_out, slug)
            print(f"wrote {pdf_out}")
            print(f"  highlighted lines: {pdf_counts}")
        except RuntimeError as e:
            print(f"warning: PDF skipped — {e}", file=sys.stderr)

    if unmatched:
        print(f"  unmatched (sentence not found in paper.txt): {unmatched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
