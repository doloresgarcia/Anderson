# Artifact formats

Every phase deliverable has a fixed format so downstream agents can parse it
mechanically.

## `claims.jsonl`

The canonical claim list. One JSON record per line, produced by
`src/extract_claims.py` directly from `paper.tex` and (optionally) refined in
place by `claim_reviewer`. Full schema: `src/claims_schema.md`.

Top-level fields per record: `id`, `type` (`prose` | `equation` | `caption` |
`table_cell`), `text`, `section_path`, `line`, plus type-specific fields
(`cite_keys`, `is_first_person`, `is_numeric`, `is_footnote`,
`is_definition`, `epistemic` for `prose`; `env` for `equation`/`caption`;
`value`, `error`, `best` for `table_cell`).

This is the artifact downstream agents (`literature_searcher`,
`graph_builder`, `strategist`, checkers) read. There is no separate markdown
table form in the contract — agents that want one can derive it on demand.
Specifically:

- `literature_searcher` filters/iterates `claims.jsonl` via `jq`.
- `graph_builder` reads `claims.jsonl` and emits node IDs that match the
  `id` field.
- `strategist` reads `claims.jsonl` and the literature artifact; emits
  `STRATEGY.md` with rows keyed by the same `id` values.

`CLAIM_REVIEW.md` (also in `phase1/outputs/`) is `claim_reviewer`'s
human-readable audit log of edits and flags — not consumed by downstream
agents, useful for human review.

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
| claim_id | importance | checkability | categories | rationale |
|----------|------------|--------------|------------|-----------|
| C001     | high       | high         | unreferenced, literature_collision | … |
```

`categories` lists the error categories from `conventions/error_categories.md`
most relevant to the claim. All five checkers still run against all claims;
the categories column guides prioritization.

## `VERIFICATION.md`

Organized by error category, one top-level section per checker. Within each
section, one subsection per claim that the checker examined:

```
## unreferenced

### C003 — FLAGGED — confidence: high
- evidence: paper.txt:42-44
- reasoning: Claims X without citing any source.

### C007 — CLEAR — confidence: high

## ambiguous

### C001 — FLAGGED — confidence: medium
- evidence: paper.txt:14-15
- interpretations:
  1. "significant" means statistically significant (p < 0.05)
  2. "significant" means practically meaningful (large effect size)
- reasoning: The distinction matters because …

## internal_contradiction

### C004 — FLAGGED — confidence: high
- evidence:
  - paper.txt:30 — "We use 10,000 training samples"
  - paper.txt:89 — "Our training set contains 8,500 examples"
- reasoning: Irreconcilable counts.

## literature_collision

### C002 — FLAGGED — confidence: medium
- evidence:
  - paper.txt:22
  - [@smith2020] §3.2 — "snippet"
- reasoning: …

## domain_violation

### C009 — FLAGGED — confidence: high
- evidence: paper.txt:105
- violated_principle: …
- canonical_source: …
- reasoning: …
```

`VERDICT` is one of `FLAGGED`, `CLEAR`, `INCONCLUSIVE`. `FLAGGED` requires
evidence meeting the standard in `conventions/error_categories.md` for that
category. `INCONCLUSIVE` requires a stated reason. `confidence` values come
from `conventions/confidence.md`.

## `REPORT.md`

Human-facing summary, sectioned: Overview, Method, What we checked, What failed
(claim-by-claim), Limitations.

## Highlighted paper

`paper.highlighted.pdf` and `paper.highlighted.html`. Highlight color encodes
the error category (per `conventions/error_categories.md`):

- blue (`#4285F4`) — `unreferenced` (needs a citation)
- amber (`#FFBF00`) — `ambiguous` (unclear or underspecified)
- orange (`#FF6D00`) — `internal_contradiction` (self-contradictory)
- red (`#D32F2F`) — `literature_collision` (conflicts with published work)
- purple (`#7B1FA2`) — `domain_violation` (conflicts with established knowledge)
- (no highlight) — all CLEAR or not checked

When a sentence triggers multiple categories, the highlight uses the most
severe category's color. Severity order (highest first): `domain_violation`,
`literature_collision`, `internal_contradiction`, `ambiguous`, `unreferenced`.

Each highlighted span carries a tooltip / margin note listing **all** triggered
categories and linking back to each `VERIFICATION.md` section.
