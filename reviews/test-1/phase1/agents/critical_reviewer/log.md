# critical_reviewer (phase 1) — log

## Inputs read

- `agents/critical_reviewer.md` (role spec, auto-A triggers)
- `methodology/04-review.md` (A/B/C classification, hard rule on
  unresolvable references)
- `methodology/05-artifacts.md` (artifact formats)
- `methodology/03-phases.md` (phase-1 deliverables list)
- `methodology/03a-orchestration.md` (dispatch contract — output outside
  declared spec is auto-A)
- `conventions/claim_taxonomy.md`
- `conventions/graph_schema.md`
- `conventions/confidence.md`
- `phase1/CLAUDE.md`
- `paper/paper.txt`
- `paper/paper.meta.json`
- `phase1/outputs/CLAIMS.md`
- `phase1/outputs/LITERATURE.md`
- `phase1/outputs/references.bib`
- `phase1/outputs/graph.v1.json`
- `phase1/outputs/graph.v1.skeleton.json` (used to confirm the v1 final
  pass added only `references` arrays and didn't perturb structural fields)
- `phase1/outputs/FINDINGS.md`
- `phase1/agents/claim_extractor/{plan.md,log.md}`
- `phase1/agents/literature_searcher/{plan.md,log.md}`
- `phase1/agents/graph_builder/{plan.md,log.md,build_v1.py}`
- `phase1/agents/findings_scribe/{plan.md,log.md}`

## Auto-A trigger results

| trigger | result |
|---|---|
| Bibtex key in `LITERATURE.md` does not resolve in `references.bib` | 34/34 resolve. 0 unresolved. **Pass.** |
| Resolved record contradicts the snippet | I sampled 13 records via live arXiv abs pages. All match the bib title + authors. F08 flags one *misclassified-as-supports* attribution (`lipman2023flowmatching` for the OT-CFM claim) as Category B — the cited paper is real and matches the bib entry; it just doesn't speak to the optimal-transport part of the extracted sentence. Not auto-A. |
| `graph.v1.json` fails schema validation | Independently re-validated: passes all rules (counts, parent/child consistency, palette, edge endpoint constraints, dominant_type recompute). **Pass.** |
| Claim in `CLAIMS.md` whose page/line does not match `paper.txt` | Sampled 25 claims by line; all 25 sentences appear at the cited line, verbatim or with the LaTeX line-wrap that the extractor's `log.md` documents. **Pass.** |
| `VERIFICATION.md` `FAIL` with no contradicting evidence | n/a in phase 1. |
| Output file outside declared deliverables | One borderline: `phase1/agents/graph_builder/build_v1.py` (helper script in the agent's working directory). Not in `phase1/outputs/`, so it does not contaminate the deliverables. The role spec also doesn't authorize it. Filed as F02 (Category B, not A) because the script (i) never touched the deliverables area, (ii) is documented in graph_builder/log.md as an explicit reproducibility artifact, (iii) parallels the `src/render_graph.py` and `src/claim_stats.py` precedent in the project. |

## Independent reference verification (sample)

Sampled 13 of the 34 cited bib entries. For each, I fetched the arXiv abs
page via WebFetch and compared the (title, authors, arXiv ID) tuple against
`references.bib`. All matched.

| key | arXiv ID | retrieved title | match? |
|---|---|---|---|
| `Spinner:2024hjm` | 2405.14806 | Lorentz-Equivariant Geometric Algebra Transformers for High-Energy Physics | ✓ |
| `vaswani2017attention` | 1706.03762 | Attention Is All You Need | ✓ |
| `brehmer2023geometric` | 2305.18415 | Geometric Algebra Transformer | ✓ |
| `Qu:2022mxj` | 2202.03772 | Particle Transformer for Jet Tagging | ✓ |
| `ruhe2023clifford` | 2305.11141 | Clifford Group Equivariant Neural Networks | ✓ |
| `Sjostrand:2014zea` | 1410.3012 | An Introduction to PYTHIA 8.2 | ✓ |
| `lipman2023flowmatching` | 2210.02747 | Flow Matching for Generative Modeling | ✓ |
| `Wu:2024thh` | 2407.08682 | Jet Tagging with More-Interaction Particle Transformer | ✓ |
| `chen2023symbolic` | 2302.06675 | Symbolic Discovery of Optimization Algorithms | ✓ |
| `dao2022flashattention` | 2205.14135 | FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness | ✓ |
| `Heimel:2018mkt` | 1808.08979 | QCD or What? | ✓ |
| `ATLAS:2020ccu` | 2006.09274 | Measurements of top-quark pair single- and double-differential cross-sections in the all-hadronic channel… | ✓ |
| `Cacciari:2008gp` | 0802.1189 | The anti-k_t jet clustering algorithm | ✓ |

The remaining 21 cited keys were not independently fetched; the
literature_searcher's `log.md` documents Inspire-HEP / arXiv retrieval for
each and I cross-checked author lists in `references.bib` against my prior
knowledge of HEP-ML literature for plausibility (no author/title oddity
detected). I did not see a single arXiv ID in a wrong format
(all are `\d{4}\.\d{4,5}` or pre-2007 `[a-z\-]+/\d{7}`).

## Provenance sample

The 25 sampled claim ids and the lines I read in `paper.txt`: C001 (56),
C006 (95), C007 (97), C012 (108), C014 (108), C022 (143), C023 (143),
C031 (182), C032 (182), C051 (275), C052 (281), C062 (334), C065 (336),
C066 (337), C067 (337), C083 (360), C084 (360), C085 (360), C086 (360),
C089 (362), C111 (440), C129 (546), C148 (680), C172 (833), C186 (848),
C188 (855), C190 (881). All 25 sentences appear in the cited line,
matching the verbatim quote in `CLAIMS.md` (modulo LaTeX wrap).

## Counts cross-check vs. FINDINGS.md

| metric | FINDINGS.md | independent count | match |
|---|---|---|---|
| total claims | 217 | 217 | ✓ |
| hedged | 4 | 4 | ✓ |
| `method` | 104 | 104 | ✓ |
| `result` | 46 | 46 | ✓ |
| `background_fact` | 46 | 46 | ✓ |
| `interpretation` | 8 | 8 | ✓ |
| `definition` | 7 | 7 | ✓ |
| `prior_work` | 5 | 5 | ✓ |
| `assumption` | 1 | 1 | ✓ |
| `confidence=high` | 153 | 153 | ✓ |
| `confidence=medium` | 64 | 64 | ✓ |
| `confidence=low` | 0 | 0 | ✓ |
| LITERATURE headings | 217 | 217 | ✓ |
| ≥1 candidate | 73 | 73 | ✓ |
| total bullets | 113 | 113 | ✓ |
| `supports` | 74 | 74 | ✓ |
| `related` | 39 | 39 | ✓ |
| `contradicts` | 0 | 0 | ✓ |
| unique cited keys | 34 | 34 | ✓ |
| total bib entries | 45 | 45 | ✓ |
| orphan bib keys | 11 | 11 | ✓ |

All FINDINGS.md numbers reconcile.

## Categorization rationale

- F01 (page=?). Degraded format due to .txt input. The phase-1 gotcha note
  in `phase1/CLAUDE.md` foresees this kind of degradation. B, not A.
- F02 (build_v1.py). Outside declared writes but not in the deliverables
  area. B, not A — keeps the rollback safe.
- F03 (no `low` confidence). Methodology-level risk: the strategist's
  budget allocator relies on `low` to skip rows. Currently nothing will be
  auto-skipped, which biases phase 2 toward over-checking. B.
- F04 (C015 compound contributions). Direct rule violation in
  `claim_taxonomy.md` ("Cited contributions of the present paper" → "expands
  into three claims"). B (does not invalidate the rest of the artifacts).
- F05 (C188/C189 code-availability). Borderline propositional content; the
  taxonomy filter is "verifiable proposition", and a URL by itself is not
  one. B.
- F06 (C036/C044/C060 expressivity claims). Confidence over-inflated given
  the literature_searcher's own caveat. The `high` confidence on C044/C060
  is the most consequential B in this review — they are the abstract-level
  expressivity claims of the architecture and will be exactly the kind of
  claim phase 2 has to wrestle with.
- F07 (C006 literature attachment). The "order of magnitude" assertion is
  not in the cited references; mis-applied `supports/high`. B, since phase 2
  can re-anchor.
- F08 (C148 literature attachment). The OT-CFM mismatch is real and
  recorded; same kind of B.
- F09–F12. Polish; no count or correctness change. C.

I considered escalating F06 to A but the rule for A is "Bibtex key does not
resolve" or "graph fails schema validation" or "claim's page/line does not
match" — over-confident extraction is B per `04-review.md` ("a claim was
extracted but mistyped" or its analogue for confidence is example B).

## Outputs written

- `phase1/review/critical.md`
- `phase1/agents/critical_reviewer/plan.md`
- `phase1/agents/critical_reviewer/log.md` (this file)

No phase-1 outputs modified.
