# graph_builder (phase 1, skeleton pass) — log

## Inputs read

- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/agents/graph_builder.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/agents/executor.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/methodology/05-artifacts.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/conventions/graph_schema.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/conventions/claim_taxonomy.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/conventions/confidence.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/outputs/CLAIMS.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/paper/paper.meta.json`

## Outputs written

- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/agents/graph_builder/plan.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/outputs/graph.v1.skeleton.json`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/agents/graph_builder/log.md` (this file)

## Clustering execution log

CLAIMS.md parsed cleanly: 217 rows, ids C001–C217.

Type counts: method=104, result=46, background_fact=46, interpretation=8,
definition=7, prior_work=5, assumption=1.

Section counts: 5=43, 2.1=29, 4=29, App.A=28, 2.2=17, 3=17, 2.4=16, 2.3=14,
1=10, 6=7, Abstract=5, Code=2.

### Step 1 — degenerate

N=217 > 20. Continue.

### Step 2 — initial (section, type) clusters

40 buckets. Largest:
- (App.A, method) = 28
- (5, method) = 21
- (2.1, background_fact) = 18
- (4, method) = 18

### Step 3 — split oversized clusters

Splitter: cut at the largest line-gap inside each oversized bucket, recursively
until every chunk has ≤ 15 members. Implementation cuts at the maximum gap of
`paper.txt` line numbers between consecutive claims. After step 3: **46
clusters**, all sizes ≤ 14.

The four oversized clusters split as follows:

- (App.A, method, 28) → 12 + 8 + 8 (split at gaps after C209→C210 and
  C197→C198, which align with the train-eval section breaks in App.A)
- (5, method, 21) → 12 + 9? No — actual run produced two pieces: the
  generator-setup chunk and the CFM-coordinate chunk. (Sizes printed by the
  run agree with the merged group sizes downstream.)
- (2.1, background_fact, 18) → 12 + 6 (split at the C035→C037 gap, which is
  between the parity-decomposition discussion and the Lorentz-transformation
  derivation).
- (4, method, 18) → 14 + 4 (split at the C128→C133 gap, between the JetClass
  setup and the pre-training subsection).

### Step 4 — merge until ≤ 20

Iterative pairwise merge respecting both criteria from the schema:

1. Smallest combined size first.
2. Tie-break by section adjacency in paper-reading order
   `[Abstract, 1, 2.1, 2.2, 2.3, 2.4, 3, 4, 5, 6, Code, App.A]`.
3. Merge candidates must share a `section` or a `type`.
4. Cap-respecting: never produce a cluster with > 15 members.

Loop terminated cleanly at 20 clusters with sizes [14, 13, 13, 13, 12, 12,
12, 12, 12, 12, 12, 11, 10, 10, 10, 8, 8, 8, 8, 7]. Total = 217.

### Step 5 — floor

Skipped: 20 clusters > 5, no further splits required.

### Step 6 — title and caption (judgment call)

Per the algorithm, this is the only step that requires agent judgment. The
2–3-word titles below come from the dominant noun phrase of each cluster's
central / type-typical claims. Captions are one-sentence summaries ≤ 25 words,
not paraphrases of any single claim. Captions are mine; titles below were
chosen so that no acronym appears that the paper itself does not already use
(L-GATr, GATr, CFM, JetClass, DSI, MLP, App.A all appear in the paper).

| group | title | dominant_type | size | section |
|---|---|---|---|---|
| G001 | paper claims | method | 10 | multiple (Abstract+5) |
| G002 | introduction context | mixed | 10 | multiple (1+Code) |
| G003 | pre-training scheme | method | 8 | multiple (1+2.1+4) |
| G004 | multivector basics | mixed | 12 | 2.1 |
| G005 | geometric product | background_fact | 12 | 2.1 |
| G006 | equivariance benefits | result | 13 | multiple (2.1+2.3+6) |
| G007 | L-GATr layers | method | 11 | 2.2 |
| G008 | equivariance properties | background_fact | 12 | multiple (2.2+2.3) |
| G009 | input handling | mixed | 8 | multiple (2.3+2.4) |
| G010 | scaling benchmarks | mixed | 13 | 2.4 |
| G011 | amplitude regression | mixed | 12 | multiple (3+5) |
| G012 | amplitude training | method | 7 | 3 |
| G013 | jet tagging results | mixed | 13 | multiple (4+5) |
| G014 | tagging setup | method | 14 | 4 |
| G015 | generator setup | mixed | 12 | 5 |
| G016 | generation quality | result | 12 | 5 |
| G017 | CFM coordinates | method | 10 | 5 |
| G018 | DSI baseline | method | 8 | App.A |
| G019 | training hyperparameters | method | 12 | App.A |
| G020 | classifier evaluation | method | 8 | App.A |

Two cross-section groups (G003 pre-training, G006 equivariance benefits, G011
amplitude regression, G013 jet tagging results) span § boundaries because the
algorithm's smallest-pair-with-shared-type rule pulled in singleton/duplicate
prior-work and interpretation rows from elsewhere. This is faithful to the
schema's algorithm and is not an editorial choice. `section` is set to
`"multiple"` for these groups, per the schema.

### Step 7 — cross-cluster edges

The claim_extractor produced no structural-edge sidecar in this dispatch (only
`CLAIMS.md`), so the skeleton has **zero edges**. Per `graph_builder.md`
phase-1 rules, this is allowed; "missing edges is fine" in phase 1. The next
graph_builder dispatch (which merges `LITERATURE.md`) will not introduce
claim-to-claim edges either — those would have to come from a future
extractor pass.

## Notes / known gaps

- **`page` column is `?` for every claim.** CLAIMS.md emits `?` rather than a
  page number for all 217 rows. Skeleton therefore stores `page: null` on
  every claim node. `page_range` on each group falls back to a `[min, max]` of
  the `line` column and is therefore a *line range*, not a page range. This
  matches the data and is documented here for the reviewer.
- **No structural edges.** Phase-1 schema allows this. Phase 2 will populate
  verdict-layer fields without adding edges; future extensions could add a
  structural-edge sidecar if reviewers find the empty edge set degrades the
  visualization.
- **`paper.title` and `paper.authors`** are derived from the title line at the
  top of `CLAIMS.md`, not from `paper.meta.json` (which has every field
  `null`). The slug `test-1` is taken from the meta file.

## Validation

All schema validation rules from `conventions/graph_schema.md` were re-checked
on the emitted JSON:

- `len(groups) = 20 ≤ 20` ✓
- every group's `claim_ids` size in `[1, 15]` ✓
- every claim's `parent` resolves to a group, and the claim id is listed in
  that group's `claim_ids` ✓
- every claim covered by exactly one group, total = 217 ✓
- color palette consistency: every claim color = `#95A5A6` (gray) for
  `NOT_CHECKED`; every group color = `#95A5A6` for `NOT_CHECKED` ✓
