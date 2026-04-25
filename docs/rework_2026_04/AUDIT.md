# Anderson workflow_rework — post-implementation audit

**Branch:** `workflow_rework` @ `57968eb` (six rework commits on top of pre-rework history)
**Auditor:** Claude Opus 4.7 (1M context), 2026-04-25
**Scope:** verify the six rework commits against `PLAN_REVIEW.md` (the contract)

---

## 1. Verdict

**SHIP WITH SMALL FIXES.**

Every blocking item from the revised plan landed and works. `make demo` is
green, all three hooks parse JSON / handle edge cases / exit 0 cleanly,
the schema validates the demo graph, every agent's model matches the
balanced profile, and no agent file still carries `{{slot}}` templates or
"## Prompt template" sections. The only two non-trivial issues are
documentation drift (a stale "PyMuPDF" line in README, the missing
`.claude/settings.local.json` gitignore entry) and one fragile interaction
between the `usage_log.py` fallback path and the project repo (it writes a
non-gitignored file). Everything else is cosmetic.

Headline issue: nothing is broken. The headline lever for the user is
deciding what to do with `paper_mistakes0` and `test-1`, which the rework
deliberately did not touch.

---

## 2. Critical findings (must fix before merge)

**None.** Every gate from the revised plan is met. See §6 cross-check
table.

---

## 3. Important findings (should fix soon)

### I1. `usage_log.py` fallback writes a non-gitignored file inside the repo

`/Users/oscar/Documents/Coding/Hackathon/Anderson/.claude/hooks/usage_log.py:82-88`
falls back to `.claude/agent-memory/_global/usage.jsonl` when it can't
infer slug+phase from `cwd`. That path is **not** in
`.gitignore`. After the smoke test in this audit, the file now exists
with two test records and will appear in `git status`:

```
{"timestamp": "2026-04-25T21:33:59+00:00", "agent_type": "test", ... "cwd": "/tmp"}
{"timestamp": "2026-04-25T21:37:08+00:00", "agent_type": "test", ... "cwd": "/tmp"}
```

This is the intended behavior of the hook, but every real `claude`
session in *any other project* on the machine will append to this file
too if `CLAUDE_PROJECT_DIR` happens to point here. Two concrete fixes
(pick one):

- Add `.claude/agent-memory/_global/usage.jsonl` to `.gitignore`
  (`/Users/oscar/Documents/Coding/Hackathon/Anderson/.gitignore`).
- Or change `usage_log.py:88` to write under
  `.claude/agent-memory-local/` (which would naturally be gitignored)
  and update the README at `.claude/agent-memory/README.md:33-36` to
  match.

**Reproduction:** the smoke test in §5 below already left two records in
the file; `git status` confirms it as untracked.

### I2. README still claims `requirements.txt` is "PyMuPDF" only

`/Users/oscar/Documents/Coding/Hackathon/Anderson/README.md:40`:

```
│   ├── requirements.txt           # PyMuPDF
```

`requirements.txt` now adds `jsonschema>=4,<5` and `bibtexparser>=1.4,<2`.
Update the comment; the user's first read of the README will mislead
them about the dependency surface (no warning that the validation hooks
need `pip install -r requirements.txt`).

### I3. `.claude/settings.local.json` not in `.gitignore`

The plan (PLAN_workflow_rework.md §1, §3 Req. 2) and the orchestrator
both reference `settings.local.json` as a per-user / gitignored override
file. It does not currently exist (fine — optional), but `.gitignore` at
`/Users/oscar/Documents/Coding/Hackathon/Anderson/.gitignore` does not
ignore it. If the user creates one with MCP credentials, `git status`
will offer to commit it.

Add `.claude/settings.local.json` to `.gitignore`.

### I4. Schema drift note is in `$comment`, but `graph_schema.md` still uses old vocabulary

