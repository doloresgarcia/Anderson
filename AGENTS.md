# Codex Wrapper

Codex support for Anderson is intentionally a thin compatibility layer. Do not
create a parallel `.codex/` agent tree, duplicate phase instructions, or fork
the role specs. The Claude-oriented files remain the source of truth.

## Canonical Sources

- Read `CLAUDE.md` first. It is the canonical Anderson orchestrator contract.
- For phase-style requests, use the matching runbook in
  `.claude/commands/{scaffold,phase1,phase2,phase3,render}.md`.
- For role-specific work, use `.claude/agents/<role>.md` as the canonical role
  spec. Ignore Claude-only frontmatter fields (`model`, `tools`, `memory`) and
  Claude settings/hooks where Codex cannot apply them directly.
- Domain and artifact rules live in `src/conventions/` and `src/methodology/`.
  Do not restate them here.

## Codex Translation Rules

- Preserve the flat orchestration model: the main Codex session coordinates
  work, and roles do not spawn nested roles.
- When a runbook says to dispatch an agent, read that agent file and follow its
  declared reads, writes, and output discipline.
- Preserve disjoint outputs for parallelizable work. If Codex cannot safely run
  roles in parallel, run them sequentially without changing their file
  ownership.
- Keep the per-agent `plan.md` and `log.md` convention in the relevant
  `reviews/<slug>/phase<N>/agents/<role>/` directory.
- Treat `reviews/<slug>/CLAUDE.md` as paper-specific context only; it does not
  replace the root orchestrator contract.

If behavior needs to change, update the canonical Claude/runbook/agent,
methodology, or convention file instead of adding Codex-only instructions here.