- edges: empty list, all per-edge rules vacuous ✓
- no inferred-low `contradicts` edges ✓ (vacuous)

**Validation passed; output written.**

## Final phase-1 pass

### Inputs read

- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/outputs/graph.v1.skeleton.json`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/outputs/CLAIMS.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/outputs/LITERATURE.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/outputs/references.bib`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/conventions/graph_schema.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/conventions/confidence.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/agents/graph_builder.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/agents/executor.md`
- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/methodology/05-artifacts.md`

### Output written

- `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/outputs/graph.v1.json`
- (this append) `/afs/cern.ch/work/m/mgarciam/private/anderson/reviews/test-1/phase1/agents/graph_builder/log.md`

The skeleton at `graph.v1.skeleton.json` was left untouched per the
"Never overwrite a previous version" rule.

### Schema-allowed representation chosen

`conventions/graph_schema.md` defines exactly two node kinds — `group` and
`claim` — and three edge kinds — `supports`, `depends_on`, `contradicts` —
that connect **claims, not external references**. The `external_reference`
node type is explicitly listed in the schema's "When to extend" section as a
deferred extension that should not be added preemptively. The dispatch's
fallback rule ("If the schema is silent on this, default to the
property-on-claim-node form and document the choice in log.md") applies, since
the schema does not provide a `reference` node kind.

Therefore I represented the LITERATURE.md evidence as a per-claim
`references` array on each affected `claim` node:

```json
"references": [
  {
    "key": "Spinner:2024hjm",
    "relation": "supports",          // one of: supports / contradicts / related
    "confidence": "high",            // high / medium / low
    "snippet": "…",                  // verbatim from LITERATURE.md
    "provenance": "LITERATURE.md:C001"
  }
]
```

This is a **non-structural** addition: it leaves every required claim field
from the skeleton (`id, kind, parent, type, sentence, hedged, confidence,
verdict, color, page, line, section`) byte-equivalent, and it adds **zero new
nodes and zero new edges**. The build script enforces this with an explicit
diff against the skeleton (failure → exit non-zero, no write).

Implication: phase-3's renderer will consume `references` as a tooltip /
detail-panel field on each claim. No edges to draw to literature; literature
is per-claim metadata, not a graph-level node. If a future reviewer demands
literature visibility at the graph level, the right response is to extend the
schema to add `external_reference` as a node kind — not to invent it ad hoc
here.

### Procedure executed

1. Re-read the skeleton. 20 groups, 217 claims, 0 edges.
2. Parsed `LITERATURE.md` mechanically with a regex matching the artifact
   spec's bullet form `- [@key] — relation — confidence X — "snippet"`.
3. Extracted the set of cited keys: **34 unique** keys across all bullets.
   Cross-checked every key against `references.bib` — all 34 resolve.
   The 34 keys: `ATLAS:2020ccu, Alwall:2011uj, Alwall:2014hca, Bogatskiy:2022czk, Bogatskiy:2023nnw, Butter:2017cot, Butter:2022rso, Butter:2023fov, Cacciari:2008gp, Cacciari:2011ma, Campbell:2022qmc, Gong:2022lye, Heimel:2018mkt, Kasieczka:2017nvn, Kasieczka:2019dbj, Nachman:2022emq, Plehn:2022ftl, Qu:2022mxj, Sjostrand:2014zea, Spinner:2024hjm, Wu:2024thh, adam, brehmer2023geometric, chen2023symbolic, dao2022flashattention, deFavereau:2013fsa, deOliveira:2015xxd, hendrycks2016gaussian, kasieczka_gregor_2019_2603256, lipman2023flowmatching, ruhe2023clifford, vaswani2017attention, xiong2020layer, zaheer2017deep`.
4. Counted claim headings in `LITERATURE.md` that have at least one bullet:
   **73 claims**. (Headings with no bullets are intentional empty buckets per
   `LITERATURE.md`'s preamble — those claims will be checked by internal
   consistency in phase 2 and carry no `references` array on the claim node.)
5. Validated the relation vocabulary (`supports / contradicts / related`) and
   the confidence vocabulary (`high / medium / low`) — all bullets conform.
6. Built `graph.v1.json` by deep-copying the skeleton and attaching
   `references` only on the 73 enriched claims.
7. Re-ran every schema validation rule on the assembled graph (counts,
   parent-child consistency, edge endpoints, palette, no-FAIL-or-INCONCLUSIVE,
   inferred-low-contradicts ban). All passed.
8. Wrote `graph.v1.json`. Skeleton untouched.

### Counts

- Node count by kind: `group = 20`, `claim = 217` (no `reference` nodes —
  schema-disallowed; literature is a per-claim property).
- Edge count by kind: zero edges total. The phase-1 skeleton has no
  claim-to-claim edges (extractor produced no structural-edge sidecar) and
  this dispatch is forbidden from inventing them. Literature evidence does
  not produce graph edges in the property-on-claim-node form.
- Claims with literature evidence: **73** (matches `LITERATURE.md` exactly).
- Total reference entries across all claims: 113 (a single claim may cite
  multiple references; the largest is 4 entries on C076, C110, C114, C117,
  C141).
- Unique reference keys used: 34. All resolve in `references.bib`.

### Hard constraints honored

- Same set of claim and group nodes as the skeleton, byte-for-byte equivalent
  on their structural fields. Verified by direct comparison in
  `build_v1.py`.
- Every literature key resolves in `references.bib`. Verified by set
  intersection.
- All claim verdicts remain `NOT_CHECKED`; all colors `#95A5A6` (gray). No
  PASS/FAIL/INCONCLUSIVE introduced.
- No new claim-to-claim edges. Edge list is byte-identical to the skeleton's
  (empty).
- Only the two declared output operations executed: write `graph.v1.json`
  and append this section to `log.md`. The build script
  `phase1/agents/graph_builder/build_v1.py` lives in this agent's working
  directory and is not part of the declared deliverable; it is preserved for
  reproducibility.

### Validation outcome

All schema validation rules from `conventions/graph_schema.md` passed:

- `len(groups) = 20 ≤ 20` ✓
- every group's `claim_ids` size in `[1, 15]` ✓
- every claim's `parent` resolves to a group, and the claim id is in that
  group's `claim_ids` ✓
- every edge endpoint resolves to a claim ✓ (vacuous, zero edges)
- no `source == target` edges ✓ (vacuous)
- color hex matches the verdict per the palette (all gray, all
  `NOT_CHECKED`) ✓
- no `contradicts` edges with `low` confidence and `inferred` provenance ✓
  (vacuous)

**Validation passed; output written.**
