# Anderson Workflow Rework — Implementation Plan

**Branch:** `workflow_rework`
**Repo root:** `/Users/oscar/Documents/Coding/Hackathon/Anderson`

---

## 0. Guiding constraints

- One person, hackathon-grade. Prefer small, sequenceable PRs over a big-bang refactor.
- Deterministic Python (`scaffold_review.py`, `render_graph.py`, `highlight_*.py`, `claim_stats.py`) MUST keep working — `make demo` is the smoke test we never break.
- Don't invent harness features. Where unsure (worktree isolation for nested subagents, Stop-hook token telemetry, MCP availability), flagged with fallback.
- Backward compat for in-progress reviews is **not** required for `reviews/test-1` (already broken — those `/afs/cern.ch/...` symlinks are dead) but IS required for `reviews/paper_mistakes0` (real symlinks under user's home).

---

## 1. Final target file tree

```
anderson/
├── .claude/
│   ├── settings.json                       # permission allowlist, hook bindings, model default, env
│   ├── settings.local.json                 # gitignored; per-user overrides (model profile, opt-in MCP)
│   ├── agents/                             # REAL subagents — replace src/agents/*.md
│   │   ├── _shared/
│   │   │   ├── executor_contract.md        # the "plan-first, declared-outputs-only" rules (was executor.md)
│   │   │   └── memory_protocol.md          # how every agent reads/writes agent-memory (req. 13)
│   │   ├── claim_extractor.md              # frontmatter + body. Tools: Read, Write, Edit
│   │   ├── literature_searcher.md          # Tools: Read, Write, Edit, WebFetch, WebSearch, mcp__arxiv__*, mcp__semantic_scholar__*
│   │   ├── graph_builder.md                # Tools: Read, Write, Edit, Bash(python3 src/render_graph.py:*)
│   │   ├── strategist.md
│   │   ├── checker_unreferenced.md
│   │   ├── checker_ambiguous.md
│   │   ├── checker_contradiction.md
│   │   ├── checker_literature.md           # Tools incl. WebFetch + MCP
│   │   ├── checker_domain.md
│   │   ├── highlighter.md                  # Tools: Read, Write, Bash(python3 src/highlight_*.py:*)
│   │   ├── report_writer.md                # Tools: Read, Write, Bash(python3 src/claim_stats.py:*)
│   │   ├── fixer.md
│   │   ├── critical_reviewer.md
│   │   ├── constructive_reviewer.md
│   │   └── arbiter.md
│   ├── commands/
│   │   ├── scaffold.md                     # /scaffold <slug> <pdf|text|arxiv:ID|doi:X|url:X>
│   │   ├── phase1.md                       # /phase1 <slug>
│   │   ├── phase2.md                       # /phase2 <slug>
│   │   ├── phase3.md                       # /phase3 <slug>
│   │   ├── review-phase.md                 # /review-phase <slug> <N>  (fans out crit + constr + arbiter)
│   │   ├── fix.md                          # /fix <slug> <phase> <category-A-id|all>
│   │   └── render.md                       # /render <slug>  (re-runs phase-3 deterministic scripts)
│   ├── skills/                             # Conventions promoted to skills (req. 4)
│   │   ├── error-categories/SKILL.md
│   │   ├── claim-taxonomy/SKILL.md
│   │   ├── graph-schema/SKILL.md
│   │   ├── verification-conventions/SKILL.md
│   │   ├── confidence-scale/SKILL.md
│   │   └── review-protocol/SKILL.md        # methodology/04-review.md as a skill (loaded by reviewers/arbiter)
│   ├── hooks/
│   │   ├── validate_graph.py               # PostToolUse(Write|Edit) on graph.v*.json + graph.final.json
│   │   ├── validate_bib.py                 # PostToolUse(Write|Edit) on LITERATURE.md / references.bib
│   │   ├── commit_prefix.py                # PreToolUse(Bash) — auto-prefix `phase<N>(<role>):` to git commit -m
│   │   ├── stop_commit_nudge.py            # Stop — warn if uncommitted changes when orchestrator stops
│   │   └── usage_log.py                    # Stop / SubagentStop — append per-agent token estimate (req. 11)
│   ├── profiles/                           # Adaptive model picker (req. 10)
│   │   ├── all-opus.json                   # everything → opus-4.7
│   │   ├── balanced.json                   # default — opus/sonnet/haiku mix
│   │   └── fast-cheap.json                 # opus only for arbiter/orchestrator; haiku elsewhere
│   ├── agent-memory/                       # Persistent agent notes (req. 13)
│   │   ├── README.md                       # protocol summary
│   │   ├── _global/
│   │   │   └── orchestrator.md             # cross-paper orchestrator lessons
│   │   ├── literature_searcher/
│   │   │   ├── backends.md                 # rate limits, useful queries, fallback notes
│   │   │   └── domains/<domain>.md         # e.g. `ml.md`, `physics.md` — domain-specific search tips
│   │   ├── checker_literature/
│   │   │   ├── known-miscites.md           # "Bengio 2003 is often miscited as ..."
│   │   │   └── domains/<domain>.md
│   │   ├── checker_domain/domains/<domain>.md
│   │   └── ...                             # one dir per agent that opts into memory
│   └── status.md                           # optional: rendered by hooks for `claude --status`
├── .mcp.json                               # arXiv + Semantic Scholar MCPs (req. 8)
├── CLAUDE.md                               # NEW — root orchestrator at repo root (req. 12, no-cd)
├── Makefile                                # updated, see §3 phase 5
├── README.md                               # updated
├── requirements.txt                        # add: jsonschema, bibtexparser
├── demo/                                   # unchanged
├── literature_bank/                        # unchanged
├── papers/                                 # unchanged
├── reviews/
│   └── <slug>/
│       ├── CLAUDE.md                       # THIN per-review pointer (just slug + paper meta + nav)
│       ├── prompt.md
│       ├── paper/
│       │   ├── paper.pdf | paper.txt
│       │   └── paper.meta.json
│       ├── phase1/   {outputs/, agents/, review/, logs/}
│       ├── phase2/   {outputs/, agents/, review/, logs/}
│       └── phase3/   {outputs/, agents/, review/, logs/}
│       # NO methodology/conventions/agents symlinks — those live under .claude/ and src/
│       # literature_bank/ is no longer symlinked per-review either; agents read the repo-root path
└── src/
    ├── methodology/                        # KEPT — orchestration prose, read by reviewers
    ├── conventions/                        # KEPT — single source of truth; .claude/skills are thin wrappers
    │   └── graph_schema.json               # NEW — formal JSON Schema for hook validation
    ├── templates/
    │   └── per_review_claude.md            # NEW thin per-review template (replaces root_claude.md duty)
    ├── vendor/                             # unchanged
    ├── scaffold_review.py                  # rewritten: relative symlinks (or no symlinks), thin output
    ├── render_graph.py                     # unchanged
    ├── highlight_paper.py                  # unchanged
    ├── highlight_text.py                   # unchanged
    ├── claim_stats.py                      # unchanged
    └── token_log.py                        # NEW — read by usage_log.py hook; aggregates per-agent usage
```

**What's gone:** `src/agents/` (moved to `.claude/agents/`), `src/templates/root_claude.md` (replaced by repo-root `CLAUDE.md` + thin per-review template), `verifier.md` (deprecated, can finally be deleted).

**What stays in `src/`:** `methodology/` (loaded by reviewers, referenced from skills), `conventions/` (the canonical source — `.claude/skills/*/SKILL.md` are thin wrappers that include or summarize them), and all the deterministic Python.

**Key architectural shift:** the orchestrator's `CLAUDE.md` lives at the repo root, takes a `<slug>` argument from the slash command, and reads `reviews/<slug>/CLAUDE.md` for paper-specific framing. This solves req. 12 (no-cd).

---

## 2. Migration plan, ordered into 6 ship-able phases

Each phase is sized for a single review-and-merge cycle. They depend in order, but Phase 5 can ship before Phase 4 if needed.

### Phase A — Subagents + repo-root CLAUDE.md (foundation, ~half a day)

**Goal:** make `.claude/agents/` the source of truth and stop requiring `cd reviews/<slug>` to run a review.

**Create:**
- `.claude/agents/*.md` — one per role (15 files; `verifier.md` dropped). Convert from `src/agents/<name>.md`. Each file gets YAML frontmatter; the body is the existing role spec with `{{slot}}` slots removed (the slash command + dispatch prompt provide them now).
- `.claude/agents/_shared/executor_contract.md` — the contract from `src/agents/executor.md`.
- `/Users/oscar/Documents/Coding/Hackathon/Anderson/CLAUDE.md` — repo-root orchestrator. Parameterized by `$REVIEW_SLUG` env or by a literal slug substituted by the slash command (see Phase B). Replaces `src/templates/root_claude.md`.
- `src/templates/per_review_claude.md` — thin template (≤ 30 lines) for per-review CLAUDE.md: paper meta, slug, paths to phase outputs, pointer to repo-root orchestrator. No subagent dispatch logic — that's all in the repo-root file now.
- `.claude/settings.json` — minimal first cut (model + permission allowlist; hooks added in Phase D).

**Sample agent file pattern (showing one — the orchestrator implementer applies the same recipe to all 15):**

```yaml
---
name: checker_literature
description: Checks each claim in CLAIMS.md against the literature bank and external search results to find statements that conflict with published work. Use during phase 2. MUST cite both paper passage and contradicting source with snippets.
tools: Read, Write, Edit, Grep, Glob, WebFetch, mcp__arxiv__search, mcp__semantic_scholar__search
model: ${PROFILE.checker_literature}    # resolved by orchestrator from active profile
isolation: worktree                      # see §4.9 — flagged as harness-uncertain
---

# checker_literature

(body = current src/agents/checker_literature.md content from "Reads" onward,
 with {{paper_slug}} / {{phase}} slots removed; the dispatching slash command
 supplies them in the prompt instead.)

## Memory

Before starting, read .claude/agent-memory/checker_literature/known-miscites.md
and .claude/agent-memory/checker_literature/domains/<domain>.md (if present).
After finishing, append any new lessons under "## YYYY-MM-DD <slug>" headers.
See .claude/agents/_shared/memory_protocol.md.
```

**Edit:**
- `src/scaffold_review.py` — emit RELATIVE symlinks for `paper/` only, drop `methodology/`/`conventions/`/`agents/`/`literature_bank/` symlinks (no longer needed since `.claude/` lives at repo root and agents resolve absolute paths via the orchestrator). Render the new thin per-review template instead of `root_claude.md`. (See req. 5.)
- `Makefile` — `make demo` calls `python3 src/scaffold_review.py --text demo/paper.txt --slug __demo__ --force`; that still works because phase-3 deterministic scripts read `reviews/<slug>/...` paths, not symlinks.

**Delete (move, really):**
- `src/agents/*.md` — moved to `.claude/agents/`. Leave a stub `src/agents/README.md` for one release saying "agents now live in `.claude/agents/`".
- `src/agents/verifier.md` — deprecated; delete.
- `src/templates/root_claude.md` — superseded by repo-root `CLAUDE.md`.

**Could break:**
- `make demo` — only if scaffold_review.py drops too much. Mitigation: explicit smoke test in PR description: "ran `make demo`, check 4 outputs in reviews/__demo__/phase3/outputs/".
- Anyone with an in-progress review under `reviews/<slug>/` whose CLAUDE.md still expects symlinked `methodology/agents/conventions/` dirs. Mitigation: leave a one-shot upgrade script `src/migrate_review.py` that rewrites a review's CLAUDE.md to point at `.claude/`.
- `reviews/test-1` — already broken via dead `/afs/cern.ch/...` symlinks. Recommend deleting it as part of this PR.

**Effort:** ~4-6 hours of mechanical conversion + 2 hours of testing.

---

### Phase B — Slash commands + no-cd workflow (~half a day)

**Goal:** `/scaffold`, `/phase1 <slug>`, `/phase2 <slug>`, `/phase3 <slug>`, `/review-phase <slug> <N>`, `/fix <slug> <phase> <category>`, `/render <slug>` all work from the repo-root `claude` session.

**Create:** the 7 files in `.claude/commands/`. Each is a markdown file whose body is the prompt the orchestrator should run. Pattern:

```markdown
---
description: Run phase 1 (ingest & map) for the given review slug
argument-hint: <slug>
---

You are the Anderson orchestrator. The user is at the repo root.
Active review: $1 (resolves to reviews/$1/).

Read in order:
- ./CLAUDE.md
- reviews/$1/CLAUDE.md
- src/methodology/03-phases.md (phase 1 section)
- .claude/agents/_shared/executor_contract.md

Then dispatch phase-1 subagents in the order in
src/methodology/03a-orchestration.md § Phase 1, ending with the single-bot
review (critical_reviewer + arbiter). Pause for human OK before /phase2.

Profile: read .claude/profiles/$(cat .claude/.active_profile 2>/dev/null || echo balanced).json
to resolve each subagent's model.
```

**Resolved questions:**
- The slug is the only mandatory positional arg; everything else is in `paper.meta.json` or in the per-review CLAUDE.md.
- `/scaffold <slug> <source>` shells out to `python3 src/scaffold_review.py` with the right flags inferred from the source format (PDF → `--paper`, txt → `--text`, `arxiv:NNNN.NNNNN` → `--arxiv`, `doi:X` → `--doi`, `https://...` → `--url`).
- `/render <slug>` is the slash-command equivalent of `make graph stats highlight REVIEW=reviews/<slug>` — useful between phases.

**Effort:** ~3 hours (mostly prompt writing).

---

### Phase C — Conventions → Skills (~2-3 hours)

**Goal:** progressive disclosure; checker agents only load the convention they care about.

**Create:** `.claude/skills/<name>/SKILL.md` for each of the 5 conventions and `review-protocol`. Each SKILL.md has frontmatter:

```yaml
---
name: error-categories
description: The five Anderson error categories (unreferenced, ambiguous, internal_contradiction, literature_collision, domain_violation), their colors, evidence standards, and severity order. Load when authoring a checker verdict, when assigning highlight colors, or when reviewing a phase 2 verdict.
---
```

The body of `SKILL.md` is a 1-page summary; full text stays in `src/conventions/error_categories.md` and is `@`-included or linked. This way:
- Deterministic Python (`render_graph.py`, `highlight_paper.py`, `claim_stats.py`) keeps reading `src/conventions/*.md` — unchanged.
- Subagents trigger the skill via description matching and read the linked source-of-truth file.

**Edit:** the per-checker agent files reference the skill in their frontmatter description so the harness loads it. Example: `checker_literature.md` description starts "Uses error-categories skill and review-protocol skill..." (the harness's progressive-disclosure mechanism handles the rest).

**Open question:** do skills auto-load when their description matches, or must the agent invoke them? If the latter, agent bodies need a "Skills to invoke" section. The implementer should verify against current Claude Code docs before writing all 6 skills.

**Effort:** ~3 hours.

---

### Phase D — Hooks + JSON schema for graphs (~1 day)

**Goal:** automated guardrails replace some manual review work.

**Create:**
- `src/conventions/graph_schema.json` — formal JSON Schema derived from `src/conventions/graph_schema.md`. The body of graph_schema.md remains the prose source; this file is the machine-readable extract for the hook.
- `.claude/hooks/validate_graph.py` — PostToolUse on Write/Edit where the path matches `reviews/*/phase*/outputs/graph*.json`. Loads `src/conventions/graph_schema.json`, runs `jsonschema.validate`, exits non-zero with a structured message on failure (which the harness surfaces back to the agent for self-correction).
- `.claude/hooks/validate_bib.py` — PostToolUse on Write/Edit of `LITERATURE.md` or `references.bib`. Parses both with `bibtexparser`/regex, emits a finding for any `[@key]` in `LITERATURE.md` not present in `references.bib`. (This is the #1 failure mode per README.)
- `.claude/hooks/commit_prefix.py` — PreToolUse on `Bash(git commit -m:*)`. Inspects current dir against `reviews/<slug>/phase<N>/...` to infer phase number; if the message doesn't already start with `phase<N>(`, prefix it. Read-only check + suggestion if it can't infer (don't block).
- `.claude/hooks/stop_commit_nudge.py` — Stop hook. `git -C <repo> status --porcelain`; if non-empty, append a reminder to the agent transcript: "uncommitted changes; commit before next dispatch."
- `.claude/hooks/usage_log.py` — see Phase E.

**Edit:**
- `requirements.txt` — add `jsonschema>=4`, `bibtexparser>=1.4`.
- `.claude/settings.json` — wire all hooks under their event keys.

**Could break:** if `graph_schema.json` doesn't perfectly mirror the prose, every graph fails validation. Mitigation: derive the schema from `demo/graph.v2.json` first (it must validate), then tighten.

**Effort:** ~6-8 hours.

---

### Phase E — Token monitoring + adaptive model profiles (~half a day each, 1 day total)

**Goal:** req. 10 + req. 11.

**Profiles (req. 10):**
- Create `.claude/profiles/{all-opus,balanced,fast-cheap}.json`. Schema:
  ```json
  {
    "name": "balanced",
    "default_model": "claude-sonnet-4-7",
    "agents": {
      "claim_extractor":      "claude-haiku-4-7",
      "literature_searcher":  "claude-sonnet-4-7",
      "graph_builder":        "claude-haiku-4-7",
      "strategist":           "claude-sonnet-4-7",
      "checker_unreferenced": "claude-haiku-4-7",
      "checker_ambiguous":    "claude-haiku-4-7",
      "checker_contradiction":"claude-sonnet-4-7",
      "checker_literature":   "claude-sonnet-4-7",
      "checker_domain":       "claude-sonnet-4-7",
      "highlighter":          "claude-haiku-4-7",
      "report_writer":        "claude-haiku-4-7",
      "fixer":                "claude-sonnet-4-7",
      "critical_reviewer":    "claude-sonnet-4-7",
      "constructive_reviewer":"claude-sonnet-4-7",
      "arbiter":              "claude-opus-4-7",
      "orchestrator":         "claude-opus-4-7"
    }
  }
  ```
- Active profile selected by `.claude/.active_profile` (a one-line file containing the profile name) or `ANDERSON_PROFILE` env var. Default = `balanced`.
- Each subagent's frontmatter uses `model: inherit` and the slash command's dispatch prompt looks up the profile and passes the chosen model in the dispatch (the orchestrator hands the resolved model to each Task call).
- Justification of `balanced`: arbiter + orchestrator need cross-document reasoning (opus). Reviewers + literature_searcher + checker_literature/contradiction/domain need to read whole docs and judge subtle conflicts (sonnet). Extractor / graph builder / highlighter / report_writer / unreferenced / ambiguous checkers are mechanical (haiku).

**Token monitoring (req. 11) — be honest about the harness:**

I cannot guarantee Stop / SubagentStop hooks receive token-usage telemetry as a structured field. Two-tier design:

- **Tier 1 (definitely works):** `usage_log.py` is a SubagentStop hook (or equivalent) that records dispatch metadata: `{slug, phase, role, started_at, ended_at, duration_s, model_used}` to `reviews/<slug>/phase<N>/agents/<role>/usage.jsonl`. Wall-time + model is the workable proxy.
- **Tier 2 (best-effort, depends on harness):** if the hook event payload includes `input_tokens` / `output_tokens` (current Claude Code does for some events but not all — verify before relying), append them.
- **Tier 3 (always works as fallback):** every subagent's prompt template gets a final instruction: "before exiting, write a one-line `usage.md` containing your read-byte count, write-byte count, and a rough self-estimate of input/output tokens." Cheap, slightly inaccurate, fully under our control.

`src/token_log.py` is a small CLI that aggregates `reviews/*/phase*/agents/*/usage.jsonl` into a per-phase summary (`reviews/<slug>/USAGE.md`). The `/render` command and `make demo` invoke it at the end so the user gets a summary.

**Effort:** profiles ~3h, token logging ~4-5h.

---

### Phase F — MCP + worktree isolation polish (~half a day)

**Goal:** req. 8 + req. 9.

**Create `.mcp.json`:**
```json
{
  "mcpServers": {
    "arxiv":              { "command": "uvx", "args": ["mcp-server-arxiv"] },
    "semantic_scholar":   { "command": "uvx", "args": ["mcp-server-semanticscholar"] }
  }
}
```
(Exact server packages need user verification — there are several arXiv MCPs and we shouldn't pick blind. Phase-F first task is "research the right packages.")

`literature_searcher` and `checker_literature` get these MCP tools added to their frontmatter `tools:` list. All other agents are NOT granted MCP access (lock-down by allowlist).

**Worktree isolation (req. 9) — flagged uncertain:**

`isolation: "worktree"` is a documented frontmatter field for parallel subagents in the best-practices repo, but I'm not 100% sure it works for nested parallel dispatches inside an orchestrator that's itself inside a Task. **Plan A:** set `isolation: "worktree"` on the 5 checkers + 3 phase-3 agents and verify with a test run. **Plan B (fallback):** if worktree isolation misbehaves, fall back to the current "each checker writes its own `phase2/agents/<name>/section.md` and a sequential concat step assembles `VERIFICATION.md`" pattern (already documented in `phase2_claude.md`). The disjoint-output write pattern works whether or not we get worktree isolation.

**Effort:** ~3h (research MCP packages, ~30 min wiring, ~2h verifying worktree behavior or implementing fallback).

---

### Phase G — Memory subsystem (~half a day, parallelizable with F)

See req. 13 design below. Files:
- `.claude/agent-memory/README.md` — protocol summary (when to read, when to write, format).
- `.claude/agents/_shared/memory_protocol.md` — same content from agent's POV.
- Bootstrap empty `.claude/agent-memory/<agent>/` dirs for every agent that opts in (literature_searcher, checker_literature, checker_domain, orchestrator).
- A small Stop-hook addition or a guideline in each agent's body: agents read their memory dir at start, append-only at end with a date header.

**Effort:** ~3-4h (mostly prose).

---

## 3. Per-requirement design decisions

### Req. 1 — `src/agents/*.md` → `.claude/agents/*.md` with frontmatter

**Decision:** top-level `.claude/agents/` (not per-review). Reason: subagents are stateless w.r.t. paper slug — they take inputs as arguments. Per-review duplication is wasted complexity.

**Decision:** `src/agents/` goes away entirely (with a one-release stub README). The `.claude/agents/<name>.md` file IS the role spec; the body keeps the existing prose, only the prompt-template slots get removed (now supplied by slash command).

**Rejected alternatives:**
- Per-review `.claude/agents/`: redundant, breaks no-cd workflow.
- Keep `src/agents/` as canonical and symlink into `.claude/agents/`: extra indirection, harness may not follow symlinks for agent discovery.

**Files:** all of `.claude/agents/*.md`, repo-root `CLAUDE.md`, `src/templates/per_review_claude.md`, `src/scaffold_review.py`.

**Open Q:** does the harness re-read agent files between dispatches in one session, or cache them? If cached, editing `.claude/agents/X.md` mid-session won't take effect — minor for one-shot reviews, annoying for iteration.

---

### Req. 2 — `.claude/settings.json`

**Decision:** ship a minimal first cut and grow it. Initial allowlist:
```json
{
  "permissions": {
    "allow": [
      "Bash(python3 src/*.py:*)",
      "Bash(make *)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git add:*)",
      "Bash(git commit -m:*)",
      "Edit(reviews/**)",
      "Write(reviews/**)",
      "Read(**)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push:*)",
      "Edit(.claude/**)",
      "Edit(src/**)",
      "Edit(literature_bank/**)"
    ]
  },
  "model": "claude-sonnet-4-7",
  "hooks": { ... wired in Phase D ... }
}
```

**Rejected:** wide-open `Bash(*)` — defeats the purpose. Per-agent allowlists in frontmatter — too much duplication; settings.json is the choke point.

**Open Q:** the `simplify` and `fewer-permission-prompts` skills can post-hoc generate this from a transcript; consider running it once after Phase B to catch missed allowlist entries.

**Files:** `.claude/settings.json`, `.claude/settings.local.json` (gitignored, for per-user MCP credentials and profile overrides).

---

### Req. 3 — Slash commands

Designed in Phase B above. **Decision:** slug is the single positional arg for everything except `/scaffold` (slug + source). All paper-specific data lives in `reviews/<slug>/paper/paper.meta.json`.

**Open Q:** should `/phase2 my-paper` automatically run the phase-2 review trio, or stop after EXECUTE and let the user fire `/review-phase my-paper 2`? My recommendation: phase commands run EXECUTE → REVIEW → CHECK → COMMIT and pause before ADVANCE; the user dispatches `/phase<N+1>` themselves. (Consistent with current methodology.)

**Files:** all 7 in `.claude/commands/`.

---

### Req. 4 — Conventions → Skills

Designed in Phase C above. **Decision:** SKILL.md is a thin wrapper; the canonical text stays in `src/conventions/`. Two readers (Claude via skill description; deterministic Python via `src/conventions/`) read the same content (the SKILL.md file `@`-includes the source).

**Files:** all 6 in `.claude/skills/<name>/SKILL.md`.

---

### Req. 5 — Fix scaffold_review.py symlinks

**Decision:** drop most symlinks entirely. With `.claude/` at repo root and the orchestrator launched from repo root (no-cd), there is no need to symlink `methodology/`, `conventions/`, `agents/`, or `literature_bank/` into each review. Subagents read absolute paths through the orchestrator.

What stays in a per-review tree: `paper/`, `phase{1,2,3}/`, `CLAUDE.md` (now thin), `prompt.md`. No symlinks.

**Rejected:** keep relative symlinks — works but is dead weight once paths are absolute through repo root.

**Migration concern:** `paper_mistakes0/` has dead but valid-looking symlinks under the user's home; running `scaffold_review.py --force` against it would clobber the work. Solution: a separate `src/migrate_review.py` (one-shot) rewrites a review's CLAUDE.md and removes the now-obsolete symlinks without touching the artifacts.

**Files:** `src/scaffold_review.py`, `src/migrate_review.py` (new).

**Open Q:** drop `reviews/test-1` entirely? It's a dead artifact pointing to /afs/cern.ch/. Recommend yes — git rm the whole dir.

---

### Req. 6 — `<important if="...">` tags in CLAUDE.md

**Decision:** tag the 5 hard rules from the current `root_claude.md` with `<important>` blocks (unconditional) and add `<important if="literature_searcher_just_finished">` style conditional blocks where context-relevant. Specifically tag:
- "No fabricated citations" (always important)
- "Commit before each subagent dispatch" (always important)
- "Use the role spec; do not author prompts ad hoc" (always important)
- "Bibtex keys must resolve in references.bib" (`if="working_with_LITERATURE.md"`)
- "FLAGGED requires evidence per error_categories.md" (`if="working_with_VERIFICATION.md"`)

**Open Q:** the conditional `if="..."` syntax is from the best-practices repo; verify the harness supports it. If not, fall back to plain `<important>`.

**Files:** repo-root `CLAUDE.md`, `src/templates/per_review_claude.md`.

---

### Req. 7 — Hooks

Designed in Phase D above. **Decision matrix:**

| Hook | Event | Trigger | Action |
|---|---|---|---|
| `validate_graph.py` | PostToolUse | `Write\|Edit` matching `reviews/*/phase*/outputs/graph*.json` | jsonschema validate; exit 2 on fail |
| `validate_bib.py` | PostToolUse | `Write\|Edit` matching `LITERATURE.md` or `references.bib` | parse both, find dangling keys, exit 2 on fail |
| `commit_prefix.py` | PreToolUse | `Bash(git commit -m:*)` | infer phase, prefix message if missing |
| `stop_commit_nudge.py` | Stop | always | `git status --porcelain`; warn on dirty |
| `usage_log.py` | SubagentStop (preferred) or Stop | always | append usage record; see req. 11 |

**Open Q:** confirm the harness's PostToolUse hook can block / surface an error message back to the agent for self-correction (vs. just logging). If it can only log, we lose the auto-fix loop and validation becomes informational only — still useful but weaker.

**Files:** `.claude/hooks/*.py`, `.claude/settings.json`, `src/conventions/graph_schema.json`, `requirements.txt`.

---

### Req. 8 — `.mcp.json` with arXiv + Semantic Scholar

Designed in Phase F above. **Decision:** wire MCPs only for `literature_searcher` and `checker_literature`. Other agents have no internet access (locked down by `tools:` frontmatter — doesn't list WebFetch or any `mcp__*` tool).

**Rejected:** generic web search for everyone — invites fabrication, which is the #1 failure mode.

**Open Q:** which exact MCP packages? There are 3+ arXiv MCPs in the wild. Phase-F task 1 is "verify which arXiv + Semantic Scholar MCPs are maintained and credential-free." If credentials are needed, document them in `.claude/settings.local.json` (gitignored).

**Files:** `.mcp.json`, `.claude/agents/literature_searcher.md`, `.claude/agents/checker_literature.md`.

---

### Req. 9 — Worktree isolation for parallel checkers

**Decision:** add `isolation: worktree` to the 5 checker agents and the 3 phase-3 agents (highlighter, graph_builder, report_writer). **Verify in a test run** before claiming victory.

**Fallback:** the current disjoint-output pattern (each checker writes `phase2/agents/<name>/section.md`, a concat step assembles `VERIFICATION.md`) doesn't strictly require worktree isolation — disjoint paths suffice. If worktree isolation misbehaves with nested subagents, fall back to disjoint paths and accept that two subagents *could* in principle stomp each other (they don't, given the path discipline).

**Open Q:** does worktree isolation work when the orchestrator is itself a slash-command-driven session, not a subagent?

**Files:** all 8 affected agent frontmatters.

---

### Req. 10 — Adaptive model picker

Designed in Phase E above. **Decision:** profiles live in `.claude/profiles/<name>.json`, active profile selected by `.claude/.active_profile` or `ANDERSON_PROFILE` env var. Each subagent's frontmatter uses `model: inherit`; the orchestrator looks up the profile per dispatch and passes the chosen model.

**Rejected:**
- Hardcode in each agent's frontmatter — locks profiles in, no global toggle.
- Single env var per agent — too many env vars.
- Read profile from `settings.json` directly — couples model picking to permission config; profiles are a separate concern.

**Default profile:** `balanced` (justified above).

**Open Q:** can a slash command read a JSON file at dispatch time and substitute model into the Task call? If the harness doesn't support runtime model selection per Task, we'd need to materialize each agent's frontmatter from the profile at scaffold time — uglier but workable. Verify before implementation.

**Files:** `.claude/profiles/*.json`, `.claude/.active_profile` (gitignored), repo-root `CLAUDE.md` (orchestrator reads profile), all 15 agent files.

---

### Req. 11 — Token monitoring

Designed in Phase E (3-tier). **Decision summary:**

- **Always log:** dispatch metadata (role, phase, model, wall-time) via SubagentStop hook → `reviews/<slug>/phase<N>/agents/<role>/usage.jsonl`.
- **Log if available:** token counts from hook payload.
- **Always available fallback:** each subagent writes a `usage.md` with self-estimated tokens (read-byte count is a fine proxy for input; write-byte count for output).
- Aggregator: `src/token_log.py` produces `reviews/<slug>/USAGE.md` with per-phase, per-agent breakdowns. Called by `/render` and `make demo`.

**Open Q:** investigate `claude --resume` / session JSONL logs — they may contain ground-truth token counts that we can post-hoc sum. If yes, `token_log.py` reads from there instead of relying on hooks.

**Files:** `.claude/hooks/usage_log.py`, `src/token_log.py`, every agent body (final-step instruction).

---

### Req. 12 — No-cd workflow

Designed in Phase B + Phase A. **Decision:** repo-root `CLAUDE.md` is the orchestrator. Slash commands take `<slug>` and resolve to `reviews/<slug>/`. Subagents receive absolute paths via the dispatch prompt.

**Rejected:**
- Per-review CLAUDE.md as orchestrator — keeps the cd requirement.
- Symlink the repo-root `.claude/` into each review — `.claude/` discovery is ancestor-walked, so this works for free if you cd, but defeats the purpose.

**Path implication:** all subagent prompts use absolute paths like `reviews/<slug>/phase1/outputs/CLAIMS.md` instead of `phase1/outputs/CLAIMS.md`. A trivial textual change in each agent's prompt template.

**Files:** repo-root `CLAUDE.md`, all 7 slash commands, all 15 agent files (path-prefix substitution).

---

### Req. 13 — Agent memory

**Decision:** `.claude/agent-memory/<agent>/` (top-level, not per-review) with sub-organization by **theme** rather than per-paper or per-domain alone:

```
.claude/agent-memory/
├── README.md
├── _global/
│   └── orchestrator.md       # cross-paper lessons (e.g. "phase 2 fixer pass usually catches this")
├── literature_searcher/
│   ├── backends.md           # rate limits, query templates that work
│   ├── domains/
│   │   ├── ml.md
│   │   └── physics.md
│   └── known-papers.md       # bib keys we've resolved before, with canonical record
├── checker_literature/
│   ├── known-miscites.md     # "Bengio 2003 is often cited with wrong year"
│   └── domains/<domain>.md
├── checker_domain/
│   └── domains/<domain>.md
├── claim_extractor/
│   └── patterns.md           # common claim-extraction edge cases
└── arbiter/
    └── precedents.md         # past PASS/ITERATE/ESCALATE rationales
```

**Update protocol:**
- **Read at start.** Each agent's body (post-frontmatter) includes a "Memory" section that names exactly which files to read first. The agent's slash-command-issued prompt prefixes "Before starting, read your memory files at .claude/agent-memory/<agent>/...".
- **Write at end.** After completing its task, the agent appends a dated entry under `## YYYY-MM-DD <slug>` to the relevant memory file. Append-only. Never delete or rewrite past entries.
- **Format.** Each entry: 1-3 bullets max, lesson framed as "When you see X, prefer Y because Z." No paper-specific facts (those go in the review's artifacts, not memory).
- **Domain detection.** The agent infers domain from `paper/paper.meta.json` (`venue` field) and chooses a `domains/<domain>.md` file; if the domain is new, it creates the file.

**Staleness handling (the "smart" part):**
- Each entry has a `## YYYY-MM-DD <slug>` header. When reading, the agent considers entries older than 6 months "stale" and weights them less.
- Conflicting notes: the orchestrator runs a quarterly (manual, via `/loop` or scheduled) `/consolidate-memory` command that reads each memory file and asks Claude to deduplicate / reconcile / mark superseded entries. Out of scope for this rework but stub in `.claude/agent-memory/README.md` as a future skill.
- The orchestrator surfaces relevant memory to each dispatch by including the file paths in the dispatch prompt — let the agent read them itself rather than the orchestrator paraphrasing.

**Rejected:**
- Per-review memory (`reviews/<slug>/phase<N>/agents/<role>/memory.md`) — defeats the cross-paper-learning goal.
- Single shared `MEMORY.md` — becomes a context-blowing dumping ground.
- Per-domain only (no per-agent dirs) — mixes concerns; checker_literature and checker_domain learn very different things about the same domain.
- Auto-write on Stop hook — too coarse; only the agent knows what to write.

**Open Q:** how big do these files get before we need to summarize? Probably not an issue in the first 50 reviews; revisit then.

**Files:** `.claude/agent-memory/README.md`, `.claude/agents/_shared/memory_protocol.md`, every agent body gets a "Memory" section.

---

## 4. Risks & gotchas

1. **`make demo` regression.** The most-likely casualty. After Phase A, `scaffold_review.py` outputs a different tree shape (no symlinks). Mitigation: `make demo` is the smoke test for every PR. Add it to a `make ci` target if helpful.
2. **`reviews/test-1`.** Dead, broken symlinks to `/afs/cern.ch/...`. Recommend deleting in Phase A. (`reviews/paper_mistakes0` has user-home symlinks that are real but won't work for anyone else — also a candidate for deletion or migration.)
3. **In-progress reviews.** If anyone has a partly-completed review when this lands, their CLAUDE.md will reference symlinks that no longer exist. Mitigation: `src/migrate_review.py` rewrites a review's CLAUDE.md and prunes obsolete symlinks. Document in upgrade notes.
4. **Harness uncertainty.** Three things I cannot verify without running:
   - `isolation: "worktree"` for nested parallel subagents.
   - PostToolUse hooks blocking/surfacing errors for agent self-correction.
   - Per-Task model selection from a runtime-loaded profile.
   - SubagentStop hook payload containing token counts.
   Each has a stated fallback. Build Phase A-D first; verify these three before committing to Phase E-F design.
5. **MCP package selection.** Don't wire arbitrary MCPs without confirming maintenance + auth requirements.
6. **Schema drift.** `graph_schema.md` (prose) and `graph_schema.json` (formal) can diverge silently. Mitigation: a single test (`tests/test_schema_in_sync.py`?) that asserts the demo graph passes the JSON schema; failure forces a manual reconciliation.
7. **Memory pollution.** A bad lesson written to `.claude/agent-memory/checker_literature/known-miscites.md` propagates forever. Mitigation: append-only + dated entries make manual cleanup possible; quarterly consolidation pass.
8. **CLAUDE.md ancestor loading.** With `.claude/` at repo root and `reviews/<slug>/CLAUDE.md` as a per-review file, the harness should ancestor-load both. Verify; if it doesn't, we read both explicitly in slash commands.
9. **Permission-prompt fatigue.** Every new Bash invocation is a prompt unless allowlisted. After Phase A-D, run `/fewer-permission-prompts` against a real review transcript and tighten the allowlist.

---

## 5. Decisions to surface to the user before implementation

I am **opinionated by default** below. Push back where you disagree.

1. **Delete `reviews/test-1` and `reviews/paper_mistakes0`** as part of Phase A. They're dead. (Default: yes, delete both. Push back if `paper_mistakes0` has work you want to keep — in which case, run `migrate_review.py` on it instead.)

2. **`src/agents/` goes away entirely** (replaced by `.claude/agents/`). No back-compat stub beyond a one-release pointer README. (Default: yes.)

3. **No per-review symlinks** — `methodology/conventions/agents/literature_bank` references go through absolute repo-root paths. (Default: yes. Cleaner. Trade-off: a review dir is no longer self-contained if you tar it up.)

4. **Default profile = `balanced`** (opus for arbiter+orchestrator, sonnet for reviewers + 3 hard checkers + literature_searcher + strategist + fixer, haiku for the rest). (Default: this. Push back if you want all-sonnet for predictability.)

5. **Memory at `.claude/agent-memory/<agent>/`** (top-level, theme-organized, append-only with date headers). (Default: this. Push back if you want per-domain instead of per-agent as the top-level split.)

6. **MCPs:** ship `.mcp.json` with arXiv + Semantic Scholar but Phase-F starts with "verify which packages." (Default: yes. Push back if you want to defer MCPs entirely to a later iteration.)

7. **Phase commands stop before ADVANCE** — `/phase1` runs through COMMIT and pauses; user issues `/phase2`. (Default: yes, mirrors current methodology. Push back if you want auto-advance with a `--auto` flag.)

8. **Repo-root `CLAUDE.md`** is the orchestrator; per-review `CLAUDE.md` is a thin paper-meta pointer. (Default: yes. Push back if you want per-review to remain authoritative — but then no-cd is much harder.)

9. **Token monitoring tier mix:** ship Tier 1 (metadata) + Tier 3 (self-estimate) immediately; defer Tier 2 (hook-payload tokens) until verified. (Default: yes.)

10. **Worktree isolation:** declare it, verify, fall back if needed. (Default: yes, with the disjoint-paths fallback documented.)

11. **`<important if="...">` conditional tags:** use them; fall back to unconditional `<important>` if harness doesn't support `if`. (Default: yes.)

12. **Hooks block on validation failure** (vs. log-only): want them to block + return error so the agent self-corrects. Verify harness; if log-only, ship as informational and surface in review. (Default: blocking, with informational fallback.)

13. **Add `jsonschema` and `bibtexparser` to `requirements.txt`** for the validators. (Default: yes.)

---

## 6. Effort summary

| Phase | Description | Effort | Depends on |
|---|---|---|---|
| A | Subagents + repo-root CLAUDE.md + scaffold rewrite | ~6h | — |
| B | Slash commands + no-cd | ~3h | A |
| C | Conventions → Skills | ~3h | A |
| D | Hooks + JSON schema + bib validator | ~6-8h | A, C |
| E | Profiles + token monitoring | ~7h | A, B |
| F | MCP + worktree isolation | ~3h | A |
| G | Memory subsystem | ~3-4h | A |

Total: roughly 1.5-2 days of focused work; spread over 3-5 days at hackathon pace with the verification interruptions for the 4 harness-uncertain items.

**Recommended ship order:** A → B → C → D in series; E, F, G can ship in any order after A and (for E) B.
