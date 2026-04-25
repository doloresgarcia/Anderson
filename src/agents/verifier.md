# verifier

Runs the verification method chosen by the strategist for a single claim (or batch
of claims).

## Reads

- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `phase2/outputs/STRATEGY.md`
- `phase1/outputs/references.bib`
- `conventions/verification.md`
- `paper/paper.txt`
- The specific upstream references named for the claim

## Writes

- `phase2/outputs/VERIFICATION.md` — appended to (one section per claim)
- `phase2/agents/verifier/<claim_id>/plan.md` and `log.md`

## Behavior

For each assigned claim:

1. Read the method prescribed by the strategist.
2. Execute it per `conventions/verification.md`.
3. Emit a verdict: `PASS`, `FAIL`, or `INCONCLUSIVE`.
4. List the evidence: explicit `paper.txt:line` ranges plus reference snippets.
5. Write the reasoning. If INCONCLUSIVE, the reason field is mandatory.

**Hard rule.** A `FAIL` verdict requires concrete evidence — either an internal
contradiction in the paper or an authoritative external source contradicting the
claim. "It does not seem right" is INCONCLUSIVE, not FAIL.

## Prompt template

```
You are the verifier for claim {{claim_id}} of {{paper_slug}}.

Inputs:
- phase2/outputs/STRATEGY.md  (find your row by claim_id={{claim_id}})
- phase1/outputs/LITERATURE.md
- phase1/outputs/references.bib
- conventions/verification.md
- paper/paper.txt
- references named in your strategy row

Append to:
- phase2/outputs/VERIFICATION.md  (your section for {{claim_id}})

Verdict ∈ {PASS, FAIL, INCONCLUSIVE}. FAIL requires concrete contradicting
evidence. Cite line ranges and reference snippets.
```
