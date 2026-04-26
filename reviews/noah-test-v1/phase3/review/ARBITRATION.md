# Phase 3 Arbitration

## A1 verdict: DISMISSED

The critical reviewer claims claim-0441 is absent from paper.highlighted.html. This is factually incorrect. Direct inspection of the file shows an `<div class="tooltip"><span class="hl-orange">` wrapping the prose beginning "In Tab.~\ref{tab:symbreak_comparison_generation}, we compare the impact..." — the sentence that contains claim-0441 (line 772). The span color is `hl-orange`, which is correct for `internal_contradiction` per error_categories.md. The tooltip text reads: "claim-0165/0441 [internal_contradiction]: Reference multivectors stated 'essential' here (AUC 0.996→0.514 without them) directly contradicts line 341...".

The highlight is present, correctly colored, and correctly attributed. A1 is dismissed.

Note: The highlight combines claims 0165 and 0441 into a single span because both legs of the contradiction are flagged. This is consistent with the B2 pattern the critical reviewer itself notes for claim-0019/0018. It is a minor presentational choice, not a Category-A violation.

## A2 verdict: SUSTAINED

The REPORT.md header states:

> **Claims checked:** 418 prose claims (127 equations, captions, and table cells not checked)
> **Claims with findings:** 28 FLAGGED + 4 INCONCLUSIVE

The authoritative source (graph.v2.json) records:

| Verdict | graph.v2.json | REPORT.md header |
|---------|--------------|-----------------|
| FAIL | **34** | 28 |
| INCONCLUSIVE | **6** | 4 |
| PASS | 368 | not stated |
| NOT_CHECKED | **137** | 127 |

All three numbers in the REPORT.md header are wrong. The discrepancies are not rounding or categorization ambiguity — graph.v2.json has 545 claim nodes with explicit verdict fields, and the counts are unambiguous. The REPORT.md header was likely written from an intermediate draft of VERIFICATION.md before the graph_builder finalized the verdict layer. This is a Category-A accuracy failure: the report's summary statistics do not match the authoritative artifact.

A2 is sustained.

## Other findings: summary

**B1 (critical) — claim-0488 tooltip omits cross-reference to claim-0365:** Presentational gap; color is correct (amber/ambiguous). Not a blocking issue.

**B2 (critical) — claim-0019 combined into claim-0018 tooltip:** The combined tooltip appears on the correct line. Per the arbitration of A1 above, combining co-located contradiction pairs into one highlight is an acceptable convention. This is Category-B, not Category-A.

**B3 (critical) — REPORT.md summary table uses checker-flag counts, not claim-level verdict counts:** This compounds A2. The table's category-level FLAGGED counts (e.g., "unreferenced: 25 FLAGGED") sum to more than 28 unique claims and more than 34 FAIL claims — both because multiple categories flag the same claim, and because the header counts are themselves wrong. The table is not independently incorrect, but it cannot be reconciled with the header without guidance.

**Constructive: graph.final.html has no PASS group cards:** Confirmed by the constructive reviewer; technically correct per the "dominant verdict" grouping rule, but reduces navigability. Category-B.

**Constructive: highlight offsets in LaTeX source HTML:** Acknowledged extraction artifact from LaTeX line boundaries. Not a blocking issue.

**Constructive: INCONCLUSIVE claims lack resolution recommendations:** Minor actionability gap. Not blocking.

## Verdict: ITERATE

One Category-A issue is sustained (A2). The REPORT.md header and summary statistics must be corrected before human presentation.

## Required fixes

1. **REPORT.md header — correct all three wrong counts:**
   - Change "418 prose claims (127 equations, captions, and table cells not checked)" → "408 prose claims (137 equations, captions, and table cells not checked)"
   - Change "28 FLAGGED + 4 INCONCLUSIVE" → "34 FAIL + 6 INCONCLUSIVE + 368 PASS + 137 NOT_CHECKED"
   - Use the terminology "FAIL" (matching graph.v2.json verdict field) rather than "FLAGGED", or add a mapping note if "FLAGGED" is preferred for human readability.

2. **REPORT.md summary table — reconcile checker-flag counts with claim-level counts:**
   - Add a clarifying sentence in the summary table header explaining that category counts reflect checker-level flags (some claims appear in multiple categories) and the claim-level totals are 34 FAIL / 6 INCONCLUSIVE.
   - Correct "127" → "137" in the NOT_CHECKED breakdown (33 equations + 17 captions + 77 table cells = 127, but graph.v2.json has 137 NOT_CHECKED nodes — the breakdown itself needs to be re-derived or corrected).

No changes are required to paper.highlighted.html or graph.final.json/html — those artifacts are correct.
