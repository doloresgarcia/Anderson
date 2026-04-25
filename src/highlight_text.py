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

Color palette is the canonical one from conventions/graph_schema.md:
  red    (#E74C3C) — FAIL
  yellow (#F1C40F) — INCONCLUSIVE
PASS and NOT_CHECKED produce no highlight.

Each highlight is a `<mark>` span with an anchor id `claim-<id>`, a tooltip
showing the verdict, and a small superscript label so the reader can
cross-reference VERIFICATION.md.

No external dependencies — produces a self-contained HTML file.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Reuse the parsers from highlight_paper.py (same CLAIMS.md / VERIFICATION.md
# format). Importing rather than duplicating keeps both renderers in sync.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from highlight_paper import parse_claims_md, parse_verification_md  # noqa: E402

# Canonical palette (graph_schema.md).
HIGHLIGHT_COLORS = {
    "FAIL":         "#E74C3C",
    "INCONCLUSIVE": "#F1C40F",
}


def find_ranges(text: str, claims: dict, verdicts: dict) -> list[tuple]:
    """Return [(start, end, claim_id, verdict, confidence), ...] sorted by
    start, with overlaps resolved by keeping the earlier-start range."""
    ranges: list[tuple] = []
    for cid, claim in claims.items():
        v = verdicts.get(cid)
        if not v or v["verdict"] not in HIGHLIGHT_COLORS:
            continue
        sentence = claim["sentence"]
        if not sentence:
            continue
        idx = 0
        while True:
            pos = text.find(sentence, idx)
            if pos == -1:
                break
            ranges.append((pos, pos + len(sentence), cid, v["verdict"], v.get("confidence", "")))
            idx = pos + len(sentence)
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
    p.add_argument("--out", type=Path,
                   help="override output HTML path")
    args = p.parse_args()

    review = args.review_dir
    if not review.is_dir():
        print(f"error: {review} is not a directory", file=sys.stderr)
        return 2

    text_path = args.text or (review / "paper" / "paper.txt")
    claims_md = args.claims or (review / "phase1" / "outputs" / "CLAIMS.md")
    verification_md = args.verification or (review / "phase2" / "outputs" / "VERIFICATION.md")
    out_path = args.out or (review / "phase3" / "outputs" / "paper.highlighted.html")

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
    html, counts = render(text, ranges, slug)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html)
    print(f"wrote {out_path}")
    print(f"  highlighted: {counts}")
    if unmatched:
        print(f"  unmatched (sentence not found in paper.txt): {unmatched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
