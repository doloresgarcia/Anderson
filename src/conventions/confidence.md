# Confidence

A single discrete scale used across every Anderson artifact that needs to express
"how sure is the agent of this." Three levels, anchored differently per context.

## Why discrete

LLM-emitted continuous scores in [0, 1] are poorly calibrated — they pile up at
0.7 / 0.8 / 0.9 regardless of true confidence. Three discrete buckets with
explicit "you may say `high` only when X" criteria force the agent to actually
distinguish.

If you ever need to rank N claims with the same confidence, break ties on:

1. extraction order in the paper (earlier = higher prior)
2. presence of hedge words (no hedge → higher prior)
3. sentence length (shorter, denser → higher prior)

Do not introduce a continuous score to break ties.

## The three levels (general)

| level | meaning |
|---|---|
| `high` | direct, unambiguous evidence; agent would defend this without caveats |
| `medium` | evidence is present but required some interpretation or a choice between plausible readings |
| `low` | best guess; agent had to paraphrase, infer, or choose under genuine ambiguity |

Use `high` sparingly. The default for routine work is `medium`; `high` is reserved
for cases where the agent could quote the paper or a reference verbatim to defend
the call.

## Per-context anchors

### Claim extraction (`CLAIMS.md` row)

The extractor's confidence in (a) that this is a claim and (b) that the type is
correct.

- `high` — single-proposition sentence, unambiguous type, no hedging, the
  extractor copied the sentence essentially verbatim.
- `medium` — type sits between two categories (e.g. `result` vs `interpretation`),
  OR the row was split from a compound sentence, OR the propositional content is
  hedged.
- `low` — the extractor paraphrased substantially to make the proposition
  standalone, OR the sentence is grammatically ambiguous, OR the type is a
  judgment call between three or more types.

### Literature relevance (`LITERATURE.md` candidate row)

The literature_searcher's confidence that the candidate reference actually
addresses the claim.

- `high` — the reference's title or abstract directly addresses the claim's
  proposition; the quoted snippet contains the relevant assertion.
- `medium` — same domain and topic, but does not speak to the specific
  proposition; reading the full reference would be needed to confirm relevance.
- `low` — loosely related; same field or same object of study but the connection
  is conjectural.

This replaces the prior continuous `relevance 0.xx` float in the artifact spec.

### Verification verdict (`VERIFICATION.md` section)

The verifier's confidence in the assigned verdict (orthogonal to the verdict
itself — a `low`-confidence `PASS` is meaningful and different from
`INCONCLUSIVE`).

- `high` — direct, decisive evidence: a numerical contradiction, a canonical
  reference flatly disagreeing, an internal inconsistency the verifier can quote.
- `medium` — the evidence supports the verdict but requires some interpretation,
  OR the verifier had to pick between two plausible readings of the claim.
- `low` — verdict is the verifier's best guess; the evidence is thin, the method
  is partially applicable, or the relevant references are paywalled / not
  retrievable.

Note: the rule "a FAIL with no concrete contradicting evidence demotes to
INCONCLUSIVE" runs *before* confidence is assigned. So `low`-confidence FAIL is
allowed, but only when there is some concrete evidence — just less of it.

### Graph edges (`graph.v*.json`)

The graph_builder's confidence that an edge exists between two nodes.

- `high` — the relationship is stated explicitly in the paper or by a direct
  citation.
- `medium` — implied by the paper (e.g. by adjacency in the argument structure)
  but not explicitly stated.
- `low` — inferred by the agent from the surrounding context.

## How downstream uses confidence

- **Strategist** deprioritizes `low`-confidence extractions when allocating
  verifier budget. `low` claims are still listed in `STRATEGY.md`, but with
  method `skip` unless the user overrides.
- **Critical reviewer** scrutinizes `low`-confidence rows more carefully. A
  `high`-confidence claim with a verbatim sentence is rarely flagged; a
  `low`-confidence claim where the extractor paraphrased is often Category B.
- **Highlighter** does not encode confidence in PDF colors (kept binary
  red/yellow). Confidence is shown in the margin tooltip and in `REPORT.md`.
- **Report writer** mentions confidence in the "What we checked" section so the
  reader knows which findings are firm and which are tentative.

## When to override

Confidence is not free to invent at fix time. If a reviewer flags a row's
confidence as wrong, the fixer must justify the change in `log.md` with a
specific reason (e.g. "missed the `we suggest` hedge — demoting from high to
medium"). Silent up-grades are Category A.

## Storage

- `CLAIMS.md`, `LITERATURE.md`, `VERIFICATION.md`: a `confidence` column /
  field with literal value `high`, `medium`, or `low`.
- `graph.v*.json`: an edge property `"confidence": "high|medium|low"`.

No numeric encoding; the literal string is the value.
