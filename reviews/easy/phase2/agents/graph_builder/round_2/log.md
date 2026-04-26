# Phase 2 Round 2 Log — graph_builder — slug: easy

Date: 2026-04-26

## Summary

Successfully regenerated `graph.v2.json` by merging verdicts and evidence from the re-concatenated `VERIFICATION.md` (after fixer round 1's updates to per-checker section.md files) onto `graph.v1.json`.

## Execution

1. **Parsed VERIFICATION.md**: Extracted verdicts and evidence from all five checker sections:
   - unreferenced: 114 claims parsed
   - ambiguous: 27 FLAGGED claims (per M6 count reconciliation in fixer log)
   - internal_contradiction: 12 key contradiction claims
   - literature_collision: 1 FLAGGED (C157), rest CLEAR
   - domain_violation: 1 FLAGGED (C068), rest CLEAR

2. **Aggregated verdicts per claim**:
   - FLAGGED if any checker reports FLAGGED
   - INCONCLUSIVE if any checker reports INCONCLUSIVE (and no FLAGGED)
   - CLEAR otherwise

3. **Captured evidence**: For each claim, collected evidence from all applicable checkers:
   - Multi-line evidence parsing improved to handle nested evidence blocks (e.g., C183/C185 dual passages)
   - Preserved special evidence fields: `[violated_principle]`, `[canonical_source]`, `[corrected-citation]`
   - Deduplicated identical evidence strings while preserving semantic distinctness

4. **Applied color mapping** per error_categories.md severity:
   - domain_violation: #7B1FA2 (purple) — highest severity
   - literature_collision: #D32F2F (red)
   - internal_contradiction: #FF6D00 (orange)
   - ambiguous: #FFBF00 (amber)
   - unreferenced: #4285F4 (blue)
   - CLEAR: #2ECC71 (green)
   - INCONCLUSIVE: #F1C40F (yellow)

5. **Aggregated group verdicts**: Applied verdict aggregation rule to group children.

6. **Preserved edges**: All 20 edges from graph.v1.json carried forward unchanged.

7. **Schema validation**: Validated output against `src/conventions/graph_schema.json` — PASSED.

## Outputs

- **File written**: `/afs/cern.ch/work/m/mgarciam/private/anderson_2/Anderson/reviews/easy/phase2/outputs/graph.v2.json`
- **Size**: ~145 KB (200 claims + 20 groups + 20 edges + evidence)

## Statistics

### Claims by verdict:
- **FLAGGED**: 35 (17.5%)
- **INCONCLUSIVE**: 3 (1.5%)
  - C077 (internal_contradiction: "72 channels" arithmetic)
  - C112 (internal_contradiction: "new record" vs. "at least on par")
  - C195 (internal_contradiction: "three particles" ambiguity)
- **CLEAR**: 162 (81%)

### Flagged by category:
- **domain_violation**: 1 (C068 — Lorentz stabilizer subgroup error)
- **literature_collision**: 1 (C157 — CFM cited incorrectly as leading technique)
- **internal_contradiction**: 3 (C004, C183, C185 — conflicting performance descriptions)
- **ambiguous**: 27 (per fixer M6 reconciliation)
- **unreferenced**: 7 (C007, C060, C070, C094, C142, C162, C191)

### Groups by verdict:
- **FLAGGED**: 11 groups (mixed flagged categories)
- **INCONCLUSIVE**: 1 group (G003)
- **CLEAR**: 8 groups

### Total structure:
- **Claims**: 200 (unchanged from v1)
- **Groups**: 20 (unchanged from v1)
- **Edges**: 20 (unchanged from v1)

## Key evidence notes

### C068 (domain_violation)
- Includes 3 evidence items:
  1. Paper passage (paper.txt:549-554)
  2. violated_principle: Lorentz stabilizer subgroup analysis
  3. canonical_source: Weinberg §2.5

### C183 / C185 (internal_contradiction)
- C183 evidence: 3 items (clear improvement passage + marginal improvement passage + unreferenced context)
- C185 evidence: 3 items (marginal passage + clear improvement passage + unreferenced context)

### C157 (literature_collision)
- Includes 3 evidence items:
  1. Paper passage with citation [77]
  2. Cited source (butter2023jetdiffusion) snippet showing it does NOT support CFM superiority claim
  3. Corrected-citation note: "No clearly-correct citation found in references.bib"

### C077, C112, C195 (INCONCLUSIVE)
- Each retains evidence despite INCONCLUSIVE verdict
- No additional evidence needed per fixer instructions

## Fixer round 1 coordination

The fixer's round 1 edits to per-checker section.md files are now reflected in regenerated graph.v2.json:

- **M1 (C068 evidence)**: violated_principle and canonical_source from checker_domain/section.md
- **M2 (C183/C185 evidence)**: dual contradicting passages from checker_contradiction/section.md
- **M10 (deduplication)**: applied during aggregation; identical evidence strings removed

No direct conflicts detected between fixer's graph.v2.json edits and regenerated output; format may differ slightly (e.g., line-wrapping) but semantic content is preserved.

## Validation results

- **jsonschema.validate()**: PASSED
- **Claim count**: 200 ✓
- **Group count**: 20 ✓
- **Edge count**: 20 ✓
- **Expected FLAGGED count**: ~35 ✓ (actual: 35)
- **Expected INCONCLUSIVE count**: 3 ✓ (actual: 3)
- **Expected CLEAR count**: ~162 ✓ (actual: 162)

## No issues detected

All verdict aggregations, evidence captures, color mappings, and edge preservation completed without error.
