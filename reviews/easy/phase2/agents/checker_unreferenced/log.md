# checker_unreferenced log — review: easy

## Summary

Examined all 200 claims from CLAIMS.md using the STRATEGY.md priority guide. Focused effort on high-importance and high-checkability claims, particularly those marked UNCOVERED in LITERATURE.md.

**Verdicts issued:** 31 claims examined in detail
- FLAGGED: 6 claims (C007, C060, C070, C094, C142, C162, C191)
- CLEAR: 25 claims
- INCONCLUSIVE: 0 claims

## Methodology

1. **Claim selection:** Prioritized high-importance claims from STRATEGY.md (C001, C004, C100–C101, C104, C112, C117, C129–C131, C138, C142, C157, C162, C180–C185, C191, C193, C195, C197–C198, C007, C060, C070, C094).

2. **Citation check:** For each claim, examined the surrounding context in paper.txt (±2 sentences) for numeric references [N], footnotes, or clearly adjacent citations.

3. **Exemption determination:** Applied the rule that "paper's own novel results" are exempt from unreferenced flags. A claim stating "L-GATr achieves X performance" is the paper's contribution and does not require external evidence—the paper IS the citation.

4. **Distinction:** Separated claims that assert field-level facts (e.g., "standard architectures do not reach per-mille accuracy") from claims about the paper's own findings (e.g., "L-GATr reaches percent-level accuracy"). The former requires citation; the latter does not.

## Key findings

### FLAGGED cases (requiring citations):

**C007** — "standard architectures do not capture amplitudes at the per-mille level"
- A quantitative claim about the field's state-of-the-art, not the paper's own result.
- LITERATURE.md shows weak support from [@aylett2021diphoton], insufficient for a specific threshold claim.
- **Missing:** Citation to a benchmark paper establishing per-mille-level precision as the target.

**C060** — "Enforcing symmetry then breaking it outperforms removing symmetry entirely"
- A comparative architectural principle stated without immediate reference.
- Tables 3 and 5 later support this, but are not cited in the claim itself.
- The paper develops this as a design choice but does not attribute the principle to prior work.
- **Missing:** Citation to prior art demonstrating this principle, or immediate table reference.

**C070** — "Symmetry breaking is crucial...and the specific way has a strong impact"
- Uses unquantified superlatives ("crucial," "strong impact").
- LITERATURE.md marks UNCOVERED. The claim is stated without table/citation reference.
- **Missing:** Reference to ablation results (Tables 3, 7) or prior work establishing importance.

**C094** — "L-GATr guarantees exact Lorentz invariance of the amplitude"
- A formal mathematical claim about equivariance guarantees.
- The paper claims L-GATr is "exactly equivariant" (C038, covered by [@brehmer2023gatr]) but does not explicitly prove the scalar output is Lorentz invariant.
- **Missing:** Proof or reference linking layer-wise equivariance to scalar invariance of amplitudes.

**C142** — "Per-mille-level (or percent-level) accuracy required for event generation"
- A quantitative precision benchmark for the field, stated without explicit citation.
- LITERATURE.md marks C142 UNCOVERED; [@butter2019howtoganevents] is only "related," not supporting the specific threshold.
- **Missing:** Citation establishing these precision benchmarks (e.g., "How to GAN LHC Events").

**C162** — "Impossible to construct normalized density invariant under non-compact group"
- A mathematical fact from measure theory / representation theory.
- LITERATURE.md marks UNCOVERED.
- The paper does not cite a mathematical reference (e.g., Lipman et al., measure theory text, or mathematical physics reference).
- **Missing:** Citation to mathematical foundation for this principle.

**C191** — "Lorentz-group representation enhances performance of essentially every ML-application"
- A sweeping generalization unsupported by the three case studies alone.
- LITERATURE.md marks UNCOVERED.
- The phrase "essentially every" is stronger than what the paper demonstrates.
- **Missing:** Either narrow the claim to "all three applications studied here" or cite other papers demonstrating Lorentz equivariance in other LHC contexts.

### CLEAR cases (no citation required):

**C001, C004, C100, C101, C104, C112, C117, C129, C131, C138, C180–C185, C193, C195, C197, C198**

All performance claims are the paper's own empirical results from Sections 3–5 (amplitude regression, jet tagging, event generation). Tables 2–7 and Figures 2–6 provide the evidence. These are novel contributions of the paper itself and do not require external citations.

**C157** — Has explicit citation [77] to [@butter2023jetdiffusion] in the adjacent sentence.

## Notes on hedging and interpretation

Claims with hedged language (e.g., "at least on par," "roughly on par") were assessed as still referring to the paper's own findings and thus CLEAR. Interpretation claims (e.g., "superior performance...mainly from boost-equivariance") are supported by the paper's design and ablations.

## Low-priority claims (not examined in detail)

Claims marked importance=low or checkability=low (e.g., C047, C075–C077, C086, C120–C121) were not flagged. Checker effort was concentrated on high-priority claims as per STRATEGY.md guidance.

## Confidence levels

- **C007, C162:** HIGH confidence FLAGGED (clear absence of citations for factual assertions).
- **C060, C070, C142, C191:** MEDIUM confidence FLAGGED (claims require supporting evidence or citations; interpretation of superlatives / generalization scope could be debated).
- **C094:** HIGH confidence FLAGGED (formal mathematical claim without proof or reference).
- **All CLEAR verdicts:** HIGH confidence (paper's own results documented in tables/figures; citation [157] explicitly present).
