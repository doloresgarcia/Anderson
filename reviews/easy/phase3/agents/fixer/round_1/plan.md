# Fixer Plan — Phase 3 Round 1

## Inputs

- `reviews/easy/phase3/outputs/graph.final.json` — main fix target
- `reviews/easy/phase3/outputs/STATS.md` — already correct (authoritative)
- `reviews/easy/phase3/outputs/REPORT.md` — content fixes
- `reviews/easy/phase2/outputs/VERIFICATION.md` — source of truth for verdicts

## Steps

### 1. Fix graph.final.json

**F2 — Claim verdicts:**
STATS.md shows 0 CLEAR claims, 35 FLAGGED, 165 INCONCLUSIVE.
The graph has many claims with `"verdict": "CLEAR"` and `"color": "#2ECC71"`.
All CLEAR claim nodes must become INCONCLUSIVE (yellow: #F1C40F).

Strategy: Replace all instances of:
  `"verdict": "CLEAR",\n      "color": "#2ECC71"` with `"verdict": "INCONCLUSIVE",\n      "color": "#F1C40F"`
  on claim nodes (those that also have flagged_categories: []).
  But I need to not touch FLAGGED claims (which have "#2ECC71" nowhere relevant).

**F1 — Group verdicts:**
G006, G015, G016, G017, G018 have `"verdict": "CLEAR"` and `"color": "#2ECC71"`.
All 5 should become `"verdict": "INCONCLUSIVE"` and `"color": "#F1C40F"`.

**B2 — Paper metadata:**
Add `"title"` and `"arxiv"` to the paper object.

**B3 — Edge E021 provenance:**
Change `"provenance": "paper.txt:analysis"` to `"provenance": "paper.txt:1660-1661,1928"`.

### 2. Re-render graph (cannot run scripts — note in log)
Note: cannot run `python3 src/render_graph.py` without bash access.
The HTML will be out of sync; note in log and flag for orchestrator.

### 3. Fix REPORT.md

**F5 — Source path:**
Change `papers/annotated/paper_corrupted.pdf` to `reviews/easy/paper/paper.pdf`.

**F3 — Add C017 and C086 to ambiguous section:**
REPORT.md says "27 claims flagged" in ambiguous, but only lists 26.
Add C017 and C086 entries.

**B1 — Add internal_contradiction INCONCLUSIVE note:**
From VERIFICATION.md: C077, C112, C195 received INCONCLUSIVE under internal_contradiction.
Add a note in the Inconclusive section.

**B4 — Trust score formula:**
Add one sentence explaining the weighting formula.

### 4. Note F6 in log (informational only)

### 5. Regenerate STATS.md
Note: cannot run `python3 src/claim_stats.py` without bash access.
STATS.md already correctly shows 0 CLEAR claims (it was generated before the graph).
After graph fix, STATS.md per-group breakdown should be regenerated.
Flag for orchestrator.
