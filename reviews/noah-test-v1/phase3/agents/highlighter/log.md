# Highlighter Log — noah-test-v1 Phase 3

## Run summary

- Input: `paper/paper.txt` (977 lines)
- Reference: `phase2/outputs/VERIFICATION.md`, `phase2/outputs/graph.v2.json`
- Output: `phase3/outputs/paper.highlighted.html`

## Highlight map

32 lines highlighted from 977 total.

### Severity assignments (most severe wins per line)

| Line | Category | Color | Claims |
|------|----------|-------|--------|
| 53 | unreferenced | blue | 0004 |
| 60 | unreferenced | blue | 0007 |
| 64 | ambiguous | amber | 0008 |
| 79 | unreferenced | blue | 0009 |
| 90 | unreferenced | blue | 0014 |
| 95 | unreferenced | blue | 0018, 0019 |
| 108 | unreferenced | blue | 0031 |
| 120 | unreferenced | blue | 0043 |
| 133 | domain_violation | purple | 0052 |
| 142 | domain_violation | purple | 0058 |
| 190 | unreferenced | blue | 0079 |
| 229 | domain_violation | purple | 0099 |
| 230 | unreferenced | blue | 0100, 0101 |
| 289 | unreferenced | blue | 0132 |
| 332 | unreferenced | blue | 0146 |
| 334 | ambiguous | amber | 0147, 0150 |
| 339 | unreferenced | blue | 0162 |
| 341 | internal_contradiction | orange | 0165 |
| 360 | unreferenced | blue | 0195 |
| 381 | ambiguous | amber | 0202 |
| 440 | unreferenced | blue | 0237 |
| 500 | unreferenced | blue | 0294 |
| 542 | unreferenced | blue | 0336 |
| 620 | internal_contradiction | orange | 0365 |
| 626 | ambiguous | amber | 0368 |
| 707 | unreferenced | blue | 0402 |
| 772 | internal_contradiction | orange | 0165/0441 |
| 833 | unreferenced | blue | 0472 |
| 839 | unreferenced | blue | 0483 |
| 841 | unreferenced | blue | 0484 |
| 843 | ambiguous | amber | 0484 |
| 847 | ambiguous | amber | 0488 |

## Decisions

- claim-0008 appears at both line 62 (unreferenced) and line 64 (ambiguous). Ambiguous takes precedence over unreferenced; highlighted at line 64 with amber.
- Lines 95 carries two unreferenced claims (0018, 0019); merged into single blue highlight with combined tooltip.
- Lines 230 carries two unreferenced claims (0100, 0101); merged similarly.
- Line 334 carries two ambiguous claims (0147, 0150); merged into single amber highlight.
- Lines 841 and 843 both map to claim-0484 (unreferenced and ambiguous respectively); both highlighted separately with correct severity per line.
- INCONCLUSIVE claims (literature_collision, domain_violation) NOT highlighted per spec.
- claim-0008 task spec listed line 62 for unreferenced and line 64 for ambiguous; highlighted line 64 as amber (higher severity).

## Output format

Self-contained HTML; fixed legend top-right; tooltip on hover for each highlighted line; line-by-line rendering preserving original paper.txt structure.
