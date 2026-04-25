# highlighter

Produces the paper-with-highlights deliverable using the five-category color
scheme from `conventions/error_categories.md`.

## Reads

- `paper/paper.pdf`
- `paper/paper.txt`
- `phase1/outputs/CLAIMS.md`
- `phase2/outputs/VERIFICATION.md`
- `phase2/outputs/graph.v2.json`
- `conventions/error_categories.md`

## Writes

- `phase3/outputs/paper.highlighted.pdf`
- `phase3/outputs/paper.highlighted.html`

## Behavior

For each claim with at least one `FLAGGED` verdict in `VERIFICATION.md`:

1. Locate the originating sentence in `paper.pdf` using the page/line provenance
   from `CLAIMS.md` (carried into the graph).
2. Determine which error categories flagged this claim.
3. Apply the highlight color per `conventions/error_categories.md`:
   - blue (`#4285F4`) — `unreferenced`
   - amber (`#FFBF00`) — `ambiguous`
   - orange (`#FF6D00`) — `internal_contradiction`
   - red (`#D32F2F`) — `literature_collision`
   - purple (`#7B1FA2`) — `domain_violation`
4. If a sentence triggers multiple categories, use the color of the most severe
   category (severity order: `domain_violation` > `literature_collision` >
   `internal_contradiction` > `ambiguous` > `unreferenced`).
5. Attach a margin note (PDF) / tooltip (HTML) listing **all** triggered
   categories, their verdicts, and a link to each `VERIFICATION.md` section.

For `internal_contradiction`, both contradicting passages are highlighted.

Sentences where all checkers report `CLEAR` or that were not checked receive
no highlight. The highlighter does not invent annotations — every highlight
maps to a `FLAGGED` verdict in `VERIFICATION.md`.

## Prompt template

```
You are the highlighter for {{paper_slug}}.

Inputs:
- paper/paper.pdf
- paper/paper.txt
- phase1/outputs/CLAIMS.md
- phase2/outputs/VERIFICATION.md
- phase2/outputs/graph.v2.json
- conventions/error_categories.md

Output exactly:
- phase3/outputs/paper.highlighted.pdf
- phase3/outputs/paper.highlighted.html

Color scheme from conventions/error_categories.md:
  blue = unreferenced, amber = ambiguous, orange = internal_contradiction,
  red = literature_collision, purple = domain_violation.
Multi-category: use most severe color; list all categories in tooltip.
Every highlight must trace to a FLAGGED verdict.
```
