# Agent memory

Each subagent declared with `memory: project` in its `.claude/agents/<name>.md`
frontmatter gets a persistent directory here, owned by the Claude Code harness.
The harness auto-injects the first ~25KB of `MEMORY.md` into that subagent's
system prompt every dispatch and instructs it to curate / append as it learns.

## Agents currently using project memory

- `literature_searcher` — backends, rate limits, query templates that worked
- `checker_literature` — known miscites, common citation traps per domain
- `checker_domain` — established-knowledge anchors per domain
- `arbiter` — past PASS/ITERATE/ESCALATE precedents

## Update protocol

The harness manages reads + writes. You don't need to wire anything by hand —
each opted-in agent's system prompt already contains:

1. "Here is the current MEMORY.md contents…" (auto-injection)
2. "If you learned something useful, append it to MEMORY.md…" (curation rule)

What the agent should write is up to its body spec. House style:

- One entry per dispatch under a `## YYYY-MM-DD <slug>` header.
- 1–3 bullets. Frame as "When you see X, prefer Y because Z."
- No paper-specific facts (those go in the review's artifacts, not memory).
- Append-only. Never delete past entries — let manual cleanup catch
  bad lessons.

## Catch-all

`_global/usage.jsonl` is appended to by the SubagentStop hook
(`.claude/hooks/usage_log.py`) for dispatches it cannot route to a
specific review. `src/token_log.py` skips this file when aggregating
per-review usage.
