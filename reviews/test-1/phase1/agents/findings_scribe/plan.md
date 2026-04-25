# findings_scribe — plan

## Role

Phase 1 FINDINGS.md scribe. Produce a short, mechanical summary of phase 1
artifacts that downstream phases (and reviewers) can rely on as a single
source of truth.

## Inputs (read-only)

- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `phase1/outputs/references.bib`
- `phase1/outputs/graph.v1.json`
- `phase1/agents/claim_extractor/log.md`
- `phase1/agents/literature_searcher/log.md`
- `phase1/agents/graph_builder/log.md`
- `paper/paper.meta.json`
- methodology/03-phases.md, 05-artifacts.md
- conventions/claim_taxonomy.md, conventions/confidence.md
- agents/executor.md

## Outputs (only these)

- `phase1/outputs/FINDINGS.md`
- `phase1/agents/findings_scribe/plan.md` (this file)
- `phase1/agents/findings_scribe/log.md`

## Steps

1. **Cross-check counts mechanically.** Re-derive from the artifacts:
   - total claim rows in CLAIMS.md (expect 217)
   - per-type histogram (expect method 104, result 46, background_fact 46,
     interpretation 8, definition 7, prior_work 5, assumption 1, UNCLASSIFIED 0)
   - hedged-true count (expect 4)
   - confidence histogram (high/medium/low)
   - LITERATURE.md headings, headings with ≥1 bullet, total bullets, relation
     breakdown (supports/contradicts/related), unique cited keys
   - references.bib entries
   - groups in graph.v1.json (expect 20) plus titles and sizes
2. **Pull gaps from logs.** Read each agent's log.md and lift only items the
   agents themselves flagged: `page=?`, no structural edges, ambiguous-type
   decisions, no-search / no-result claims, unused bib entries.
3. **Write FINDINGS.md** with the seven sections required by phase1/CLAUDE.md
   and the dispatch (Overview, Claim counts, Confidence distribution, Group
   structure, Literature coverage, Gaps identified, Phase-2 prompts).
4. **Write log.md** capturing the cross-check numbers and any departures from
   the agent logs.
5. **Do not modify any phase-1 outputs.** Plan-then-execute.

## Numbers verified before writing

- CLAIMS.md rows: 217 ✓
- per-type: method=104, result=46, background_fact=46, interpretation=8,
  definition=7, prior_work=5, assumption=1, UNCLASSIFIED=0 ✓
- hedged=true rows: 4 (C089, C109, C136, C179) ✓
- confidence: high=153, medium=64, low=0 ✓
- LITERATURE.md headings: 217; headings with ≥1 bullet: 73; bullets total: 113;
  unique cited keys: 34; relations: supports=74, related=39, contradicts=0 ✓
- references.bib entries: 45; unused (in LITERATURE.md) keys: 11 ✓
- graph.v1.json: 20 groups, 217 claims, 0 edges ✓
