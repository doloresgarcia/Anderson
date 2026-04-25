# checker_contradiction — log

**Paper:** noah-test-v1 (L-GATr, arXiv:2312.07897)
**Run date:** 2026-04-25

---

## Scope

Checked all 418 prose claims for `internal_contradiction`. Focused detailed
attention on the 55 claims flagged as having `internal_contradiction` risk in
STRATEGY.md, plus the five high-priority patterns called out in the task spec.

## Verdicts summary

| Verdict | Count |
|---------|-------|
| FLAGGED | 3 (claim-0165, claim-0441, claim-0365) |
| CLEAR   | ~52 checked + all low-importance claims |
| INCONCLUSIVE | 0 |

---

## Pattern-by-pattern analysis

### 1. Abstract vs Results numbers (claim-0008)

Abstract says "significant improvements over previous architectures." Checked
against Tables 1, 3, 4 and Figs. 2, 4, 5.

- **JetClass (Table 3):** L-GATr beats ParT and MIParT on all 9 per-class
  rejection metrics and overall AUC. Supports "significant improvements."
- **Top tagging without fine-tuning (Table 1):** L-GATr* AUC = 0.9870 matches
  equivariant competitors (LorentzNet* 0.9868, PELICAN* 0.9870, CGENN* 0.9869)
  and beats non-equivariant ParT (0.9858) and MIParT (0.9868) marginally.
  "Significant" is a stretch here but the comparison set includes non-equivariant
  architectures which L-GATr does beat.
- **Amplitude regression (Fig. 2):** L-GATr leads at high multiplicity.
- **Event generation (Fig. 4/5):** L-GATr clearly outperforms all CFM baselines.

Verdict: CLEAR. "Significant improvements over previous architectures" is a
broad claim that holds for some comparison pairs; `ambiguous` is a better
category for the softness of "significant." No logical self-contradiction found
within the paper.

### 2. Numeric consistency across tables

- **Table 1 fine-tuned rows:** L-GATr-f.t. 1/εB(εS=0.5) = 651±11 vs
  ParT-f.t. = 691±15. The claim (line 620) says "matches across all metrics."
  → **FLAGGED** (claim-0365).
- **Dataset size (claims 0241/0244):** 2M total = 1.2 + 0.4 + 0.4M. Consistent.
- **JetClass 100M (claims 0525/0336):** Consistent.
- **L-GATr scaling config 2.3×10^4 (claim-0185) vs tagging 1.1×10^6
  (claim-0520):** Different configurations, explicitly stated. Not a
  contradiction.
- **CGENN scaling config 2.5×10^4 (claim-0186) vs amplitude CGENN 3.2×10^5
  (tab:amp_build):** Different configurations (single-block scaling test vs.
  full amplitude regression network). Not a contradiction.
- **LR ratio fine-tuning (claims 0532/0533):** 3×10^{-5} / 3×10^{-3} = 1/100
  factor. Internally consistent.

### 3. Parameter count claims

- Scaling test: L-GATr 2.3×10^4, transformer 6.7×10^5, CGENN 2.5×10^4
  (line 358). These are single-block configs for the scaling study, explicitly
  described as such. Consistent with the architectural description.
- Top tagging L-GATr: 1.1×10^6 (Table tab:top_build). Different from scaling
  test — consistent because different number of blocks (12 vs 1) and channels.

### 4. Pre-training / fine-tuning claim (claim-0365)

"L-GATr matches the performance of the best fine-tuned networks in the
literature across all metrics." Table 1 shows L-GATr-f.t. at 651±11 for
1/εB(εS=0.5) vs ParT-f.t. 691±15. The difference is ~40 at a combined σ≈19,
so roughly 2σ below ParT-f.t. on this metric. → **FLAGGED.**

### 5. Grade mixing (claims 0098/0099)

Both appear in the same sentence (line 230):
"Lorentz transformations will never mix grades. Each algebra grade transforms
under a separate sub-representation of the Lorentz group, although in practice
grade mixing can occur through the combined action of boosts and rotations on
composite multivector states."

The first clause applies to single-grade elements; the second clause explicitly
carves out composite multivector states (which are sums of different grades).
The two statements are logically compatible: the sandwich product vxv^{-1}
preserves grade for pure-grade x, but a composite multivector y = a + b
(grade-0 + grade-2) does not transform to a state of definite grade when v
induces grade mixing between a and b. The authors are making a precise technical
point. → CLEAR.

### 6. Symmetry breaking contradiction (claims 0165 vs 0441)

Line 341: "the network still performs comparably even with full Lorentz
equivariance" (for both tagging and generation).
Line 772: "including reference multivectors for both beam and time directions is
essential; omitting them leads to inferior performance."

Table 6 data: no-reference row has AUC = 0.996 (classifier can trivially
distinguish generated from real = terrible generator) vs default AUC = 0.514
(near-ideal). This is not "comparable" — it is a catastrophic failure. → **FLAGGED.**

The tagging case (Table 2): no-reference row gives AUC = 0.9846 vs default
0.9870. This difference (0.0024) is arguably "comparable" at a practical level,
and line 298 only says it "significantly contributes" rather than is essential.
So the contradiction is clearest for the generation case.

---

## Decisions

- Grade-mixing pair (claims 0098/0099): CLEAR. Both clauses in one sentence;
  logically compatible when parsed carefully. Raising this as a contradiction
  would require misreading the grammar.
- claim-0165 vs 0298: Not directly contradicted — claim-0165 says "performs
  comparably" and claim-0298 says "significantly contributes"; the tagging
  data in Table 2 shows meaningful but not catastrophic degradation without
  reference vectors. The generation data shows catastrophic degradation, which
  is captured by the 0165/0441 flag.
- Fine-tuning claim-0365: Flagged even though the AUC metric and the εS=0.3
  rejection metric both favor L-GATr-f.t. The εS=0.5 rejection metric clearly
  does not match the stated claim of "across all metrics."
