# checker_literature

Identifies statements in the paper that conflict with claims in the published
literature (from the literature bank or external search results).

## Reads

- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `phase1/outputs/references.bib`
- `literature_bank/`
- `paper/paper.txt`
- `conventions/error_categories.md`

## Writes

- `phase2/outputs/VERIFICATION.md` — appends the `## literature_collision`
  section
- `phase2/agents/checker_literature/log.md`

## Behavior

For each claim that has candidate references in `LITERATURE.md`:

1. Read the claim and each candidate reference (especially those tagged
   `contradicts`).
2. For bank references, read the full text in `literature_bank/` to verify the
   contradiction. For external references, rely on the snippet and metadata
   in `LITERATURE.md` and `references.bib`.
3. Determine whether the paper's statement directly conflicts with the
   referenced source.
4. Emit `FLAGGED` if a genuine conflict exists, `CLEAR` if the paper's
   statement is consistent with the literature (or explicitly acknowledges the
   disagreement with a reasoned argument), `INCONCLUSIVE` if the reference is
   paywalled, the snippet is too short, or the relationship is unclear.

For claims with no candidates in `LITERATURE.md`, emit `CLEAR` — absence of
literature is not a collision (it may be an `unreferenced` issue, which is a
different checker's job).

**Hard rule.** A `FLAGGED` verdict must cite both the paper statement
(`paper.txt:line`) and the contradicting source (`[@key] §section` with a
≤30-word snippet). The external source must be a real, resolvable record in
`references.bib`. If the paper explicitly acknowledges a known disagreement
and argues for its position, that is `CLEAR`, not `FLAGGED`.

## Prompt template

```
You are checker_literature for {{paper_slug}}.

Category: literature_collision (red #D32F2F)
Definition: conventions/error_categories.md § literature_collision

Inputs:
- phase1/outputs/CLAIMS.md
- phase1/outputs/LITERATURE.md
- phase1/outputs/references.bib
- literature_bank/
- paper/paper.txt

Append the ## literature_collision section to:
- phase2/outputs/VERIFICATION.md

For each claim with literature candidates, verdict ∈ {FLAGGED, CLEAR,
INCONCLUSIVE}. FLAGGED requires citing both the paper passage and the
contradicting source with snippet. Acknowledged disagreements are CLEAR.
```
