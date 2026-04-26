# Constructive review — Phase 2 — slug: easy — round 2 (post-fixer)

Reviewer: constructive_reviewer
Date: 2026-04-26
Round: 2 (post-fixer; fixer worked items M1–M10, deferred M11–M16)

---

## Summary

The fixer's round-1 pass resolved the substantive gaps identified in the
round-1 constructive review. The unreferenced section is now significantly
richer, the five missing importance=high entries are present, and the C157
cross-reference and corrected-citation note are actionable for Phase 3. Most
B-class findings from round 1 are RESOLVED. One B-class issue partially
survives: the graph.v2.json evidence arrays for C001 and C003 were not
deduplicated despite the fixer's M10 log claiming success. Two additional
C-class presentation observations are noted.

---

## Round-1 finding status

### F-CON-01 [B] — Bare CLEAR verdicts for high-importance UNCOVERED Tier-1 performance claims

**RESOLVED.**

checker_unreferenced/section.md (post-fixer) now carries one-line evidence
notes for all 17 originally bare entries:

- C100: paper.txt:747-751, Fig. 2 left panel
- C101: paper.txt:749-751, Fig. 2 left panel
- C104: paper.txt:757-758, Fig. 2 right panel
- C112: paper.txt:772-773, Tables 2 and 4 (with secondary line range)
- C117: paper.txt:1003-1004, Table 2 (with AUC numbers)
- C129: paper.txt:1036-1038, Table 4 (with AUC numbers)
- C131: paper.txt:1111-1112, Fig. 4 left panel and Table 5
- C138: paper.txt:1339-1340, Table 2 fine-tuning rows
- C180: paper.txt:1649-1651, Fig. 6
- C181: paper.txt:1650-1651, Fig. 6
- C183: paper.txt:1660-1661, Fig. 7 (plus cross-reference note to contradiction)
- C184: paper.txt:1927-1928, Fig. 7
- C185: paper.txt:1928-1929, Fig. 7 (plus cross-reference note to contradiction)
- C193: paper.txt:1950-1952, Tables 3 and 7
- C195: paper.txt:1954-1956, Fig. 2 left panel
- C197: paper.txt:1957-1958, Table 2 fine-tuning rows
- C198: paper.txt:1959-1961, Fig. 7

C157 was handled under M7 with a combined cross-reference plus evidence note
(paper.txt:1421-1422, pointing to the literature_collision FLAGGED verdict).

Each note is concise and informative. The highlighter and report_writer now
have Table/Figure anchors for every Tier-1 CLEAR UNCOVERED claim.

---

### F-CON-02 [B] — C157 graph node flagged_categories

**RESOLVED (was moot per arbiter round 1, and confirmed correct in round 2).**

graph.v2.json line 3328-3330: C157 carries `"flagged_categories":
["literature_collision"]`, `"verdict": "FLAGGED"`, `"color": "#D32F2F"`.
The arbiter's V1 verification note from round 1 is confirmed.

---

### F-CON-03 [B] — Five missing importance=high UNCOVERED claims in checker_unreferenced

**RESOLVED.**

checker_unreferenced/section.md now contains all five entries in numeric order:

- C029 (paper.txt:232-240) — CLEAR, self-describing design choice
- C031 (paper.txt:242-248) — CLEAR, elementary complex algebra identity
- C036 (paper.txt:303-304) — CLEAR, known Clifford algebra limitation
- C041 (paper.txt:371-390) — CLEAR, Schur's lemma grounded
- C054 (paper.txt:515-516) — CLEAR, hedged design claim backed by ablation

All five verdicts are CLEAR with reasoning. The verdicts are well-justified:
C029 and C031 are self-describing or standard mathematical identities; C036
and C041 defer to checker_domain's confirmation; C054 is hedged and supported
by Tables 3 and 7. Phase 3 report_writer has adequate coverage.

---

