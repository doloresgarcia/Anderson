# Constructive Review — Phase 3 Round 2 (post-fixer)
## Review slug: easy

---

## Round 1 finding resolutions

### B-1: REPORT omitted 3 INCONCLUSIVE internal_contradiction claims
**Status: RESOLVED**

REPORT.md now contains a dedicated "INCONCLUSIVE verdicts under `internal_contradiction`" subsection within the Inconclusive section (lines 296–303). All three claims are documented with full provenance, reasoning, and explicit INCONCLUSIVE reasons:
- C077 (channel-counting arithmetic ambiguity)
- C112 ("new record" fine-tuned vs. non-fine-tuned ambiguity)
- C195 ("more than three particles" gluon-vs-total ambiguity)

The explanations are clear and complete.

### B-2: graph.final.json missing paper metadata
**Status: RESOLVED**

The `paper` block at lines 2–7 of graph.final.json now contains:
```
"title": "A Lorentz-Equivariant Transformer for All of the LHC"
"arxiv": "2405.14806"
```

### B-3: Edge E021 invalid provenance
**Status: RESOLVED**

E021 now carries `"provenance": "paper.txt:1660-1661,1928"` — the comma-separated multi-location format is correct and both locations correspond to the C183 and C185 claim sites respectively.

### B-4: Trust score formula absent from REPORT
**Status: RESOLVED**

REPORT.md line 54 now reads: "The score is computed as (CLEAR × 1.0 + INCONCLUSIVE × 0.5 + FLAGGED × 0.0) / (number of checked claims) × 100; NOT_CHECKED claims are excluded from the denominator. Buckets: ≥85 = high trust, ≥60 = medium trust, <60 = low trust." The formula is clear and bucket thresholds are stated.

### C-1: 0 hedged claims unaddressed
**Status: NOT ADDRESSED**

STATS.md still shows 0 hedged / 200 not hedged. No comment was added to explain why a paper with phrasing like "roughly on par," "essentially every," and "for the first time" yields zero hedged claims. The round-1 finding stands as a presentation gap: readers cannot tell whether the extractor actively evaluated hedging and found none, or whether hedging detection was not implemented.

### C-2: Ambiguous section needs sub-grouping
**Status: NOT ADDRESSED**

The ambiguous section lists 28 claim entries sequentially with no thematic sub-grouping. The round-1 finding stands as a readability gap.

### C-3: Coverage gaps lack type breakdown
**Status: NOT ADDRESSED**

The Limitations/Coverage gaps subsection still refers only to raw counts ("112 of 200 claims are UNCOVERED in LITERATURE.md") without breakdown by claim type. The round-1 finding stands.

### C-4: Source path wrong (merged with critical F5)
**Status: NOT ASSESSED HERE**

This was a critical_reviewer finding (F5) merged into the C-4 note. The REPORT now correctly states `reviews/easy/paper/paper.pdf` as the source on line 11. Source path appears corrected.

---

## New findings (round 2)

### [B] Ambiguous section header count inconsistent with STATS and Closing

**Category B** — misinformation risk for downstream readers.

REPORT.md line 116 states "**28 claims flagged**" for the ambiguous section. However:
- STATS.md records 27 FLAGGED for `ambiguous`
- The Closing summary (line 334) states "27 ambiguous claims"

Counting the claim entries in the ambiguous section body: 28 entries are listed, but C157 is a cross-reference with no independent content ("See literature_collision section above"). This suggests C157 is flagged in both `ambiguous` and `literature_collision` categories — which is valid — but the section count should then either (a) read "28 claims flagged (including C157 which is also flagged as literature_collision)" or (b) be "27 unique additional ambiguous claims" with C157 excluded from the count since it is covered in full above. The current state is internally inconsistent: the section header (28) disagrees with STATS.md (27) and the Closing (27). The fixer did not address this because it predates round 1; it appears to have been present throughout.

This is a presentation error that should be reconciled: either update the section header to 27 and note C157 is double-flagged, or update the Closing and STATS to 28. The Closing summary is the highest-visibility text, so the inconsistency creates reader confusion about how many distinct ambiguous claims exist.

---

## Summary

| Finding | Status |
|---------|--------|
| B-1: INCONCLUSIVE internal_contradiction documented | RESOLVED |
| B-2: graph.final.json paper metadata added | RESOLVED |
| B-3: E021 provenance corrected | RESOLVED |
| B-4: Trust score formula added | RESOLVED |
| C-1: 0 hedged claims unexplained | NOT ADDRESSED (non-blocking) |
| C-2: Ambiguous section sub-grouping | NOT ADDRESSED (non-blocking) |
| C-3: Coverage gap type breakdown | NOT ADDRESSED (non-blocking) |
| C-4: Source path | RESOLVED (via critical fixer) |
| NEW B: Ambiguous count inconsistency (28 vs 27) | OPEN |

All four B-class findings from round 1 are resolved. Three C-class items remain unaddressed but are non-blocking. One new B-class finding is raised: the "28 claims flagged" header in the ambiguous section disagrees with STATS.md and the Closing summary (both say 27).
