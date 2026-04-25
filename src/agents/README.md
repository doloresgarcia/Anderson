# Agents (moved)

Agent specifications now live at `.claude/agents/<name>.md` with proper
Claude Code subagent frontmatter (model, tools, memory). The orchestrator
at the repo-root `CLAUDE.md` dispatches them via slash commands in
`.claude/commands/`.
