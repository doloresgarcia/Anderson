"""Render graph.*.json (per conventions/graph_schema.md) to graph.*.html.

    python3 src/render_graph.py reviews/foo/phase3/outputs/graph.final.json
    # writes graph.final.html alongside the .json

The output is a Cytoscape.js compound-graph view: groups are containers, claims
are nodes inside groups, edges connect claims. Color follows the canonical
palette in conventions/graph_schema.md.

The Cytoscape.js library is **inlined** into the HTML from
`src/vendor/cytoscape.min.js`, so the resulting file is fully self-contained
and works offline. If the vendor file is missing, the renderer falls back to
loading from a public CDN (and warns the user — useful while iterating, but
the file won't render without internet).

V1 limitation: default state shows all nodes (groups + claims). The schema
specifies click-to-expand collapse behavior; implementing that needs the
cytoscape-expand-collapse extension and is deferred.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

# Canonical palettes — keep in sync with conventions/error_categories.md and
# the graph node colors set by graph_builder.

# Five-category palette for FLAGGED claims.
CATEGORY_COLORS = {
    "unreferenced":           "#4285F4",
    "ambiguous":              "#FFBF00",
    "internal_contradiction": "#FF6D00",
    "literature_collision":   "#D32F2F",
    "domain_violation":       "#7B1FA2",
}

# Aggregate verdict palette (per-claim and per-group rollup).
VERDICT_COLORS = {
    "CLEAR":        "#2ECC71",   # all checkers CLEAR
    "INCONCLUSIVE": "#F1C40F",   # at least one INCONCLUSIVE, none FLAGGED
    "FLAGGED":      "#E74C3C",   # at least one FLAGGED (graph_builder may
                                 # override with the most-severe category color)
    "NOT_CHECKED":  "#95A5A6",
}

DEFAULT_COLOR = VERDICT_COLORS["NOT_CHECKED"]


VENDOR_DIR = Path(__file__).resolve().parent / "vendor"
CYTOSCAPE_VENDOR = VENDOR_DIR / "cytoscape.min.js"
CYTOSCAPE_CDN = "https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"


def _cytoscape_script_block() -> str:
    """Return the <script>…</script> tag(s) that load Cytoscape.js.

    Prefers the inlined vendor copy (offline-safe). Falls back to the public
    CDN with a console.warn if the vendor copy is missing.
    """
    if CYTOSCAPE_VENDOR.exists():
        # Inline-embed — emit a literal <script> with the library source.
        # The minified JS shouldn't contain </script>, but guard just in case.
        body = CYTOSCAPE_VENDOR.read_text().replace("</script>", "<\\/script>")
        return "<script>\n" + body + "\n</script>"
    return (
        f'<script src="{CYTOSCAPE_CDN}"></script>'
        '<script>console.warn("Anderson: cytoscape.min.js was loaded from a '
        'CDN; ship src/vendor/cytoscape.min.js for an offline-safe build.");</script>'
    )


# Layout constants for the deterministic grid placement (see
# _compute_claim_positions).
_CELL = 30           # per-claim cell size inside a group (claim node is 22px)
_GROUP_PAD = 14      # inner whitespace between children's bbox and group edge
_COLS_PER_ROW = 4    # groups per row across the canvas
_GROUP_GAP_X = 36    # horizontal gap between groups
_GROUP_GAP_Y = 56    # vertical gap between rows (also makes room for the
                     # next row's title, which is drawn above its rectangle)


def _compute_claim_positions(graph: dict) -> dict[str, tuple[float, float]]:
    """Pre-compute absolute (x, y) positions for every claim node.

    - Groups are emitted in the order they appear in the JSON, which is
      paper order (graph_builder writes them top-to-bottom by section).
    - Groups pack into rows of `_COLS_PER_ROW`. All slots in a row use
      the same width (= max group width across the whole graph) so the
      columns line up; each group is centered in its slot.
    - Claims inside a group sit in a square-ish grid (`cols ≈ sqrt(N)`).
    - Group rectangles auto-size around their children plus the CSS
      `padding`. The group title is drawn *above* the rectangle, so we
      only need vertical breathing room in `_GROUP_GAP_Y`, not extra
      padding inside.
    """
    group_claims: dict[str, list[str]] = {}
    for c in graph.get("claims", []):
        gid = c.get("parent") or "_orphan"
        group_claims.setdefault(gid, []).append(c["id"])

    group_order = [g["id"] for g in graph.get("groups", [])]
    for gid in group_claims:
        if gid not in group_order:
            group_order.append(gid)

    # (gid, claim_ids, cols, rows, width, height) per group, in paper order.
    boxes: list[tuple[str, list[str], int, int, float, float]] = []
    for gid in group_order:
        cids = group_claims.get(gid, [])
        n = max(1, len(cids))
        cols = max(1, math.ceil(math.sqrt(n)))
        rows = math.ceil(n / cols)
        w = cols * _CELL + 2 * _GROUP_PAD
        h = rows * _CELL + 2 * _GROUP_PAD
        boxes.append((gid, cids, cols, rows, w, h))

    if not boxes:
        return {}

    slot_w = max(b[4] for b in boxes)
    n_rows = math.ceil(len(boxes) / _COLS_PER_ROW)
    row_heights = [
        max(b[5] for b in boxes[r * _COLS_PER_ROW:(r + 1) * _COLS_PER_ROW])
        for r in range(n_rows)
    ]
    row_y0 = [0.0]
    for h in row_heights[:-1]:
        row_y0.append(row_y0[-1] + h + _GROUP_GAP_Y)

    positions: dict[str, tuple[float, float]] = {}
    for idx, (gid, cids, cols, rows, w, h) in enumerate(boxes):
        row_i, col_i = divmod(idx, _COLS_PER_ROW)
        slot_x = col_i * (slot_w + _GROUP_GAP_X)
        # Center the group horizontally inside its slot when narrower than slot_w.
        x0 = slot_x + (slot_w - w) / 2 + _GROUP_PAD
        y0 = row_y0[row_i] + _GROUP_PAD
        for i, cid in enumerate(cids):
            r, c = divmod(i, cols)
            positions[cid] = (
                x0 + c * _CELL + _CELL / 2,
                y0 + r * _CELL + _CELL / 2,
            )

    return positions


def to_cytoscape_elements(graph: dict) -> list[dict]:
    """Convert a graph.json (per the schema) into Cytoscape.js elements."""
    elements: list[dict] = []
    positions = _compute_claim_positions(graph)

    for g in graph.get("groups", []):
        elements.append({
            "data": {
                "id": g["id"],
                "label": g.get("title", g["id"]),
                "caption": g.get("caption", ""),
                "verdict": g.get("verdict", "NOT_CHECKED"),
                "color": g.get("color") or VERDICT_COLORS.get(g.get("verdict", ""), DEFAULT_COLOR),
                "kind": "group",
                "section": g.get("section", ""),
            }
        })

    for c in graph.get("claims", []):
        sentence = c.get("sentence", "")
        # If graph_builder didn't supply an explicit color, fall back: prefer
        # the most-severe-category color when categories are listed; else fall
        # back to the verdict palette.
        color = c.get("color")
        if not color:
            cats = c.get("flagged_categories") or []
            if cats:
                color = CATEGORY_COLORS.get(cats[0], DEFAULT_COLOR)
            else:
                color = VERDICT_COLORS.get(c.get("verdict", ""), DEFAULT_COLOR)
        el: dict = {
            "data": {
                "id": c["id"],
                "parent": c.get("parent"),
                "label": c["id"],
                "sentence": sentence,
                "type": c.get("type", ""),
                "hedged": c.get("hedged", False),
                "confidence": c.get("confidence", ""),
                "verdict": c.get("verdict", "NOT_CHECKED"),
                "verdict_confidence": c.get("verdict_confidence", ""),
                "flagged_categories": c.get("flagged_categories") or [],
                "color": color,
                "kind": "claim",
                "page": c.get("page"),
                "line": c.get("line"),
            }
        }
        if c["id"] in positions:
            x, y = positions[c["id"]]
            el["position"] = {"x": x, "y": y}
        elements.append(el)

    for e in graph.get("edges", []):
        elements.append({
            "data": {
                "id": e["id"],
                "source": e["source"],
                "target": e["target"],
                "kind": e.get("kind", "supports"),
                "confidence": e.get("confidence", "medium"),
                "provenance": e.get("provenance", ""),
            }
        })

    return elements


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Anderson — claim graph for __SLUG__</title>
<style>
  :root {
    --bg: #14161f;
    --bg-panel: #1f2230;
    --border: #2a2e3f;
    --text: #e9ecf3;
    --text-dim: #9aa3b8;
    --text-muted: #6b7488;
    --accent: #ffffff;
    --edge: #6b7488;
  }
  html, body {
    margin: 0; padding: 0; height: 100%;
    font-family: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--bg); color: var(--text);
  }
  #cy { width: 100vw; height: 100vh; background: var(--bg); }

  #header {
    position: absolute; top: 16px; left: 20px;
    z-index: 10; pointer-events: none;
  }
  #header .brand {
    font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
    color: var(--text-muted); margin-bottom: 2px;
  }
  #header .slug {
    font-size: 20px; font-weight: 700; color: var(--text);
    letter-spacing: -0.01em;
  }

  #info {
    position: absolute; top: 16px; right: 16px;
    background: var(--bg-panel); color: var(--text);
    padding: 18px 20px;
    border: 1px solid var(--border); border-radius: 8px;
    max-width: 380px; min-width: 280px;
    font-size: 14px; line-height: 1.5;
    box-shadow: 0 8px 24px rgba(0,0,0,.4);
  }
  #info h2 {
    font-size: 16px; margin: 0 0 8px;
    color: var(--text); font-weight: 600;
  }
  #info .sentence { font-style: italic; margin-bottom: 8px; color: var(--text); }
  #info .caption  { color: var(--text); margin-bottom: 8px; }
  #info .meta { color: var(--text-dim); font-size: 12px; margin-top: 4px; }

  .verdict {
    display: inline-block; padding: 3px 10px; border-radius: 4px;
    color: #14161f; font-weight: 700; font-size: 11px;
    text-transform: uppercase; letter-spacing: 1px;
  }

  #legend {
    position: absolute; bottom: 16px; left: 20px;
    background: var(--bg-panel); color: var(--text);
    padding: 12px 16px;
    border: 1px solid var(--border); border-radius: 8px;
    font-size: 12px; box-shadow: 0 8px 24px rgba(0,0,0,.4);
  }
  #legend .row { margin: 4px 0; display: flex; align-items: center; }
  #legend .swatch {
    display: inline-block; width: 14px; height: 14px;
    margin-right: 8px; border-radius: 3px;
  }
  #legend .edges { margin-top: 10px; padding-top: 10px;
    border-top: 1px solid var(--border); color: var(--text-dim); font-size: 11px;
  }
  #legend .line { display: inline-block; width: 24px; height: 2px;
    background: var(--edge); margin-right: 6px; vertical-align: middle; }
  #legend .line.dashed {
    background: none; border-top: 2px dashed var(--edge); height: 0;
  }
  #legend .line.contradicts { background: #E74C3C; height: 3px; }

  #status {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    background: var(--bg-panel); color: var(--text);
    padding: 24px 32px; border: 1px solid var(--border); border-radius: 8px;
    font-size: 14px; max-width: 600px; line-height: 1.5;
    box-shadow: 0 8px 24px rgba(0,0,0,.5); z-index: 100;
  }
  #status.error { border-color: #E74C3C; }
  #status code {
    font-family: ui-monospace, "SFMono-Regular", monospace;
    font-size: 12px; background: rgba(255,255,255,0.04);
    padding: 2px 6px; border-radius: 3px; color: #FFBF00;
  }
</style>
__CYTOSCAPE_SCRIPT__
</head>
<body>
<div id="cy"></div>
<div id="status">Loading graph…</div>
<div id="header">
  <div class="brand">ANDERSON · CLAIM GRAPH</div>
  <div class="slug">__SLUG__</div>
</div>
<div id="info">
  <h2>Hover a node</h2>
  <div class="meta">…for the full claim, verdict, and reasoning. Drag to reposition. Scroll to zoom.</div>
</div>
<div id="legend">
  <div class="row"><span class="swatch" style="background:#4285F4"></span>unreferenced</div>
  <div class="row"><span class="swatch" style="background:#FFBF00"></span>ambiguous</div>
  <div class="row"><span class="swatch" style="background:#FF6D00"></span>internal_contradiction</div>
  <div class="row"><span class="swatch" style="background:#D32F2F"></span>literature_collision</div>
  <div class="row"><span class="swatch" style="background:#7B1FA2"></span>domain_violation</div>
  <div class="row"><span class="swatch" style="background:#2ECC71"></span>CLEAR</div>
  <div class="row"><span class="swatch" style="background:#F1C40F"></span>INCONCLUSIVE</div>
  <div class="row"><span class="swatch" style="background:#95A5A6"></span>NOT CHECKED</div>
  <div class="edges">
    <div class="row"><span class="line"></span>supports</div>
    <div class="row"><span class="line dashed"></span>depends on</div>
    <div class="row"><span class="line contradicts"></span>contradicts</div>
  </div>
</div>
<script>
const ELEMENTS = __ELEMENTS__;
const status = document.getElementById("status");

function showStatus(msg, isError) {
  status.innerHTML = msg;
  status.style.display = "block";
  if (isError) status.className = "error";
}
function hideStatus() { status.style.display = "none"; }

if (typeof cytoscape === "undefined") {
  showStatus(
    "<b>Cytoscape.js failed to load.</b><br><br>" +
    "The library is supposed to be inlined in this HTML. If you're " +
    "seeing this, the file may be truncated, or another script is " +
    "blocking it. Check the browser console (F12) for the actual error.",
    true
  );
  throw new Error("cytoscape global not defined");
}
if (!ELEMENTS || ELEMENTS.length === 0) {
  showStatus("<b>No graph data.</b><br>The JSON contained no nodes or edges.", true);
}

let cy;
try {
  cy = cytoscape({
  container: document.getElementById("cy"),
  elements: ELEMENTS,
  wheelSensitivity: 0.2,
  style: [
    { selector: "node[kind = 'group']",
      style: {
        "background-color": "data(color)",
        "background-opacity": 0.10,
        "border-color": "data(color)",
        "border-width": 2,
        "border-opacity": 0.85,
        "label": "data(label)",
        "font-size": 13,
        "font-weight": 700,
        "font-family": "Inter, system-ui, sans-serif",
        "shape": "round-rectangle",
        "text-valign": "top",
        "text-halign": "center",
        "text-margin-y": -12,
        "text-wrap": "wrap",
        "text-max-width": "260px",
        "padding": "8px",
        "color": "#e9ecf3",
        "text-outline-color": "#14161f",
        "text-outline-width": 2,
        "text-outline-opacity": 0.9
      }
    },
    { selector: "node[kind = 'claim']",
      style: {
        "background-color": "data(color)",
        "background-opacity": 0.95,
        "border-color": "data(color)",
        "border-width": 1,
        "label": "data(label)",
        "font-size": 7,
        "font-weight": 700,
        "font-family": "Inter, system-ui, sans-serif",
        "shape": "ellipse",
        "width": 22,
        "height": 22,
        "text-valign": "center",
        "text-halign": "center",
        "color": "#14161f",
        "text-wrap": "none",
        "padding": "0px"
      }
    },
    { selector: "edge",
      style: {
        "line-color": "#6b7488",
        "target-arrow-color": "#6b7488",
        "target-arrow-shape": "triangle",
        "curve-style": "bezier",
        "width": 2,
        "arrow-scale": 1.1,
        "opacity": 0.85
      }
    },
    { selector: "edge[kind = 'depends_on']",
      style: { "line-style": "dashed" }
    },
    { selector: "edge[kind = 'contradicts']",
      style: {
        "line-color": "#E74C3C",
        "target-arrow-color": "#E74C3C",
        "width": 4,
        "opacity": 1
      }
    },
    { selector: ":selected",
      style: {
        "border-width": 4,
        "border-color": "#ffffff",
        "border-opacity": 1
      }
    }
  ],
  layout: {
    // Positions are pre-computed in Python (_compute_claim_positions).
    // 'preset' uses node.position() as-is, so groups auto-size to wrap
    // their grid of children — deterministic and tight.
    name: "preset",
    fit: true,
    padding: 30
  }
});

// Force a fit pass after layout to make sure everything is visible.
cy.ready(function() {
  cy.fit(undefined, 60);
  if (cy.nodes().length === 0) {
    showStatus(
      "<b>Layout produced no visible nodes.</b><br>" +
      ELEMENTS.length + " elements in data but Cytoscape rendered 0 nodes.",
      true
    );
  } else {
    hideStatus();
  }
});

} catch (err) {
  console.error("Anderson render error", err);
  showStatus(
    "<b>Graph render failed.</b><br><br>" +
    "<code>" + (err && err.message ? err.message : String(err)) + "</code><br><br>" +
    "Open the browser console (F12) for the full stack trace.",
    true
  );
}

const info = document.getElementById("info");
const DEFAULT_INFO = '<h2>Hover a node</h2><div class="meta">…for the full claim, verdict, and reasoning. Drag to reposition. Scroll to zoom.</div>';

function renderInfo(node) {
  if (!node) { info.innerHTML = DEFAULT_INFO; return; }
  const d = node.data();
  let html = "<h2>" + escapeHtml(d.label || d.id) + "</h2>";
  if (d.kind === "group") {
    if (d.caption) html += '<div class="caption">' + escapeHtml(d.caption) + '</div>';
    html += '<div><span class="verdict" style="background:' + d.color + '">' + d.verdict + '</span></div>';
    if (d.section) html += '<div class="meta">section ' + escapeHtml(d.section) + '</div>';
  } else {
    html += '<div class="sentence">"' + escapeHtml(d.sentence) + '"</div>';
    html += '<div class="meta">type: ' + escapeHtml(d.type) + (d.hedged ? " · hedged" : "") + ' · confidence: ' + escapeHtml(d.confidence) + '</div>';
    html += '<div style="margin-top:8px;"><span class="verdict" style="background:' + d.color + '">' + d.verdict + '</span>';
    if (d.verdict_confidence) html += ' <span class="meta" style="margin-top:0;">(' + escapeHtml(d.verdict_confidence) + ')</span>';
    html += '</div>';
    if (Array.isArray(d.flagged_categories) && d.flagged_categories.length) {
      html += '<div class="meta">flagged: ' + d.flagged_categories.map(escapeHtml).join(", ") + '</div>';
    }
    if (d.page != null) html += '<div class="meta">page ' + d.page + (d.line ? ", line " + d.line : "") + '</div>';
  }
  info.innerHTML = html;
}
function escapeHtml(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
cy.on("mouseover", "node", e => renderInfo(e.target));
cy.on("mouseout",  "node", () => renderInfo(null));
</script>
</body>
</html>
"""


def render(graph: dict) -> str:
    elements = to_cytoscape_elements(graph)
    slug = (graph.get("paper") or {}).get("slug", "graph")
    return (
        HTML_TEMPLATE
        .replace("__CYTOSCAPE_SCRIPT__", _cytoscape_script_block())
        .replace("__SLUG__", slug)
        .replace("__ELEMENTS__", json.dumps(elements, indent=2))
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("input", type=Path, help="path to graph.*.json")
    p.add_argument("--out", type=Path, help="output HTML path (default: replace .json with .html)")
    args = p.parse_args()

    if not args.input.exists():
        print(f"error: {args.input} does not exist", file=sys.stderr)
        return 2

    graph = json.loads(args.input.read_text())
    out_path = args.out or args.input.with_suffix(".html")
    out_path.write_text(render(graph))
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
