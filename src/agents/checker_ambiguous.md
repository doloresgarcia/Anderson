# checker_ambiguous

Identifies statements whose meaning is unclear, underspecified, or open to
multiple reasonable interpretations in a way that affects the paper's claims.

## Reads

- `phase1/outputs/CLAIMS.md`
- `paper/paper.txt`
- `conventions/error_categories.md`

## Writes

- `phase2/outputs/VERIFICATION.md` — appends the `## ambiguous` section
- `phase2/agents/checker_ambiguous/log.md`

## Behavior

For each claim in `CLAIMS.md`:

1. Read the statement in context (surrounding paragraph in `paper.txt`).
2. Determine whether the statement has a single clear meaning or admits
   multiple plausible readings that would change the paper's conclusions.
3. Emit a verdict: `FLAGGED` if genuinely ambiguous in a way that matters,
   `CLEAR` if the meaning is unambiguous (even if inelegant), `INCONCLUSIVE`
   if the checker lacks sufficient domain context to judge.

Patterns that commonly trigger this checker:
- Vague quantifiers without metrics ("significant improvement", "large dataset")
- Undefined terms used as if established
- Pronouns or references with unclear antecedents
- Conditionals with unspecified scope
- Methodology descriptions too vague to reproduce

**Hard rule.** A `FLAGGED` verdict must present at least two distinct, plausible
interpretations of the sentence and explain why the ambiguity matters for the
paper's claims. Stylistic preferences are not errors.

## Prompt template

```
You are checker_ambiguous for {{paper_slug}}.

Category: ambiguous (amber #FFBF00)
Definition: conventions/error_categories.md § ambiguous

Inputs:
- phase1/outputs/CLAIMS.md
- paper/paper.txt

Append the ## ambiguous section to:
- phase2/outputs/VERIFICATION.md

For each claim, verdict ∈ {FLAGGED, CLEAR, INCONCLUSIVE}. FLAGGED requires
two distinct interpretations and an explanation of why it matters.
```
