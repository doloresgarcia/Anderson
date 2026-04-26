# Phase 2 Graph Builder Plan

## Objective
Merge Phase 2 verification verdicts from `VERIFICATION.md` (concatenated output of five checker agents) into `graph.v1.json` to produce `graph.v2.json` with claim and group verdict layers.

## Inputs
1. `reviews/easy/phase1/outputs/graph.v1.json` — 200 claims across 20 groups, 20 edges
2. `reviews/easy/phase2/outputs/VERIFICATION.md` — Concatenated output from five checker agents:
   - checker_unreferenced
   - checker_ambiguous
   - checker_contradiction
   - checker_literature
   - checker_domain
3. `src/conventions/error_categories.md` — Category definitions and severity order
4. `src/conventions/graph_schema.json` — Executable validation schema

## Phases

### Phase A: Parse VERIFICATION.md
- Extract verdict per claim per checker category
- Parse evidence lines (prefixed with `- evidence:`)
- Aggregate multiple verdicts per claim using the rule:
  - If any category reports `FLAGGED` → claim verdict = `FLAGGED`
  - Else if any category reports `INCONCLUSIVE` → claim verdict = `INCONCLUSIVE`
  - Else if all examined categories report `CLEAR` → claim verdict = `CLEAR`
  - Else → claim verdict = `NOT_CHECKED`

### Phase B: Assign claim properties
- `verdict`: aggregated from checkers
- `verdict_confidence`: high/medium/low from checker confidence, using lowest confidence among flagged categories
- `flagged_categories`: list of all categories that reported FLAGGED for this claim
- `color`: derived from verdict and most severe flagged category (severity: domain_violation > literature_collision > internal_contradiction > ambiguous > unreferenced)
  - FLAGGED → use most severe category color
  - INCONCLUSIVE → yellow (#F1C40F)
  - CLEAR → green (#2ECC71)
  - NOT_CHECKED → gray (#95A5A6)
- `evidence`: array of evidence pointers from VERIFICATION.md

### Phase C: Aggregate group verdicts
For each group, apply aggregation rule from graph_schema.md:
- If any child claim is FLAGGED → group is FLAGGED (with most severe child category color)
- Else if any child claim is INCONCLUSIVE → group is INCONCLUSIVE (yellow)
- Else if all children are CLEAR → group is CLEAR (green)
- Else (mix of CLEAR and NOT_CHECKED) → group is NOT_CHECKED (gray)

### Phase D: Validate
- Validate output against `src/conventions/graph_schema.json`
- Check: ≤20 groups, 1≤claim_ids≤15 per group, all parents resolve, all edges target valid claims
- Verify no edges have source == target
- Verify color format matches hex pattern

### Phase E: Write output
- Write `reviews/easy/phase2/outputs/graph.v2.json`

## Expected Results (sanity check)
From VERIFICATION.md quick tally: ~41 FLAGGED entries + ~8 INCONCLUSIVE entries across 5 checkers.
After per-claim aggregation: ~35–40 unique FLAGGED claims, ~6–8 INCONCLUSIVE, rest CLEAR.

Actual counts:
- FLAGGED claims: 35
- INCONCLUSIVE claims: 3
- CLEAR claims: 162
- Groups with FLAGGED: 14 (flagged status propagates from children)
- Groups with INCONCLUSIVE: 1
- Groups CLEAR: 5

## Notes
- Phase 1 carry-over issues (E017 and C003/C005 provenance) are preserved as-is in graph.v2.json
- No modifications to VERIFICATION.md or graph.v1.json
- Graph structure (groups, claims, edges) remains identical; only verdict layer changes
