# Fixer plan — phase 1, round 1

Address the 7 forwarded findings (F01-F08, F03 absorbs F06) in this order:

## Step 1 — F02: relocate build_v1.py
- Move `phase1/agents/graph_builder/build_v1.py` → `src/build_graph_v1.py`
- Verify removal from agent working directory.

## Step 2 — F03 + F06: confidence demotions in CLAIMS.md
- C036: medium → low (was already medium per CLAIMS.md inspection)
- C044: high → low
- C060: high → low
- C148: medium → low
- Leave C046 and C152 unchanged.

## Step 3 — F04: split C015 into 3 rows
- Update C015 sentence to first sub-claim ("we extend amplitude regression to handle high-multiplicity LHC events"); confidence medium; type method; provenance/line stays paper.txt:108.
- Append new rows C218 ("improve classification by introducing a new pre-training scheme") and C219 ("deliver a competitive Lorentz-equivariant generative network") at end of CLAIMS.md table. Both type=method, hedged=false, confidence=medium, line=108, section=1, provenance=paper.txt:108.
- Add `## C218` and `## C219` headings to LITERATURE.md (empty by default).

## Step 4 — F05: drop C188 and C189
- Remove rows C188 and C189 from CLAIMS.md (leaving a gap; do not renumber).
- Remove `## C188` and `## C189` headings from LITERATURE.md.

## Step 5 — F07: re-tag literature for C006
- `Butter:2017cot`: supports high → related medium
- `Bogatskiy:2022czk`: supports medium → related medium
- `Gong:2022lye`: supports medium → related medium
- Add note: "Phase-2 verifier should locate a quantitative source for the order-of-magnitude figure (e.g. Spinner:2024hjm §4 or Bogatskiy:2020tje)."

## Step 6 — F08: re-tag literature for C148
- `lipman2023flowmatching`: supports medium → related medium
- Add note: "Vanilla CFM (Lipman 2023) does not provide optimal-transport paths; that is the OT-CFM extension. Phase-2 verifier may flag the underlying claim wording."

## Step 7 — F01: deferral note in FINDINGS.md
- Add §8 "Deferred to phase 3" documenting that page-number recovery for paper.txt is intentionally deferred to phase 3 highlighter dispatch (which uses src/highlight_text.py to synthesize a paginated PDF).

## Cross-verification
- After all edits, count CLAIMS.md rows: expect 217 - 2 (drop C188/C189) + 2 (add C218, C219) = 217 rows in the table.
- Count LITERATURE.md `## Cxxx` headings: expect 217 - 2 (drop C188/C189) + 2 (add C218, C219) = 217 headings.
- IDs: gap at C188/C189; new IDs C218 and C219 at the end.

## Out of scope / forbidden
- Do not touch graph.v1.json, graph.v1.skeleton.json, references.bib.
- Do not touch C-category findings F09-F12.
- Do not modify role specs, methodology, or convention files.
- Do not renumber any existing IDs.
