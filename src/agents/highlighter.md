# highlighter

Produces the paper-with-highlights deliverable.

## Reads

- `paper/paper.pdf` (if present)
- `paper/paper.txt`
- `phase1/outputs/CLAIMS.md`
- `phase2/outputs/VERIFICATION.md`
- `phase2/outputs/graph.v2.json`
- `conventions/graph_schema.md` (canonical color palette)

## Writes

One of these, depending on input:

- `phase3/outputs/paper.highlighted.pdf` — if `paper/paper.pdf` exists
- `phase3/outputs/paper.highlighted.html` — if only `paper/paper.txt` exists

Plus:

- `phase3/agents/highlighter/log.md`

## Behavior

Dispatch on input. Invoke the bundled utility — **do not** hand-edit the PDF
or hand-write the HTML.

If `paper/paper.pdf` exists:

```bash
python3 ../../src/highlight_paper.py .
```

If only `paper/paper.txt` exists (the paper was provided as plain text):

```bash
python3 ../../src/highlight_text.py .
```

Both scripts apply the canonical palette from `conventions/graph_schema.md`
(red `#E74C3C` for FAIL, yellow `#F1C40F` for INCONCLUSIVE) and produce
per-highlight annotations referencing the `claim_id` and verdict so the
reader can cross-reference `VERIFICATION.md`.

Sentences that PASS or were not checked are not highlighted. (Green and gray in
the graph translate to "no highlight" in the marked-up paper — positive
marking would be visual noise.)

If a script cannot match a sentence to a location in the paper (text-extraction
edge cases, hyphenation, soft line breaks for the PDF; verbatim mismatch for
the text version), it skips that claim and reports the unmatched ids in its
output. Such skips appear in the highlighter's `log.md` and trigger a
Category B finding for the reviewer to resolve — usually by the extractor
producing a tighter `sentence` quote.

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

Red = FAIL, yellow = INCONCLUSIVE. Every highlight must trace to a verdict.
```
