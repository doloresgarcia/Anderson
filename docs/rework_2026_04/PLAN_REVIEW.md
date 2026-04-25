# PLAN_workflow_rework.md — Review

Reviewed against repo state at `workflow_rework@c5d9160`, plus the official
Claude Code docs (sub-agents, skills, hooks, slash-commands at
`code.claude.com/docs/en/...`).

---

## 1. TL;DR verdict

**SHIP WITH CHANGES.** The architecture is broadly right — `.claude/agents/` as
source of truth, repo-root `CLAUDE.md`, slash commands taking a slug — and the
phase ordering is sane. But there are **three blocking bugs** the user must hear
about before approval, all rooted in unverified harness assumptions:

1. The slash-command argument syntax in §2 Phase B is wrong: `$1` is the
   *second* positional arg (0-indexed). The slug substitution will silently
   point at the wrong value.
2. The plan never says where the orchestrator actually runs. Per docs,
   **subagents cannot spawn other subagents**, so the orchestrator *must* be
   the main session, not a subagent itself. Phase F's worktree question is
   therefore moot (no nested-parallel case exists), but the plan's design has
   to acknowledge this and stop talking about "the orchestrator that's itself
   inside a Task" (§F).
3. Claude Code already ships a built-in `memory` frontmatter field with three
   scopes (`user`/`project`/`local`) and an auto-curated `MEMORY.md`. The plan
   reinvents this from scratch in Phase G. By happy accident the path the
   built-in chooses for `project` scope is *exactly* `.claude/agent-memory/<name>/`
   — but the plan doesn't know that, so its hand-rolled "Memory" sections in
   each agent body double up with the harness behavior.

There are also several over-engineered pieces (3 model profiles, 7 slash
commands, conventions-as-skills wrapper indirection) that should be cut for v1.

Estimated rework before implementation: 2–3 hours of edits to the plan
document, no code yet.

---

## 2. Critical findings (must fix before implementation)

### C1. Slash-command `$1` is wrong; the slug is `$0` (or use `$ARGUMENTS`)

**Plan §2 Phase B**, every command body:

```
Active review: $1 (resolves to reviews/$1/).
…
reviews/$1/CLAUDE.md
…
src/methodology/03-phases.md (phase 1 section)
```

Per the Claude Code skills/commands docs (commands and skills are unified —
files in `.claude/commands/` use the same substitutions as skills):

> `$N` Shorthand for `$ARGUMENTS[N]`, such as `$0` for the first argument or
> `$1` for the second.

So `/phase1 my-paper` makes `$0 = my-paper` and `$1` is empty. Every command
that uses `$1` for the slug will resolve `reviews//CLAUDE.md`. This will look
like it works on the very first dispatch (no error from path resolution) and
then silently misroute every subsequent file write.

**Fix:** rewrite all 7 commands to use `$ARGUMENTS` (when there is exactly one
arg, this is unambiguous and matches the existing examples in the docs) or use
`$0`. Recommend `$ARGUMENTS` for `/phase1 <slug>` style; use `$0`/`$1`/`$2`
only for `/scaffold <slug> <source>` and `/review-phase <slug> <N>` and
`/fix <slug> <phase> <category>`.

Also: the plan should declare named args via the frontmatter `arguments:` field
so the substitutions are self-documenting. Example:

```yaml
---
description: Run phase 1 (ingest & map)
argument-hint: <slug>
arguments: [slug]
---
…use reviews/$slug/…
```

### C2. The orchestrator must run as the main session — subagents cannot nest

Plan §1 places the orchestrator in repo-root `CLAUDE.md` and §2 Phase B has
slash commands that "dispatch phase-1 subagents". §F discusses worktree
isolation "when the orchestrator is itself a slash-command-driven session, not
a subagent" — that distinction matters.

The docs are explicit:

> Subagents cannot spawn other subagents. If your workflow requires nested
> delegation, use Skills or chain subagents from the main conversation.

Implications the plan must spell out:

- The orchestrator *is* the main `claude` session. It calls subagents via
  the Agent (formerly Task) tool. None of the slash commands can be defined
  with `context: fork` or run "as a subagent."