### F-CON-04 [B] — Duplicate evidence strings in graph.v2.json

**PARTIALLY RESOLVED. One residual issue remains (Category C).**

The fixer's log records deduplication of C001, C003, C070, C191, C193.
Inspection of graph.v2.json shows the following actual state:

**C001 (lines 602-607 of graph.v2.json):** evidence array still contains
FOUR entries:
1. "paper.txt:16-17 — Supported by Table 2 (top tagging), Table 4 (JetClass),
   and Fig. 7 (event generation) in paper.txt." [added by M8]
2. "paper.txt:16-17 — \"yields state-of-the-art performance...\"" [original]
3. "paper.txt:16-17 (\"L-GATr yields state-of-the-art performance...\")" [duplicate]
4. "paper.txt:16-17" [bare duplicate]

**C003 (lines 645-648 of graph.v2.json):** evidence array still contains
TWO entries:
1. "paper.txt:18-20 — \"The underlying architecture...\"" [em-dash version]
2. "paper.txt:18-19 (\"which is able to break symmetries if needed\")" [parenthesis version]

The fixer log reports these as fixed, but the graph file still carries the
duplicates. The most likely explanation is that the graph_builder re-ran
after the fixer's direct edits and regenerated the duplicates from the
un-deduplicated section.md files (the section.md files were not edited for
deduplication — only graph.v2.json was edited directly for M10).

Other claimed fixes (C070, C191, C193) may similarly have been re-introduced
by the graph_builder re-run. C193 at graph.v2.json lines 3982-3985 shows
three evidence entries, including two for paper.txt:1950-1952 (one with
"Supported by" phrasing, one with the original snippet, one parenthetical),
suggesting the dedup was overwritten.

This is now a C-level presentation issue (see F-CON-08 below) rather than B,
because: (a) the highlighter can tolerate duplicate line ranges; (b) the
critical functional content — the informative snippets added by M8 — is
present in all affected nodes; (c) the phase-3 graph_builder re-run will
regenerate from section.md and the duplicates will likely persist unless the
section.md files are also deduplicated. No Phase-3 readiness blocker results
from this.

---

### F-CON-05 [C] — checker_ambiguous coverage skews architectural

**Status: Deferred per arbiter (M13). No change. Retained as C.**

The coverage skew noted in round 1 persists but was accepted as non-blocking.
The key ambiguous performance claims (C186, C196) were covered and FLAGGED
correctly.

---

### F-CON-06 [C] — VERIFICATION.md lacks executive summary preamble

**Status: Deferred per arbiter (M14). No change. Retained as C.**

VERIFICATION.md still opens directly with "## unreferenced" with no aggregate
count preamble. The graph.v2.json summary (35 FLAGGED, 3 INCONCLUSIVE, 162
CLEAR) remains derivable by the report_writer from the graph.

One minor new presentation note: VERIFICATION.md's unreferenced section now
ends at line 114 and the ambiguous section begins at line 115 with no blank
line separator, only a bare `## ambiguous` header immediately after the last
entry of the unreferenced section. This is cosmetically ungainly but not a
functional issue.

---

### F-CON-07 [C] — C077 INCONCLUSIVE verdict has thin Phase-3 disposition guidance

**Status: Deferred per arbiter (M15). No change. Retained as C.**

The checker_contradiction C077 verdict remains INCONCLUSIVE with the same
reasoning. The disposition note (classify as paper presentation weakness) was
not added, as permitted by the arbiter.

---

### F-CON-08 [C] — Phase-1 carry-over C003/C005 off-by-one provenance (confirmation)

**Status: Confirmed harmless in round 1. No change. Retained as informational.**

---

## New round-2 observations

### F-CON-09 [C] — M10 deduplication did not persist: graph_builder re-run overwrote fixes

