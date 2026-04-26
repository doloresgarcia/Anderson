# graph_builder — Phase 3 log

**Role:** graph_builder (final pass)
**Phase:** 3
**Date:** 2026-04-25

## Inputs read

- `phase2/outputs/graph.v2.json` — 23 groups, 545 claims

## Summary statistics (from graph.v2.json)

| Verdict | Claims | Groups |
|---------|--------|--------|
| PASS | 368 | 0 |
| FAIL | 34 | 18 |
| INCONCLUSIVE | 6 | 1 |
| NOT_CHECKED | 137 | 4 |

Note: the task brief stated 370 PASS / 4 INCONCLUSIVE; actual counts from the
JSON are 368 PASS / 6 INCONCLUSIVE. The actual data was used in all outputs.

## Outputs written

| File | Description |
|------|-------------|
| `phase3/outputs/graph.final.json` | Copy of graph.v2.json with schema_version="final" and phase=3; no claim/group data changed |
| `phase3/outputs/graph.final.html` | Self-contained interactive HTML (~200 KB); 23 group cards in a responsive grid, expandable to show all 545 claims colored by verdict; no external network requests |
| `phase3/outputs/graph.final.svg` | Static SVG, 4-column grid of 23 group nodes colored by verdict, with titles and verdict labels |

## Decisions

- Used actual claim/group verdict counts from the JSON (not the brief's rounded
  figures) in the HTML summary header.
- HTML is fully self-contained (pure HTML/CSS/JS, no CDN, no external fonts).
- SVG uses a 6×4 grid (4 columns, 6 rows) to fit all 23 groups.
- FAIL/INCONCLUSIVE claim rows in the HTML show evidence pointers inline.
