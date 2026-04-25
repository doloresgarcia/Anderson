# Artifact formats

Every phase deliverable has a fixed format so downstream agents can parse it
mechanically.

## `CLAIMS.md`

Markdown table, one row per claim:

```
| claim_id | type | sentence | page | line | section | provenance |
|----------|------|----------|------|------|---------|------------|
| C001     | …    | "…"      | 3    | 14   | 2.1     | paper.txt:142 |
```

`type` values come from `conventions/claim_taxonomy.md`.

## `LITERATURE.md`

Per claim, a sub-section listing candidate references:

```
## C001
- [@smith2020] — supports — relevance 0.82 — "snippet from abstract"
- [@jones2019] — contradicts — relevance 0.71 — "snippet"
```

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
## C001 — VERDICT: FAIL
- method: …
- evidence:
  - paper.txt:142
  - [@smith2020] §3.2
- reasoning: …
```

`VERDICT` is one of `PASS`, `FAIL`, `INCONCLUSIVE`. `INCONCLUSIVE` requires a stated
reason (e.g., paywalled reference, ambiguous wording).

## `REPORT.md`

Human-facing summary, sectioned: Overview, Method, What we checked, What failed
(claim-by-claim), Limitations.

## Highlighted paper

`paper.highlighted.pdf` and `paper.highlighted.html`. Highlight color encodes
verdict:

- red — FAIL
- yellow — INCONCLUSIVE
- (no highlight) — PASS or not checked

Each highlighted span carries a tooltip / margin note linking back to the
`VERIFICATION.md` entry.