- Phase F's "Plan B" fallback for `isolation: worktree` is the only relevant
  worry: worktree isolation works fine because the parent (main session) calls
  parallel subagents. There is no "nested parallel" case to verify.
- Reviewers (critical/constructive/arbiter) likewise must be dispatched by the
  main-session orchestrator, not by another subagent. The current methodology
  says "EXECUTE → REVIEW" within a phase — fine, but this is sequential
  dispatch from the main session, not a nested call.
- The `fixer` pattern (Category-A finding triggers a `fixer` re-dispatch) also
  needs to be from the main session, not from `critical_reviewer`.

**Fix:** add a one-paragraph "Architecture invariant" to §1 stating that the
orchestrator is the main session and that all subagent dispatch is flat. Cut
or rephrase §F's "the orchestrator that's itself inside a Task" framing.

### C3. The plan duplicates Claude Code's built-in agent-memory feature

Plan §1 invents `.claude/agent-memory/<agent>/...md` with a Memory protocol,
read-at-start / write-at-end conventions, and per-agent body sections.

The docs:

> The `memory` field gives the subagent a persistent directory that survives
> across conversations. … Choose a scope based on how broadly the memory
> should apply: `user` → `~/.claude/agent-memory/<name-of-agent>/`,
> `project` → `.claude/agent-memory/<name-of-agent>/`, `local` →
> `.claude/agent-memory-local/<name-of-agent>/`. … The subagent's system
> prompt includes instructions for reading and writing to the memory
> directory. … The subagent's system prompt also includes the first 200
> lines or 25KB of `MEMORY.md` … with instructions to curate `MEMORY.md` if
> it exceeds that limit.

Two consequences:

(a) The path the plan picks (`.claude/agent-memory/<agent>/...`) collides
exactly with the harness's built-in `project` scope. If the plan also adds
`memory: project` to a subagent's frontmatter, the harness will own that
directory — write `MEMORY.md`, auto-truncate, and inject the first 25KB into
the subagent's system prompt automatically. The plan's "agents append-only,
date-headed" protocol then either fights the harness or duplicates it.

(b) The plan's per-agent "Memory" body sections (showing literal "read these
files first", "write a YYYY-MM-DD entry") are unnecessary if `memory:` is set
— the harness already does this. They become dead weight and a maintenance
hazard (two sources of memory protocol).

**Fix options (pick one before implementation):**

- **Option A (recommended): adopt the built-in `memory` field.** Add
  `memory: project` to the 4 agents that need persistent learning
  (`literature_searcher`, `checker_literature`, `checker_domain`, `arbiter`).
  Drop the custom `_shared/memory_protocol.md`. Drop the `domains/<domain>.md`
  hierarchy — the harness only manages a flat `MEMORY.md` and supporting
  files. Re-scope §G to "write `.claude/agent-memory/<agent>/MEMORY.md`
  starter content + a one-paragraph note in each opted-in agent body telling
  it to consult/append memory."
- **Option B: opt out of the built-in.** Don't set `memory:`, document that
  we manage the directory ourselves, and warn the implementer to never enable
  the field on these agents (else conflict). This loses the auto-injection
  benefit and requires every dispatch prompt to include "read your memory
  files first" — which is what the plan already does, just hand-rolled.

The plan must pick one; the current design accidentally does both.

---

## 3. Important findings (should fix)

### I1. `<important if="condition">` is not a documented harness feature

Plan §3 Req. 6 + §5 #11 use `<important if="literature_searcher_just_finished">`
as if the harness understood conditional inclusion. I searched the public docs
(sub-agents, skills, hooks, memory, slash-commands pages) and found no `if=`
attribute on any tag. The "best-practices repo" the plan refers to in §5 is not
cited, and `<important>` is at best a Markdown convention, not parsed by the
harness.

