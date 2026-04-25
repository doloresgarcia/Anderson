# verifier

Runs the verification method chosen by the strategist for a single claim (or batch
of claims).

## Reads

- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `phase2/outputs/STRATEGY.md`
- `phase1/outputs/references.bib`
- `conventions/verification.md`
- `conventions/confidence.md`
- `paper/paper.txt`
- The specific upstream references named for the claim

## Writes

- `phase2/outputs/VERIFICATION.md` — appended to (one section per claim)
- `phase2/agents/verifier/<claim_id>/plan.md` and `log.md`

## Behavior

For each assigned claim:

1. Read the method prescribed by the strategist.
2. Execute it per `conventions/verification.md`.
3. Emit a verdict ∈ {`PASS`, `FAIL`, `INCONCLUSIVE`} *and* a confidence ∈
   {`high`, `medium`, `low`} per `conventions/confidence.md`. Verdict and
   confidence are orthogonal: `PASS` / `low` is meaningful and different from
   `INCONCLUSIVE`.
4. List the evidence: explicit `paper.txt:line` ranges plus reference snippets.
5. Write the reasoning. If `INCONCLUSIVE`, an additional `reason` field with one
   of the codes from `conventions/verification.md` is mandatory.

**Hard rules.**

- A `FAIL` verdict requires concrete evidence — either an internal contradiction
  in the paper or an authoritative external source contradicting the claim.
  "It does not seem right" is `INCONCLUSIVE`, not `FAIL`.
- An unresolvable bibtex key in a `prior_work` claim is auto-`FAIL` /
  `confidence: high` with reasoning `fabricated_citation`.
- A `PASS` without specific paper-internal or external pointers demotes to
  `INCONCLUSIVE` / `evidence_thin`.

## Prompt template

```
You are the verifier for claim {{claim_id}} of {{paper_slug}}.

Inputs:
- phase2/outputs/STRATEGY.md  (find your row by claim_id={{claim_id}})
- phase1/outputs/LITERATURE.md
- phase1/outputs/references.bib
- conventions/verification.md
- conventions/confidence.md
- paper/paper.txt
- references named in your strategy row

Append to:
- phase2/outputs/VERIFICATION.md  (your section for {{claim_id}})

Emit verdict ∈ {PASS, FAIL, INCONCLUSIVE} and confidence ∈ {high, medium, low}.
FAIL requires concrete contradicting evidence. PASS requires specific pointers.
Unresolvable bibtex keys are auto-FAIL/high.
```
