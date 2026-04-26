# Fixer Round 1 Log — slug: easy — phase 2

Date: 2026-04-26
Fixer: fixer (round 1)

---

## M2 [A] — Populate evidence arrays for C183 and C185 in graph.v2.json

**Status: RESOLVED**

**File edited:** `reviews/easy/phase2/outputs/graph.v2.json`

**Change:** Added evidence arrays to C183 and C185 nodes, copying the contradicting passage pair from `checker_contradiction/section.md`.

- C183 evidence now contains:
  1. `paper.txt:1660-1661, 1926` — primary claim passage ("clear performance improvement")
  2. `paper.txt:1928` — contradicting passage ("only marginally better")

- C185 evidence now contains:
  1. `paper.txt:1928` — primary claim passage ("only marginally better")
  2. `paper.txt:1660-1661, 1926` — contradicting passage ("clear performance improvement")

The evidence strings were sourced from `checker_contradiction/section.md` lines 136-152, which already contained the correct full quotes and line citations. No new evidence was fabricated.

**Coordination note:** `checker_contradiction/section.md` already contains the full evidence; the graph.v2.json edits mirror that source. The orchestrator's graph_builder re-run will regenerate from section.md and should produce consistent results.

---

## M1 [A] — Populate evidence for C068 in graph.v2.json

**Status: RESOLVED**

**File edited:** `reviews/easy/phase2/outputs/graph.v2.json`

**Change:** Added two additional evidence strings to the C068 node's existing evidence array:

1. `violated_principle` string: "The stabilizer subgroup of the pair {(1,0,0,1), (1,0,0,-1)} in SO+(1,3) is SO(2) (rotations around the beam axis), not SO(3). Stab_{SO+(1,3)}{(1,0,0,0)} = SO(3); within SO(3), Stab{(0,0,0,1)} = SO(2). Fixing both the time direction and the beam direction reduces the preserved symmetry to SO(2), not SO(3)."
2. `canonical_source` string: "Weinberg, The Quantum Theory of Fields Vol. 1, §2.5 (little group classification of Lorentz subgroups)"

The paper.txt:549-554 provenance entry was already present and is kept unchanged.

**Sourced from:** `checker_domain/section.md` lines 181-186 (the C068 FLAGGED entry).

**Coordination note:** `checker_domain/section.md` already contains the `violated_principle` and `canonical_source` fields. The graph.v2.json edits mirror that content. The graph_builder re-run will regenerate and should produce the same values.

---

## M3 [A] — Add corrected-citation note for C157 in checker_literature/section.md

**Status: RESOLVED**

**File edited:** `reviews/easy/phase2/agents/checker_literature/section.md`

**Change:** Added a `corrected-citation note` field to the C157 FLAGGED entry after the existing `reasoning` field.

**Citation analysis:** The arbiter suggested `heimel2023madnis` as a candidate. Checking `references.bib`: `heimel2023madnis` ("MadNIS — Neural Multi-Channel Importance Sampling", SciPost Phys. 15 (2023) 141) describes neural importance sampling using normalizing flows for LHC event generation — not a CFM-superiority benchmark. It does not establish CFM as the leading technique for precision partonic LHC event generation.

No entry in references.bib directly supports the claim that CFM is "currently the leading technique in precision generation of partonic LHC events."

**Note written:** "No clearly-correct citation found in references.bib; the claim itself may need to be softened to 'one of the leading techniques' or attributed to a specific generative-model survey." — per the instruction to not fabricate bibtex keys.

---

## M5 [B] — Add C002 unreferenced entry in checker_unreferenced/section.md

**Status: RESOLVED**

**File edited:** `reviews/easy/phase2/agents/checker_unreferenced/section.md`

**Change:** Inserted a new `### C002 — CLEAR — confidence: high` entry between C001 and C004, with reasoning: "L-GATr represents data in G_{1,3} and is equivariant under Lorentz transformations by architectural construction. This is the paper's own self-describing architectural claim; no external citation is required for a self-describing architectural property. CLEAR as novel contribution."

**Basis:** C002 is tagged importance=high and unreferenced in STRATEGY.md but was absent from the unreferenced section. As a self-describing architectural claim, CLEAR is the correct verdict per `error_categories.md`.

---

## M9 [B] — Add unreferenced entries for C029, C031, C036, C041, C054

**Status: RESOLVED**

**File edited:** `reviews/easy/phase2/agents/checker_unreferenced/section.md`