The schema's drift acknowledgement is correct and well-placed
(`/Users/oscar/Documents/Coding/Hackathon/Anderson/src/conventions/graph_schema.json:4`).
However, `src/conventions/graph_schema.md` is in the deny-edit list of
`.claude/settings.json:71` so the rework agent intentionally couldn't
fix it. The user should either (a) loosen the deny-edit policy long
enough to reconcile the prose with `error_categories.md`, or (b) add a
`<!-- DRIFT: see graph_schema.json $comment -->` HTML comment at the
top of `graph_schema.md` so future readers find it. Currently a checker
agent reading the prose source will get an outdated `PASS/FAIL`
vocabulary with no in-file warning.

### I5. `make demo` regenerates `__demo__` but `__testaudit__` lingers

This audit ran `python3 src/scaffold_review.py --slug __testaudit__
--force` per the brief. The directory exists at
`/Users/oscar/Documents/Coding/Hackathon/Anderson/reviews/__testaudit__/`
and is **not** in `.gitignore` (only `reviews/__demo__/` is). Per the
brief I did not delete it. Two parts to clean up:

- The orchestrator should delete `reviews/__testaudit__/` before merge.
- `.gitignore` could optionally ignore `reviews/__*__/` to handle this
  pattern generically.

---

## 4. Minor / nice-to-haves

- `/Users/oscar/Documents/Coding/Hackathon/Anderson/CLAUDE.md` is 109
  lines, well within the ≤120 budget. Plain `<important>` blocks (no
  `if=`). Architecture invariant present at lines 6–13. ✓
- Settings file lists both `Bash(make:*)` (line 14) and `Bash(make *)`
  (line 15). The first is the canonical permission-spec shape; the
  second is broader. Harmless duplication but pick one.
- `/Users/oscar/Documents/Coding/Hackathon/Anderson/.claude/settings.json:43-44`
  allows `Write(.claude/**)` and `Edit(.claude/**)` — wide. The deny
  block doesn't carve out exceptions, so any subagent with Write tool
  could overwrite an agent's own `.md` definition mid-session. Consider
  scoping write access under `.claude/agent-memory/` only, since the
  harness manages MEMORY.md curation directly.
- `.mcp.json` is the deliberate empty stub
  (`/Users/oscar/Documents/Coding/Hackathon/Anderson/.mcp.json`,
  `mcpServers: {}`); matches the plan's "ship empty, fill in later"
  decision.
- Agent frontmatter `tools:` lists are comma-separated and consistent
  across all 15 files.
- The `_global/usage.jsonl` design has no rotation or size cap. Not
  urgent for hackathon scope but worth a TODO in the README.
- `src/agents/README.md` is the one-release stub the plan asked for;
  good.
- `src/templates/` is now exactly one file (`per_review_claude.md`); the
  three deleted phase templates' "gotchas" are folded into
  `src/methodology/03-phases.md` (verified line 38–43 — phase 1 gotchas
  inline). ✓
- The phase commands are 5 (`scaffold`, `phase1`, `phase2`, `phase3`,
  `render`); `/review-phase` and `/fix` from the original plan were
  cut, matching PLAN_REVIEW recommendation.
- `.claude/agent-memory/_global/orchestrator.md` mentioned in the
  original plan is **not** present (the harness only auto-injects for
  agents with `memory: project` in their frontmatter, and the
  orchestrator is the main session — so this is correct, but the
  README at `.claude/agent-memory/README.md` doesn't mention global
  notes either, which is fine).

---

## 5. Smoke test results

All commands run from `/Users/oscar/Documents/Coding/Hackathon/Anderson`.

