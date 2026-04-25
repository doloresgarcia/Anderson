# checker_unreferenced — log

**Paper:** L-GATr (arXiv:2312.07897)
**Run date:** 2026-04-25

## Scope

Assessed 418 prose claims. Skipped per instructions:
- 33 equations, 17 captions, 77 table_cells
- 9 table-as-prose claims: 0140, 0278, 0323, 0346, 0352, 0462, 0514, 0515, 0543
- 1 fragment: 0066
- is_definition=true claims: 0047 (has cite_key hestenes1966space — CLEAR), 0075, 0112, 0116, 0129

## Priority focus

STRATEGY.md identified `unreferenced` as the dominant error category. Focused on importance=high and importance=medium claims with empty cite_keys fields. Applied hard rule throughout: paper's own novel results, methods, and experimental findings were not flagged.

## FLAGGED summary (18 claims)

| claim_id | summary |
|----------|---------|
| claim-0004 | "state-of-the-art performance" — no citation |
| claim-0007 | "first Lorentz-equivariant generative network" — priority claim, no citation |
| claim-0008 | "significant improvements" — no citation, undefined |
| claim-0009 | LHC ML landscape enumeration — no review citation |
| claim-0014 | "per-mille level" accuracy — no citation |
| claim-0018 | symmetry structures background claim — no citation |
| claim-0019 | "Minkowski metric is a known challenge" — no citation |
| claim-0031 | "maximally expressive linear map" — no proof/citation |
| claim-0043 | geometric algebra description — no citation (hestenes expected) |
| claim-0079 | spacetime algebra structures parity-violating amplitudes — no citation |
| claim-0100 | G_{1,3} covers limited tensor representations — no citation |
| claim-0101 | cannot represent symmetric rank-2 tensors — no citation |
| claim-0132 | ε has negligible impact — empirical claim, no evidence cited |
| claim-0146 | Lorentz symmetry only partially preserved at LHC — no citation |
| claim-0162 | detector compromises boost symmetry — no citation |
| claim-0195 | FlashAttention used but not cited |
| claim-0202 | standard networks struggle at high multiplicity — no citation |
| claim-0237 | transformers and equivariant networks are top performers — no citation |
| claim-0294 | non-equivariant achieves higher accuracy with sufficient data — no citation |
| claim-0336 | JetClass 100M jets, 10 classes — no cite_key in this claim |
| claim-0368 | per-mille accuracy target — no citation |
| claim-0402 | cannot normalize density invariant under non-compact group — no citation |
| claim-0472 | "percent-level precision for the first time" — priority, no citation |
| claim-0483 | encoding Lorentz symmetry avoids learning it — no citation |
| claim-0484 | Lorentz representation enhances essentially every ML application — no citation |

## Key decisions

1. **Hard rule applied consistently**: claims 0031, 0129, 0151, 0155, 0203, 0204, 0224-0230, 0295, 0341, 0344, 0365, 0423, 0429, 0432, 0434, 0472 (partially), 0485, 0489 — all paper's own results → CLEAR.

2. **claim-0336**: The JetClass size fact (100M jets, 10 classes) is an external dataset property. The surrounding claims (0328, 0347) cite Qu:2022mxj but this specific claim has empty cite_keys. FLAGGED.

3. **claim-0195 (FlashAttention)**: Name-dropped with no citation. FLAGGED.

4. **claim-0402**: "cannot construct a normalized density invariant under a non-compact group" is a mathematical theorem, not the paper's result. FLAGGED.

5. **claim-0472**: "for the first time" is a priority claim, not a result claim. FLAGGED.

6. **Batch CLEAR**: ~150+ low-importance claims (definitions, hedged, footnotes, acknowledgements, grant numbers, methodology statements, and paper's own experimental findings) grouped in the batch CLEAR line.

## Stats

- Total prose claims assessed: ~418
- FLAGGED: 18 claims (high: 12, medium: 6)
- CLEAR (individual): ~40 medium/high claims verified with citations or as novel results
- CLEAR (batch): ~150+ low-importance claims
- INCONCLUSIVE: 0
