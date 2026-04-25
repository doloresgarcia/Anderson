# Verification rules (PLACEHOLDER — fill in before serious use)

> **Status: PLACEHOLDER.** Until this file is written, the `strategist` marks every
> claim's method as `TBD` and the `verifier` returns `INCONCLUSIVE` for every
> assigned claim with reason "verification rules unspecified".

## What this file must specify

### Method catalog

A closed list of verification methods, each with:

- name (e.g. `internal_consistency`, `external_corroboration`,
  `numerical_recompute`, `proof_audit`, `dataset_recheck`)
- input requirements (what the verifier needs to read)
- procedure (step-by-step)
- pass / fail / inconclusive criteria — explicit and ideally mechanical

### Method-to-claim-type mapping

For each claim type from `claim_taxonomy.md`, the default method (or set of
methods). The strategist follows this mapping; deviations require justification.

### Evidence standards

What counts as evidence good enough to support each verdict:

- PASS — what is sufficient
- FAIL — what is required (recall: "it doesn't seem right" is INCONCLUSIVE)
- INCONCLUSIVE — what reasons are acceptable (paywalled source, ambiguous
  wording, method not applicable, …)

### External-source hierarchy

When the literature contradicts a claim, which sources outrank which? E.g.:

- peer-reviewed > preprint > technical report > blog post
- domain-canonical reference (e.g. PDG for particle physics) > generic survey

This is the rule reviewers use to decide whether a `FAIL` is warranted.

## Until this file is filled in

The strategist still ranks claims and produces `STRATEGY.md`, but every method
column is `TBD`. The verifier still iterates the list but every verdict is
`INCONCLUSIVE`. Phase 3 still runs and produces a report — just one that says
mostly "not checked".

This degraded mode exists so the orchestration loop can be exercised before the
domain conventions are nailed down.
