# Plan: Phase 3 Report Writer for "easy" review

## Objective
Compose REPORT.md synthesizing the verification results from Phase 2 checkers into a human-facing summary, organized by error category in severity order.

## Inputs to read
1. paper.meta.json — paper metadata
2. CLAIMS.md — all 200 claims
3. FINDINGS.md (Phase 1) — paper background, coverage summary
4. STRATEGY.md (Phase 2) — strategist's guidance, importance levels
5. VERIFICATION.md (Phase 2) — detailed verdict from all 5 checkers
6. graph.v2.json — logical dependencies and groups (for context only)
7. error_categories.md — category definitions and severity order

## Execution steps

1. **Read all inputs** — complete (done above)
2. **Generate STATS.md** — invoke `python3 src/claim_stats.py reviews/easy` to produce mechanical summary counts
3. **Analyze verdicts** — extract all FLAGGED claims by category:
   - domain_violation
   - literature_collision
   - internal_contradiction
   - ambiguous
   - unreferenced
4. **Extract inconclusive claims** — gather claims where any checker reported INCONCLUSIVE (C077, C112, C157, C195)
5. **Compose REPORT.md sections in order:**
   - Overview: paper title, authors, what was reviewed
   - Method: conventions, checkers that ran, how they worked
   - What we checked: claim count, strategist's prioritization, which checkers ran
   - Findings by category: one subsection per category with FLAGGED verdicts
   - Inconclusive: reasons grouped
   - Limitations: constraints, gaps, checker limitations
6. **Write log.md** — summary of what was read and composed

## Notes
- Apply F-CON-10 filter: redirect `[corrected-citation]` evidence to separate list
- No new findings — describe what checkers already found
- Prose only; refer to verdicts in VERIFICATION.md
- Link to paper.txt provenance where helpful
- Severity order: domain_violation > literature_collision > internal_contradiction > ambiguous > unreferenced
