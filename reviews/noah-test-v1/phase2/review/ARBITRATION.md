# Phase 2 Arbitration

## Findings assessed

### A1: Missing `contradicts` edge between claim-0098 and claim-0099 — DOWNGRADED (Category-B)

**Reasoning.** The critical reviewer frames this as a structural gap: claim-0098 is PASS and claim-0099 is FAIL with no edge connecting them, while STRATEGY.md listed both under `domain_violation, internal_contradiction`. On inspection, this is not the structural failure alleged.

The checker_contradiction section addresses both claims individually (lines 61-67 of section.md) and marks both CLEAR — its reasoning is that claims 0098 and 0099 are not logically inconsistent: 0098 is the general statement (grade-preserving under the sandwich product) and 0099 is the qualification for composite multivector states. The checker_domain section independently reaches a different conclusion: claim-0099 is factually wrong because the versor representation theorem guarantees grade-preservation unconditionally, making the paper's "composite multivector states" qualification physically confused.

The resulting graph state — 0098 PASS, 0099 FAIL, no edge — is *correct*. These are not contradictory claims that need a `contradicts` edge; they are a true claim (0098) paired with a false one (0099). What is missing is a note in the domain_violation finding for 0099 making explicit that claim-0098 is the correct statement and 0099 departs from it. That is a documentation gap, not a graph structure error.

The critical reviewer's requirement for a `contradicts` edge is therefore not warranted: a `contradicts` edge would imply the two claims are mutually exclusive, but they are not — 0098 is right and 0099 is wrong on independent grounds (the versor theorem). The constructive reviewer correctly identifies that the checker should clarify the direction; this is a Category-B documentation issue.

**Required action (B-level):** Add a cross-reference note in the domain_violation entry for claim-0099 stating that claim-0098 is the correct form of the statement and that claim-0099 incorrectly qualifies it.

---

### A2: Batch-CLEAR treatment of high-importance `internal_contradiction` and `literature_collision` claims — SUSTAINED (Category-A, scope narrowed)

**Reasoning.** The critical reviewer lists 22 high-importance claims disposed of by batch clears. On inspection, the actual situation is mixed:

**checker_contradiction:** The section.md *does* individually address the high-importance claims cited. Every claim the reviewer lists as missing — claim-0040, claim-0155, claim-0224, claim-0225, claim-0226, claim-0229, claim-0293, claim-0298, claim-0341, claim-0344, claim-0378, claim-0471, claim-0475, claim-0476, claim-0478, claim-0485, claim-0487, claim-0489 — has its own named entry with at least one sentence of reasoning and a confidence level. The constructive reviewer flags claims-0004, claim-0229, claim-0471, claim-0487, claim-0489 as dismissed without explanation, but the section.md contains individual CLEAR entries for all of them (lines 37-43, 109-111, 173-175, 193-195, 199-203). The checker_contradiction agent met the individual-documentation standard for the internal_contradiction category.

**checker_literature:** This is the genuine gap. The section.md contains exactly two individually named claims (claim-0384 INCONCLUSIVE, claim-0522 INCONCLUSIVE), then terminates with "All other claims with literature entries: CLEAR." The high-importance literature_collision claims — claim-0023, claim-0030, claim-0109, claim-0160, claim-0201, claim-0288, claim-0289, claim-0290, claim-0291, claim-0292, claim-0341, claim-0355, claim-0395 — are disposed of entirely by this batch statement. None appear in VERIFICATION.md. The key notes section confirms the checker did examine some of these (ParT/MIParT numbers, LorentzNet/PELICAN descriptions, JetClass count), but this reasoning was written as prose notes rather than individual claim entries. For high-importance claims, the convention requires traceable per-claim documentation; "key notes" prose does not substitute for it.

The Bogatskiy cite-key mismatch (affecting claim-0289) is particularly problematic: the checker correctly identifies the gap in key notes but then still returns CLEAR for claim-0289 in the graph (`verdict=PASS`), when the appropriate disposition given an unresolvable cite-key is INCONCLUSIVE.

**This finding is sustained but scoped to checker_literature only.** The checker_contradiction agent is not in violation.

---

### B1: claim-0336 cross-reference gap between unreferenced and literature_collision — SUSTAINED