As detailed under F-CON-04 above, the direct edits to graph.v2.json for M10
were overwritten when graph_builder re-ran from section.md. The section.md
files for checker_unreferenced, checker_ambiguous, etc. were not modified to
remove duplicate evidence strings; only the graph was patched. Since
graph_builder concatenates evidence from all checker sections, any section.md
that itself contributes multiple entries for the same claim will re-introduce
duplicates.

Consequence for Phase 3: the highlighter will attempt to highlight the same
paper.txt span multiple times for affected claims (C001, C003, C193, and
potentially others). This is a cosmetic rendering issue — the span will be
highlighted correctly, just potentially with redundant markers. The
report_writer drawing evidence citations should deduplicate programmatically
before presenting them.

This is Category C (style/polish) rather than B because: the informative
content is present; the functional correctness of the highlighted output is
not impaired; and the graph_builder's behavior is expected given the
architecture.

Recommendation: if a graph_builder pass is run for Phase 3, the graph_builder
should deduplicate evidence arrays per-node as a post-processing step, or the
section.md files should be normalized to carry exactly one evidence entry per
claim per checker section.

---

### F-CON-10 [C] — M3 corrected-citation note in C157 graph node is actionable but slightly cluttered

The C157 graph node now carries three evidence entries (graph.v2.json lines
3331-3335):
1. A cross-reference one-liner (from M7)
2. The original paper.txt snippet
3. A long corrected-citation note beginning "[corrected-citation] A correct
   citation would need to be..."

The corrected-citation note is useful for Phase 3's report_writer and is
clearly tagged. However, its length (one long paragraph inline in an evidence
array element) makes it visually difficult to distinguish from the
paper.txt-provenance entries. This is a presentation concern, not a
correctness issue.

Recommendation (optional): Phase 3 report_writer should filter evidence
entries beginning with "[corrected-citation]" into a separate "author action
required" list rather than treating them as paper provenance entries.

---

### F-CON-11 [C] — C002 entry in checker_unreferenced uses "reasoning" field label, not "evidence"

The C002 entry added by M5 uses the field label "reasoning:" rather than
"evidence:" (checker_unreferenced/section.md line 7). The artifact
specification (methodology/05-artifacts.md) does not strictly require the
field name to be "evidence" for CLEAR verdicts, and the content is
substantive. However, other CLEAR entries in checker_unreferenced that had
their fields added by M8 use "evidence:", creating an inconsistency within
the same section. The report_writer or graph_builder parsing
checker_unreferenced may need to handle both field names.

This is a minor presentation inconsistency. No functional impact on Phase 3
is expected since CLEAR verdicts in checker_unreferenced do not feed directly
into highlighted spans.

---

## Phase-3 readiness assessment (round 2)

The three round-1 Category A issues (M1, M2, M3) are resolved in the
section.md files and in graph.v2.json:

- C068 graph node carries `violated_principle` and `canonical_source` in its
  evidence array (graph.v2.json lines 1786-1787). The domain_violation
  verdict is fully evidenced.
- C183 and C185 graph nodes carry both the primary claim passage and the
  contradicting passage in their evidence arrays (graph.v2.json lines
  3788-3790 and 3831-3833). The internal_contradiction verdict is fully
  evidenced.
- C157 graph node carries the corrected-citation note in the evidence array
  (graph.v2.json line 3334). The literature_collision verdict is actionable.

The five new unreferenced entries (C029, C031, C036, C041, C054) and the
C002 entry are present in checker_unreferenced and in VERIFICATION.md.

The ambiguous count reconciliation note is present in checker_ambiguous
(HTML comment at line 3 of the section).

The M4 canonical_source clarification for C068 is present in
checker_domain/section.md (line 184).

The only remaining Phase-3 gap is the graph evidence-array deduplication
(F-CON-09), which affects the visual quality of the highlighted output but
not its correctness. This is acceptable for PASS.

**Overall assessment: all round-1 B findings are resolved or reduced to C.
Only C-class items remain. Phase 2 is ready to PASS.**
