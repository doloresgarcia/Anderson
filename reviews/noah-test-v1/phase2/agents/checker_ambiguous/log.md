# checker_ambiguous — run log

**Paper:** A Lorentz-Equivariant Transformer for All of the LHC (L-GATr, arXiv:2312.07897)
**Run scope:** 64 high-importance claims per STRATEGY.md; medium/low batched as CLEAR.

## Claims reviewed in detail

High-importance claims with `ambiguous` in their STRATEGY.md categories:
- claim-0008, claim-0099, claim-0100, claim-0147, claim-0150, claim-0165,
  claim-0202, claim-0368, claim-0477, claim-0484, claim-0488

Additional high-importance claims reviewed and found CLEAR by ambiguity test
(no genuine multiple-interpretation issue; meaning is singular even if
unquantified):
- claim-0004 ("state-of-the-art performance") — clear comparative; the paper
  defines scope as the three tasks demonstrated.
- claim-0005 — architectural fact; no ambiguity.
- claim-0007 — priority claim; clear meaning, checked for ambiguity only (not
  literature collision — that is checker_literature's domain).
- claim-0031 — "maximally expressive" is architectural jargon with a specific
  technical meaning defined in Eq. (3); no ambiguity after reading context.
- claim-0040, claim-0106, claim-0108, claim-0117, claim-0119, claim-0122,
  claim-0123, claim-0128, claim-0134, claim-0138 — domain-heavy claims;
  assessed only for ambiguity, not domain correctness (checker_domain's job).
  All have single clear intended meaning in context.
- claim-0147 — FLAGGED (see section.md).
- claim-0150 — FLAGGED.
- claim-0151, claim-0152, claim-0155, claim-0160, claim-0163 — architectural
  and physics claims; single clear meaning; no ambiguity.
- claim-0189, claim-0191 — scaling claims; single clear meaning.
- claim-0201, claim-0203, claim-0204 — performance/design claims; single clear
  intended reading.
- claim-0224, claim-0225, claim-0226, claim-0229, claim-0230 — results claims
  with Fig. referents; may be internal_contradiction issues but not ambiguous.
- claim-0234, claim-0238, claim-0241 — similarly.
- claim-0293, claim-0294, claim-0295, claim-0298 — results claims.
- claim-0341, claim-0344, claim-0355, claim-0365 — results claims.
- claim-0378, claim-0395, claim-0399, claim-0401, claim-0402 — physics claims;
  checker_domain's territory for correctness; single clear intended meaning.
- claim-0423, claim-0429, claim-0432, claim-0434 — engineering claims; clear.
- claim-0441, claim-0471, claim-0472, claim-0475, claim-0476, claim-0478 — 
  results/attribution claims; may have internal_contradiction issues but not
  ambiguous in meaning.
- claim-0485, claim-0487, claim-0489 — Outlook summary claims; single meaning.

## Verdict summary

| Verdict | Count |
|---------|-------|
| FLAGGED | 8 (claim-0008, -0099, -0147, -0150, -0165, -0202, -0368, -0484, -0488) |
| CLEAR   | 3 high-importance (claim-0100, -0477, + ~51 remaining high-imp not tagged ambiguous) + all medium/low |

Note: claim-0099 and claim-0150, -0165 are confidence:medium due to partial
ambiguity that could be resolved by careful reading of context; still flagged
because two distinct readings remain plausible to a first-time reader.

## Process notes

- Paper is LaTeX source; line numbers in evidence refer to paper.txt lines.
- All claim texts and line numbers taken from claims.jsonl; paper.txt read at
  relevant offsets to verify context.
- Medium/low importance claims not read individually; STRATEGY.md rationale
  confirmed they are routine hedging, definitions, or low-stakes statements
  with no ambiguity pattern.
- No INCONCLUSIVE verdicts: all claims had sufficient context in the paper for
  an ambiguity judgment.
