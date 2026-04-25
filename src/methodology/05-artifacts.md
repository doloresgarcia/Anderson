# Artifact formats

Every phase deliverable has a fixed format so downstream agents can parse it
mechanically.

## `CLAIMS.md`

Markdown table, one row per claim:

```
| claim_id | type | sentence | hedged | confidence | page | line | section | provenance |
|----------|------|----------|--------|------------|------|------|---------|------------|
| C001     | …    | "…"      | false  | high       | 3    | 14   | 2.1     | paper.txt:142 |
```

`type` values and the `hedged` flag definition come from
`conventions/claim_taxonomy.md`. `confidence` values come from
`conventions/confidence.md`.

## `LITERATURE.md`

Per claim, a sub-section listing candidate references. Bank matches appear
before external matches.

```
## C001
- [@smith2020] — supports — confidence high — bank — "snippet from paper text"
- [@jones2019] — contradicts — confidence medium — external — "snippet"
```

The fourth field is the **source**: `bank` (found in the local literature bank)
or `external` (retrieved via internet search). `confidence` values come from
`conventions/confidence.md`.

Bibtex keys must resolve in `references.bib` (also written by
`literature_searcher`). Unresolvable keys are Category A at review.

## `graph.vN.json`

JSON conforming to `conventions/graph_schema.md`. Minimum top-level shape (the
schema file refines this):

```json
{
  "paper": { "id": "…", "title": "…" },
  "nodes": [ { "id": "C001", "kind": "claim", "…": "…" } ],
  "edges": [ { "source": "C001", "target": "C002", "kind": "depends_on" } ]
}
```

Each version is committed; do not overwrite older versions. `graph.v1.json` is
phase-1 output, `graph.v2.json` is phase-2 output, `graph.final.json` is phase-3
output.

## `STRATEGY.md`

```
| claim_id | importance | checkability | method | rationale |
|----------|------------|--------------|--------|-----------|
| C001     | high       | high         | …      | …         |
```

`method` values come from `conventions/verification.md`.

## `VERIFICATION.md`

Per checked claim:

```
## C001 — VERDICT: FAIL — confidence: medium
- method: …
- evidence:
  - paper.txt:142
  - [@smith2020] §3.2
- reasoning: …
```

`VERDICT` is one of `PASS`, `FAIL`, `INCONCLUSIVE`. `INCONCLUSIVE` requires a stated
reason (e.g., paywalled reference, ambiguous wording). `confidence` values come
from `conventions/confidence.md` and are orthogonal to the verdict — a
`PASS` with `low` confidence is meaningful and different from `INCONCLUSIVE`.

## `STATS.md`

Mechanical claim statistics — type counts, extraction confidence, hedging,
verdict breakdown, type×verdict matrix, coverage, methods used, INCONCLUSIVE
reasons, per-group rows. Produced by `src/claim_stats.py`. No LLM in the
loop; numbers are guaranteed to match `CLAIMS.md` and `VERIFICATION.md`.

## `REPORT.md`

Human-facing summary, sectioned: Overview, Method, Statistics, What we
checked, What failed (claim-by-claim), Limitations. The Statistics section
embeds the relevant tables from `STATS.md` verbatim — prose must agree with
those numbers.

## Highlighted paper

`paper.highlighted.pdf` always. `paper.highlighted.html` additionally if the
input was plain text.

Highlight color encodes verdict, using the canonical palette in
`conventions/graph_schema.md`:

- red `#E74C3C` — FAIL
- yellow `#F1C40F` — INCONCLUSIVE
- (no highlight) — PASS or not checked (green and gray in the graph)

Produced by `src/highlight_paper.py` for PDF input (character-level) or
`src/highlight_text.py` for text input (line-level in a synthesized PDF, plus
character-level in a companion HTML).

Each highlighted span carries a tooltip / margin note linking back to the
`VERIFICATION.md` entry.