```
# 1. JSON parse for all the new config files
python3 -c "import json; json.load(open('.claude/settings.json'))"          → OK
python3 -c "import json; json.load(open('.claude/profiles/balanced.json'))" → OK
python3 -c "import json; json.load(open('.mcp.json'))"                      → OK

# 2. Schema validation on the canonical demo graph
python3 -c "import json, jsonschema; jsonschema.validate(
    json.load(open('demo/graph.v2.json')),
    json.load(open('src/conventions/graph_schema.json')))"                  → OK

# 3. Hooks (each fed a representative payload via stdin)
.claude/hooks/validate_graph.py  → exit=0
.claude/hooks/validate_bib.py    → exit=0  (skipped: LITERATURE.md not present)
.claude/hooks/usage_log.py       → exit=0  (wrote to _global/usage.jsonl)

# 4. validate_bib.py with non-review path (false-positive check)
echo '{"tool_name":"Write","tool_input":{"file_path":"some/random/LITERATURE.md"}}' \
    | .claude/hooks/validate_bib.py  → exit=0  (correctly ignored)

# 5. make demo
make demo  → 5 outputs in reviews/__demo__/phase3/outputs/:
  STATS.md, graph.final.html, graph.final.json,
  paper.highlighted.html, paper.highlighted.pdf

# 6. make usage on the just-built demo
make usage REVIEW=reviews/__demo__  → exit=0
  USAGE.md says "no usage recorded for this review yet" — matches plan.

# 7. Per-deliverable Make targets
make graph     REVIEW=reviews/__demo__ → exit=0  (rewrote graph.final.html)
make stats     REVIEW=reviews/__demo__ → exit=0  (rewrote STATS.md, trust=58)
make highlight REVIEW=reviews/__demo__ → exit=0  (rewrote both highlighted files)

# 8. New scaffold (no symlinks, thin CLAUDE.md)
python3 src/scaffold_review.py --text demo/paper.txt --slug __testaudit__ --force
  → reviews/__testaudit__/{CLAUDE.md, prompt.md, paper/, phase1/, phase2/, phase3/}
  → no symlinks for methodology/conventions/agents/literature_bank
  → CLAUDE.md is 30 lines, points at repo-root orchestrator. ✓

# 9. Per-agent model ↔ profile cross-check (15/15 match)
   See §6 below.

# 10. Stale-template grep
grep "{{paper_slug}}|{{phase}}|## Prompt template" .claude/agents/*.md → no matches
```

---

## 6. Cross-checks (plan → delivered)

### Phase A — agents + repo-root CLAUDE.md + scaffold rewrite

| Plan requirement | File | Status |
|---|---|---|
| 15 agent files in `.claude/agents/` | `arbiter.md, checker_*, claim_extractor.md, constructive_reviewer.md, critical_reviewer.md, fixer.md, graph_builder.md, highlighter.md, literature_searcher.md, report_writer.md, strategist.md` | PASS — 15/15 |
| YAML frontmatter parses (name, description, tools, model on each) | all 15 | PASS |
| `memory: project` on exactly 4 agents | `literature_searcher`, `checker_literature`, `checker_domain`, `arbiter` | PASS — exactly the four |
| No `{{paper_slug}}` / `{{phase}}` slots | grep | PASS |
| No `## Prompt template` sections | grep | PASS |
| `_shared/executor_contract.md` present | `.claude/agents/_shared/executor_contract.md` | PASS |
| Repo-root `CLAUDE.md` ≤120 lines, plain `<important>` blocks, "main session" invariant | `CLAUDE.md` (109 lines, lines 6–13 carry invariant, no `if=`) | PASS |
| `src/templates/per_review_claude.md` thin | 1117 bytes, single template file | PASS |
| `src/scaffold_review.py` rewritten — no 4 dead symlinks | source confirms only `paper/` files copied; thin CLAUDE.md template rendered | PASS |
| Phase-template gotchas folded into `src/methodology/03-phases.md` | "Phase 1 gotchas" subsection at line 38 | PASS |
| Deprecated files gone (`src/agents/*.md` except README, `src/templates/phase{1,2,3}_claude.md`, `src/templates/root_claude.md`) | `src/agents/` contains only `README.md`; `src/templates/` contains only `per_review_claude.md` | PASS |
| README updated (no-cd workflow, slash commands) | `README.md:85-117` | PASS |
| `.claude/settings.json` permission allowlist | `.claude/settings.json:3-80` | PASS |