**Changes:** Inserted five new entries in numeric order (after C007, before C060):

- **C029 — CLEAR:** PID encoding (xS = PID, xV_µ = pµ) is the paper's own design decision; no external citation required. Evidence: paper.txt:232-240.
- **C031 — CLEAR:** |M|² decomposition is elementary complex algebra (standard identity); no external citation required. Evidence: paper.txt:242-248.
- **C036 — CLEAR:** Limitation that G_{1,3} cannot represent symmetric rank-2 tensors is a known Clifford algebra result; checker_domain confirms CLEAR. Paper acknowledges it as a limitation. Evidence: paper.txt:303-304.
- **C041 — CLEAR:** "Most general linear combination" follows from Schur's lemma (confirmed by checker_domain); novel architectural application. Evidence: paper.txt:371-390.
- **C054 — CLEAR:** "Performance can degrade significantly" is a hedged design-observation claim substantiated by ablation Tables 3 and 7 within the paper. Evidence: paper.txt:515-516.

All five rated CLEAR (no external citation needed). None shows evidence of an uncited external claim that would warrant FLAGGED.

---

## M10 [B] — Deduplicate evidence arrays in graph.v2.json

**Status: RESOLVED (confirmed instances fixed)**

**File edited:** `reviews/easy/phase2/outputs/graph.v2.json`

**Changes (deduplication):**

- **C001:** Had 3 entries for paper.txt:16-17 with different formatting. Reduced to 1 (most informative, with snippet text).
- **C003:** Had 2 entries for paper.txt:18-20 and paper.txt:18-19 with different formatting. Reduced to 1 (most informative, with full snippet text).
- **C070:** Had 2 entries — bare `paper.txt:555–556` and longer `paper.txt:555-557 — "..."`. Kept the informative entry with snippet text; removed the bare one.
- **C191:** Had 2 entries — bare `paper.txt:1947–1949` and full `paper.txt:1947-1949 — "..."`. Kept the informative entry; removed the bare one.
- **C193:** Had 2 near-identical entries for paper.txt:1950-1952 differing only in parenthesis vs em-dash formatting. Kept the em-dash version (consistent with other entries); removed the parenthesis duplicate.

**Non-deduplicated:** C082 has `"paper.txt:594-595; paper.txt:593-594"` as a single string — this is one evidence entry containing two line references, not two duplicate entries. Left as-is per the "do not collapse genuinely distinct evidence pieces" rule.

---

## M7 [B] — C157 cross-reference in checker_unreferenced/section.md

**Status: RESOLVED**

**File edited:** `reviews/easy/phase2/agents/checker_unreferenced/section.md`

**Change:** Added evidence line to the C157 CLEAR entry: "paper.txt:1421-1422 — Claim has a citation [77] (butter2023jetdiffusion); citation content does not support the claim — see literature_collision section for the FLAGGED verdict."

This satisfies both M7 (cross-reference) and M8 (evidence one-liner) simultaneously for C157.

---

## M8 [B] — Evidence one-liners for bare CLEAR Tier-1 entries in checker_unreferenced/section.md

**Status: RESOLVED**

**File edited:** `reviews/easy/phase2/agents/checker_unreferenced/section.md`

**Changes:** Added one-line evidence notes to the following previously bare CLEAR entries:

| Claim | Evidence added |
|-------|----------------|
| C100  | paper.txt:747-751, Fig. 2 left panel |
| C101  | paper.txt:749-751, Fig. 2 left panel |
| C104  | paper.txt:757-758, Fig. 2 right panel |
| C112  | paper.txt:772-773, Tables 2 and 4 |
| C117  | paper.txt:1003-1004, Table 2 |
| C129  | paper.txt:1036-1038, Table 4 |
| C131  | paper.txt:1111-1112, Fig. 4 left panel + Table 5 |
| C138  | paper.txt:1339-1340, Table 2 fine-tuning rows |
| C157  | paper.txt:1421-1422 (handled under M7 above) |
| C180  | paper.txt:1649-1651, Fig. 6 |
| C181  | paper.txt:1650-1651, Fig. 6 |
| C183  | paper.txt:1660-1661, Fig. 7 (+ cross-ref to contradiction section) |
| C184  | paper.txt:1927-1928, Fig. 7 |
| C185  | paper.txt:1928-1929, Fig. 7 (+ cross-ref to contradiction section) |
| C193  | paper.txt:1950-1952, Tables 3 and 7 |
| C195  | paper.txt:1954-1956, Fig. 2 left panel |
| C197  | paper.txt:1957-1958, Table 2 fine-tuning rows |
| C198  | paper.txt:1959-1961, Fig. 7 |

