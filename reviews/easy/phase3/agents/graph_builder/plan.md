# Phase 3 Graph Builder Plan

## Objective
Finalize the claim graph for Phase 3 by copying graph.v2.json to graph.final.json, post-process to deduplicate evidence arrays and check for missing contradicts edges, validate against schema, and render HTML visualization.

## Inputs
- `reviews/easy/phase2/outputs/graph.v2.json` — graph from Phase 2 (200 claims, 20 edges, 20 groups)
- `src/conventions/graph_schema.json` — executable JSON schema
- `src/conventions/graph_schema.md` — prose reference
- `src/conventions/error_categories.md` — color mapping

## Steps
1. Read graph.v2.json as Python dict
2. Post-process:
   - Iterate all claim nodes, deduplicate evidence arrays (remove duplicates where string content is identical)
   - Check for M11 advisory: consider adding `contradicts` edge between C183 and C185 if not present
3. Validate result against src/conventions/graph_schema.json
4. Write to `reviews/easy/phase3/outputs/graph.final.json`
5. Shell out to `python3 src/render_graph.py reviews/easy/phase3/outputs/graph.final.json` to render HTML
6. Write `log.md` documenting what was done

## Outputs
- `reviews/easy/phase3/outputs/graph.final.json`
- `reviews/easy/phase3/outputs/graph.final.html`
- `log.md` (in working dir)
