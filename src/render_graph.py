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
        elements.append({
            "data": {
                "id": c["id"],
                "parent": c.get("parent"),
                "label": (sentence[:60] + "…") if len(sentence) > 60 else sentence,
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
</style>
<!-- INLINE-TODO: replace this CDN script with inlined JS for offline self-containment. -->
<script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script>
</head>
<body>
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

const cy = cytoscape({
  container: document.getElementById("cy"),
  elements: ELEMENTS,
  wheelSensitivity: 0.2,
  style: [
    { selector: "node[kind = 'group']",
      style: {
        "background-color": "data(color)",
        "background-opacity": 0.12,
        "border-color": "data(color)",
        "border-width": 3,
        "border-opacity": 0.85,
        "label": "data(label)",
        "font-size": 18,
        "font-weight": 700,
        "font-family": "Inter, system-ui, sans-serif",
        "shape": "round-rectangle",
        "text-valign": "top",
        "text-halign": "center",
        "text-margin-y": -10,
        "padding": "24px",
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
        "border-width": 1.5,
        "label": "data(label)",
        "font-size": 12,
        "font-weight": 600,
        "font-family": "Inter, system-ui, sans-serif",
        "shape": "round-rectangle",
        "width": 220,
        "height": 56,
        "text-valign": "center",
        "text-halign": "center",
        "color": "#14161f",
        "text-wrap": "wrap",
        "text-max-width": "200px",
        "padding": "8px"
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
    name: "cose",
    nodeRepulsion: 12000,
    idealEdgeLength: 140,
    padding: 60,
    nodeOverlap: 30,
    animate: false
  }
});

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
