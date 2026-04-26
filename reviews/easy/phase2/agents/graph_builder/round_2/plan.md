# Phase 2 Round 2 Plan — graph_builder — slug: easy

Date: 2026-04-26

## Objective

Regenerate `graph.v2.json` by merging verdicts and evidence from the re-concatenated `VERIFICATION.md` (after the fixer's round-1 edits to per-checker section.md files) onto the claims and groups in `graph.v1.json`.

## Strategy

1. **Read graph.v1.json**: Start with the 200 claims and 20 groups (unchanged).

2. **Parse VERIFICATION.md**: Extract verdicts and evidence for all five checker categories:
   - unreferenced (114 claims: C001, C002, C004, C007, C029, C031, C036, C041, C054, C060, C070, C094, C100-C104, C112, C117, C129, C131, C138, C142, C157, C162, C180, C181, C183-C185, C191, C193, C195, C197-C198)
   - ambiguous (27 FLAGGED: C001, C003, C004, C015, C017, C026, C029, C033, C040, C052, C054, C057, C070, C074, C086, C093, C129, C142, C166, C175, C181, C182, C186, C191, C192, C193, C196)
   - internal_contradiction (12 key claims: C001-C004, C038, C060, C065, C069, C077, C078, C081-C084, C094, C101, C104, C112, C117, C119, C129-C131, C138, C148, C180, C183-C185, C193, C195, C197-C198)
   - literature_collision (1 FLAGGED: C157; rest CLEAR)
   - domain_violation (1 FLAGGED: C068; rest CLEAR)

3. **Aggregate verdicts per claim**:
   - Any FLAGGED from any checker → claim verdict = FLAGGED
   - Else any INCONCLUSIVE → claim verdict = INCONCLUSIVE
   - Else all CLEAR → claim verdict = CLEAR
   - Else NOT_CHECKED

4. **Capture evidence**:
   - For each FLAGGED claim, read the full evidence entries from VERIFICATION.md (each checker section)
   - For C068: include paper.txt passage + violated_principle + canonical_source (from domain_violation section)
   - For C183/C185: include both contradicting passages with provenance (from internal_contradiction section)
   - For C157: include paper passage + cited-source contradiction snippet + corrected-citation note (from literature_collision section)
   - For CLEAR claims with inline evidence (one-liners from unreferenced section): include as single evidence entry
   - Deduplicate identical evidence strings

5. **Color mapping** (per error_categories.md severity):
   - domain_violation (#7B1FA2 purple)
   - literature_collision (#D32F2F red)
   - internal_contradiction (#FF6D00 orange)
   - ambiguous (#FFBF00 amber)
   - unreferenced (#4285F4 blue)
   - CLEAR (#2ECC71 green)
   - INCONCLUSIVE (#F1C40F yellow)
   - NOT_CHECKED (#808080 gray)

6. **Aggregate group verdicts**: Apply verdict rules to claim children per graph_schema.md.

7. **Preserve edges**: Keep the 20 edges from graph.v1.json unchanged.

8. **Validate**: Schema-validate the final graph.v2.json against graph_schema.json.

## Expected outputs

- 35 FLAGGED claims (give or take 1–2)
- 3 INCONCLUSIVE claims (C077, C112, C195)
- ~162 CLEAR claims
- 200 total claims (unchanged)
- 20 groups (unchanged)
- 20 edges (unchanged)

## Fixer round-1 coordination

The fixer populated evidence fields for:
- C068: violated_principle + canonical_source (now in checker_domain/section.md)
- C183/C185: dual-passage evidence (now in checker_contradiction/section.md)
- C001, C003, C070, C191, C193: deduplicated evidence

This regeneration will read these values from VERIFICATION.md and encode them consistently in graph.v2.json.

## Risk notes

- If evidence format in VERIFICATION.md differs from prior graph.v2.json encoding, the regenerated output may have different string formatting (e.g., wrapping, line-breaks) but should capture the same semantic content.
- C077 (internal_contradiction) is explicitly INCONCLUSIVE due to unresolvable "72 channels" arithmetic; preserved as-is.
- C112 (internal_contradiction) is INCONCLUSIVE due to "new record" vs. "at least on par" tension; preserved as-is.
- C195 (internal_contradiction) is INCONCLUSIVE due to "three particles" reference ambiguity; preserved as-is.
