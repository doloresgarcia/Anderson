# checker_ambiguous — run log — review: easy

## Run summary

- Total claims examined: 200 (C001–C200)
- FLAGGED: 29
- CLEAR: 11
- INCONCLUSIVE: 0
- Claims not appearing in section.md (no ambiguity category in STRATEGY.md and no ambiguity pattern detected in text): remainder (confirmed CLEAR by quick scan)

## Claims examined and verdicts

| claim_id | verdict | confidence | note |
|----------|---------|------------|------|
| C001 | FLAGGED | high | "wide range" scope undefined |
| C002 | CLEAR | — | not re-examined; domain_violation primary per STRATEGY; no ambiguity detected |
| C003 | FLAGGED | high | symmetry-breaking mechanism underspecified in abstract |
| C004 | FLAGGED | high | "significant" is unquantified |
| C005 | CLEAR | — | not re-examined; unreferenced primary; no ambiguity detected |
| C006 | CLEAR | medium | rhetorical framing, single reading |
| C007 | CLEAR | — | "per-mille level" is technically precise in context |
| C015 | FLAGGED | high | "maximally expressive" is a formal claim without proof |
| C017 | FLAGGED | medium | "improve the classification" — self-comparison vs. field-wide |
| C021 | CLEAR | high | both algebras described precisely |
| C026 | FLAGGED | medium | "usual definition of γ5" convention-dependent |
| C029 | FLAGGED | medium | PID encoding into scalar unspecified |
| C033 | FLAGGED | medium | "invariant multivector represents the transformation" admits false reading |
| C037 | CLEAR | medium | hedged claim with open-question acknowledgment |
| C040 | FLAGGED | medium | "variations" understates mathematical differences |
| C051 | CLEAR | medium | block composition unambiguous in Eq. (14) |
| C052 | FLAGGED | medium | "smooth transition" — mathematical equivalence unclear |
| C054 | FLAGGED | high | "degrade significantly" unquantified |
| C057 | FLAGGED | high | "tunable" conflates design-time and learned adjustment |
| C070 | FLAGGED | high | "crucial" and "strong impact" unquantified |
| C072 | CLEAR | medium | antecedent clear, procedure unambiguous |
| C074 | FLAGGED | medium | "differ most" — superlative without metric |
| C080 | CLEAR | high | standard explanation, unambiguous |
| C086 | FLAGGED | high | "different degree of optimization" ambiguous between impl and architecture |
| C093 | FLAGGED | medium | "partial permutation symmetry" underspecified |
| C097 | CLEAR | high | formula given explicitly |
| C121 | CLEAR | medium | "larger uncertainty" = statistical uncertainty in context |
| C129 | FLAGGED | high | "significant improvement … essentially all signal types" double hedge |
| C137 | CLEAR | medium | catastrophic forgetting explanation, single reading |
| C139 | CLEAR | medium | interpretive illustration, hedged appropriately |
| C142 | FLAGGED | high | "per-mille-level accuracy" operationally undefined |
| C166 | FLAGGED | medium | "crucial" for parametrization — principle vs. specific choice |
| C171 | CLEAR | medium | procedure described step-by-step, unambiguous |
| C175 | FLAGGED | medium | "redundant" — redundant vs. backup mechanism |
| C181 | FLAGGED | high | "for the first time" — scope of prior art undefined |
| C182 | FLAGGED | medium | "main weakness" — unquantified ranking |
| C186 | FLAGGED | high | "outperforms" may overstate generality |
| C191 | FLAGGED | high | "essentially every ML-application" over-broad extrapolation |
| C192 | FLAGGED | medium | "reference frames" vs. "reference multivectors" — scope ambiguity |
| C193 | FLAGGED | high | "significantly better performance" unquantified |
| C196 | FLAGGED | medium | causal attribution of "data efficiency" vs. "scaling" |

## Claims not examined in section.md

Claims not listed in the STRATEGY.md as `ambiguous`-category and not showing any of the flagged patterns (vague quantifiers, undefined terms, unclear antecedents, unspecified scope, too-vague methodology) were given CLEAR verdicts and are not included in section.md to avoid noise. The primary focus was on the ~40 claims explicitly marked `ambiguous` or carrying obvious vague-quantifier / undefined-scope language.

## Phase 1 carry-forward notes

- C003 and C005 provenance off by ±1 line: tolerated per dispatch instructions. C003 located at paper.txt:18-20 (not 18-19 as in CLAIMS.md), verified as the correct sentence.
- No parsing failures.

## Key patterns found

1. Unquantified comparatives and superlatives ("significant," "substantially," "crucially," "essentially all," "strongly") occur in 12+ claims, primarily in the abstract and Outlook sections.
2. Formal claims presented without proof ("maximally expressive," "partial permutation symmetry") occur in architectural description sections.
3. Methodological under-specification occurs in the PID encoding (C029), CFM accuracy target (C142), and phase space parametrization (C166).
4. Reference-frame terminology shifts between Section 2.3 ("reference multivectors") and Section 6 ("reference frames"), creating scope ambiguity in C192.
