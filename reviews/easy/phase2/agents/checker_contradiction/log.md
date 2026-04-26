# checker_contradiction — log

## Review slug: easy
## Paper: A Lorentz-Equivariant Transformer for All of the LHC (L-GATr)
## Date: 2026-04-26

## Claims examined: All 200 (C001–C200)

## Method

1. Read all claims from CLAIMS.md and their provenance in paper.txt.
2. Read strategy guidance from STRATEGY.md (contradiction-priority clusters).
3. Read all relevant paper sections (abstract, Sec. 2–6, appendix, tables).
4. Compared claims pairwise and against tables/figures for numeric consistency.
5. Checked abstract-vs-results alignment for C001, C004.
6. Checked C183/C185 for consistency of performance characterizations.
7. Checked C112/C117/C138 for jet tagging headline consistency.
8. Checked C077/C078 for parameter and channel count arithmetic.
9. Checked C069 against Tables 3 and 7 for reference vector insertion mode.

---

## Key investigations

### Abstract vs. amplitude regression (C004 vs. C101) — FLAGGED

- Abstract (line 22-23): "For all three LHC tasks, we find significant improvements over previous architectures."
- Section 3 (lines 750-751): "L-GATr is roughly on par with the leading DSI network for a small number of gluons."
- Verdict: FLAGGED. The abstract's universal "significant improvements" claim cannot be reconciled with the Section 3 explicit qualification that L-GATr is only "roughly on par" at low multiplicities (Z+1g, Z+2g). The improvement exists only at higher multiplicities.

### Performance hierarchy in Section 5 (C183 vs. C185) — FLAGGED

- Line 1660-1661, 1926: "clear performance improvement as symmetry awareness increases...to the rotation-equivariant GATr and the Lorentz-equivariant L-GATr"
- Line 1928: "the rotation-equivariant E(3)-GATr performs only marginally better than the plain transformer"
- Verdict: FLAGGED. "Clear performance improvement" at the transformer→GATr step is directly contradicted by "only marginally better" for the same comparison, in the same paragraph.

### Jet tagging headline (C112 "new record" vs. C117 "at least on par") — INCONCLUSIVE

- These refer to different experimental configurations: C117 is non-fine-tuned (already in Ref. [35]), C112 is the fine-tuned result (new to this paper). The tension is real but interpretable. Marked INCONCLUSIVE.

### Channel count arithmetic (C077: 8 mv + 16 scalar = 72) — INCONCLUSIVE

- The paper states that "8 multivector channels and 16 scalar channels" achieve "72 total attention input channels." Straightforward arithmetic gives 8×16 + 16 = 144 components (if each mv is decomposed) or 8 + 16 = 24 channels — neither equals 72. However, L-GATr may use a non-standard channel-counting convention for the attention that is not defined in the text. Marked INCONCLUSIVE.

### Reference vector mode (C069 vs. Tables 3 & 7) — CLEAR

- Section 2.3 (line 555) says jet tagging uses extra tokens, generation uses extra channels. Table 3 confirms Token as default for tagging; Table 7 confirms Channel as default for generation. Consistent.

### Amplitude regression: data efficiency (C104 vs. C101) — CLEAR

- C104 is about training-data-scaling performance (right panel of Fig. 2), C101 is about multiplicity-scaling performance (left panel). They address different axes and are not contradictory.

### Parameter counts (C078) — CLEAR

- Parameter counts (L-GATr: 2.3×10^4, Transformer: 6.7×10^5, CGENN: 2.5×10^4) appear only once in the paper and are not repeated or contradicted elsewhere.

### Lorentz equivariance in experiments (C002 vs. C069/C118) — CLEAR

- C002 describes the base architecture property. The experiments deliberately and consistently describe when equivariance is broken. The paper does not claim the deployed configurations are always fully equivariant; it claims the architecture is capable of equivariance, which is accurate.

---

## Claims with no contradiction found (CLEAR)

C001, C002, C003, C038, C060, C065, C069, C078, C081, C082, C084, C094, C101, C104, C117, C119, C129, C130, C131, C138, C148, C180, C184, C193, C197, C198, and all claims C005–C037, C039–C059, C061–C064, C066–C068, C070–C100, C102–C111, C113–C116, C120–C128, C132–C147, C149–C179, C181–C182, C186–C200 (checked for contradiction; none found beyond those explicitly noted above).

---

## Summary of verdicts

| Verdict | Count | Claims |
|---------|-------|--------|
| FLAGGED | 2 | C004, C183 (C185 is reciprocal of C183) |
| INCONCLUSIVE | 3 | C077, C112, C195 |
| CLEAR | 195+ | all remaining |

Note: C185 is flagged as the reciprocal party to the C183 contradiction.
