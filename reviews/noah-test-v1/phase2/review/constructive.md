# Phase 2 Constructive Review

## Strengths

- **Internal contradiction findings are precise and high-impact.** The claim-0165/claim-0441 pair is the strongest finding in the report: the checker quotes both contradicting passages with line numbers, reproduces the key Table 6 numbers (NLL = 29.36 vs. −32.64), and explains exactly why they are incompatible. This is exactly the evidence standard the category requires.

- **claim-0365 is a well-calibrated falsification.** The checker computes the significance of the gap (691 ± 15 vs. 651 ± 11, difference > 2σ) rather than accepting the paper's "across all metrics" language at face value. The finding is concise, backed by table values, and correctly judges the verdict as FLAGGED rather than INCONCLUSIVE.

- **domain_violation checker is technically authoritative.** The flags on claim-0052 and claim-0099 cite primary sources (Doran & Lasenby, Lounesto) and state the correct algebraic facts. Flagging claim-0052 (same-grade commutativity) as a clear error rather than a nuance is the right call — this is a false statement.

- **literature_collision checker is appropriately conservative.** It correctly resolves all the high-importance competitor descriptions (LorentzNet, PELICAN, CGENN, ParT) as CLEAR and limits INCONCLUSIVEs to genuine bibliography gaps (missing cite-keys). Not over-flagging here avoids polluting the report with unverified claims.

## Potential false negatives

- **claim-0007 ("first Lorentz-equivariant generative network"):** The literature_collision checker notes this is filed as unreferenced/ambiguous rather than a literature_collision, but the checker does not attempt any external search to rule out earlier work. This is the highest-stakes priority claim in the paper and warrants at least an INCONCLUSIVE from checker_literature with a note that no external search was performed, not a blanket CLEAR.

- **claim-0031 ("maximally expressive linear map"):** The unreferenced checker flags this for missing citation, but checker_domain does not address it. "Maximal expressiveness" is a well-defined concept in the equivariant network literature (tied to the theory of steerable CNNs and tensor product representations); a domain checker should at minimum note whether the paper provides a proof or whether the claim is verifiable against the GATr literature (brehmer2023geometric). Currently only gets one flag when two categories apply.

- **claim-0402 ("not possible to construct normalized density invariant under non-compact group"):** Flagged as unreferenced but not reviewed by checker_domain. This is a non-trivial mathematical claim about Haar measure on non-compact groups; it is correct but a domain checker should have confirmed that explicitly rather than leaving it as "needs citation only."

- **claim-0098/claim-0099 tension (grade mixing):** checker_domain correctly flags claim-0099. However, claim-0098 ("Lorentz transformations will never mix grades") is marked CLEAR by checker_contradiction despite being logically upstream of the flagged claim-0099. If claim-0099 is a domain violation (grade mixing does not occur), then claim-0098 is actually correct — and the caveating language in claim-0099 is the error. The checker should have resolved this direction explicitly rather than leaving both claims in ambiguous standing.

- **Several high-importance performance claims (claim-0004, claim-0229, claim-0471, claim-0487, claim-0489)** were assigned to checker_contradiction in STRATEGY.md but appear as CLEAR in VERIFICATION.md with no explanation. The strategy specifically flagged these as needing table cross-checks; a dismissal with "CLEAR" without explanation is insufficient for high-importance claims.

## Calibration concerns

- **unreferenced count (24 FLAGGED vs. 18 reported in summary header):** The summary states 18 FLAGGED but a count of the entries in the unreferenced section yields 24. This is a bookkeeping error that reduces trust in the summary statistics.

- **claim-0018 and claim-0019 (confidence: medium, unreferenced):** These are standard background physics statements about symmetry structures in LHC data. Flagging claim-0018 ("much of this knowledge is reflected in complex symmetry structures") as requiring a citation is an overreach — this is common knowledge in the field. The evidence standard says "not common knowledge" is required for a flag; these arguably do not meet that bar.

- **claim-0294 (confidence: high, unreferenced):** The flag is warranted in principle, but the checker assigns it high confidence without noting that the claim is at least partially supported by the paper's own results (Table 1 shows ParT/MIParT outperforming L-GATr without fine-tuning at full data). The flag should note the partial in-paper support and explain why an external citation is still needed.

- **literature_collision CLEAR on claim-0007:** Given the paper makes a "first ever" claim, a CLEAR verdict requires either a literature search or explicit acknowledgment that one was not performed. Returning CLEAR here implies the checker verified no prior work exists, which it did not.

## Suggestions for the fixer (if ITERATE is called)

1. Fix the unreferenced summary header count (says 18, should be 24).

2. Demote claim-0018 from FLAGGED to CLEAR with a note that standard background physics statements about symmetry structures in HEP are field-common-knowledge.

3. Upgrade claim-0007 in checker_literature from CLEAR to INCONCLUSIVE, citing inability to perform external search to confirm the priority claim; recommend human verification.

4. Add a checker_domain finding for claim-0402 confirming (or qualifying) the mathematical statement about non-compact group measures — even a brief CLEAR with the Haar measure argument would close the gap.

5. Add a checker_domain or checker_unreferenced note on claim-0031 ("maximally expressive linear map") cross-referencing whether brehmer2023geometric contains the expressiveness proof.

6. For the high-importance claims in the internal_contradiction category that appear as CLEAR with no explanation (claim-0004, claim-0229, claim-0471, claim-0487, claim-0489), the checker should supply explicit table cross-checks rather than batch-dismissing them.

7. Clarify the claim-0098 direction: if checker_domain is correct that grade mixing does not occur (via the versor representation), then claim-0098 is correct and claim-0099 is the sole error. The current report flags claim-0099 from two checkers (ambiguous + domain_violation) while leaving claim-0098 as CLEAR, which is confusing.

## Overall assessment

The Phase 2 checkers produced a solid report anchored by three high-quality findings: the claim-0165/0441 internal contradiction (the most consequential finding, directly undermining a central conclusion), the claim-0365 table falsification, and two genuine domain errors in the geometric algebra exposition. The literature_collision checker shows appropriate restraint. The main weaknesses are a summary count error, mild over-flagging of background statements in the unreferenced section, a missed opportunity on the "first ever" priority claim, and insufficient explanation for several high-importance internal_contradiction claims that were dismissed without table cross-checks.
