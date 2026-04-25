"""Render graph.*.json (per conventions/graph_schema.md) to graph.*.html.

    python3 src/render_graph.py reviews/foo/phase3/outputs/graph.final.json
    # writes graph.final.html alongside the .json

The output is a Cytoscape.js compound-graph view: groups are containers, claims
are nodes inside groups, edges connect claims. Color follows the canonical
palette in conventions/graph_schema.md.

V1 limitations (deliberate, document-and-iterate):

- Loads Cytoscape.js from a public CDN. The schema asks for fully self-contained
  HTML; this version isn't. Switch to inline-embedded JS once the renderer's
  output stabilizes — search for INLINE-TODO below.
- Default state shows all nodes (groups + claims). The schema specifies
  click-to-expand collapse behavior. Implementing that requires the
  cytoscape-expand-collapse extension; deferred for v1.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Canonical palette from conventions/graph_schema.md.
COLORS = {
    "PASS":         "#2ECC71",
    "INCONCLUSIVE": "#F1C40F",
    "FAIL":         "#E74C3C",
    "NOT_CHECKED":  "#95A5A6",
}

DEFAULT_COLOR = COLORS["NOT_CHECKED"]


def to_cytoscape_elements(graph: dict) -> list[dict]:
    """Convert a graph.json (per the schema) into Cytoscape.js elements."""
    elements: list[dict] = []

    for g in graph.get("groups", []):
        elements.append({
            "data": {
                "id": g["id"],
                "label": g.get("title", g["id"]),
                "caption": g.get("caption", ""),
                "verdict": g.get("verdict", "NOT_CHECKED"),
                "color": g.get("color") or COLORS.get(g.get("verdict", ""), DEFAULT_COLOR),
                "kind": "group",
                "section": g.get("section", ""),
            }
        })

    for c in graph.get("claims", []):
        sentence = c.get("sentence", "")
        elements.append({
            "data": {
                "id": c["id"],
                "parent": c.get("parent"),
                "label": (sentence[:32] + "…") if len(sentence) > 32 else sentence,
                "sentence": sentence,
                "type": c.get("type", ""),
                "hedged": c.get("hedged", False),
                "confidence": c.get("confidence", ""),
                "verdict": c.get("verdict", "NOT_CHECKED"),
                "verdict_confidence": c.get("verdict_confidence", ""),
                "color": c.get("color") or COLORS.get(c.get("verdict", ""), DEFAULT_COLOR),
                "kind": "claim",
                "page": c.get("page"),
                "line": c.get("line"),
            }
        })

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
  html, body { margin: 0; padding: 0; height: 100%; font-family: system-ui, -apple-system, sans-serif; }
  #cy { width: 100vw; height: 100vh; }
  #info {
    position: absolute; top: 12px; right: 12px;
    background: white; padding: 12px 14px;
    border: 1px solid #d0d0d0; border-radius: 4px;
    max-width: 360px; min-width: 240px;
    font-size: 13px; line-height: 1.45;
    box-shadow: 0 2px 8px rgba(0,0,0,.12);
  }
  #info h2 { font-size: 14px; margin: 0 0 6px; }
  #info .sentence { font-style: italic; margin-bottom: 6px; }
  #info .meta { color: #555; font-size: 12px; }
  .verdict {
    display: inline-block; padding: 2px 8px; border-radius: 3px;
    color: white; font-weight: bold; font-size: 11px;
    text-transform: uppercase; letter-spacing: .5px;
  }
  #legend {
    position: absolute; bottom: 12px; left: 12px;
    background: white; padding: 8px 10px;
    border: 1px solid #d0d0d0; border-radius: 4px;
    font-size: 11px; box-shadow: 0 2px 6px rgba(0,0,0,.08);
  }
  #legend .swatch { display: inline-block; width: 12px; height: 12px;
    vertical-align: middle; margin-right: 4px; border-radius: 2px; }
</style>
<!-- INLINE-TODO: replace these CDN scripts with inlined JS for offline self-containment. -->
<script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script>
</head>
<body>
<div id="cy"></div>
<div id="info">
  <h2>__SLUG__</h2>
  <div class="meta">Hover a node for detail. Drag to reposition.</div>
</div>
<div id="legend">
  <div><span class="swatch" style="background:#2ECC71"></span>PASS</div>
  <div><span class="swatch" style="background:#F1C40F"></span>INCONCLUSIVE</div>
  <div><span class="swatch" style="background:#E74C3C"></span>FAIL</div>
  <div><span class="swatch" style="background:#95A5A6"></span>NOT CHECKED</div>
</div>
<script>
const ELEMENTS = __ELEMENTS__;

const cy = cytoscape({
  container: document.getElementById("cy"),
  elements: ELEMENTS,
  wheelSensitivity: 0.2,
  style: [
    { selector: "node[kind = 'group']",
      style: {
        "background-color": "data(color)",
        "background-opacity": 0.18,
        "border-color": "data(color)",
        "border-width": 2,
        "label": "data(label)",
        "font-size": 13,
        "font-weight": "bold",
        "shape": "round-rectangle",
        "text-valign": "top",
        "text-halign": "center",
        "text-margin-y": -6,
        "padding": "16px",
        "color": "#222"
      }
    },
    { selector: "node[kind = 'claim']",
      style: {
        "background-color": "data(color)",
        "label": "data(label)",
        "font-size": 9,
        "shape": "round-rectangle",
        "width": 130,
        "height": 30,
        "text-valign": "center",
        "text-halign": "center",
        "color": "#fff",
        "text-wrap": "ellipsis",
        "text-max-width": "120px"
      }
    },
    { selector: "edge",
      style: {
        "line-color": "#7F8C8D",
        "target-arrow-color": "#7F8C8D",
        "target-arrow-shape": "triangle",
        "curve-style": "bezier",
        "width": 1.6,
        "arrow-scale": 0.9
      }
    },
    { selector: "edge[kind = 'depends_on']",
      style: { "line-style": "dashed" }
    },
    { selector: "edge[kind = 'contradicts']",
      style: {
        "line-color": "#E74C3C",
        "target-arrow-color": "#E74C3C",
        "width": 3
      }
    },
    { selector: ":selected",
      style: { "border-width": 3, "border-color": "#2c3e50" }
    }
  ],
  layout: {
    name: "cose",
    nodeRepulsion: 8000,
    idealEdgeLength: 90,
    padding: 30,
    animate: false
  }
});

const info = document.getElementById("info");
function renderInfo(node) {
  if (!node) {
    info.innerHTML = '<h2>__SLUG__</h2><div class="meta">Hover a node for detail. Drag to reposition.</div>';
    return;
  }
  const d = node.data();
  let html = "<h2>" + escapeHtml(d.label || d.id) + "</h2>";
  if (d.kind === "group") {
    if (d.caption) html += '<div>' + escapeHtml(d.caption) + '</div>';
    html += '<div style="margin-top:6px;"><span class="verdict" style="background:' + d.color + '">' + d.verdict + '</span></div>';
    if (d.section) html += '<div class="meta">section ' + escapeHtml(d.section) + '</div>';
  } else {
    html += '<div class="sentence">' + escapeHtml(d.sentence) + '</div>';
    html += '<div class="meta">type: ' + escapeHtml(d.type) + (d.hedged ? " · hedged" : "") + ' · confidence: ' + escapeHtml(d.confidence) + '</div>';
    html += '<div style="margin-top:6px;"><span class="verdict" style="background:' + d.color + '">' + d.verdict + '</span>';
    if (d.verdict_confidence) html += ' <span class="meta">(' + escapeHtml(d.verdict_confidence) + ')</span>';
    html += '</div>';
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
