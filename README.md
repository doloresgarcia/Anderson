# Anderson — Paper Claim Verification Orchestrator

Anderson is a multi-agent orchestrator that ingests a scientific paper and produces:

1. A **claim graph** of the paper, built per the conventions in `src/conventions/`.
2. A **verification report** identifying which claims could not be verified or are not well supported by the paper itself or the surrounding literature.
3. The **paper with sentences highlighted** that fail verification.

The architecture follows a "thin orchestrator + specialized subagents" pattern adapted from
[jfc-mit/jfc](https://github.com/jfc-mit/jfc): the orchestrator never extracts claims, runs
literature searches, or judges proofs itself — it dispatches subagents whose role
specifications live in `src/agents/`, and tracks artifacts that subagents produce.

## Phases

| Phase | Purpose | Primary artifact |
|-------|---------|------------------|
| 1. Ingest & Map  | Parse paper, extract claims, run literature search, build initial claim graph | `CLAIMS.md`, `graph.v1.json`, `LITERATURE.md` |
| 2. Strategy & Verify | Choose which claims to check; verify against the paper itself and external literature; update graph | `STRATEGY.md`, `VERIFICATION.md`, `graph.v2.json` |
| 3. Report  | Final claim graph + paper with unverified sentences highlighted | `graph.final.json`, `paper.highlighted.pdf`, `REPORT.md` |

Per phase the orchestrator runs the loop **EXECUTE → REVIEW → CHECK → COMMIT → ADVANCE**.

## Repository layout

```
anderson/
├── src/
│   ├── methodology/       # phase definitions, orchestration loop, review protocol, artifact specs
│   ├── agents/            # role specifications the orchestrator dispatches
│   ├── conventions/       # graph schema, claim taxonomy, verification rules (USER-DEFINED)
│   ├── templates/         # CLAUDE.md templates dropped into per-paper review dirs
│   └── scaffold_review.py # creates a new reviews/<slug>/ tree wired to a paper
└── reviews/               # one subdirectory per paper under review
```

## Starting a review

```bash
python src/scaffold_review.py --paper /path/to/paper.pdf --slug some-paper-slug
```

This creates `reviews/some-paper-slug/` with phase subdirectories, symlinks to
`src/methodology/` and `src/conventions/`, and a root `CLAUDE.md` that boots the
orchestrator with the paper as input.

## What is intentionally not yet specified

The following live in `src/conventions/` as placeholders and must be filled in before
the system can produce non-trivial output:

- **`graph_schema.md`** — node/edge types, IDs, properties of the claim graph
- **`claim_taxonomy.md`** — what counts as a claim, how to label claim types
- **`verification.md`** — verification strategies and pass/fail rules

Until these are written, agents will produce a structurally correct but semantically
empty skeleton — exactly enough to wire and test the orchestration loop.
