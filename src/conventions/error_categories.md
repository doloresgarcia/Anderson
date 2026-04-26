# Error categories

Five mutually exclusive categories of error that the checker agents detect.
Each category has a dedicated checker agent, a dedicated color in the
highlighted output, and specific evidence standards.

## The five categories

### `unreferenced`

A statement that makes a factual claim requiring a citation but provides none.
This includes empirical results attributed to prior work, quantitative
thresholds, and non-obvious factual assertions.

- **Checker agent:** `checker_unreferenced`
- **Highlight color:** blue (`#4285F4`)
- **What triggers a flag:** The statement asserts a fact, result, or finding
  that is not common knowledge in the field and is not supported by a citation
  in the paper. Statements of the paper's own novel contributions (clearly
  presented as such) are exempt.
- **Evidence standard for FLAGGED:** The checker must explain what kind of
  source the statement requires and confirm that no citation is present in the
  surrounding context.
- **Not this category:** If the statement *has* a citation but the citation is
  wrong or misleading, that belongs in `literature_collision`.

### `ambiguous`

A statement whose meaning is unclear, underspecified, or open to multiple
reasonable interpretations in a way that affects the paper's claims.

- **Checker agent:** `checker_ambiguous`
- **Highlight color:** amber (`#FFBF00`)
- **What triggers a flag:** Vague quantifiers ("significant improvement")
  without a metric, undefined terms used as if established, pronouns or
  references with unclear antecedents, conditionals with unspecified scope,
  or methodology descriptions too vague to reproduce.
- **Evidence standard for FLAGGED:** The checker must state at least two
  distinct, plausible interpretations of the sentence and explain why the
  ambiguity matters for the paper's claims.
- **Not this category:** Stylistic issues or unusual phrasing that has only one
  reasonable reading. Minor grammar issues are not errors.

### `internal_contradiction`

Two or more statements within the paper that cannot both be true.

- **Checker agent:** `checker_contradiction`
- **Highlight color:** orange (`#FF6D00`)
- **What triggers a flag:** A direct logical inconsistency between statements
  in the paper (e.g., conflicting numbers, a method section that contradicts
  the evaluation, an abstract claim not supported by the results section).
- **Evidence standard for FLAGGED:** The checker must quote both contradicting
  passages with their provenance (`paper.txt:line`) and explain why they are
  incompatible. Both passages are highlighted.
- **Not this category:** A statement that is merely surprising or unusual given
  other statements is not a contradiction. The conflict must be logical, not
  just unexpected.

### `literature_collision`

A statement in the paper that conflicts with a claim in the literature (either
in the literature bank or from external search).

- **Checker agent:** `checker_literature`
- **Highlight color:** red (`#D32F2F`)
- **What triggers a flag:** A statement in the paper directly contradicts a
  finding, result, or established conclusion from a published source in
  `LITERATURE.md` or `references.bib`.
- **Evidence standard for FLAGGED:** The checker must cite both the paper
  statement (`paper.txt:line`) and the contradicting source (`[@key] §section`
  with a ≤30-word snippet). The external source must be a real, resolvable
  record.
- **Not this category:** If the paper explicitly acknowledges the disagreement
  and provides a reasoned argument for why its results differ, that is not a
  collision — it is a known divergence. The checker should note it as CLEAR
  with a comment.

### `domain_violation`

A statement that contradicts basic, established knowledge that any expert in
the paper's field would recognize as wrong.

- **Checker agent:** `checker_domain`
- **Highlight color:** purple (`#7B1FA2`)
- **What triggers a flag:** The statement conflicts with a well-established
  fact, law, definition, or convention in the field (e.g., misdefining an
  established term, claiming an impossible physical result, using a formula
  incorrectly, applying a method to a setting where it is known not to work).
- **Evidence standard for FLAGGED:** The checker must state the established
  fact or principle being violated, explain why it is established (naming a
  canonical source or textbook where possible), and show how the paper's
  statement conflicts with it. If a canonical reference is citable, name it in
  the checker output's `canonical_source:` field; bibliography updates are
  handled by the orchestrator or a fixer because checker agents do not own
  `references.bib`.
- **Not this category:** Controversial or actively debated positions in the
  field are not domain violations. The violated knowledge must be settled and
  uncontroversial among practitioners.

## Color scheme summary

| Category                | Color   | Hex       | Meaning |
|-------------------------|---------|-----------|---------|
| `unreferenced`          | blue    | `#4285F4` | Needs a citation |
| `ambiguous`             | amber   | `#FFBF00` | Unclear or underspecified |
| `internal_contradiction`| orange  | `#FF6D00` | Self-contradictory |
| `literature_collision`  | red     | `#D32F2F` | Conflicts with published work |
| `domain_violation`      | purple  | `#7B1FA2` | Conflicts with established knowledge |

Sentences that pass all checkers or were not checked receive no highlight.
Sentences with an aggregate `INCONCLUSIVE` verdict and no `FLAGGED` category
use the yellow inconclusive highlight defined in `graph_schema.md`.

When a single sentence triggers multiple categories, apply the color of the
**most severe** category. Severity order (highest first):

1. `domain_violation`
2. `literature_collision`
3. `internal_contradiction`
4. `ambiguous`
5. `unreferenced`

The margin note / tooltip must list all triggered categories, not just the
displayed color.

## Verdicts per checker

Each checker emits one of three verdicts per claim it examines:

- **FLAGGED** — the error was detected; evidence is required.
- **CLEAR** — the checker examined the claim and found no error of this type.
- **INCONCLUSIVE** — the checker could not determine; a stated reason is
  mandatory (e.g., paywalled reference, insufficient domain context).

## Relationship to the old verification model

These five checkers replace the generic `verifier` agent. The old three-verdict
system (`PASS` / `FAIL` / `INCONCLUSIVE`) maps to the new model as follows:

- Old `FAIL` → one or more checkers report `FLAGGED`
- Old `PASS` → all checkers report `CLEAR`
- Old `INCONCLUSIVE` → at least one checker reports `INCONCLUSIVE` and none
  report `FLAGGED`
