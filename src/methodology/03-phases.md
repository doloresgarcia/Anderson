# Phases

Three phases. Each phase ends with a commit; phase 2 has a review-arbiter gate; phase
3 has a human gate before final delivery.

## Phase 1 — Ingest & Map

**Goal.** Read the paper, list its claims, scan the literature for relevant prior
work, and emit a first-pass claim graph.

**Subagents dispatched.**

- `claim_extractor` — reads `paper.txt`, emits `CLAIMS.md` (one row per claim with
  sentence-level provenance) using the taxonomy from
  `conventions/claim_taxonomy.md`.
- `literature_searcher` — for each claim, first crosschecks against the local
  literature bank (if provided), then falls back to external search for
  uncovered claims (biased toward published, peer-reviewed papers over
  preprints); emits `LITERATURE.md` (claim → candidate references with
  confidence, source, and snippet).
- `graph_builder` — consumes `CLAIMS.md` and `LITERATURE.md`, produces
  `graph.v1.json` per `conventions/graph_schema.md`.

**Deliverables (in `reviews/<slug>/phase1/outputs/`).**

- `CLAIMS.md`
- `LITERATURE.md`
- `graph.v1.json`
- `FINDINGS.md` — short prose summary: how many claims, distribution by type, gaps
  identified at this stage.

**Review.** Single-bot review (correctness/completeness of claim extraction and graph
well-formedness). Arbiter PASS required to advance.

## Phase 2 — Strategy & Check

**Goal.** Decide which claims are worth checking, run five specialized checker
agents against the claims, and update the graph with their findings.

**Subagents dispatched.**

- `strategist` — reads `graph.v1.json` and `FINDINGS.md`; emits `STRATEGY.md`
  ranking claims by importance and listing the most relevant error categories
  per claim (per `conventions/error_categories.md`).
- Five **checker agents** — run in parallel, each checking all claims for one
  error category (per `conventions/error_categories.md`):
  - `checker_unreferenced` — missing citations
  - `checker_ambiguous` — unclear or underspecified statements
  - `checker_contradiction` — internal contradictions
  - `checker_literature` — conflicts with published literature
  - `checker_domain` — violations of established domain knowledge
  Each checker appends its section to `VERIFICATION.md` with verdicts
  `FLAGGED` / `CLEAR` / `INCONCLUSIVE`.
- `graph_builder` — re-runs to merge checker findings onto the graph, emitting
  `graph.v2.json`.

**Deliverables (in `reviews/<slug>/phase2/outputs/`).**

- `STRATEGY.md`
- `VERIFICATION.md`
- `graph.v2.json`

**Review.** 3-bot review (a critical reviewer, a constructive reviewer, and an
arbiter). Findings classified A/B/C per `04-review.md`.

## Phase 3 — Report

**Goal.** Produce the final, human-facing artifacts.

**Subagents dispatched.**

- `highlighter` — reads `graph.v2.json` and `VERIFICATION.md`; produces
  `paper.highlighted.pdf` and `paper.highlighted.html` with flagged sentences
  color-coded by error category per `conventions/error_categories.md`.
- `graph_builder` — final pass; emits `graph.final.json` plus `graph.final.svg` for
  human reading.
- `report_writer` (specialization of `executor`) — writes `REPORT.md` summarizing
  what was checked, what failed, and why.

**Deliverables (in `reviews/<slug>/phase3/outputs/`).**

- `graph.final.json`
- `graph.final.svg`
- `paper.highlighted.pdf`
- `paper.highlighted.html`
- `REPORT.md`

**Gate.** Human review of the highlighted PDF. Possible responses: APPROVE,
ITERATE (fix in phase 3 scope), REGRESS(N) (re-open phase N).
