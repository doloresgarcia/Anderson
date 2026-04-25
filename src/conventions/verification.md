# Verification rules (PLACEHOLDER — fill in before serious use)

> **Status: PLACEHOLDER.** Until this file is written, the checkers fall back
> to their built-in evidence standards from `conventions/error_categories.md`.
> Filling this file in adds domain-specific refinements on top of those
> defaults.

## Relationship to error categories

The five error categories and their evidence standards are defined in
`conventions/error_categories.md`. This file provides **domain-specific
refinements** — additional rules, thresholds, or method details that tailor the
checkers' behavior to the field of the paper under review.

## What this file must specify

### Domain-specific method details

For each error category, optional refinements:

- **unreferenced** — what counts as "common knowledge" in this field (exempt
  from citation requirements); any field-specific citation norms.
- **ambiguous** — domain-specific terms that require precise definitions;
  accepted conventions for quantifiers in this field.
- **internal_contradiction** — numerical precision thresholds (e.g., when do
  two reported numbers count as contradictory vs. rounding differences).
- **literature_collision** — field-specific source hierarchy and precedence
  rules.
- **domain_violation** — canonical references, textbooks, or authoritative
  sources for the field; which principles are considered settled.

### External-source hierarchy

When the literature contradicts a claim, which sources outrank which? E.g.:

- peer-reviewed > preprint > technical report > blog post
- domain-canonical reference (e.g. PDG for particle physics) > generic survey

This is the rule reviewers use to decide whether a `literature_collision`
flag is warranted.

## Until this file is filled in

The five checker agents still run using the evidence standards from
`conventions/error_categories.md`. The strategist still ranks claims and
produces `STRATEGY.md`. Phase 3 still runs and produces a report. Results
will be reasonable but may miss field-specific nuances.

This degraded mode exists so the orchestration loop can be exercised before the
domain conventions are nailed down.
