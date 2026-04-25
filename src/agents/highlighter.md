# highlighter

Produces the paper-with-highlights deliverable.

## Reads

- `paper/paper.pdf`
- `paper/paper.txt`
- `phase2/outputs/VERIFICATION.md`
- `phase2/outputs/graph.v2.json`
- `conventions/graph_schema.md` (canonical color palette)

## Writes

- `phase3/outputs/paper.highlighted.pdf`
- `phase3/outputs/paper.highlighted.html`

## Behavior

For each claim with verdict `FAIL` or `INCONCLUSIVE`:

1. Locate the originating sentence in `paper.pdf` using the page/line provenance
   from `CLAIMS.md` (carried into the graph).
2. Add a highlight using the canonical palette in `conventions/graph_schema.md`:
   red `#E74C3C` for FAIL, yellow `#F1C40F` for INCONCLUSIVE.
3. Attach a margin note (PDF) / tooltip (HTML) containing the verification verdict
   and a link to the corresponding `VERIFICATION.md` anchor.

Sentences that PASS or were not checked are not highlighted. (Green and gray in
the graph translate to "no highlight" in the PDF — positive marking would be
visual noise.) The highlighter does not invent annotations — every highlight
maps to a verdict in `VERIFICATION.md`.

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
