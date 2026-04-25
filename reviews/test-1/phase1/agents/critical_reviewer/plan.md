# Plan — critical_reviewer phase 1 (test-1)

Single-bot review mode (phase 1). Auto-A triggers must be checked first.

## Steps

1. Read role spec + methodology + conventions (done above).
2. Read the artifacts under review:
   - CLAIMS.md (217 claims expected per dispatch summary)
   - LITERATURE.md (34 cited keys)
   - references.bib
   - graph.v1.json + skeleton
   - FINDINGS.md
3. Read phase1/agents/*/log.md and plan.md for context (especially boundary-call notes from claim_extractor).
4. Run auto-A triggers in order:
   a. Set-intersection of LITERATURE.md keys vs. references.bib keys.
   b. Independent verification of >= 8 references.bib entries via WebFetch / WebSearch.
   c. Validate graph.v1.json against conventions/graph_schema.md rules.
   d. Sample >= 20 CLAIMS.md rows: verify provenance line in paper.txt.
   e. Check declared deliverables list — flag any extra files.
5. Completeness/correctness checks:
   - Sample >= 15 CLAIMS.md type tags.
   - Verify FINDINGS.md count tables match CLAIMS.md / LITERATURE.md.
   - Verify graph.v1.json claim count (217), group count (<=20), literature representation.
   - Audit `contradicts` candidates (zero reported) and a sample of `prior_work` `supports` rows.
   - Look for fabricated-looking arXiv IDs / DOIs / generic-sounding snippets.
6. Write critical.md as flat A/B/C table with cites.
7. Final report.

## Tools

- Read for files
- Bash for grep/diff/jq line lookups
- WebFetch / WebSearch for citation verification (load via ToolSearch)

## Hard constraints

- Read-only on phase-1 outputs.
- Write only to phase1/review/critical.md, this plan.md, and log.md.
- Auto-A triggers stay A even if "feels minor".
