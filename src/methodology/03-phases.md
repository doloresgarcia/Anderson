# Phases

Three phases. Phases 1 and 2 end with a checkpoint commit after arbiter PASS.
Phase 3 reaches a human gate after arbiter PASS and commits final artifacts only
after human APPROVE.

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
- `references.bib`
- `graph.v1.json`
- `FINDINGS.md` — short prose summary: how many claims, distribution by type, gaps
  identified at this stage.

**Review.** Single-bot review (correctness/completeness of claim extraction and graph
well-formedness). Arbiter PASS required to advance.

### Phase 1 gotchas

- If `conventions/claim_taxonomy.md` is the placeholder, every claim will be
  `UNCLASSIFIED`. The `critical_reviewer` will raise that as Category B; that
  is expected. Surface the gap in the dispatch summary, do not block on it.
- `references.bib` must contain every key that appears in `LITERATURE.md`.
  Mismatches are auto-Category-A.
- The literature searcher always searches `literature_bank/` (at the repo
  root) before any external call. If the bank is missing, empty, or
  unreadable, the searcher logs this and falls back to external search — this
  is not a phase failure.

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
  Each checker writes its own `section.md` with verdicts `FLAGGED` / `CLEAR` /
  `INCONCLUSIVE`; the orchestrator concatenates the five sections into
  `VERIFICATION.md` in canonical section order.
- `graph_builder` — re-runs to merge checker findings onto the graph, emitting
  `graph.v2.json`.

**Deliverables (in `reviews/<slug>/phase2/outputs/`).**

- `STRATEGY.md`
- `VERIFICATION.md`
- `graph.v2.json`

**Review.** 3-bot review (a critical reviewer, a constructive reviewer, and an
arbiter). Findings classified A/B/C per `04-review.md`.

### Phase 2 gotchas

- Checker agents are independent; do not let them write to the same file
  simultaneously. Each writes its section first under
  `phase2/agents/<checker_name>/section.md`; the orchestrator's concat step
  assembles `VERIFICATION.md` in canonical section order: `unreferenced`,
  `ambiguous`, `internal_contradiction`, `literature_collision`,
  `domain_violation`. This order is for deterministic assembly only; highlight
  severity remains defined by `conventions/error_categories.md`.
- All five checkers always run. If a checker finds nothing to flag for any
  claim, its section still appears in `VERIFICATION.md` with all `CLEAR`
  entries.
- Concurrency: all five checkers run in parallel from the main session (one
  agent per category, not per claim). This keeps the total agent count at 5
  regardless of claim count.
- Common phase-2 fixer fixes:
  - A `FLAGGED` verdict without the evidence required by
    `conventions/error_categories.md` → demote to `INCONCLUSIVE` or supply
    the evidence.
  - Strategist skipped an `importance=high` claim → re-run checkers for it.
  - A checker used the wrong category → reassign the finding.
  - Any changed checker section → re-concatenate `VERIFICATION.md` and re-run
    `graph_builder` so `graph.v2.json` matches the current sections.

## Phase 3 — Report

**Goal.** Produce the final, human-facing artifacts.

**Subagents dispatched.**

- `highlighter` — reads `graph.v2.json` and `VERIFICATION.md`; produces the
  highlighted paper with `FLAGGED` sentences color-coded by error category and
  `INCONCLUSIVE` sentences colored yellow. PDF input produces
  `paper.highlighted.pdf`; text input produces `paper.highlighted.html` and,
  when PyMuPDF is available, a synthesized `paper.highlighted.pdf`.
- `graph_builder` — final pass; emits `graph.final.json`. The HTML
  visualization (`graph.final.html`) is rendered separately by
  `python3 src/render_graph.py`, invoked by `make graph` or the
  phase-3 dispatcher.
- `report_writer` (specialization of `executor`) — invokes
  `src/claim_stats.py` for `STATS.md`, then writes `REPORT.md` summarizing what
  was checked, what failed, and why.

**Deliverables (in `reviews/<slug>/phase3/outputs/`).**

- `graph.final.json`
- `graph.final.html` (rendered from `graph.final.json` by `src/render_graph.py`)
- `paper.highlighted.pdf` (PDF input, or text input when PyMuPDF is available)
- `paper.highlighted.html` (text input)
- `STATS.md`
- `REPORT.md`

**Gate.** Human review of the highlighted paper, graph, stats, and report.
Possible responses: APPROVE (commit final Phase 3 artifacts), ITERATE (fix in
phase 3 scope, re-run affected outputs and review, then return to this gate),
REGRESS(N) (re-open phase N without making the final Phase 3 commit).

### Phase 3 gotchas

- If most claims in `VERIFICATION.md` are `INCONCLUSIVE` because the
  verification conventions are the placeholder, the highlighted paper output
  will have many yellow highlights and the report will say "inconclusive" a
  lot. That is the intended degraded output, not a phase-3 bug. Tell the user;
  do not paper over it.
- Phase-3 specific Category-A triggers (in addition to the global ones):
  - A highlight in the highlighted paper output whose claim_id has no
    `FLAGGED` or `INCONCLUSIVE` entry in `VERIFICATION.md`.
  - A `FLAGGED` highlight whose color does not match the most severe flagged
    category for that claim per `conventions/error_categories.md`, or an
    `INCONCLUSIVE` highlight that is not yellow.
  - A node in `graph.final.json` lacking the verdict layer when
    `graph.v2.json` had it.
  - The phase-3 prose summary introducing a verdict that is not in
    `VERIFICATION.md`.
