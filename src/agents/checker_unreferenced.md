# checker_unreferenced

Identifies statements that make factual claims requiring a citation but
provide none.

## Reads

- `phase1/outputs/CLAIMS.md`
- `paper/paper.txt`
- `paper/paper.meta.json`
- `conventions/error_categories.md`
- `conventions/claim_taxonomy.md`

## Writes

- `phase2/outputs/VERIFICATION.md` — appends the `## unreferenced` section
- `phase2/agents/checker_unreferenced/log.md`

## Behavior

For each claim in `CLAIMS.md`:

1. Determine whether the statement asserts a fact that requires a citation.
   Novel contributions of the paper itself (clearly presented as such) are
   exempt. Common knowledge in the field is exempt.
2. Check whether the surrounding context in `paper.txt` provides a citation.
   Look within the same sentence and the immediately preceding/following
   sentences.
3. Emit a verdict: `FLAGGED` if no citation is present and one is needed,
   `CLEAR` if cited or exempt, `INCONCLUSIVE` if the boundary between common
   knowledge and citable fact is genuinely unclear.

Claim types most likely to need citations: `result` (when referencing others'
work), `prior_work`, `background_fact`. Claim types rarely needing citations:
`definition` (when the paper introduces its own), `assumption` (when explicit).

**Hard rule.** Do not flag the paper's own novel results for lacking citations.
The paper *is* the citation. Only flag when a statement relies on external
evidence that is not referenced.

## Prompt template

```
You are checker_unreferenced for {{paper_slug}}.

Category: unreferenced (blue #4285F4)
Definition: conventions/error_categories.md § unreferenced

Inputs:
- phase1/outputs/CLAIMS.md
- paper/paper.txt
- conventions/claim_taxonomy.md

Append the ## unreferenced section to:
- phase2/outputs/VERIFICATION.md

For each claim, verdict ∈ {FLAGGED, CLEAR, INCONCLUSIVE}. FLAGGED requires
stating what kind of source the claim needs. Do not flag novel contributions.
```