The checker_literature key notes confirm JetClass accuracy but do not note the missing citation — leaving a reader who sees the literature CLEAR note with a false impression that no action is needed. This is a real but minor documentation gap.

---

### B2: Bogatskiy cite-key mismatch (claim-0289) not elevated to INCONCLUSIVE — SUSTAINED

The checker_literature identified the cite-key mismatch (`Bogatskiy:2023nnw` vs. `Bogatskiy:2022czk`) and correctly classified it as a bibliography management gap rather than a literature collision. However, claim-0289 is `high / high / literature_collision` in STRATEGY.md, the cited key is unresolvable in references.bib, and the graph records `verdict=PASS`. An unresolvable key on a high-importance claim should yield INCONCLUSIVE, not PASS.

---

### B3: claim-0099 dual-flagged (ambiguous + domain_violation) without cross-reference — SUSTAINED

The ambiguous flag and the domain_violation flag are independent entries with no cross-reference. The graph records only one evidence pointer. As noted under A1, the direction is clear (0099 is wrong), but the graph's `evidence` field for claim-0099 should cite both findings. Minor.

---

### B4: G006 NOT_CHECKED for high-importance claims — SUSTAINED

Confirmed: G006 contains high-importance domain_violation candidates that received no checker pass. This is a coverage gap in the checkers' scope, not the graph_builder's error. As the phase 2 run is already complete, this is a deferred concern rather than a blocking fix — the claims in G006 were not assigned to any checker by the strategist.

---

### B5: Unreferenced summary count (25 FLAGGED, not 18) — SUSTAINED

Actual count in the unreferenced section of VERIFICATION.md: **25 FLAGGED** entries (not 18 as stated in the header, nor 24 as the constructive reviewer counted). This is a bookkeeping error in the summary header. Non-blocking but reduces trust in summary statistics.

---

### B6: claim-0007 "first ever" priority claim — SUSTAINED (constructive)

The literature_collision section returns CLEAR for claim-0007 with a key note that this is really an unreferenced/ambiguous concern. That categorization is correct (priority claims are not literature collisions unless a prior work exists in the bank). However, the checker_literature should have noted explicitly that no external search was performed to confirm the priority claim rather than implying CLEAR by omission. Minor.

---

### B7: claim-0018/0019 over-flagged as unreferenced — DISMISSED

The constructive reviewer suggests these are common-knowledge background physics statements that should not require citation. The conventions' evidence standard specifies "not common knowledge" as a prerequisite for an unreferenced flag. "Much of this knowledge is reflected in complex symmetry structures" (claim-0018) is arguably common knowledge in HEP-ML. The checker applied a conservative standard. This is a judgment call within the checker's discretion; DISMISSED as a blocking concern.

---

## Verdict: ITERATE

The checker_literature agent did not individually document the 13 high-importance, high-checkability `literature_collision` claims from STRATEGY.md. They were batch-cleared without per-claim entries, and claim-0289 — which has an unresolvable cite-key — was recorded as PASS rather than INCONCLUSIVE. These are the only blocking issues; checker_contradiction met the individual-documentation standard.

## If ITERATE: required fixes

1. **checker_literature (blocking):** Add individual CLEAR or INCONCLUSIVE entries for each high-importance `literature_collision` claim not yet named in VERIFICATION.md: claim-0023, claim-0030, claim-0109, claim-0160, claim-0201, claim-0288, claim-0289, claim-0290, claim-0291, claim-0292, claim-0341, claim-0355, claim-0395. Per-claim entries must include at least one sentence of reasoning. The key notes content already contains the reasoning; it needs to be restructured into named entries.

2. **claim-0289 graph verdict (blocking):** Change `claim-0289.verdict` in `graph.v2.json` from `PASS` to `INCONCLUSIVE` to reflect the unresolvable `Bogatskiy:2023nnw` cite-key. Add an `evidence` pointer to the bibliography gap note.

3. **VERIFICATION.md summary header (non-blocking, fix alongside above):** Correct `unreferenced: 18 FLAGGED` to `unreferenced: 25 FLAGGED`.

4. **claim-0099 domain_violation entry (non-blocking, fix alongside above):** Add a cross-reference note stating that claim-0098 is the correct form of the grade-preservation statement and that claim-0099's qualification is the error.
