# Artifact formats

Every phase deliverable has a fixed format so downstream agents can parse it
mechanically.

Files documented as optional intermediates are allowed only when the
orchestrator explicitly declares a large-paper parallelization plan and includes
those paths in a role's output spec. They are not default phase deliverables.
Downstream phases consume the final artifacts in `phase<N>/outputs/`, not shard
or batch part files.

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
When assembled from batch intermediates, final sections are ordered by final
`claim_id`, bank candidates appear before external candidates, local part-file
keys are rewritten to final deduplicated keys, and every `[@key]` reference must
resolve in final `references.bib`.

## `references.bib`

BibTeX file written by `literature_searcher`. It must include every key cited
from `LITERATURE.md`. It may be empty only when `LITERATURE.md` contains no
citation keys.

## Optional Phase 1 intermediates

These files live under `reviews/<slug>/phase1/agents/...`, not under
`phase1/outputs/`. They are merge inputs only.

### `CLAIMS.part.md`

Shard-local claim table written by a `claim_extractor` shard worker:

```
| temp_claim_id | type | sentence | hedged | confidence | page | line | section | provenance |
|---------------|------|----------|--------|------------|------|------|---------|------------|
| T001-001      | …    | "…"      | false  | high       | 3    | 14   | 2.1     | paper.txt:142 |
```

`temp_claim_id` values are temporary and must not use the final `C001` pattern.
They only need to be unique across the declared shard run. The `sentence`,
`type`, `hedged`, `confidence`, page/line/section, and provenance columns follow
the same rules as final `CLAIMS.md`.

### `claim_id_map.md`

Serial claim-merge map written in the claim merge working directory:

```
| temp_claim_id | final_claim_id | prior_claim_id | status | normalized_sentence | provenance | note |
|---------------|----------------|----------------|--------|---------------------|------------|------|
| T001-001      | C001           | C001           | preserved | …                 | paper.txt:142 | … |
| T002-004      | C019           | -              | inserted  | …                 | paper.txt:311 | … |
| -             | -              | C007           | deleted   | …                 | paper.txt:208 | … |
```

`status` is `preserved`, `inserted`, or `deleted`. Changed claims are represented
as deletion of the old exact `(normalized_sentence, provenance)` signature plus
insertion of the new signature. The merge log must summarize insertions and
deletions and state whether downstream Phase 1 artifacts need regeneration.

### `coverage.md`

Literature bank batch coverage manifest:

```
| claim_id | covered | best_relation | best_confidence | candidate_keys | reason |
|----------|---------|---------------|-----------------|----------------|--------|
| C001     | true    | supports      | high            | smith2020      | bank high-confidence support |
| C002     | false   | related       | low             | lee2018        | no support/contradiction at medium+ |
```

Every assigned claim appears exactly once. `covered` is `true` only when the
bank found at least one `supports` or `contradicts` candidate with `high` or
`medium` confidence. `candidate_keys` are local to that batch part and must
resolve in the sibling `references.part.bib` when present.

### `uncovered.md`

Barrier manifest produced only after all declared bank batches complete:

```
| claim_id | reason | bank_batches | notes |
|----------|--------|--------------|-------|
| C002     | no medium+ support/contradiction from bank | 001,002 | external search allowed |
```

External literature batches may search only claim IDs listed here. A claim not
listed in `uncovered.md` is treated as bank-covered for the batched run.

### `LITERATURE.part.md`

Batch-local literature candidates. The structure matches final `LITERATURE.md`
but covers only the batch's assigned claims:

```
## C001
- [@smith2020] — supports — confidence high — bank — "snippet from paper text"
```

Keys are local to the part file and must resolve in the sibling
`references.part.bib`. Bank batch parts use source `bank`; external batch parts
use source `external`. The serial literature merge rewrites local keys to final
deduplicated keys before writing `LITERATURE.md`.

### `references.part.bib`

Batch-local BibTeX file. It must include every key cited by the sibling
`LITERATURE.part.md` and no fabricated records. Keys may conflict across
batches; the serial literature merge deduplicates records by DOI, then arXiv id,
then normalized title, resolves key conflicts deterministically, and writes the
final `references.bib`.

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

## `STATS.md`

Deterministic stats written by `src/claim_stats.py`: trust score block, claim
counts, aggregate verdict counts, category breakdowns, inconclusive reasons, and
per-group rows derived from `CLAIMS.md` and `VERIFICATION.md`.

## Highlighted paper

Highlighted output depends on input mode. PDF input produces
`paper.highlighted.pdf`. Text input produces `paper.highlighted.html` and, when
PyMuPDF is available, a synthesized `paper.highlighted.pdf`. Highlight color
encodes the error category for `FLAGGED` claims and yellow for
`INCONCLUSIVE` claims:

- blue (`#4285F4`) — `unreferenced` (needs a citation)
- amber (`#FFBF00`) — `ambiguous` (unclear or underspecified)
- orange (`#FF6D00`) — `internal_contradiction` (self-contradictory)
- red (`#D32F2F`) — `literature_collision` (conflicts with published work)
- purple (`#7B1FA2`) — `domain_violation` (conflicts with established knowledge)
- yellow (`#F1C40F`) — `INCONCLUSIVE` (checked but not resolved)
- (no highlight) — all CLEAR or not checked

When a sentence triggers multiple categories, the highlight uses the most
severe category's color. Severity order (highest first): `domain_violation`,
`literature_collision`, `internal_contradiction`, `ambiguous`, `unreferenced`.

Each `FLAGGED` span carries a tooltip / margin note listing **all** triggered
categories and linking back to each `VERIFICATION.md` section. Each
`INCONCLUSIVE` span links back to the unresolved checker reason.