**Fix:** drop `if=` entirely. Use plain `<important>` for the always-on rules
and rely on the agent body's own structure for context-conditional emphasis
(e.g. put the `LITERATURE.md`-specific rule in the literature_searcher agent
body, not in the orchestrator CLAUDE.md). Update §3 Req. 6 to remove the
"verify the harness supports it" sentence and the conditional examples.

### I2. SubagentStop payload has no documented token-count field

Plan §2 Phase E Tier 2 hopes for `input_tokens`/`output_tokens` in the hook
payload. Per the hooks docs, `SubagentStop` has no detailed schema published
and the only documented common fields are `session_id`, `transcript_path`,
`cwd`, `agent_id`, `agent_type`. `PostToolUse` exposes `duration_ms` but no
token counts.

The plan's Tier-1 + Tier-3 fallback design correctly anticipates this. Two
concrete edits:

- In §3 Req. 11, demote Tier 2 to "currently undocumented; not part of v1."
- In §2 Phase E, point implementers at `transcript_path`: subagent transcripts
  live at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`
  per the sub-agents docs. The aggregator (`src/token_log.py`) can read the
  JSONL files and sum `usage.input_tokens` / `usage.output_tokens` from API
  response messages — this is the actual "ground-truth" path the plan
  speculates about under Req. 11's "Open Q."

That removes the Tier-2 / Tier-3 ambiguity and gives a concrete way to get
real numbers.

### I3. `.claude/commands/` and `.claude/skills/` are now the same thing

Plan §1 lists both. Per the skills docs:

> Custom commands have been merged into skills. A file at
> `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md`
> both create `/deploy` and work the same way.

This isn't a bug per se — both paths still work — but keeping them separate
adds a second mental model for no benefit. Recommend either:

- Use `.claude/commands/` for the 7 phase commands (tasks, user-invoked) and
  `.claude/skills/` for the 6 conventions (reference content, model-invoked).
  Document this split explicitly in §1 so future maintainers don't ask why
  we have both.
- Or move everything to `.claude/skills/`, with the phase commands marked
  `disable-model-invocation: true` so they only fire when the user types
  `/phase1`. This is the harness's recommended path for new work.

### I4. "Conventions as skills" is over-indirected for v1

Plan Phase C wraps each `src/conventions/<name>.md` in a thin
`.claude/skills/<name>/SKILL.md` that "@-includes" the source file. The plan
also notes (Phase C, "Open question") it doesn't know whether skills auto-load
on description match. Per the skills docs they do — descriptions are always
in context, full body loads on invocation — so the wrapper layer mostly works.

But: the SKILL.md files add a second source of truth (the description and
when-to-use copy) for content that lives in `src/conventions/`. Two failure
modes:

- A checker reads the SKILL summary and skips loading `src/conventions/error_categories.md`
  because the summary "looks complete." Severity-order subtleties get missed.
- The wrapper's description gets stale relative to the source.

For v1, recommend: skip the skills wrapper entirely. The conventions are
small (~5 files, total <1500 lines per `wc -l`). Reference them directly from
each agent body's "Reads:" section the way the current `src/agents/*.md`
specs already do. Add the skills layer in v2 if context bloat becomes a
problem.

If keeping the skills wrapper, drop `verification-conventions/` (the source
file is a placeholder) and `confidence-scale/` (one paragraph — not worth a
skill). That cuts to 4 skills, two of which (`error-categories`,
`graph-schema`) are actually plausible to extract.

### I5. 3 model profiles is over-engineered; ship 1 default + an env override

Plan §3 Req. 10 ships `all-opus.json`, `balanced.json`, `fast-cheap.json` plus
a `.active_profile` file plus an `ANDERSON_PROFILE` env var. For a one-person
hackathon project where the user said "don't gold-plate", this is too much.

Recommend:

- Ship one `balanced` profile (the proposed default) committed as
  `.claude/profiles/balanced.json`. Document the schema. Done.
- Per-agent override: each `.claude/agents/<name>.md` frontmatter has a
  static `model:` field. The harness already supports `model: inherit`, model
  alias, or full ID. The orchestrator does NOT need a runtime profile picker
  for v1.
- If the user wants to flip everything to Opus for one expensive run, they
  override `model:` in agent frontmatter for that session, or set
  `CLAUDE_CODE_SUBAGENT_MODEL` (which the docs say takes top priority in the
  resolution order).

This cuts the "verify per-Task model selection from a runtime-loaded profile"
open question (Plan §4 risk #4) entirely. Static frontmatter works today,
fully documented. Add the runtime profile picker in v2 once the actual
workflow is exercised.

### I6. `verifier.md` is referenced in two convention files; "safe to delete" is over-confident

Plan §1 says verifier.md is "deprecated, can finally be deleted" without check.
`grep -rn verifier src/`:

- `src/agents/verifier.md` — the file itself, marked DEPRECATED.
- `src/conventions/graph_schema.md:48` — table row referring to "verifier" as
  the source of `verdict_confidence`.
- `src/conventions/error_categories.md:134` — historical note "These five
  checkers replace the generic verifier agent."

Deleting the file is safe; the two convention-file references are just
documentation about what was replaced. But the plan should say "delete the
file; leave the explanatory references in conventions/ alone (they document
the migration for future readers)."

### I7. Phase-template handling is unspecified

The repo has `src/templates/phase1_claude.md`, `phase2_claude.md`,
`phase3_claude.md`. They are referenced by `src/scaffold_review.py` lines
169–173 (`render_template(TEMPLATES / f"{phase}_claude.md", slots_phase)`).
The plan never mentions them by name. Three options:

(a) Delete them — phase orchestration is now driven by `.claude/commands/phase{N}.md`
    plus the orchestrator at repo-root CLAUDE.md.
(b) Move them under `src/methodology/` as phase-specific orchestration prose
    (which is what they actually are — they explain "execution order" per
    phase and "Phase-N specific gotchas").
(c) Keep as templates, drop the per-review CLAUDE.md generation since the new
    per_review_claude.md is "thin."

Recommend (a) + fold the "Phase-N specific gotchas" sections into
`src/methodology/03-phases.md` (or an existing phase file) so the gotchas
aren't lost. Add a one-line item to Phase A "delete src/templates/phase{1,2,3}_claude.md
after merging phase-specific gotchas into methodology/03-phases.md."

### I8. `make demo` interaction with the new scaffold output is not actually tested

Plan §0 declares `make demo` the smoke test "we never break", and §2 Phase A
asserts it still works because phase-3 scripts read `reviews/<slug>/...`
paths. But the Makefile (line 45) calls `python3 src/scaffold_review.py
--text demo/paper.txt --slug __demo__ --force` then copies `demo/CLAIMS.md`
into `reviews/__demo__/phase1/outputs/CLAIMS.md`. The phase-3 scripts read
those copied files, not the symlinks — so dropping the symlinks doesn't break
`make demo`.

**However**: the new `scaffold_review.py` will now also need to (a) write the
new thin per-review CLAUDE.md (not the current `root_claude.md` template) and
(b) NOT create methodology/conventions/agents/literature_bank symlinks.
`make demo` will succeed even with broken Claude Code wiring, because the
demo doesn't exercise the orchestrator.

**Fix:** add a separate smoke target, `make demo-orchestrator` or a CI script,
that actually launches `claude` non-interactively against the demo and
verifies a phase-1 dispatch lands. Without it, the smoke test only validates
the deterministic Python path. Otherwise call out in §0 that `make demo`
proves the Python pipeline only, not the agent harness.

### I9. Permission allowlist is missing some Bash invocations the agents will need

Plan §3 Req. 2 lists allowlist entries. Missing:

- `Bash(git status:*)`, `Bash(git diff:*)`, `Bash(git log:*)`, `Bash(git add:*)`,
  `Bash(git commit -m:*)` — listed, good.
- `Bash(git status --porcelain:*)` — used by `stop_commit_nudge.py`. The
  pattern `Bash(git status:*)` should match this; but the hook script runs
  out-of-band as a hook (no permission needed for the hook subprocess
  itself).
- Missing: `Bash(make demo:*)`, `Bash(make graph:*)`, `Bash(make stats:*)`,
  `Bash(make highlight:*)`. Plan has only `Bash(make *)` which works.
- Missing: `Bash(uvx:*)` — needed if MCPs are launched via `uvx`. Hooks
  shouldn't require this since `.mcp.json` handles process spawning, but
  worth confirming.
- Missing read-only Bash that scaffold_review.py will need (the orchestrator
  will call it): plan has `Bash(python3 src/*.py:*)` ✅.
- Missing: `Read(literature_bank/**)` — `Read(**)` covers it but worth
  double-checking literature_bank stays unsymlinked-but-readable from
  reviews/<slug>/ via absolute path.

Run `/fewer-permission-prompts` (the bundled skill) once after Phase A as
the plan §3 Req. 2 "Open Q" already suggests. Make this explicit in Phase B's
"acceptance criteria."

### I10. paper_mistakes0 has a real review that will be clobbered

Plan §0 + §4 #2 + §5 #1 propose deleting `reviews/paper_mistakes0`. From
`ls -la`, that review's symlinks point at
`/afs/cern.ch/work/m/mgarciam/...` — not the user's home as the plan claims;
this is a CERN AFS path. The user (Oscar, oscarbarrera@fas.harvard.edu) likely
collaborated with another user (mgarciam). The CLAUDE.md and any phase
artifacts there represent real work product that will be lost.

**Fix:** do NOT propose deleting `paper_mistakes0`. Migrate it instead:

- Replace its symlinks with absolute paths to *this* repo's `src/agents/`,
  `src/conventions/`, etc. before Phase A. This is a one-shot fix-up
  — keep the existing `paper/`, `phase{1,2,3}/`, `prompt.md`, and any
  intermediate artifacts.
- Or: just delete the dangling symlinks (their targets are unreachable from
  this machine) and leave the rest alone. The new scaffold doesn't need
  them.

The `migrate_review.py` proposed in §3 Req. 5 is the right tool. Make it a
hard prerequisite for Phase A merge, not an afterthought.

`reviews/test-1` is fair game — same dead AFS symlinks, no `prompt.md`
content suggesting work in flight.

---

## 4. Minor / nice-to-haves

- §1 file tree says `.claude/status.md` is "rendered by hooks for `claude --status`".
  No such command/file is documented. Drop it.
- §1 `_shared/executor_contract.md` and `_shared/memory_protocol.md` — the
  plan should clarify these are *included* into other agent bodies (how?
  manual copy-paste? `@`-include? they're not subagents themselves). Probably
  reference them by relative path from the agent body and let the harness
  resolve `@./_shared/...` mentions. Verify before relying.
- The 7 slash commands feel like 5: `/scaffold`, `/phase1`, `/phase2`,
  `/phase3`, `/render`. `/review-phase` and `/fix` could be inline operations
  the orchestrator decides on automatically (the methodology already says the
  orchestrator runs review and fixer in CHECK). Cut those two for v1.
- Frontmatter `tools:` syntax: the docs use space-separated *or* comma-separated
  *or* YAML list. Plan uses comma-separated. Fine, but pick one and be
  consistent across all 15 agents.
- `tools:` in plan includes `Bash(python3 src/render_graph.py:*)` for
  graph_builder. The harness syntax for tool-permission specifiers in
  `tools:` is the same as `permissions.allow` in settings, but it's worth
  testing this once — the docs show `tools: Read, Glob, Grep` style without
  `Bash(...)` parameter restriction in the subagents page. The
  parameter-restriction syntax is documented for permissions, not necessarily
  for `tools:`. If the harness chokes, fall back to `tools: Bash` and rely on
  `settings.json`'s `permissions.allow` to constrain.
- §3 Req. 13's "consolidate-memory" command (quarterly cleanup) is explicitly
  marked out of scope but stubbed — fine, but don't mention it in `.claude/agent-memory/README.md`
  unless you intend to ship at least the stub.
- `requirements.txt` add: plan says `jsonschema>=4`, `bibtexparser>=1.4`. Note
  `bibtexparser 2.x` exists with a different API; pin to v1 explicitly:
  `bibtexparser>=1.4,<2`.
- Plan §2 Phase E justification of `balanced` profile: "haiku for unreferenced
  + ambiguous checkers" — these checkers need to read the whole paper and
  judge nuance. Haiku's reading comprehension on long technical text may not
  be sufficient. Recommend bumping ambiguous to sonnet at minimum; verify
  unreferenced empirically (citation-density check is more mechanical).
- §3 Req. 7 hooks: `commit_prefix.py` infers phase from cwd. With the
  no-cd workflow (Req. 12), the cwd is always repo root, so this hook can
  no longer infer phase from path. It would need to read recent git
  diff/status to guess which phase's outputs changed. Either drop the hook,
  or have the orchestrator pass phase via env var (`ANDERSON_CURRENT_PHASE`)
  set before each commit Bash call.

---

## 5. Harness-uncertainty resolution

| Open Q in plan | Doc finding | Verdict |
|---|---|---|
| `isolation: worktree` for nested parallel dispatches | Documented frontmatter field on subagents. **But subagents cannot spawn other subagents at all** — there is no nested case. | **Primary plan works** for the flat case (orchestrator → N parallel checkers). Drop the "nested" framing. |
| PostToolUse blocks + surfaces error to agent | Yes — `decision: "block"` + `reason` (shown to Claude) + optional `additionalContext`. Block happens *after* tool execution; for *before*, use PreToolUse. | **Primary plan works.** For graph/bib validators, PostToolUse is correct (the file already exists; we want to prompt the agent to fix it). |
| Per-Task runtime model selection from profile JSON | Per-invocation `model` parameter is supported in the resolution order: `CLAUDE_CODE_SUBAGENT_MODEL` env > per-invocation > frontmatter > main. So the orchestrator can pass `model:` per Agent dispatch. **But this requires writing custom dispatch prompts that include model-name strings** — the harness doesn't load profile JSON for you. | **Primary plan works** but is more code than the user needs for v1. Recommend dropping profiles and using static frontmatter `model:` per agent (see I5). |
| SubagentStop payload includes token counts | No documented token fields on SubagentStop. Common fields only: `session_id`, `transcript_path`, `cwd`, `agent_id`, `agent_type`. | **Primary plan blocked, use fallback.** Tier 1 (metadata) + Tier 3 (self-estimate) work. Better still: post-hoc parse `transcript_path` JSONL files for `usage.input_tokens` (see I2). |
| Skills auto-load when description matches | Yes — descriptions are always in context up to the listing budget; full body loads on invocation. | **Primary plan works.** No "agent invokes skill" boilerplate needed. |
| `<important if="...">` conditional tags | No reference in docs. Likely aspirational. | **Plan blocked, drop the feature.** Use plain `<important>` (or just bold/heading) and put context-conditional content in agent bodies (see I1). |
| Slash-command argument syntax | `$ARGUMENTS` (full string), `$ARGUMENTS[N]` or `$N` (0-indexed). `$0` = first arg, `$1` = second. | **Plan has a bug** — `$1` is the *second* arg, not the slug. See C1. |

Bonus discovery the plan didn't ask about: **subagents have a built-in
`memory: user|project|local` field** with auto-curated `MEMORY.md`. The plan
reinvents this; see C3.

---

## 6. Per-decision verdicts

| # | Decision (plan §5) | Verdict | Reasoning |
|---|---|---|---|
| 1 | Delete `reviews/test-1` and `reviews/paper_mistakes0` | **PUSH BACK** on paper_mistakes0 — symlinks point to a *collaborator's* CERN AFS path, not the user's. May contain real shared work. Migrate it instead (I10). test-1 is fine to delete. |
| 2 | `src/agents/` goes away entirely | Accept. Stub README is fine. |
| 3 | No per-review symlinks | Accept. Trade-off (review dirs no longer self-contained as tarballs) is acceptable for hackathon scope. |
| 4 | Default profile = `balanced` | Flag — see I5. Ship one profile only, not three. Profile JSON is over-engineered for v1. |
| 5 | Memory at `.claude/agent-memory/<agent>/` | **PUSH BACK** — see C3. Use the built-in `memory: project` field; the path collides with the harness's auto-managed location. |
| 6 | Ship `.mcp.json` with arXiv + Semantic Scholar | Accept, with the plan's own caveat ("verify which packages"). The ones the plan picked (`mcp-server-arxiv`, `mcp-server-semanticscholar`) need to be confirmed real and maintained. |
| 7 | Phase commands stop before ADVANCE | Accept. Matches current methodology and gives the user a natural pause point. |
| 8 | Repo-root `CLAUDE.md` is the orchestrator | Accept — but spell out the "main session, no nesting" invariant (C2). |
| 9 | Token monitoring tier mix | Accept Tier 1 + Tier 3; refine Tier 2 to "post-hoc transcript parsing" instead of "depends on hook payload" (I2). |
| 10 | Worktree isolation: declare + verify + fall back | Accept. Per docs the field exists; the only test is a real run. Include the disjoint-paths fallback as a code comment, not a separate code path. |
| 11 | `<important if="...">` conditional tags | **PUSH BACK** — not a real feature (I1). Drop `if=`. |
| 12 | Hooks block on validation failure | Accept — the docs confirm this works for both Pre and Post tool use hooks. |
| 13 | Add `jsonschema` and `bibtexparser` to requirements.txt | Accept, pin `bibtexparser<2` (minor #5). |

---

## 7. Recommended changes to the plan (concrete edits before user reads it)

Apply these edits to `PLAN_workflow_rework.md` before requesting approval:

- **§1 file tree** — drop `.claude/status.md`. Add explicit comment that
  `.claude/commands/` and `.claude/skills/` are functionally equivalent per
  the harness; we keep both for organizational separation (commands = task
  triggers, skills = reference material).
- **§1** — add a new "Architecture invariant" subsection: "The orchestrator
  is always the main `claude` session. Subagents do not spawn subagents
  (per Claude Code subagents docs). All Agent-tool dispatches — checkers,
  reviewers, fixer, arbiter — originate from the main session." (C2)
- **§2 Phase A** — add bullet: "Delete `src/templates/phase{1,2,3}_claude.md`
  after folding the 'Phase-N specific gotchas' sections into
  `src/methodology/03-phases.md`." (I7)
- **§2 Phase A** — change `verifier.md` bullet to "delete `src/agents/verifier.md`;
  leave the explanatory references in `src/conventions/{graph_schema,error_categories}.md`
  untouched (they document the migration for future readers)." (I6)
- **§2 Phase A "Could break"** — replace the "delete reviews/test-1" guidance
  with: "delete `reviews/test-1` (truly dead). For `reviews/paper_mistakes0`,
  run `migrate_review.py` to swap the dangling AFS symlinks for absolute
  paths into this repo and preserve the existing artifacts. Do NOT delete
  this review — its symlinks point at a collaborator's host." (I10)
- **§2 Phase B** — replace every `$1` with `$ARGUMENTS` (one-arg commands)
  or with the correct 0-indexed `$0` (multi-arg commands like
  `/scaffold $0 $1`, `/review-phase $0 $1`, `/fix $0 $1 $2`). Add explicit
  named `arguments:` frontmatter to all 7 commands. (C1)
- **§2 Phase C** — either downsize to 2 skills (`error-categories`,
  `graph-schema`) or drop the layer entirely for v1 and reference
  `src/conventions/*.md` directly from each agent body. State the choice
  and the reason. (I4)
- **§2 Phase D** — `commit_prefix.py`: note that with no-cd, cwd-based phase
  inference no longer works. Either remove the hook, or document that the
  orchestrator must export `ANDERSON_CURRENT_PHASE` before each `git commit`
  Bash call and the hook reads that. (Minor)
- **§2 Phase E** — cut `all-opus.json` and `fast-cheap.json`. Ship one
  `balanced.json` only. Replace the runtime-profile-resolution machinery
  with static `model:` in each agent's frontmatter, plus a one-paragraph
  "to flip everything to opus, set `CLAUDE_CODE_SUBAGENT_MODEL`." (I5)
- **§2 Phase E (token monitoring)** — replace the Tier-2 paragraph with:
  "Tier 2 (preferred when feasible): post-hoc parse `transcript_path` JSONL
  files at `~/.claude/projects/{project}/{sessionId}/subagents/agent-*.jsonl`
  for `usage.input_tokens` and `usage.output_tokens` from API response
  records. `src/token_log.py` reads these. The SubagentStop hook payload
  itself does not currently expose token counts." (I2)
- **§2 Phase F** — drop the "the orchestrator is itself inside a Task"
  framing. Worktree question collapses to "do parallel subagents from the
  main session work? Yes per docs; verify with a real dispatch." (C2)
- **§2 Phase G** — rewrite to: "Adopt the harness's built-in `memory:
  project` field on `literature_searcher`, `checker_literature`,
  `checker_domain`, `arbiter`. Seed `.claude/agent-memory/<agent>/MEMORY.md`
  with starter content per agent. Drop `_shared/memory_protocol.md` and
  drop per-agent 'Memory' body sections — the harness injects MEMORY.md
  automatically." Also drop the `domains/<domain>.md` hierarchy (the
  harness manages a flat `MEMORY.md`). (C3)
- **§3 Req. 6** — drop conditional `if=` examples; use plain `<important>`.
  Move literature/verification-specific rules into the relevant agent
  bodies, not the orchestrator file. (I1)
- **§3 Req. 11 "Open Q"** — remove (the transcript-parsing answer is
  definitive; no spike needed).
- **§5 Decisions** — apply the per-decision verdicts (§6 above) directly so
  the user sees the recommended position, not the original "default: yes."
- **§4 Risks** — add: "10. `paper_mistakes0` is a real collaborator review;
  symlinks must be migrated, not deleted." Add: "11. Slash command
  argument syntax is 0-indexed `$0`/`$1`/.../`$ARGUMENTS`; an off-by-one
  in any command will silently misroute file writes."
- **§6 Effort summary** — adjust phase E down to ~3h (no profiles,
  transcript-parsing logger). Net total drops to ~1–1.5 days.

---

## 8. Re-ordered or rescoped phases

Suggested re-scoping (the current order is fundamentally correct):

- **Phase A** (foundation, ~5h) — same as plan, plus the
  `paper_mistakes0` migration (I10), plus deleting phase{1,2,3}_claude.md
  templates after folding their gotchas (I7). Also: write a tiny
  `tests/test_demo_smoke.sh` that runs `make demo` and checks the four
  outputs exist; gate Phase B on it staying green.
- **Phase B** (slash commands + no-cd, ~2h) — same as plan with C1 + I3
  fixes. Cut `/review-phase` and `/fix` to 5 commands (minor #3).
  Acceptance criterion: run `/fewer-permission-prompts` against the
  resulting transcript and tighten settings.json.
- **Phase C** (conventions, ~1h) — descope to 2 skills max, or skip
  entirely (I4). If skipped, agent bodies just reference
  `src/conventions/*.md` directly. Phase becomes "no-op for now,
  revisit in v2."
- **Phase D** (hooks + JSON schema, ~5h) — keep, but cut `commit_prefix.py`
  if the cwd-inference workaround feels gross. validate_graph + validate_bib
  are the high-value pieces.
- **Phase E** (model + tokens, ~3h) — single profile, static `model:`
  frontmatter, transcript-parsing token logger. Much smaller than plan.
- **Phase F** (MCP + worktree, ~2h) — same as plan, but with the C2
  framing fix.
- **Phase G** (memory, ~1h) — built-in `memory: project` + seed files. Much
  smaller than plan.

Total: ~1.5 days of focused work, aligning with §6's optimistic estimate
without the speculative profile/conditional-tag/custom-memory machinery.

---

*Reviewed by Claude Opus 4.7 (1M context) on 2026-04-25 against
`workflow_rework@c5d9160`. All page references are to `code.claude.com/docs/en/...`.*
