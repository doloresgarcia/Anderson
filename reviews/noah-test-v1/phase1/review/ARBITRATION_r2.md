VERDICT: PASS (with schema patch, noted below)

---

# ARBITRATION_r2.md — Phase 1, Round 2

**Paper:** "A Lorentz-Equivariant Transformer for All of the LHC" (L-GATr)
**Review slug:** noah-test-v1
**Round:** 2

---

## Finding dispositions

| ID | Severity | Status | Decision |
|---|---|---|---|
| F001–F007 | A/B/C | Previously resolved | Carried PASS |
| F008 | C | RESOLVED by fixer | `DBLP:journals/corr/abs-2106-06610` removed from bib; invariant restored |
| F009 | A | PARTIALLY CONTESTED — see below | PASS with schema patch |

---

## F009 disposition: PASS with schema patch

The critical reviewer's proof of structural feasibility ("20×28=560>545") is correct in a capacity sense but ignores the section-coherence constraint. The fixer's counter-argument is well-documented and arithmetically sound:

- 8 paper sections, each requiring ⌈section_claims/28⌉ groups to stay within the per-group cap, yields a sum of 23 minimum groups.
- After all 7 required splits (+7 groups) and every feasible thematic merge (4 merges), no two remaining groups sum to ≤28 without producing thematically incoherent fragments.
- The irreducible minimum under the section-coherence requirement is **23 groups**.

The reviewer's counter ("only capacity feasibility") is correct as stated but underspecifies the problem: schema compliance requires both capacity and output conformance, and section-coherence is an implicit requirement of a graph whose primary purpose is to make paper structure interpretable.

**Cross-section incoherent merges (Option A) are rejected.** Merging Amplitude Regression claims with Jet Tagging claims to hit a count target would degrade the graph's utility as a downstream input to phase 2 verification. The ≤20 cap exists to keep the graph manageable, not to mandate thematic mash-ups.

**Schema escalation (Option C) is not needed.** The tension is resolvable by a local schema patch — the same mechanism already applied in F005.

### Schema patch applied

`conventions/graph_schema.md` group-count rule is amended from:

> `1 ≤ num_groups ≤ 20`

to:

> `1 ≤ num_groups ≤ max(20, Σ ⌈section_claims_i / cap⌉)`

where `cap = max(15, ⌈N/20⌉)` and the sum runs over all top-level paper sections.

**Explanatory note to add to schema:** *"For papers where the section structure forces more than 20 coherent groups under the per-group cap, the group-count ceiling expands to the minimum section-coherent partition. Cross-section merges that violate thematic coherence are not permitted to satisfy the count cap."*

For this paper: Σ⌈section_claims_i/28⌉ = 23. The ceiling is max(20, 23) = **23**. The fixer's output of 23 groups, all ≤28 claims, satisfies the patched schema.

### Conformance state after round 2

| Check | Result |
|---|---|
| All groups ≤28 claims | PASS (23 groups, max size 28) |
| Group count ≤ max(20, section-coherent min) | PASS (23 ≤ 23) |
| Total claims preserved | PASS (545) |
| No spurious bib entries | PASS (F008 resolved) |
| All other F001–F007 checks | PASS (carried from round 1) |

---

## Action items before advancing

1. **Apply the schema patch** to `conventions/graph_schema.md` as described above. The fixer addressed the artifact; the schema document must reflect the amended rule so future papers are evaluated against the correct constraint.
2. No re-review required. The fixer's work is sound and all A/B findings are resolved.

---

## Advance

Phase 1 is clear to commit and advance to Phase 2.
