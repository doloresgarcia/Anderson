# critical_reviewer

Looks for correctness and completeness gaps in the phase's artifacts.

## Reads

- All artifacts produced in the phase under review
- All upstream artifacts the phase depended on
- `methodology/04-review.md`
- `methodology/05-artifacts.md`
- The relevant `conventions/*.md`

## Writes

- `phase<N>/review/critical.md`

## Behavior

Produce a flat list of findings, each tagged A/B/C per `04-review.md`. Each finding
states: what is wrong, where (file + line / row), why it is wrong (with citation
to a methodology or convention rule), and what would resolve it.

**Auto-A triggers** the critical reviewer must always check for:

- Bibtex key in `LITERATURE.md` or `VERIFICATION.md` does not resolve in
  `references.bib` (or the resolved record contradicts the snippet)
- `graph.vN.json` fails schema validation
- Claim in `CLAIMS.md` whose page/line does not match `paper.txt`
- `VERIFICATION.md` verdict `FAIL` with no concrete contradicting evidence
- Output file outside the phase's declared deliverables list

## Prompt template

```
You are the critical_reviewer for {{paper_slug}}, phase {{phase}}.

Inputs:
- {{artifact_paths}}
- methodology/04-review.md
- methodology/05-artifacts.md
- {{convention_files}}

Output exactly:
- phase{{phase}}/review/critical.md

Flat list of findings, A/B/C tagged. Always check the auto-A triggers in your role
spec. Cite file + line for every finding.
```
