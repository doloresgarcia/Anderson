ITERATE

# Arbitration — Phase 3, Round 1 — easy

**Date:** 2026-04-26
**Reviewers:** critical_reviewer, constructive_reviewer

## Rationale

Two Category A findings (F1, F2) are present. Per arbiter logic, any A triggers ITERATE. Round 1 — no prior fixer passes.

---

## Deduplicated Finding Table

| ID | Cat | Source | Summary | Fixer Pass |
|----|-----|--------|---------|------------|
| F1 | A | critical | Groups G006/G015/G016/G017/G018 carry CLEAR verdict in graph.final.json but all children are INCONCLUSIVE; must be INCONCLUSIVE/yellow per schema | -- |
| F2 | A | critical | Many claim nodes in graph.final.json have verdict CLEAR despite not being fully examined by all checkers; contradicts STATS.md (0 CLEAR). Claims should be INCONCLUSIVE, not CLEAR | -- |
| F3 | B | critical | REPORT.md ambiguous section says 27 but enumerates only 26 claims (C017 and C086 missing) | -- |
| F4 | B | critical | STATS.md per-group breakdown inflates INCONCLUSIVE counts by absorbing misclassified CLEAR claims (downstream of F2) | -- |
| F5 | B | both | REPORT.md line 10 cites nonexistent path `papers/annotated/paper_corrupted.pdf`; actual path is `reviews/easy/paper/paper.pdf` | -- |
| F6 | B | critical | Highlighter log reports 203 claims vs actual 200 in VERIFICATION.md/STATS.md | -- |
| B1 | B | constructive | REPORT silently omits the 3 INCONCLUSIVE claims under internal_contradiction category | -- |
| B2 | B | constructive | graph.final.json missing paper metadata fields (title, arxiv) required by schema | -- |
| B3 | B | constructive | Edge E021 has invalid provenance "paper.txt:analysis"; schema requires line pointer or "inferred" | -- |
| B4 | B | constructive | REPORT trust score explanation omits the weighting formula; score is unverifiable from REPORT alone | -- |
| F7 | C | critical | Only 19/200 non-CLEAR claims highlighted in paper.highlighted.pdf (9.5% match rate) | -- |
| F8 | C | critical | Highlighter log trust score denominator (41/465) inconsistent with STATS.md (41/100); different metrics share same label | -- |
| C1 | C | constructive | 0 hedged claims across 200 is implausible; REPORT should note this as an extractor limitation | -- |
| C2 | C | constructive | Ambiguous section (27 items) lacks thematic sub-grouping; hard to scan | -- |
| C3 | C | constructive | Coverage gaps mention 112 UNCOVERED claims without type breakdown | -- |

**Notes:**
- F5 (critical) and C-4 (constructive) merged as F5 — identical finding (wrong source path).
- F4 is downstream of F2; fixing F2 (claim verdicts) and regenerating STATS.md should resolve F4 automatically.
- F1 is also likely downstream of F2; correcting per-claim verdicts and re-aggregating group verdicts should fix both, but F1 is independently verifiable against the schema.
