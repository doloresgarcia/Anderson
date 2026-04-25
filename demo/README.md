# Anderson demo — EfficientFlow

A planted-issue paper that *looks* like a credible 1-page ML manuscript and
contains three problems by design:

1. **Numerical inconsistency.** The abstract claims 87.3% F1 on GLUE; the
   results section reports 78.4% average. `checker_contradiction` catches
   this and flags **both** ends of the contradiction
   (**C001 → FLAGGED [internal_contradiction]** and
   **C009 → FLAGGED [internal_contradiction]**).
2. **Fabricated citation.** The introduction cites `Chen et al. (2024)` /
   `[chen2024sparse]`, which doesn't resolve to any real record.
   `checker_literature` flags this with `confidence: high`
   (**C004 → FLAGGED [literature_collision]**).
3. **Discussion overreach.** "We thus prove that sparsity is sufficient for
   emergent reasoning." `checker_ambiguous` flags the formal-vs-colloquial
   ambiguity of "prove" against the absence of any proof
   (**C013 → FLAGGED [ambiguous]**), and the abstract-side version of the
   same overreach is flagged for missing citation
   (**C005 → FLAGGED [unreferenced]**).

The demo also contains seven legitimate claims (architecture, well-known
background fact, internally-consistent memory numbers, one hedged
interpretation) that all five checkers report `CLEAR`, plus one
INCONCLUSIVE on the "0.4% improvement over baseline" claim because the
baseline reference number isn't given.

## Run it

From the repo root:

```bash
make demo
```

This scaffolds `reviews/__demo__/`, copies in the bundled CLAIMS.md and
VERIFICATION.md, and runs the renderers. Outputs land in
`reviews/__demo__/phase3/outputs/`:

- `paper.highlighted.pdf` — the paper with the cover-page trust score and
  per-highlight comments.
- `graph.final.html` — interactive Cytoscape.js claim graph.
- `STATS.md` — counts, type×verdict matrix, INCONCLUSIVE reasons.

## What gets shipped here

- `paper.txt` — the planted-issue paper.
- `CLAIMS.md` — the expected phase-1 extraction output.
- `VERIFICATION.md` — the expected phase-2 verification output, with
  reasoning prose for each verdict (which surfaces as the comment on
  highlighted sentences in the PDF).
- `graph.v2.json` — pre-clustered into 6 groups so the Cytoscape view
  loads with the right structure.

The demo bundles these phase-1/2 outputs directly so judges can render
phase-3 deliverables without running Claude Code orchestration. To run the
*full* phase-1/2/3 pipeline on this paper through a real LLM, scaffold a
fresh review with `python3 src/scaffold_review.py --text demo/paper.txt
--slug efficientflow-real` and let Claude Code do the work.
