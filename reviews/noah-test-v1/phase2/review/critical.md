# Phase 2 Critical Review

## Category-A findings (blocking)

### A1 — claim-0098 verdict inconsistent with domain_violation finding for claim-0099

The domain checker correctly flags **claim-0099** ("grade mixing can occur through the combined action of boosts and rotations") as a domain violation: the sandwich product vxv⁻¹ with v in the Spin group is grade-preserving by the versor representation theorem, so the paper's statement is wrong. However, **claim-0098** ("Lorentz transformations will never mix grades") — which is the *correct* statement and the one motivating the architectural design — is marked `PASS` in `graph.v2.json` without an individual VERIFICATION.md entry.

The problem: if claim-0099 is a genuine domain violation, the checker must explain how claim-0098 (the paired, affirmative claim) was evaluated. The `graph_builder` needs to show that the FLAGGED finding for claim-0099 does not undermine the PASS for claim-0098, or explicitly note that 0098 is the correct statement and 0099 contradicts it. As written, a reader of the graph sees claim-0098 as PASS (green) and claim-0099 as FAIL (red) with no edge connecting them, while STRATEGY.md explicitly marks both as `high / high / domain_violation, internal_contradiction`. The graph is missing a `contradicts` edge between claim-0099 and claim-0098 that was required by STRATEGY.

**Evidence:** `graph.v2.json` — `claim-0098.verdict = PASS`, `claim-0099.verdict = FAIL`; no edge between them. STRATEGY.md row for claim-0098: `| claim-0098 | high | high | domain_violation, internal_contradiction`.

---

### A2 — Batch-CLEAR treatment of high-importance, high-checkability internal_contradiction and literature_collision claims

The `checker_contradiction` and `checker_literature` sections close with "All other checked claims: CLEAR" without individually addressing **22 high-importance, high-checkability claims** that STRATEGY.md assigned to `internal_contradiction` or `literature_collision`. Per `conventions/error_categories.md`, FLAGGED findings require evidence pointers — but the issue here is the inverse: claims that STRATEGY.md directed checkers to examine individually were disposed of by a batch statement with no documented reasoning.

The following high-importance claims with `internal_contradiction` or `literature_collision` categories in STRATEGY.md are not individually named anywhere in VERIFICATION.md (they receive neither FLAGGED, INCONCLUSIVE, nor individual CLEAR entries):

- **literature_collision**: claim-0023, claim-0030, claim-0109, claim-0160, claim-0201, claim-0288, claim-0289, claim-0290, claim-0291, claim-0292, claim-0341, claim-0355, claim-0395
- **internal_contradiction**: claim-0040, claim-0155, claim-0224, claim-0225, claim-0226, claim-0229, claim-0293, claim-0298, claim-0341, claim-0344, claim-0378, claim-0471, claim-0475, claim-0476, claim-0478, claim-0485, claim-0487, claim-0489

All are `verdict: PASS` in the graph. This is not self-evidently wrong — many may be genuinely CLEAR — but the checkers are required to document their reasoning for high-importance claims individually, not sweep them under a batch clear. The `checker_literature` section does contain useful key notes (e.g., ParT/MIParT numbers confirmed, LorentzNet/PELICAN descriptions accurate) but does not address the individual claims by ID. Similarly, the `checker_contradiction` section addresses only three contradiction pairs explicitly.

**Evidence:** STRATEGY.md rows for claim-0288, claim-0289, claim-0290, claim-0291, claim-0292 — all `high / high / literature_collision`; VERIFICATION.md `## literature_collision` section names only claim-0384 and claim-0522 individually. STRATEGY.md rows for claim-0471, claim-0475, claim-0478, claim-0485, claim-0489 — all `high / high / internal_contradiction`; VERIFICATION.md `## internal_contradiction` section names only claim-0165, claim-0441, claim-0365.

---

## Category-B findings (weakening)

### B1 — claim-0336 assigned to wrong primary category

STRATEGY.md categorizes claim-0336 as `literature_collision` (verify JetClass count against Qu:2022mxj). The `checker_unreferenced` correctly flags it for missing citation, and the `checker_literature` confirms the fact is accurate per Qu:2022mxj. However, the `checker_literature` section's key notes state "JetClass dataset description (100M jets, 10 classes) is accurate per Qu:2022mxj" without also noting that claim-0336 has no cite_key linking to that paper — a useful cross-reference that would clarify that the unreferenced flag and the literature accuracy finding are compatible. The current presentation could mislead a reader who sees the literature section's CLEAR-level note and assumes no action is needed.

