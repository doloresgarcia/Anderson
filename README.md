# Anderson — Paper Claim Verification Orchestrator

Anderson is a multi-agent orchestrator that ingests a scientific paper and produces:

1. A **claim graph** of the paper, built per the conventions in `src/conventions/`.
2. A **verification report** identifying which claims could not be verified or are not well supported by the paper itself or the surrounding literature.
3. The **paper with sentences highlighted** that fail verification, plus a **trust score** cover page summarizing the review.

The architecture follows a "thin orchestrator + specialized subagents" pattern adapted from
[jfc-mit/jfc](https://github.com/jfc-mit/jfc): the orchestrator never extracts claims, runs
literature searches, or judges proofs itself — it dispatches subagents whose role
specifications live in `src/agents/`, and tracks artifacts that subagents produce.

## Phases

| Phase | Purpose | Primary artifacts |
|-------|---------|------------------|
| 1. Ingest & Map  | Parse paper, extract claims, two-pass literature search (local bank → external), build initial claim graph | `CLAIMS.md`, `LITERATURE.md`, `graph.v1.json` |
| 2. Strategy & Check | Run five specialized checker agents (one per error category) against the claims and merge their verdicts into the graph | `STRATEGY.md`, `VERIFICATION.md`, `graph.v2.json` |
| 3. Report | Trust score, marked-up paper, interactive claim graph, statistics, prose summary | `STATS.md`, `paper.highlighted.pdf`, `graph.final.html`, `REPORT.md` |

Per phase the orchestrator runs the loop **EXECUTE → REVIEW → CHECK → COMMIT → ADVANCE**.

## Repository layout

```
anderson/
├── Makefile                   # convenience targets — `make demo`, `make graph`, `make stats`, …
├── README.md
├── requirements.txt           # PyMuPDF
├── demo/                      # planted-issue demo paper + pre-baked phase-1/2 artifacts
├── literature_bank/           # pre-collected reference PDFs (auto-symlinked into every review)
├── reviews/                   # one subdirectory per paper under review
└── src/
    ├── methodology/           # phase definitions, orchestration loop, review protocol, artifact specs
    ├── agents/                # role specifications the orchestrator dispatches
    ├── conventions/           # error categories, claim taxonomy, graph schema, confidence scale
    ├── templates/             # CLAUDE.md templates dropped into per-paper review dirs
    ├── vendor/                # cytoscape.min.js (inlined into rendered graph HTML for offline viewing)
    ├── scaffold_review.py     # creates a new reviews/<slug>/ tree wired to a paper
    ├── render_graph.py        # graph.*.json → graph.*.html (Cytoscape.js, dark theme, self-contained)
    ├── highlight_paper.py     # paper.pdf + VERIFICATION.md → paper.highlighted.pdf
    ├── highlight_text.py      # paper.txt + VERIFICATION.md → highlighted PDF + HTML
    └── claim_stats.py         # CLAIMS.md + VERIFICATION.md → STATS.md (counts + trust score)
```

## Setup

```bash
make install            # = pip install -r requirements.txt (PyMuPDF)
```

## Quick demo (no Claude Code required)

A planted-issue 1-page ML paper ships in `demo/` along with pre-authored
phase-1 and phase-2 outputs. `make demo` runs only the deterministic
phase-3 scripts on those bundled artifacts:

```bash
make demo
```

Outputs land in `reviews/__demo__/phase3/outputs/`:

| file | what it is |
|------|------------|
| `paper.highlighted.pdf` | cover page with the trust score, then the paper with five-category color-coded highlights and clickable per-claim comments |
| `graph.final.html` | dark-theme Cytoscape compound graph — fully self-contained (Cytoscape.js inlined), opens in any browser, works offline |
| `STATS.md` | trust score block, counts by type and aggregate verdict, type×verdict matrix, **per-error-category breakdown**, INCONCLUSIVE reasons across all five checkers, per-group rows |
| `paper.highlighted.html` | text-mode browser companion to the PDF |

The demo paper contains three planted problems — a fabricated `Chen et al. (2024)` citation (caught as `literature_collision`), an abstract↔results numerical contradiction (87.3% vs 78.4%, caught as `internal_contradiction` and flagged on both ends), and a "we thus prove that sparsity is sufficient for emergent reasoning" overreach (caught as `unreferenced` on the abstract version and `ambiguous` on the discussion version). Anderson catches all three; the trust score lands at **58/100 (low)**.

`make demo` only runs the deterministic Python scripts; the LLM-driven extraction and verification are pre-baked. To watch the full pipeline run live, see the next section.

## Running a real review (full pipeline)

### 1. Scaffold the review

```bash
# from a PDF:
python3 src/scaffold_review.py --paper /path/to/paper.pdf --slug my-slug

# or from plain text:
python3 src/scaffold_review.py --text  /path/to/paper.txt --slug my-slug
```

This creates `reviews/my-slug/` with:
- phase subdirectories (`phase1/`, `phase2/`, `phase3/`)
- symlinks to `src/methodology/`, `src/conventions/`, `src/agents/`, and `literature_bank/`
- a root `CLAUDE.md` that boots the orchestrator
- `paper/paper.txt` (extracted from PDF via PyMuPDF, or copied as-is for `--text`)

### 2. Open Claude Code in the review directory

```bash
cd reviews/my-slug
claude
```

### 3. Kick off the orchestrator

In Claude Code, send the prompt:

> Read CLAUDE.md and start phase 1.

Claude Code is now the orchestrator. It reads the role specs under `agents/`
and dispatches subagents. Each phase ends with a reviewer + arbiter pass and
a commit; the orchestrator pauses for your OK before advancing.

- **Phase 1 — Ingest & Map.** `claim_extractor` → `literature_searcher` (bank first, then external) → `graph_builder` → write `FINDINGS.md`. Single-bot review.
- **Phase 2 — Strategy & Check.** `strategist` → five **checker agents** in parallel — `checker_unreferenced`, `checker_ambiguous`, `checker_contradiction`, `checker_literature`, `checker_domain` — each examining every claim for its error category and writing its own section of `VERIFICATION.md` (verdicts `FLAGGED` / `CLEAR` / `INCONCLUSIVE`) → `graph_builder` (v2). Three-bot review (critical + constructive + arbiter).
- **Phase 3 — Report.** `highlighter` (invokes `highlight_paper.py` or `highlight_text.py`), `graph_builder` (invokes `render_graph.py`), and `report_writer` (invokes `claim_stats.py` then writes `REPORT.md`) run in parallel. Three-bot review, then a human gate.

### 4. Read the outputs

Everything lands in `reviews/my-slug/phase3/outputs/`. Same set as the quick demo above, plus `REPORT.md` (prose summary).

## Re-rendering individual deliverables

You can re-run any phase-3 script standalone — useful while iterating:

```bash
make graph     REVIEW=reviews/my-slug    # re-render the HTML graph
make stats     REVIEW=reviews/my-slug    # refresh STATS.md
make highlight REVIEW=reviews/my-slug    # re-render the highlighted paper
                                          # (auto-detects PDF vs txt input)

# direct invocations work too:
python3 src/render_graph.py reviews/my-slug/phase2/outputs/graph.v2.json
python3 src/claim_stats.py  reviews/my-slug
python3 src/highlight_text.py reviews/my-slug
```

`make help` lists all the targets.

## Error categories

Phase 2 detects errors across five mutually exclusive categories. One checker agent per category, each with its own highlight color:

| category | color | meaning |
|---|---|---|
| `unreferenced` | blue `#4285F4` | needs a citation |
| `ambiguous` | amber `#FFBF00` | unclear or underspecified |
| `internal_contradiction` | orange `#FF6D00` | paper contradicts itself |
| `literature_collision` | red `#D32F2F` | conflicts with published work |
| `domain_violation` | purple `#7B1FA2` | conflicts with established knowledge |

A sentence flagged in multiple categories is highlighted in the most-severe color (severity order: `domain_violation` > `literature_collision` > `internal_contradiction` > `ambiguous` > `unreferenced`); the click-through annotation lists all triggered categories with each checker's reasoning. See `src/conventions/error_categories.md` for the evidence standard each checker requires before emitting `FLAGGED`.

## Trust score

Each claim has an aggregate verdict computed from the five checkers — `FLAGGED` if any checker flagged it, else `INCONCLUSIVE` if any checker was inconclusive, else `CLEAR` if any checker examined it, else `NOT_CHECKED`. The trust score weights `CLEAR=1.0`, `INCONCLUSIVE=0.5`, `FLAGGED=0.0`, with `NOT_CHECKED` excluded from the denominator:

```
score = round(100 * (CLEAR + 0.5 * INCONCLUSIVE) / attempted)
```

Buckets: ≥85 → high (green), ≥60 → medium (yellow), <60 → low (red). The score appears as a colored cover page on `paper.highlighted.pdf`, as a banner at the top of `STATS.md`, and as the headline section of `REPORT.md`.

## Literature bank

`literature_bank/` at the repo root holds reference PDFs the literature searcher checks **before** any external search. Drop new reference papers there as PDFs (any filename); the searcher reads them and tags matches `source: bank` in `LITERATURE.md`. External search runs only for claims the bank doesn't cover, biased toward peer-reviewed published work over preprints. See `src/agents/literature_searcher.md` for the full strategy.

The bank is automatically symlinked into every review directory by `scaffold_review.py`. An empty bank is fine — the searcher just falls back to external search and logs the gap.

## Conventions (the domain logic)

The files in `src/conventions/` define what Anderson reasons about — keep these in sync with how you want the system to behave:

- `error_categories.md` — the five error categories, their colors, evidence standards, severity order
- `claim_taxonomy.md` — the seven claim types and how the extractor decides
- `graph_schema.md` — node and edge types, the ≤20-group clustering rule, the Cytoscape.js HTML output spec
- `verification.md` — domain-specific refinements layered on top of `error_categories.md` (placeholder by default; checkers fall back to the built-in standards)
- `confidence.md` — the discrete `high`/`medium`/`low` scale used everywhere

Methodology (under `src/methodology/`) defines *how* the orchestrator runs; conventions define *what* it's reasoning about. Edits to convention files do not require touching role specs or the methodology.