### Phase B — slash commands

| Plan requirement | File | Status |
|---|---|---|
| 5 commands present | `scaffold.md, phase1.md, phase2.md, phase3.md, render.md` | PASS |
| 0-indexed `$0`/`$1` correct | one-arg commands (phase1/2/3, render) use `$0`; `scaffold` uses `$0 $1`. No `$1` misuse for slug | PASS |
| `arguments:` frontmatter declared | each command has `arguments: [slug]` or `[slug, source]` | PASS |
| Subagent name references resolve | grep cross-check confirms every `.claude/agents/<X>.md` mention exists | PASS |

### Phase D — hooks + JSON schema

| Plan requirement | File | Status |
|---|---|---|
| `.claude/hooks/validate_graph.py`, `validate_bib.py`, `usage_log.py` exist | all 3 present | PASS |
| Executable bit set | `-rwxr-xr-x` on all 3 | PASS |
| `#!/usr/bin/env python3` shebangs | all 3 | PASS |
| Defensive against unparseable stdin | each catches `json.load(sys.stdin)` failure and exits 0 | PASS |
| Hooks exit 0 on demo (no false positives) | smoke tests above | PASS |
| `validate_bib.py` filters by review path (no false fire on unrelated `LITERATURE.md`) | regex `reviews/[^/]+/phase\d+/outputs/(LITERATURE\.md\|references\.bib)$` at line 22 | PASS |
| `src/conventions/graph_schema.json` validates `demo/graph.v2.json` | `jsonschema.validate` returns OK | PASS |
| Schema drift documented in `$comment` (not just code) | line 4 carries the explicit DRIFT NOTE referencing `error_categories.md` and the union enum | PASS |
| `requirements.txt` adds `jsonschema` + `bibtexparser` | both present, properly pinned (`jsonschema>=4,<5`, `bibtexparser>=1.4,<2`) | PASS |
| `.claude/settings.json` `hooks` block matches Claude Code structure | `PostToolUse` with matcher `Write\|Edit\|MultiEdit`, `SubagentStop` with matcher `*` | PASS |

### Phase E — profile + token logger

| Plan requirement | File | Status |
|---|---|---|
| `.claude/profiles/balanced.json` (documentation only) | present, schema valid | PASS |
| Each agent's `model:` matches profile entry | 15/15 (see cross-check below) | PASS |
| `src/token_log.py` transcript-parsing CLI | present, reads `usage.jsonl` records and walks `~/.claude/projects/.../subagents/agent-*.jsonl` for `usage` fields | PASS |
| `Makefile` `usage` target | line 80–81 | PASS |
| `usage_log.py` writes to `reviews/<slug>/phase<N>/agents/<role>/usage.jsonl` | line 91 of hook | PASS |
| `src/token_log.py` reads exactly that path | line 106–112 of CLI | PASS |
| Path glob and JSON field names in sync | both reference the same fields (`agent_type`, `agent_id`, `session_id`, `transcript_path`, `cwd`) | PASS |

### Phase F — MCP stub

| Plan requirement | File | Status |
|---|---|---|
| `.mcp.json` shipped as empty stub | `{"mcpServers": {}}` | PASS |

### Phase G — agent-memory seeds

| Plan requirement | File | Status |
|---|---|---|
| Seed `MEMORY.md` for each of the 4 designated agents | `arbiter/MEMORY.md`, `checker_domain/MEMORY.md`, `checker_literature/MEMORY.md`, `literature_searcher/MEMORY.md` | PASS |
| `.claude/agent-memory/README.md` present | yes, explains the harness-managed protocol | PASS |
| Only the 4 agents declare `memory: project` | grep confirms — exactly the 4 in §A above | PASS |

