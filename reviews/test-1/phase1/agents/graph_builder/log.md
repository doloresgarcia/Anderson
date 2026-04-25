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
