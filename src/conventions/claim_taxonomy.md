# Claim taxonomy

Defines what a *claim* is for Anderson, the closed type set, granularity rules, and
boundary cases. The `claim_extractor` agent reads this file and tags every row in
`CLAIMS.md` accordingly.

Designed around **what verification looks like for each type** rather than
linguistic form — types that don't differentiate verification methods just create
noise.

## What counts as a claim

A claim is a **verifiable proposition** asserted by the paper. "Verifiable" means
it is in principle possible to check — not necessarily that we have the resources
to check it. Three filters:

1. **Propositional.** It states that something is the case. Questions, exhortations,
   and pure descriptions of what the paper *does* (e.g. "Section 3 presents the
   results") are not claims.
2. **Standalone.** A reader who reads only the claim and its provenance can
   understand what is being asserted, without scrolling.
3. **Asserted by the paper.** Restating someone else's result with attribution
   (`prior_work` below) counts; mere mentions ("see [12]") do not.

Reviewer headings, table headings, and citation lists are not claims.

## The type set

Seven types. Closed list — anything that doesn't fit gets the closest type plus a
note in the extractor's `log.md`.

### `result`

The paper's empirical or measurement output — a number, a comparison, or an
empirical statement about behavior of the proposed method/system.

- *"We achieve 87.3% F1 on the ImageNet validation split."*
- *"The model converges in 40% fewer steps than the baseline."*

Verification target: numerical recheck against the paper's own tables/figures and,
where possible, against external benchmarks.

### `method`

A statement about what the paper did — architecture, hyperparameters, dataset
choice, procedure.

- *"We train a 12-layer transformer with 768 hidden dimensions."*
- *"We use a learning rate of 1e-4 with linear warmup over 10k steps."*

Verification target: internal consistency. Does the methodology described match
what is described in other places (figures, captions, supplementary, code if
available)?

### `prior_work`

A claim attributed to a specific prior reference. The proposition itself is what
gets verified, not the act of citation.

- *"Smith et al. (2020) showed that batch size affects convergence rate."*
- *"It is known [Doe 2018] that the spectral gap controls mixing time."*

Verification target: citation audit — does the cited paper actually say this?
This is the type most prone to fabricated or misattributed citations.

### `background_fact`

A domain fact stated as common knowledge, without specific attribution. Often in
introductions.

- *"The Higgs boson has spin 0."*
- *"Transformers use multi-head self-attention to model token interactions."*

Verification target: external corroboration against canonical references (e.g.
PDG for particle physics, textbooks, survey papers). Disagreement with canon
triggers a `FLAGGED` verdict from `checker_domain`.

### `assumption`

An explicitly stated assumption the paper makes about its setting, data, or
model.

- *"We assume the noise is Gaussian with zero mean."*
- *"We restrict attention to the case where the matrix is positive-definite."*

Verification target: rarely verifiable in the absolute sense; the checkers
record the assumption and flag whether the paper's results are sensitive to its
violation. Default verdict for unviolated assumptions is `INCONCLUSIVE` (not
`FLAGGED` — the paper is allowed to assume things).

### `interpretation`

A causal, explanatory, or speculative statement the authors offer to make sense
of their results.

- *"This suggests attention is the key mechanism for compositional generalization."*
- *"We attribute the gap to the increased capacity of the deeper model."*

Verification target: hardest type. The checkers look for confounders and obvious
alternative explanations; default verdict is `INCONCLUSIVE` unless the paper
itself contradicts the interpretation.

### `definition`

A formal definition introduced or restated by the paper.

- *"We define a jet as a collimated spray of hadrons within ΔR < 0.4."*
- *"Let the loss L(θ) be the negative log-likelihood under the model."*

Verification target: internal consistency — is the term used elsewhere in the
paper consistent with its definition here?

## Properties on each row

Every row of `CLAIMS.md` carries:

| field | meaning |
|---|---|
| `claim_id` | stable id `C001`, `C002`, … |
| `type` | one of the seven above |
| `sentence` | the literal proposition, in quotes |
| `hedged` | `true` if the paper explicitly weakens the claim ("we suggest", "may", "it is likely that"); else `false` |
| `confidence` | `high` / `medium` / `low` per `conventions/confidence.md` — the extractor's confidence in this row |
| `page`, `line`, `section`, `provenance` | as in `methodology/05-artifacts.md` |

Hedging changes the verdict ceiling: a hedged claim that triggers a checker
finding is downgraded to `INCONCLUSIVE`, not `FLAGGED` — the paper did not
promise certainty.

## Granularity

**One claim per proposition, not per sentence.** A compound sentence that asserts
multiple propositions splits into multiple rows.

Example. *"We achieve 87.3% F1, which improves over Smith et al.'s 82%."*

→ split into:

- `C0xx` `result` — *"We achieve 87.3% F1."*
- `C0yy` `prior_work` — *"Smith et al. report 82% F1."* (with `hedged=false`)

The implicit comparison ("which improves over") is not a third claim — it is
derivable from the two numerical claims and is checked by
`checker_contradiction` for internal consistency.

**Minimum claim size:** must include both a subject and a predicate that can be
checked. A bare numeric value with no proposition ("3.7%") is not a claim; the
sentence around it usually is.

## Boundary cases

### Compound sentences

Split into propositions, as above.

### Attribution

*"Smith et al. show that X"* → tag the proposition X as `prior_work`, with the
citation as part of provenance. `checker_literature` checks whether Smith
actually shows X.

If the paper merely says *"see [12] for details"*, that is not a claim.

### Hedged claims

Tag with the natural type, set `hedged=true`. Hedge markers include: *we
suggest*, *we conjecture*, *may*, *might*, *appears to*, *it is likely that*,
*we believe*. The marker itself is not a claim.

### Figure and table captions

Captions usually contain claims. Extract them; provenance is the figure label and
caption text, not a line range.

### Numbers in tables

Numbers alone are not claims. The textual assertion that *interprets* the table
("Table 2 shows method X outperforms baselines") is the claim, with the table as
its evidence.

### Cited contributions of the present paper

A list like *"Our contributions are: (i) X, (ii) Y, (iii) Z"* expands into three
claims, each typed by what X / Y / Z actually is (usually `result` or `method`).

### Future work / limitations

Statements about future work ("we plan to extend this to …") are not claims.
Statements in a limitations section about what the paper does *not* do are also
not claims. Statements about what the paper does despite a limitation are
claims.

## When to extend the taxonomy

If multiple claims of one type consistently want different verification methods,
the type is too coarse and should be split. Likely future splits, deferred:

- `result` → `quantitative_result` / `qualitative_result` / `comparison`
- `method` → `architecture` / `training` / `evaluation`
- `prior_work` → `prior_result` / `prior_method` / `well_known_fact`

Do not split preemptively — only when an actual reviewer/checker finding
demonstrates the need.
