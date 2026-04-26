# report_writer log

## Run

- date: 2026-04-25
- role: report_writer
- phase: 3

## Inputs read

- paper/paper.meta.json
- phase1/outputs/FINDINGS.md
- phase2/outputs/STRATEGY.md
- phase2/outputs/VERIFICATION.md
- phase2/outputs/graph.v2.json (header + first two groups for paper metadata)

## Output

- phase3/outputs/REPORT.md

## Notes

- Paper title and arXiv ID extracted from graph.v2.json (paper.meta.json had null fields).
- 545 claims total; 418 prose checked; 127 not checked (33 equations, 17 captions, 77 table_cells).
- 9 malformed claims and 1 fragment excluded.
- Summary counts taken directly from VERIFICATION.md header.
- Domain violations: 3 FLAGGED (claim-0052, claim-0058, claim-0099); 2 INCONCLUSIVE (claim-0082, claim-0163).
- Internal contradictions: 3 FLAGGED (claim-0165/claim-0441 pair + claim-0365 standalone).
- Unreferenced: 25 FLAGGED.
- Ambiguous: 9 FLAGGED.
- Literature collision: 0 FLAGGED, 4 INCONCLUSIVE.
- No fabricated citations identified; no genuine literature collisions.