Notes:
- C001 and C004 were also bare CLEAR entries (not in the M8 list but were edited while addressing M5). Evidence one-liners added for consistency — this is a minor scope expansion but harmless. If the reviewer considers this out of scope, these entries can be reverted.
- C183 and C185 have CLEAR verdicts in the unreferenced section (for a different reason than their FLAGGED contradiction verdicts). One-line notes added for both, with a cross-reference to the internal_contradiction section.

---

## M6 [B] — Reconcile ambiguous count text

**Status: RESOLVED**

**File edited:** `reviews/easy/phase2/agents/checker_ambiguous/section.md`

**Change:** Added an HTML comment to the `## ambiguous` section header explaining the count discrepancy:

"The orchestrator dispatch summary cited 29 FLAGGED ambiguous claims; the actual artifact contains 27 FLAGGED entries [...]. The artifact count of 27 is authoritative. The summary overcounted by 2; no claims were dropped during concatenation — the section.md is the complete checker output."

The 27 FLAGGED claims enumerated in the comment: C001, C003, C004, C015, C017, C026, C029, C033, C040, C052, C054, C057, C070, C074, C086, C093, C129, C142, C166, C175, C181, C182, C186, C191, C192, C193, C196.

---

## M4 [B] — Optional C068 confidence + canonical_source clarification

**Status: RESOLVED (optional item addressed)**

**File edited:** `reviews/easy/phase2/agents/checker_domain/section.md`

**Change:** Extended the `canonical_source` field for C068 to include an explanatory note: "Weinberg §2.5 covers the little-group formalism — the classification of irreducible representations of the Lorentz group by the stabilizer (little group) of a reference 4-momentum, which is directly applicable here to the stabilizer of the pair of reference multivectors."

**Confidence:** Left at medium (not raised to high). The critical reviewer's concern is noted, but medium confidence reflects appropriate caution — the stabilizer computation is elementary, but the connection to Weinberg §2.5 (which covers massive-particle little groups, not directly the stabilizer of two spacelike vectors) is indirect. A more conservative confidence level is retained.

---

## C findings (M11–M16)

Per the arbiter's instructions, C findings are recorded only and are non-blocking.

- **M11 (C068↔C185 mutual-contradiction edge):** Not added. Optional per arbiter. Graph remains technically valid without it.
- **M12 (C068 secondary evidence paper.txt:553-554):** Not added. Optional per arbiter.
- **M13 (ambiguous coverage skew, C060 gap):** No action required per arbiter.
- **M14 (VERIFICATION.md preamble):** No action required per arbiter.
- **M15 (C077 disposition note):** No action required per arbiter.
- **M16 (C003/C005 Phase-1 carry-over confirmation):** No action required per arbiter.

---

## Coordination note for graph_builder re-run

The orchestrator's next graph_builder re-run will regenerate graph.v2.json from the section.md files. The direct edits to graph.v2.json (M1, M2, M10) are also reflected in the upstream section.md files (M1/M2 evidence is in checker_domain/section.md and checker_contradiction/section.md respectively; M10 deduplication fixes noise introduced by graph_builder's concatenation). The graph_builder re-run should produce results consistent with the direct graph.v2.json edits, since the section.md files are the authoritative source.

**Risk:** If graph_builder regenerates C068/C183/C185 evidence arrays by re-reading only the section.md files and does not carry forward the `violated_principle` / `canonical_source` / contradiction-passage formats, those fields may be regenerated in a different format. The fixer's direct graph.v2.json edits serve as the target reference for what the regenerated output should contain.

---

## Validation status

After all edits:
- All five section.md files are non-empty and well-formed.
- The C157 corrected-citation note does NOT introduce a fabricated bibtex key (writes "no clearly-correct citation found" per instructions).
- graph.v2.json structural edits are confined to string content within existing `"evidence"` arrays; JSON structure is unchanged.
- All 200 claim_ids remain present in graph.v2.json (no nodes added or removed).
- Schema validation: no structural properties were changed that would affect schema compliance; the schema allows `"evidence"` as an array of strings (additionalProperties: true), so the new evidence strings are valid.
