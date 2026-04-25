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
- `phase3/agents/highlighter/log.md`

## Behavior

Invoke the bundled utility script — do **not** attempt to add highlights by
hand-editing the PDF:

```bash
python3 ../../src/highlight_paper.py .
```

The script reads `paper/paper.pdf`, `phase1/outputs/CLAIMS.md`, and
`phase2/outputs/VERIFICATION.md`, and writes
`phase3/outputs/paper.highlighted.pdf`. It applies the canonical palette
from `conventions/graph_schema.md` (red `#E74C3C` for FAIL, yellow `#F1C40F`
for INCONCLUSIVE) and attaches a margin annotation per highlight that names
the `claim_id` and verdict, so the reader can cross-reference
`VERIFICATION.md`.

Sentences that PASS or were not checked are not highlighted. (Green and gray in
the graph translate to "no highlight" in the PDF — positive marking would be
visual noise.)

If the script cannot match a sentence to a PDF location (text-extraction
edge cases, hyphenation, soft line breaks), it skips that claim and reports
the count in its output. Such skips appear in the highlighter's `log.md`
and trigger a Category B finding for the reviewer to resolve — usually by
the extractor producing a tighter `sentence` quote.

For an HTML companion view, run the script's `--html` companion (deferred —
not yet implemented; for v1 the highlighted output is PDF-only).

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
