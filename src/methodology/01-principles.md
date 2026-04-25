# Principles

## Scope

Anderson reviews **one paper at a time**. Given a paper, it produces:

1. A claim graph in the schema defined by `conventions/graph_schema.md`.
2. A verification report flagging claims the system could not verify.
3. The paper with the unverified sentences visibly highlighted.

Anderson does not rewrite the paper, propose corrections, or attempt replication of
experiments. It is a reviewer, not a co-author.

## Design principles

- **Thin orchestrator.** The orchestrator holds prompts, summaries, and verdicts. It
  never extracts claims, runs literature searches, or judges proofs itself. Real work
  happens in subagent contexts.
- **Artifacts are the only handoff.** Each phase finishes by writing files. The next
  phase reads those files; it does not read the previous phase's transcripts.
- **Conventions over preferences.** Every structural decision (what is a claim, what
  the graph looks like, what counts as verified) lives in `src/conventions/`. Agents
  read those files; they do not improvise.
- **Auditable verdicts.** Every "unverified" tag in the final report points to (a)
  the originating sentence in the paper, (b) the verification attempt in
  `VERIFICATION.md`, and (c) the corresponding node in the graph.
- **Cite or it didn't happen.** Any claim said to be supported by external literature
  must reference a real, resolvable bibliographic record. Unresolvable references
  default to "unverified".
