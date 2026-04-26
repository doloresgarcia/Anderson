# Phase 3 Critical Review

## Category-A findings

### A1 — claim-0441 missing from paper.highlighted.html

`claim-0441` is FLAGGED in VERIFICATION.md as `internal_contradiction` (cross-referenced with claim-0165; the contradiction pair is symmetric). It is FAIL in graph.v2.json. It does not appear anywhere in paper.highlighted.html — not as an orange highlight, not even in a tooltip. This directly triggers the Phase-3 Category-A rule: *"A highlight in paper.highlighted.html whose claim_id has no FLAGGED entry in VERIFICATION.md"* (applied in reverse: a FLAGGED entry in VERIFICATION.md with no corresponding highlight). paper.txt line 772 must receive an orange highlight.

### A2 — REPORT.md claim counts do not match graph.v2.json

The REPORT.md header states "Claims with findings: 28 FLAGGED + 4 INCONCLUSIVE." The actual counts in graph.v2.json (the authoritative artifact) are:

| Verdict | graph.v2.json | REPORT.md header |
|---------|--------------|-----------------|
| FAIL | **34** | 28 |
| INCONCLUSIVE | **6** | 4 |
| PASS | 368 | not stated in header |
| NOT_CHECKED | 137 | 127 (stated as "127 equations, captions, and table cells") |

The 6-claim discrepancy in FAIL and 2-claim discrepancy in INCONCLUSIVE are not rounding or categorization differences — they are distinct claim nodes present in graph.v2.json. The REPORT.md summary table also uses checker-level category counts (which double-count claims flagged in multiple categories) rather than claim-level verdict counts. The required counts — 34 FAIL / 6 INCONCLUSIVE / 368 PASS / 137 NOT_CHECKED — do not appear anywhere in REPORT.md.

Additionally, the REPORT.md states 127 NOT_CHECKED claims ("33 equations, 17 captions, and 77 table cells") but graph.v2.json has 137 NOT_CHECKED nodes. This is a further discrepancy in the header metadata.

## Category-B findings

### B1 — claim-0488 highlighted but color not evaluated for severity

`claim-0488` is highlighted hl-amber (ambiguous). Per VERIFICATION.md it is FLAGGED only as `ambiguous`. Amber is the correct color — no issue here. However, the tooltip does not note that claim-0488 is also cross-referenced with claim-0365 (which is orange/internal_contradiction). The tooltip is slightly misleading in isolation. This is presentational, not a Category-A color error.

### B2 — claim-0019 subsumed under claim-0018 tooltip without its own highlight

`claim-0019` is independently FLAGGED as `unreferenced` in VERIFICATION.md (evidence: paper.txt:95), FAIL in graph.v2.json, but it is not given its own highlight in paper.highlighted.html. It is combined into the claim-0018 tooltip as "claim-0018/0019." The conventions require highlights to correspond to individual FLAGGED claims. Combining two claims into one highlight marker may cause the line bearing claim-0019 to appear untagged if it is on a different line. This is a minor convention deviation, not a Category-A trigger, provided both lines display the blue highlight.

### B3 — REPORT.md summary table conflates checker-flags with claim-level verdicts

The summary table at the end of REPORT.md presents FLAGGED/INCONCLUSIVE counts per checker category (e.g., "unreferenced: 25 FLAGGED"). These category-level counts sum to more than the 28 unique FLAGGED claims the header cites, because several claims are flagged by multiple checkers. The table does not cross-reference the claim-level verdict counts (34 FAIL / 6 INCONCLUSIVE) from graph.v2.json. A reader cannot reconcile the two representations without inspecting the graph directly. The CLEAR counts are marked "approximate" without qualification. This weakens the report's evidentiary value.

## Verdict: ITERATE

Two Category-A issues require correction before the artifacts can be presented to the human gate:

1. Add an orange highlight at paper.txt line 772 for `claim-0441` in paper.highlighted.html.
2. Correct REPORT.md claim counts to match graph.v2.json: 34 FAIL / 6 INCONCLUSIVE / 368 PASS / 137 NOT_CHECKED, and reconcile the NOT_CHECKED breakdown (137 total, not 127).
