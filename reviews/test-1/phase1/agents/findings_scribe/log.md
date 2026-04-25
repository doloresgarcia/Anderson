# findings_scribe — log

## Status

Plan executed. The cross-checks against the input artifacts all came out
identical to the agent-log-reported numbers (see "Numbers verified" below),
so no discrepancy needed to be surfaced. The FINDINGS.md text was assembled
and returned via the agent's final assistant message rather than written to
`phase1/outputs/FINDINGS.md`: the runtime sandbox blocked the Write
operation against that path with `Subagents should return findings as
text, not write report files. Include this content in your final response
instead.` This is documented here so the orchestrator can persist the
returned text into `phase1/outputs/FINDINGS.md` itself if the harness
permits it from the orchestrator context.

## Inputs read

- `agents/executor.md`
- `methodology/03-phases.md`
- `methodology/05-artifacts.md`
- `conventions/claim_taxonomy.md`
- `conventions/confidence.md`
- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `phase1/outputs/references.bib`
- `phase1/outputs/graph.v1.json` (groups + spot-checks)
- `phase1/agents/claim_extractor/log.md`
- `phase1/agents/literature_searcher/log.md`
- `phase1/agents/graph_builder/log.md`
- `paper/paper.meta.json`

## Numbers verified

All numbers below were re-derived from the artifacts (CLAIMS.md,
LITERATURE.md, references.bib, graph.v1.json) and cross-checked against the
agent logs. They match.

- CLAIMS.md rows: 217 (`C001`–`C217`).
- Per-type histogram: method=104, result=46, background_fact=46,
  interpretation=8, definition=7, prior_work=5, assumption=1,
  UNCLASSIFIED=0.
- Hedged=true rows: 4 — `C089`, `C109`, `C136`, `C179`.
- Confidence: high=153, medium=64, low=0.
- LITERATURE.md headings: 217. Headings with ≥1 bullet: 73. Total bullets:
  113. Unique cited keys: 34. Relations: supports=74, related=39,
  contradicts=0.
- references.bib entries: 45. Used in LITERATURE.md: 34. Unused: 11
  (`ATLAS:2018wis`, `Butter:2019cae`,
  `DBLP:journals/corr/LoshchilovH16a`, `delphes`, `Hashemi:2019fkn`,
  `Huetsch:2024quz`, `Komiske:2018cqr`, `Louppe:2017ipp`, `Moore:2018lsr`,
  `Otten:2019hhl`, `Qu:2019gqs`). `delphes` is an exact alias of
  `deFavereau:2013fsa` (same arXiv ID).
- graph.v1.json: 20 groups, 217 claim nodes, 0 edges. Group sizes: 14, 13,
  13, 13, 12, 12, 12, 12, 12, 12, 12, 11, 10, 10, 10, 8, 8, 8, 8, 7
  (sum=217). All ≤ 15.
- Section distribution from CLAIMS.md (informational): 5=43, 4=29, 2.1=29,
  App.A=28, 3=17, 2.2=17, 2.4=16, 2.3=14, 1=10, 6=7, Abstract=5, Code=2.

## Departures from agent logs

None. Every cross-check matched the corresponding number in the
claim_extractor / literature_searcher / graph_builder logs. The
literature_searcher log's "≈ 110 / ≈ 34" split between no-search and
no-result claims is approximate by its own admission and was carried
forward verbatim with the "≈" qualifier; the exact totals (73 with bullets,
144 without) were re-counted directly from `LITERATURE.md`.

## Files written

- `phase1/agents/findings_scribe/plan.md`
- `phase1/agents/findings_scribe/log.md` (this file)

`phase1/outputs/FINDINGS.md` could not be written from this agent's
sandbox; the FINDINGS.md content is returned in the final assistant
message for the orchestrator to persist.
