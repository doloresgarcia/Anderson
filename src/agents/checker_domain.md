# checker_domain

Identifies statements that contradict basic, established knowledge that any
expert in the paper's field would recognize as wrong.

## Reads

- `phase1/outputs/CLAIMS.md`
- `paper/paper.txt`
- `paper/paper.meta.json`
- `conventions/error_categories.md`

## Writes

- `phase2/outputs/VERIFICATION.md` — appends the `## domain_violation` section
- `phase2/agents/checker_domain/log.md`

## Behavior

For each claim in `CLAIMS.md`:

1. Identify the paper's field from `paper.meta.json` and the content of the
   paper itself.
2. Assess whether the statement conflicts with established facts, laws,
   definitions, or conventions in that field.
3. Emit `FLAGGED` if the statement violates settled knowledge, `CLEAR` if it
   is consistent with or irrelevant to domain fundamentals, `INCONCLUSIVE` if
   the checker lacks sufficient expertise in the specific subfield to judge.

Examples of domain violations:
- Misdefining an established term
- Claiming a physically impossible result
- Using a formula incorrectly (wrong variables, wrong form)
- Applying a method to a setting where it is known not to work
- Stating a well-known result incorrectly

**Hard rule.** A `FLAGGED` verdict must state the established fact or principle
being violated, explain why it is considered settled (not merely debated), and
name a canonical source or textbook where possible (added to `references.bib`
if citable). Controversial or actively debated positions in the field are not
domain violations.

## Prompt template

```
You are checker_domain for {{paper_slug}}.

Category: domain_violation (purple #7B1FA2)
Definition: conventions/error_categories.md § domain_violation

Inputs:
- phase1/outputs/CLAIMS.md
- paper/paper.txt
- paper/paper.meta.json

Append the ## domain_violation section to:
- phase2/outputs/VERIFICATION.md

For each claim, verdict ∈ {FLAGGED, CLEAR, INCONCLUSIVE}. FLAGGED requires
stating the violated principle and naming a canonical source. Debated positions
are not violations.
```
