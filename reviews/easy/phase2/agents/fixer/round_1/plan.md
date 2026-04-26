# Fixer Round 1 Plan — slug: easy — phase 2

Generated: 2026-04-26

## Summary of findings to resolve

| ID  | Sev | File(s) to edit | Action |
|-----|-----|-----------------|--------|
| M2  | A   | graph.v2.json   | Add C183 + C185 evidence arrays from checker_contradiction section |
| M1  | A   | graph.v2.json   | Add C068 violated_principle + canonical_source to evidence array |
| M3  | A   | checker_literature/section.md | Add corrected-citation note for C157 |
| M5  | B   | checker_unreferenced/section.md | Add C002 CLEAR entry |
| M9  | B   | checker_unreferenced/section.md | Add C029, C031, C036, C041, C054 entries |
| M10 | B   | graph.v2.json   | Deduplicate evidence arrays (C001, C003, C070, C191, C193 confirmed; check others) |
| M7  | B   | checker_unreferenced/section.md | Add cross-reference note to C157 entry |
| M8  | B   | checker_unreferenced/section.md | Add one-line evidence pointers for C100, C101, C104, C112, C117, C129, C131, C138, C180, C181, C183, C184, C185, C193, C195, C197, C198 |
| M6  | B   | checker_ambiguous/section.md   | Reconcile "29" count to "27" |
| M4  | B   | checker_domain/section.md      | Optional: add Weinberg §2.5 note |

## Evidence for M2 (C183 / C185) — from checker_contradiction/section.md

### C183 evidence
- Passage 1: paper.txt:1660-1661, 1926 — "In Fig. 7 we find a clear performance improvement as symmetry awareness increases, from the unstructured MLP over the permutation-equivariant transformer to the rotation-equivariant GATr and the Lorentz-equivariant L-GATr."
- Passage 2 (contradicting): paper.txt:1928 — "the rotation-equivariant E(3)-GATr performs only marginally better than the plain transformer."

### C185 evidence
- Passage 1: paper.txt:1928 — "the rotation-equivariant E(3)-GATr performs only marginally better than the plain transformer."
- Passage 2 (contradicting): paper.txt:1660-1661, 1926 — "In Fig. 7 we find a clear performance improvement as symmetry awareness increases, from the unstructured MLP over the permutation-equivariant transformer to the rotation-equivariant GATr and the Lorentz-equivariant L-GATr."

## Evidence for M1 (C068) — from checker_domain/section.md

- violated_principle: "The stabilizer subgroup of the pair {(1,0,0,1), (1,0,0,-1)} in the Lorentz group is SO(2) (rotations around the beam axis), not SO(3). Stab_{SO+(1,3)}{(1,0,0,0)} = SO(3); within SO(3), Stab{(0,0,0,1)} = SO(2). Fixing both time and beam directions reduces symmetry to SO(2)."
- canonical_source: "Weinberg, The Quantum Theory of Fields Vol. 1, §2.5 (little group classification of Lorentz subgroups)"

## Citation check for M3 (C157)

heimel2023madnis is in references.bib. It is "MadNIS — Neural Multi-Channel Importance Sampling" which is about neural importance sampling for LHC, uses normalizing flows (not specifically CFM). It does not benchmark CFM as the leading technique. Cannot cite heimel2023madnis as a correct citation for C157.

No other entry in references.bib specifically benchmarks CFM as the leading technique for partonic LHC event generation. Will write the "no clearly-correct citation found" note.

## Coordination note for graph.v2.json vs section.md

Direct edits to graph.v2.json for M1/M2/M10 should also be reflected in the section.md files where appropriate (M2 evidence already present in checker_contradiction/section.md; M1 evidence already present in checker_domain/section.md). The orchestrator's graph_builder re-run should produce consistent results since the section.md files are the upstream source.
