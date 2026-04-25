# graph_builder skeleton pass — log.md

**Input:** `phase1/outputs/claims.jsonl` (545 claims), `conventions/graph_schema.md`
**Output:** `phase1/outputs/graph.v1.skeleton.json`

---

## Step 1 — Input summary

- 545 claims total
- 4 claim types: `prose` (399), `table_cell` (77), `equation` (33), `caption` (15), `table_cell` (77)
- 9 top-level sections: `(no section)`, `Abstract`, `Introduction`,
  `Lorentz-Equivariant Geometric Algebra Transformer`, `L-GATr for Amplitude Regression`,
  `L-GATr for Jet Tagging`, `L-GATr for Event Generation`, `Network and Training Details`, `Outlook`

## Step 2 — Initial clusters by (section, type)

Running step 2 produced exactly **20 initial clusters**. The largest were:

| cluster | count |
|---|---|
| (LGAT, prose) | 133 |
| (Jet Tagging, prose) | 73 |
| (Event Generation, prose) | 72 |
| (Jet Tagging, table_cell) | 51 |
| (Network and Training Details, prose) | 42 |

All 20 clusters were far over the 15-claim split threshold.

## Step 3 — Splitting oversized clusters

All clusters exceeded 15 claims, requiring sub-section splitting and then proximity splitting.

After step 3: **65 clusters** (many fragments of size 2–4 from section boundaries).

## Step 4 — Merging to ≤ 20 groups

### Constraint conflict (step-5 judgment call)

The schema specifies two hard rules that are **mutually incompatible** for this paper:

- `len(groups) ≤ 20`
- `every group: 1 ≤ len(claim_ids) ≤ 15`

With 545 claims and ≤ 20 groups, the minimum possible maximum group size is
⌈545 / 20⌉ = **28**. Satisfying both constraints simultaneously is mathematically
impossible.

**Decision:** The agent instruction "produce ≤ 20 groups from 545 claims" takes
precedence. The `≤ 15` cap was designed for typical papers (~100–150 claims). All
545 claims are assigned to 20 semantically coherent groups, with group sizes ranging
from 8 to 51. This constraint conflict is flagged here for the orchestrator's attention.

### Merge strategy

Fragments (size 2–4) were absorbed into the nearest semantically related group
within the same section. The merge criterion was: same section, then same sub-section,
then structural proximity (consecutive lines).

The 65 post-split clusters were collapsed to 20 groups by:
1. Merging all caption/equation fragments into the prose group of the same sub-section.
2. Merging sub-section fragments (size ≤ 4) into the adjacent sub-section group.
3. Combining small sections with neighbours:
   - `(no section)` [3] + `Abstract` [5] → G001 [8]
   - `Network and Training Details / Event Generation` [11] + `/ captions` [1] → G020 [11+captions]

### Final 20 groups

| ID | Title | Section | Size |
|---|---|---|---|
| G001 | header abstract | Abstract | 8 |
| G002 | LHC ML motivation | Introduction | 13 |
| G003 | equivariant prior work | Introduction | 21 |
| G004 | spacetime algebra | LGAT | 28 |
| G005 | multivector objects | LGAT | 34 |
| G006 | linear equivariant layers | LGAT | 26 |
| G007 | attention normalization | LGAT | 15 |
| G008 | symmetry breaking | LGAT | 25 |
| G009 | particle scaling | LGAT | 26 |
| G010 | amplitude method | Amplitude Regression | 26 |
| G011 | amplitude results | Amplitude Regression | 13 |
| G012 | top tagging method | Jet Tagging | 42 |
| G013 | top tagging results | Jet Tagging | 50 |
| G014 | multi-class tagging | Jet Tagging | 39 |
| G015 | flow matching method | Event Generation | 51 |
| G016 | velocity field | Event Generation | 49 |
| G017 | generation results | Event Generation | 12 |
| G018 | outlook summary | Outlook | 22 |
| G019 | amplitude jet training | Network and Training Details | 34 |
| G020 | generation training | Network and Training Details | 11 |

## Step 5 — Floor check

`len(clusters) = 20`, which is not < 5, so step 5 (sub-topic splitting) does not apply.

## Step 6 — Titles and captions

Titles are 2–3 words extracted from the dominant noun phrase of the most central claim
per group. Captions are ≤ 25 words summarizing the group's collective assertion.

## Step 7 — Edges

10 conservative `inferred` structural edges were added:

- 3 `supports` edges: results groups (G011, G013, G017) → abstract claim (G001/claim-0004)
- 6 `depends_on` edges: task method claims → architecture claim (G006/claim-0108),
  architecture → multivector (G005/claim-0076), architecture → GA intro (G004/claim-0043)
- 1 `supports` edge: prior work reference → GA intro (G004/claim-0043)

No `contradicts` edges were added (skeleton pass; no evidence of internal contradiction).
All edges use `provenance: "inferred"` with `confidence: "medium"`.

## Validation results

- `len(groups) = 20` ✓ (satisfies ≤ 20)
- `every group: 1 ≤ len(claim_ids)` ✓ (min = 8)
- `every group: len(claim_ids) ≤ 15` **FAIL** (14/20 groups exceed 15; see constraint conflict above)
- All `claim.parent` resolve correctly ✓
- All `claim.parent` claims appear in their group's `claim_ids` ✓
- No self-loop edges ✓
- All edge endpoints exist ✓
- `color = "#95A5A6"` for all claims and groups (verdict `NOT_CHECKED`) ✓
- No `contradicts` edge with `confidence: low` and `provenance: inferred` ✓
