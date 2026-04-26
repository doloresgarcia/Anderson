# Anderson — Paper Claim Verification Orchestrator

Anderson is a multi-agent orchestrator that ingests a scientific paper and produces:

1. A **claim graph** of the paper, built per the conventions in `src/conventions/`.
2. A **verification report** identifying which claims could not be verified or are not well supported by the paper itself or the surrounding literature.
3. The **paper with sentences highlighted** for flagged or inconclusive verification findings, plus a **trust score** cover page summarizing the review.

The architecture follows a "thin orchestrator + specialized subagents" pattern adapted from
[jfc-mit/jfc](https://github.com/jfc-mit/jfc): the orchestrator never extracts claims, runs
literature searches, or judges proofs itself — it dispatches subagents whose role
specifications live in `.claude/agents/`, and tracks artifacts that subagents produce.

The orchestrator is the main `claude` session driven by the repo-root
`CLAUDE.md`. Subagents cannot spawn other subagents; all dispatch is flat from
the main session.

## Phases

| Phase | Purpose | Primary artifacts |
|-------|---------|------------------|
| 1. Ingest & Map  | Parse paper, extract claims, two-pass literature search (local bank → external), build initial claim graph | `CLAIMS.md`, `LITERATURE.md`, `references.bib`, `graph.v1.json`, `FINDINGS.md` |
| 2. Strategy & Check | Run five specialized checker agents (one per error category) against the claims and merge their verdicts into the graph | `STRATEGY.md`, `VERIFICATION.md`, `graph.v2.json` |
| 3. Report | Trust score, marked-up paper, interactive claim graph, statistics, prose summary | `graph.final.json`, `graph.final.html`, `STATS.md`, `REPORT.md`, highlighted PDF and/or HTML depending on input |

Phases 1 and 2 run **EXECUTE → REVIEW → CHECK → COMMIT → ADVANCE**. Phase 3 runs **EXECUTE → REVIEW → CHECK → HUMAN GATE → COMMIT**, so the final commit happens only after human approval.

## Repository layout

```
anderson/
├── .claude/
│   ├── agents/                # subagent specs (frontmatter + body); 15 roles + _shared/executor_contract.md
│   ├── commands/              # [Phase B] slash commands: /scaffold, /phase1, /phase2, /phase3, /render
│   ├── settings.json          # permission allowlist
│   └── profiles/balanced.json # [Phase E] documented model mix
├── CLAUDE.md                  # root orchestrator — read by the main `claude` session at repo root
├── Makefile                   # convenience targets — `make demo`, `make graph`, `make stats`, …
├── README.md
├── requirements.txt           # PyMuPDF + jsonschema (graph hook) + bibtexparser (bib hook)
├── demo/                      # planted-issue demo paper + pre-baked phase-1/2 artifacts
├── literature_bank/           # pre-collected reference PDFs (read by literature_searcher via repo path)
├── reviews/                   # one subdirectory per paper under review (no symlinks; absolute paths)
└── src/
    ├── methodology/           # phase definitions, orchestration loop, review protocol, artifact specs
    ├── conventions/           # error categories, claim taxonomy, graph schema, confidence scale
    ├── templates/             # per_review_claude.md (thin per-review CLAUDE.md template)
    ├── vendor/                # cytoscape.min.js (inlined into rendered graph HTML for offline viewing)
    ├── scaffold_review.py     # creates a new reviews/<slug>/ tree (no symlinks; thin per-review CLAUDE.md)
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
| `paper.highlighted.pdf` | cover page with the trust score, then the paper with five-category `FLAGGED` highlights, yellow `INCONCLUSIVE` highlights, and clickable per-claim comments |
| `graph.final.html` | dark-theme Cytoscape compound graph — fully self-contained (Cytoscape.js inlined), opens in any browser, works offline |
| `STATS.md` | trust score block, counts by type and aggregate verdict, type×verdict matrix, **per-error-category breakdown**, INCONCLUSIVE reasons across all five checkers, per-group rows |
| `paper.highlighted.html` | text-mode browser companion to the PDF |

The demo uses text input, so both highlighted HTML and synthesized PDF are
expected when PyMuPDF is installed. For real reviews, PDF input produces the
highlighted PDF; text input produces highlighted HTML and, when PyMuPDF is
available, a synthesized highlighted PDF.

The demo paper contains three planted problems — a fabricated `Chen et al. (2024)` citation (caught as `literature_collision`), an abstract↔results numerical contradiction (87.3% vs 78.4%, caught as `internal_contradiction` and flagged on both ends), and a "we thus prove that sparsity is sufficient for emergent reasoning" overreach (caught as `unreferenced` on the abstract version and `ambiguous` on the discussion version). Anderson catches all three; the trust score lands at **58/100 (low)**.

`make demo` only runs the deterministic Python scripts; the LLM-driven extraction and verification are pre-baked. To watch the full pipeline run live, see the next section.

## Running a real review (full pipeline)

### 1. Open Claude Code at the repo root

```bash
cd /path/to/anderson
claude
```

The main `claude` session loads the repo-root `CLAUDE.md` and acts as the
orchestrator. There is no `cd` into a per-review directory; the slug is the
single positional arg to every phase command.

Codex support is a minimal wrapper over the same instruction graph. Claude Code
remains the native full-pipeline runner; when using Codex, start at the repo
root so Codex reads `AGENTS.md`, which delegates to `CLAUDE.md`,
`.claude/commands/`, and `.claude/agents/`. There are no Codex-specific copies
of the phase or agent instructions by design.

### 2. Scaffold and run

In Claude Code, dispatch the slash commands:

```
/scaffold my-slug paper.pdf      # or paper.txt — these produce a working paper.txt
/phase1 my-slug
/phase2 my-slug
/phase3 my-slug
/render my-slug                  # re-render phase-3 deterministic outputs
```

`/scaffold` shells out to `python3 src/scaffold_review.py` with the right
flag inferred from the source format. The new scaffold creates **no
symlinks** for methodology / conventions / agents / literature_bank — agents
resolve those via the repo root.

**arxiv / doi / url sources are recorded but not fetched.** `/scaffold my-slug arxiv:2401.12345` (or `doi:...`, `url:...`) writes the identifier into `paper.meta.json` and stops there — you have to put the paper text into `reviews/my-slug/paper/paper.txt` yourself before `/phase1` will run. (Auto-fetch is a deferred follow-up.)

The orchestrator dispatches the role specs in `.claude/agents/` flat from
the main session. Phases 1 and 2 end with a reviewer + arbiter PASS and a
checkpoint commit; the orchestrator pauses for your OK before advancing. Phase
3 reaches a human gate after arbiter PASS and makes the final commit only after
you reply `APPROVE`.

Each subagent declares a static `model:` in its frontmatter. The default
mix is documented in `.claude/profiles/balanced.json`. To override
globally for a session, set `CLAUDE_CODE_SUBAGENT_MODEL`.

- **Phase 1 — Ingest & Map.** `claim_extractor` → `literature_searcher` (bank first, then external; writes `LITERATURE.md` and `references.bib`) → `graph_builder` → write `FINDINGS.md`. Single-bot review.
- **Phase 2 — Strategy & Check.** `strategist` → five **checker agents** in parallel — `checker_unreferenced`, `checker_ambiguous`, `checker_contradiction`, `checker_literature`, `checker_domain` — each examining every claim for its error category and writing its own section of `VERIFICATION.md` (verdicts `FLAGGED` / `CLEAR` / `INCONCLUSIVE`) → `graph_builder` (v2). Three-bot review (critical + constructive + arbiter).
- **Phase 3 — Report.** `highlighter` (invokes `highlight_paper.py` or `highlight_text.py`), `graph_builder` (invokes `render_graph.py`), and `report_writer` (invokes `claim_stats.py` then writes `REPORT.md`) run in parallel. Three-bot review, then a human gate.

### 4. Read the outputs

Everything lands in `reviews/my-slug/phase3/outputs/`: `graph.final.json`,
`graph.final.html`, `STATS.md`, `REPORT.md`, and the applicable highlighted
paper output(s) for the input mode.

## Verifying the rework end-to-end

Two layers of verification.

**Structural** (no LLM cost — runs in ~10s):

```bash
make ci
```

Runs `make demo` (the deterministic Python pipeline), validates `demo/graph.v2.json` against `src/conventions/graph_schema.json`, and smoke-tests all three hooks against representative payloads. This is the pre-PR sanity check; everything `make ci` covers is structural and machine-verifiable.

**Live LLM dispatch** (real token spend; recommended once before relying on a real review):

```bash
claude                           # at the repo root
> /scaffold __live_smoke__ demo/paper.txt
> /phase1 __live_smoke__
```

What to watch:

- The harness finds `.claude/agents/*.md` and dispatches by name (no "agent type not found").
- `usage_log.py` writes records to `reviews/__live_smoke__/phase1/agents/*/usage.jsonl`.
- `make usage REVIEW=reviews/__live_smoke__` produces a `USAGE.md` with real token counts (not the "no usage recorded" stub).
- For agents with `memory: project` (`literature_searcher`, `arbiter`, etc.), the harness auto-injects `.claude/agent-memory/<name>/MEMORY.md` into their system prompt.
- PostToolUse hooks don't false-fire on writes outside `reviews/<slug>/phase*/outputs/`.

`reviews/__*__/` is gitignored, so smoke-test reviews don't dirty the working tree.

## Permission policy

`.claude/settings.json` ships with a deliberately broad allowlist so an interactive one-operator session doesn't drown in permission prompts. Specifically `Bash(python3 -c:*)`, `Bash(make:*)`, and `Edit(.claude/**)` are wide enough that a misbehaving subagent could read or modify anything reachable from the repo root, regardless of the file-level `deny` block. **This is acceptable for interactive use where you watch dispatches; it is not safe for unattended runs.** Before running this on shared infrastructure or in CI, tighten the allowlist (run `/fewer-permission-prompts` against a real session transcript and trim from there) and audit the deny list for the specific paths you want to lock down.

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

A sentence flagged in multiple categories is highlighted in the most-severe color (severity order: `domain_violation` > `literature_collision` > `internal_contradiction` > `ambiguous` > `unreferenced`); the click-through annotation lists all triggered categories with each checker's reasoning. `INCONCLUSIVE` sentences are highlighted yellow. See `src/conventions/error_categories.md` for the evidence standard each checker requires before emitting `FLAGGED`.

## Trust score

Each claim has an aggregate verdict computed from the five checkers — `FLAGGED` if any checker flagged it, else `INCONCLUSIVE` if any checker was inconclusive, else `CLEAR` if any checker examined it, else `NOT_CHECKED`. The trust score weights `CLEAR=1.0`, `INCONCLUSIVE=0.5`, `FLAGGED=0.0`, with `NOT_CHECKED` excluded from the denominator:

```
score = round(100 * (CLEAR + 0.5 * INCONCLUSIVE) / attempted)
```

Buckets: ≥85 → high (green), ≥60 → medium (yellow), <60 → low (red). The score appears as a colored cover page on `paper.highlighted.pdf`, as a banner at the top of `STATS.md`, and as the headline section of `REPORT.md`.

## Literature bank

`literature_bank/` at the repo root holds reference PDFs the literature searcher checks **before** any external search. Drop new reference papers there as PDFs (any filename); the searcher reads them and tags matches `source: bank` in `LITERATURE.md`. External search runs only for claims the bank doesn't cover, biased toward peer-reviewed published work over preprints. See `.claude/agents/literature_searcher.md` for the full strategy.

The bank is read directly from the repo root by the literature_searcher subagent — no per-review symlink. An empty bank is fine — the searcher just falls back to external search and logs the gap.

## Conventions (the domain logic)

The files in `src/conventions/` define what Anderson reasons about — keep these in sync with how you want the system to behave:

- `error_categories.md` — the five error categories, their colors, evidence standards, severity order
- `claim_taxonomy.md` — the seven claim types and how the extractor decides
- `graph_schema.md` — node and edge types, the ≤20-group clustering rule, the Cytoscape.js HTML output spec
- `verification.md` — domain-specific refinements layered on top of `error_categories.md` (placeholder by default; checkers fall back to the built-in standards)
- `confidence.md` — the discrete `high`/`medium`/`low` scale used everywhere

Methodology (under `src/methodology/`) defines *how* the orchestrator runs; conventions define *what* it's reasoning about. Edits to convention files do not require touching role specs or the methodology.
