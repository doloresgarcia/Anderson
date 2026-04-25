# Claim taxonomy (PLACEHOLDER — fill in before serious use)

> **Status: PLACEHOLDER.** Until this file is written, the `claim_extractor` tags
> every extracted claim as `UNCLASSIFIED` and logs the gap.

## What this file must specify

### What counts as a claim

A precise definition of what a "claim" is for the purpose of this project. Common
choices:

- any verifiable factual assertion
- only the paper's stated contributions / results
- claims + assumptions + definitions
- something else

### The type set

A closed list of claim types. For each type:

- name (e.g. `result`, `method`, `assumption`, `prior_work`, `numerical_fact`,
  `interpretation`)
- one-sentence definition
- 1–2 examples from a real paper

### Boundary cases

Rules for cases where the extractor will otherwise guess:

- compound sentences asserting multiple claims — split or keep together?
- claims attributed to other papers ("Smith et al. show that …") — claim or
  citation?
- hedged claims ("we suggest", "it is likely that …") — claim or not?
- claims in figure captions and tables

### Granularity

- one claim per sentence?
- one claim per logical proposition (multiple per sentence allowed)?
- minimum claim size?

## Until this file is filled in

Every claim in `CLAIMS.md` is tagged `UNCLASSIFIED`. Reviewers raise a Category B
finding.