**Evidence:** VERIFICATION.md `## unreferenced`, claim-0336; VERIFICATION.md `## literature_collision` key notes.

### B2 — cite-key mismatch for Bogatskiy (paper uses Bogatskiy:2023nnw; bib has Bogatskiy:2022czk) documented in key notes but not elevated to a finding

The `checker_literature` notes a bibliography management gap: the paper cites `Bogatskiy:2023nnw` at lines 476 and 494, but `references.bib` contains only `Bogatskiy:2022czk`. This affects claim-0289 (PELICAN description) and claim-0023 (Lorentz-equivariant taggers). The checker calls it "not a literature collision," which is correct categorically, but it is also not documented as an INCONCLUSIVE entry, leaving these two high-importance claims without a resolvable citation. Given that claim-0289 is `high / high / literature_collision` in STRATEGY.md, this should have been an INCONCLUSIVE entry rather than a key note, so it would propagate to the graph.

**Evidence:** VERIFICATION.md `## literature_collision` key notes, line referencing `Bogatskiy:2022czk`/`Bogatskiy:2023nnw`; `claim-0289.verdict = PASS` in graph.

### B3 — claim-0099 FLAGGED as domain_violation but also flagged under ambiguous with no cross-reference

Both the `checker_ambiguous` and `checker_domain` independently flag claim-0099. The ambiguous entry at VERIFICATION.md line ~130 notes that "grade mixing" is ambiguous between two interpretations, with confidence: high. The domain_violation entry independently concludes the paper's statement is wrong on the grounds that the sandwich product is grade-preserving. There is no cross-reference between these two findings, and the graph records `verdict: FAIL` for claim-0099 — correctly — but the `evidence` field only references the domain finding. The graph's `verdict_confidence` field should ideally note that two independent checkers flagged this claim, strengthening the FAIL verdict.

**Evidence:** VERIFICATION.md `## ambiguous`, claim-0099 (paper.txt:230); VERIFICATION.md `## domain_violation`, claim-0099 (paper.txt:229); `graph.v2.json` claim-0099 `evidence: ["paper.txt:229"]`.

### B4 — G006 ("linear equivariant layers") verdict is NOT_CHECKED despite containing high-importance claims

Group G006 contains claim-0106 ("exactly equivariant under Lorentz group transformations"), claim-0108, claim-0117, claim-0119, claim-0122, claim-0123, claim-0128 — all `high / high / domain_violation` in STRATEGY.md — and correctly shows `NOT_CHECKED` because the checkers did not individually address them. While this may be intentional (those claims were not in scope for a particular checker's pass), it means 25 claims in G006, several of high importance, have received no verification status at all. A reader of the graph cannot distinguish "checked and passed" from "never examined."

**Evidence:** `graph.v2.json` G006 `verdict: NOT_CHECKED`; STRATEGY.md rows for claim-0106, claim-0108, claim-0117, claim-0119, claim-0122, claim-0123, claim-0128.

---

## Verdict

**ITERATE**

The structural validation passes completely (0 violations). The three domain_violation and three internal_contradiction FLAGGED findings are well-evidenced and cite paper.txt line pointers. However, A2 is a genuine blocking issue: the checkers swept 22 high-importance, high-checkability claims into a batch CLEAR without individual documentation for claims that STRATEGY.md specifically directed them to examine. This is not a minor omission — claims like claim-0471 ("L-GATr outperforms the baselines across all distributions"), claim-0341 ("significant improvement over the previous state-of-the-art"), and claim-0488/0489 (Outlook summary claims) are core contribution claims that require individual CLEAR reasoning before the phase can be committed. Required fixes:

1. **A1**: Add a `contradicts` edge between claim-0099 and claim-0098 in `graph.v2.json`, or document in the domain_violation finding why claim-0098 is PASS despite the paired domain violation on claim-0099.
2. **A2**: The checker_contradiction and checker_literature agents must individually address — with at least one sentence of reasoning — each high-importance claim in their category from STRATEGY.md. Batch clears are acceptable for `low` or `medium` importance claims; `high/high` claims require individual treatment.
3. **B2**: Elevate the Bogatskiy cite-key mismatch for claim-0289 to an INCONCLUSIVE entry and update `graph.v2.json` accordingly.