### Per-agent model cross-check (15/15)

| agent | frontmatter model | profile model | match |
|---|---|---|---|
| arbiter | claude-opus-4-7 | claude-opus-4-7 | OK |
| checker_ambiguous | claude-sonnet-4-6 | claude-sonnet-4-6 | OK |
| checker_contradiction | claude-sonnet-4-6 | claude-sonnet-4-6 | OK |
| checker_domain | claude-sonnet-4-6 | claude-sonnet-4-6 | OK |
| checker_literature | claude-sonnet-4-6 | claude-sonnet-4-6 | OK |
| checker_unreferenced | claude-haiku-4-5 | claude-haiku-4-5 | OK |
| claim_extractor | claude-haiku-4-5 | claude-haiku-4-5 | OK |
| constructive_reviewer | claude-sonnet-4-6 | claude-sonnet-4-6 | OK |
| critical_reviewer | claude-sonnet-4-6 | claude-sonnet-4-6 | OK |
| fixer | claude-sonnet-4-6 | claude-sonnet-4-6 | OK |
| graph_builder | claude-haiku-4-5 | claude-haiku-4-5 | OK |
| highlighter | claude-haiku-4-5 | claude-haiku-4-5 | OK |
| literature_searcher | claude-sonnet-4-6 | claude-sonnet-4-6 | OK |
| report_writer | claude-haiku-4-5 | claude-haiku-4-5 | OK |
| strategist | claude-sonnet-4-6 | claude-sonnet-4-6 | OK |

### Stale-reference scan (must be empty)

```
grep -rn "src/agents/|root_claude|phase[123]_claude\.md|verifier" \
    .claude/ CLAUDE.md README.md Makefile src/templates/   → no matches
grep -rn "phase1_claude|phase2_claude|phase3_claude|root_claude" \
    src/  → no matches
```

PASS. The two intentional `verifier` mentions in `src/conventions/{graph_schema.md,error_categories.md}` are explanatory historical notes (PLAN_REVIEW I6 explicitly preserves them), not live references.

---

## 7. Open questions for the user

1. **`reviews/test-1` and `reviews/paper_mistakes0`.** Neither was touched
   by the rework. The plan's pre-rework commit `b178084 workflow_rework:
   remove dangling AFS symlinks from reviews` already cleaned the AFS
   symlinks but left the directories. PLAN_REVIEW.md I10 argued
   `paper_mistakes0` is a collaborator's review and should be migrated,
   not deleted. Should the user run `migrate_review.py` (not yet
   written) or just delete both? This is the only outstanding
   "deliberate decision" from the plan.

2. **`reviews/__testaudit__`** — left in place by this audit per the
   brief. The orchestrator should `git clean -fd reviews/__testaudit__`
   (or just `rm -rf`) before merge.

3. **`.claude/agent-memory/_global/usage.jsonl`** — the smoke tests in
   §5 left two test records in this file. Either delete the file or
   accept that the SubagentStop hook will continue appending real
   records here when it can't infer a slug. Recommend gitignoring (see
   I1).

4. **MCP stub.** `.mcp.json` ships with `{"mcpServers": {}}`. The plan
   says this is the deliberate choice. Confirm we're shipping with no
   MCPs wired up at merge — `literature_searcher` and
   `checker_literature` will fall back to `WebFetch` / `WebSearch`
   only.

5. **`src/conventions/graph_schema.md` reconciliation.** The drift
   between the prose source and the new vocabulary is acknowledged in
   the schema `$comment` but not in the prose itself. Ship as-is and
   reconcile in a follow-up PR, or block the merge to align them?
   Recommend the former.

6. **`Bash(make:*)` vs `Bash(make *)`** in `.claude/settings.json:14-15`
   — pick one; the duplicate is harmless but confusing.

---

*Audit complete. No critical findings; five small follow-ups documented above.*
