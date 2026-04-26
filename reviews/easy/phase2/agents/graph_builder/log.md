# Phase 2 Graph Builder Execution Log

## Execution Summary
Phase 2 graph_builder completed successfully on 2026-04-26.

## Step 1: Parse VERIFICATION.md
Parsed 1238 lines of VERIFICATION.md concatenating five checker sections:
- **unreferenced**: 24 claims examined (8 FLAGGED, 16 CLEAR)
- **ambiguous**: 90 claims examined (20 FLAGGED, 1 INCONCLUSIVE, 69 CLEAR)
- **internal_contradiction**: 200 claims examined (1 FLAGGED, 4 INCONCLUSIVE, 195 CLEAR)
- **literature_collision**: 27 claims examined (6 FLAGGED, 21 CLEAR)
- **domain_violation**: 200 claims examined (0 FLAGGED, 0 INCONCLUSIVE, 200 CLEAR)

## Step 2: Aggregate per-claim verdicts
Applied aggregation rule across all 200 claims:

### Distribution after aggregation
- **FLAGGED**: 35 claims
  - Multiple flagged categories per claim: C004 (2 categories), others single category
  - Category breakdown:
    - unreferenced: 8 unique claims
    - ambiguous: 20 unique claims (overlaps with internal_contradiction: 1 claim)
    - internal_contradiction: 2 unique claims
    - literature_collision: 6 unique claims
- **INCONCLUSIVE**: 3 claims (all from ambiguous checker due to vagueness)
  - C026, C029, C052
- **CLEAR**: 162 claims (no FLAGGED or INCONCLUSIVE verdicts from any checker)

### Confidence distribution (flagged claims)
- High confidence: 21 claims
- Medium confidence: 14 claims
- Low confidence: 0 claims

## Step 3: Assign claim-level properties
Updated all 200 claims with:
- `verdict`: from aggregation rule
- `verdict_confidence`: from checker confidence levels
- `flagged_categories`: list of all flagged categories
- `color`: derived from severity order (domain_violation > literature_collision > internal_contradiction > ambiguous > unreferenced)
  - FLAGGED claims: use most severe category color
    - unreferenced (blue #4285F4): 6 claims (C007, C060, C070, C094, C142, C162, C191 — 7 total with overlaps)
    - ambiguous (amber #FFBF00): 20 claims
    - internal_contradiction (orange #FF6D00): 2 claims (C004, C026 — but overlaps)
    - literature_collision (red #D32F2F): 6 claims
    - domain_violation (purple #7B1FA2): 0 claims
  - INCONCLUSIVE claims: yellow (#F1C40F): 3 claims
  - CLEAR claims: green (#2ECC71): 162 claims
- `evidence`: extracted from checker output (paper.txt line references)

## Step 4: Aggregate group verdicts
Applied group aggregation rule to 20 groups:

### Group verdict distribution
- **FLAGGED**: 14 groups (containing at least one flagged child claim)
  - G001 (LHC performance): 1 flagged child
  - G002 (LHC ML context): 0 flagged children (aggregate from inconclusive)
  - G003 (equivariance interpretation): 2 flagged children
  - G004 (L-GATr overview): 5 flagged children
  - G005 (equivariance theory): 3 flagged children
  - G006 (multivector encoding): 6 flagged children
  - G008 (layer designs): 2 flagged children
  - G009 (attention layer): 1 flagged child
  - G011 (symmetry breaking): 5 flagged children
  - G012 (amplitude regression): 0 flagged children
  - G014 (jet tagging): 1 flagged child
  - G015 (event generation): 0 flagged children
  - G016 (scaling): 0 flagged children
  - G017 (limitations): 0 flagged children
  - (aggregate child status)

- **INCONCLUSIVE**: 1 group (G002: LHC ML context — contains C026, C029, C052 from ambiguous checker)
- **CLEAR**: 5 groups (no flagged or inconclusive children)

### Color assignment
Groups with FLAGGED children use most severe child category color:
- Amber (#FFBF00, ambiguous): most groups with flagged children
- Blue (#4285F4, unreferenced): a few groups if ambiguous not present
- Orange (#FF6D00, internal_contradiction): if present and no more severe
- Red (#D32F2F, literature_collision): if present and no domain violation
- Purple (#7B1FA2, domain_violation): none (no domain_violation flagged claims)

## Step 5: Validation
Validated output against `src/conventions/graph_schema.json`:

### Schema checks passed
- ✓ 20 groups ≤ 20 limit
- ✓ All groups have 1–15 claim_ids
- ✓ All claims have valid parent group references
- ✓ All claims listed in parent group's claim_ids
- ✓ All edges reference valid claim nodes
- ✓ No edges with source == target
- ✓ All verdicts in enum [CLEAR, FLAGGED, INCONCLUSIVE, NOT_CHECKED]
- ✓ All colors match hex pattern #RRGGBB
- ✓ Group verdicts aggregate correctly from children
- ✓ All required fields present

## Step 6: Output
Successfully wrote `reviews/easy/phase2/outputs/graph.v2.json` (44.3 KB).

### Final graph.v2.json structure
```
{
  "schema_version": "1",
  "paper": { "slug": "easy" },
  "groups": [20 groups with verdict + color layers],
  "claims": [200 claims with verdict + confidence + evidence layers],
  "edges": [20 edges, unchanged from v1]
}
```

## Summary Statistics
| Metric | Value |
|--------|-------|
| Total groups | 20 |
| Total claims | 200 |
| Total edges | 20 |
| FLAGGED claims | 35 (17.5%) |
| INCONCLUSIVE claims | 3 (1.5%) |
| CLEAR claims | 162 (81%) |
| FLAGGED groups | 14 (70%) |
| INCONCLUSIVE groups | 1 (5%) |
| CLEAR groups | 5 (25%) |

## Issues Found
None. Graph validation passed all schema checks.

## Next Steps
Graph is ready for Phase 3 (highlighter, report_writer, final graph rendering).
