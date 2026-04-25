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
- `literature_searcher` — for each claim, runs targeted searches; emits
  `LITERATURE.md` (claim → candidate references with relevance score and snippet).
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

## Phase 2 — Strategy & Verify

**Goal.** Decide which claims are worth checking, attempt to verify each chosen
claim, and update the graph with verification verdicts.

**Subagents dispatched.**

- `strategist` — reads `graph.v1.json` and `FINDINGS.md`; emits `STRATEGY.md`
  ranking claims by (importance × checkability) and listing the verification method
  per claim (per `conventions/verification.md`).
- `verifier` — for each claim selected by the strategist, runs the prescribed
  verification method and emits one row in `VERIFICATION.md` (PASS / FAIL /
  INCONCLUSIVE with evidence).
- `graph_builder` — re-runs to merge verification verdicts onto the graph, emitting
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

- `highlighter` — reads `graph.v2.json`, `VERIFICATION.md`, and `CLAIMS.md`;
  invokes `src/highlight_paper.py` to produce `paper.highlighted.pdf` with
  FAIL/INCONCLUSIVE sentences visibly marked and margin annotations linking
  back to the verification anchors.
- `graph_builder` — final pass; emits `graph.final.json`,
  `graph.final.html` (interactive Cytoscape.js viz, the primary visual
  deliverable), and `graph.final.svg` (static snapshot for inclusion in PDFs
  and slides).
- `report_writer` (specialization of `executor`) — writes `REPORT.md` summarizing
  what was checked, what failed, and why.

**Deliverables (in `reviews/<slug>/phase3/outputs/`).**

- `graph.final.json`
- `graph.final.html`
- `graph.final.svg` (deferred — HTML is the primary visual)
- `paper.highlighted.pdf`
- `REPORT.md`

**Gate.** Human review of the highlighted PDF. Possible responses: APPROVE,
ITERATE (fix in phase 3 scope), REGRESS(N) (re-open phase N).
