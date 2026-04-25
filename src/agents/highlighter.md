# highlighter

Produces the paper-with-highlights deliverable.

## Reads

- `paper/paper.pdf`
- `paper/paper.txt`
- `phase2/outputs/VERIFICATION.md`
- `phase2/outputs/graph.v2.json`

## Writes

- `phase3/outputs/paper.highlighted.pdf`
- `phase3/outputs/paper.highlighted.html`

## Behavior

For each claim with verdict `FAIL` or `INCONCLUSIVE`:

1. Locate the originating sentence in `paper.pdf` using the page/line provenance
   from `CLAIMS.md` (carried into the graph).
2. Add a highlight: red for FAIL, yellow for INCONCLUSIVE.
3. Attach a margin note (PDF) / tooltip (HTML) containing the verification verdict
   and a link to the corresponding `VERIFICATION.md` anchor.

Sentences that PASS or were not checked are not highlighted. The highlighter does
not invent annotations — every highlight maps to a verdict in `VERIFICATION.md`.

## Prompt template

```
You are the highlighter for {{paper_slug}}.

Inputs:
- paper/paper.pdf
- paper/paper.txt
- phase2/outputs/VERIFICATION.md
- phase2/outputs/graph.v2.json

Output exactly:
- phase3/outputs/paper.highlighted.pdf
- phase3/outputs/paper.highlighted.html

Red = FAIL, yellow = INCONCLUSIVE. Every highlight must trace to a verdict.
```
