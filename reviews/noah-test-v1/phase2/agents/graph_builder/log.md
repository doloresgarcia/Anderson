# graph_builder — Phase 2 Log

## Task
Populate claim verdicts in graph.v1.json from VERIFICATION.md to produce graph.v2.json.

## Inputs
- `phase1/outputs/graph.v1.json` — 545 claims, 23 groups, all verdicts = NOT_CHECKED
- `phase2/outputs/VERIFICATION.md` — checker results from all five categories

## Verdict assignments

### NOT_CHECKED (skipped per instructions)
- type != prose: equations (33), captions (17), table_cells (77) = 127 claims
- is_definition=true: 0 claims found in graph.v1.json
- Table-as-prose flagged: 0140, 0278, 0323, 0346, 0352, 0462, 0514, 0515, 0543
- Fragment: 0066
Total NOT_CHECKED: 127 + 9 + 1 = 137 claims

### FAIL (34 claims)
Deduplicated from unreferenced + ambiguous + internal_contradiction + domain_violation:
0004, 0007, 0008, 0009, 0014, 0018, 0019, 0031, 0043, 0052, 0058, 0079, 0099, 0100, 0101,
0132, 0146, 0147, 0150, 0162, 0165, 0195, 0202, 0237, 0294, 0336, 0365, 0368, 0402, 0441,
0472, 0483, 0484, 0488

### INCONCLUSIVE (4 claims, none in FAIL set)
0082, 0163, 0384, 0522

### PASS
All other prose claims not in NOT_CHECKED, FAIL, or INCONCLUSIVE sets.

## Group aggregation rules
- Any child FAIL → group FAIL (#E74C3C)
- Any child INCONCLUSIVE (no FAIL) → group INCONCLUSIVE (#F1C40F)
- All children PASS → group PASS (#2ECC71)
- Mix of PASS/NOT_CHECKED or all NOT_CHECKED → group NOT_CHECKED (#95A5A6)

## Evidence / verdict_reason population
- FAIL claims: verdict_confidence from VERIFICATION.md checker findings
- INCONCLUSIVE claims: verdict_reason = reason code from VERIFICATION.md
- Evidence (paper.txt line pointers) populated where available in VERIFICATION.md

## Output
`phase2/outputs/graph.v2.json` — schema_version "2"

## Final counts
- Claims: PASS=370, FAIL=34, INCONCLUSIVE=4, NOT_CHECKED=137 (total 545)
- Groups: FAIL=18, INCONCLUSIVE=1, NOT_CHECKED=4, PASS=0 (total 23)

Note: No group achieves pure PASS because every section contains at least one equation/caption/table_cell (NOT_CHECKED) or flagged claim.
