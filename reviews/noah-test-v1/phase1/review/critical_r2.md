# critical_r2.md — Phase 1 Re-Review (Round 2)

**Paper:** "A Lorentz-Equivariant Transformer for All of the LHC" (L-GATr)
**Review slug:** noah-test-v1
**Reviewer:** critical_reviewer
**Round:** 2 (re-review after fixer addressed F001–F007)

---

## Previously Fixed Findings

| ID | Severity | Status |
|---|---|---|
| F001 | B | RESOLVED — LITERATURE.md correctly reformatted to per-claim `## claim-NNNN` sections |
| F002 | B | RESOLVED — no `related` relation values remain in LITERATURE.md or graph edges |
| F003 | A | RESOLVED — `Badger:2022hwf` removed from LITERATURE.md and references.bib; tombstone comment with real authors present |
| F004 | B | RESOLVED — `graph.v1.skeleton.json` absent from `phase1/outputs/`; correctly located at `phase1/agents/graph_builder/graph.v1.skeleton.json` |
| F005 | B | RESOLVED — schema rule patched to `1 ≤ len(claim_ids) ≤ max(15, ⌈N/20⌉)` with explanatory note |
| F006 | C | RESOLVED — `hendrycks2016gaussian` removed from references.bib |
| F007 | C | RESOLVED — `Bogatskiy:2020tje` changed to `@inproceedings` |

---

## Check Results

### 1. BibTeX key resolution (auto-A check)

All 27 keys cited in LITERATURE.md resolve in references.bib. No missing keys.

One extra key exists in references.bib that is not cited in LITERATURE.md:

- **`DBLP:journals/corr/abs-2106-06610`** — present in bib, not in LITERATURE.md. The bib entry's own comment says it is "cited in claim-0104" and inspection of claims.jsonl confirms `claim-0104` carries this as a `cite_keys` entry. The fixer included it under a "passthrough" section comment: *"These keys appear in paper's cite_keys fields but are not directly cited in LITERATURE.md cluster tables above."*

This key is **not cited in LITERATURE.md** because literature_searcher found no supporting literature for the claim it annotates (an open-question/hedged prose claim about higher-order tensors). Including it in the bib without a LITERATURE.md entry is internally inconsistent: the bib header states *"Every key in this file is cited in phase1/outputs/LITERATURE.md."* — that invariant is now false.

**→ New finding F008 below.**

### 2. LITERATURE.md per-claim format (F001 check)

All sections use the correct `## claim-NNNN` heading format. All entries follow the `- [@key] — relation — confidence level — source — "quote"` line format. Relation values are exclusively `supports` throughout. No `related` values. **PASS.**

### 3. No `related` relation values (F002 check)

Graph edges: 10 edges, kinds = `{supports, depends_on}`. No `related` edges. LITERATURE.md: no `related` values. **PASS.**

### 4. Skeleton file absent from outputs/ (F004 check)

`phase1/outputs/` contains exactly: `claims.jsonl`, `CLAIM_REVIEW.md`, `graph.v1.json`, `FINDINGS.md`, `LITERATURE.md`, `references.bib`. No skeleton file. Skeleton is at `phase1/agents/graph_builder/graph.v1.skeleton.json`. **PASS.**

### 5. Schema rule patched (F005 check)

`conventions/graph_schema.md` now reads `1 ≤ len(claim_ids) ≤ max(15, ⌈N/20⌉)` with an explanatory note. For N=545: max(15, ⌈545/20⌉) = max(15, 28) = 28. **PASS.**

### 6. graph.v1.json validity under patched schema

**N = 545 claims, 20 groups, 10 edges.**

Groups over the new per-group cap of 28:

| Group | Title | Size |
|---|---|---|
| G005 | multivector objects | 34 |
| G012 | top tagging method | 42 |
| G013 | top tagging results | 50 |
| G014 | multi-class tagging | 39 |
| G015 | flow matching method | 51 |
| G016 | velocity field | 49 |
| G019 | amplitude jet training | 34 |

Seven of 20 groups exceed the 28-claim cap. The largest (G015) has 51 claims — nearly double the allowed maximum. The patched schema rule is violated by the existing graph.v1.json output.

The graph was built before the schema patch. The patch was applied to the schema document but the output was never re-validated or re-built to comply. This is a new Category-A failure.

**→ New finding F009 below.**

Other schema checks:
- Parent/`claim_ids` consistency: **PASS** (no mismatches)
- Edge source/target validity: **PASS** (all resolve)
- Self-loop edges: **PASS** (none)
- Color/verdict consistency: **PASS** (all `NOT_CHECKED` + gray `#95A5A6`)
- No `related` edges: **PASS**
- No low-confidence inferred `contradicts` edges: **PASS** (no contradicts edges at all)

### 7. New issues introduced by fixer

See F008 and F009 below.

---

## New Findings

### F008 (C): references.bib contains a key not cited in LITERATURE.md

**File:** `phase1/outputs/references.bib`
**Key:** `DBLP:journals/corr/abs-2106-06610`

The bib file's own header states: *"Every key in this file is cited in phase1/outputs/LITERATURE.md."* This invariant is false. The DBLP key was added by the fixer under a "passthrough" comment for claim-0104, but no corresponding LITERATURE.md entry exists for that claim. The bib should either:

(a) Remove the entry (it is not literature-search output — it is the paper's own citation, not a result of the searcher's coverage work), or  
(b) Add a `## claim-0104` section to LITERATURE.md with this entry if the searcher can vouch for it.

Option (a) is cleanest. The bib header invariant must be restored.

**Severity: C** — does not affect any downstream consumer (graph, verification), but creates a false invariant that will confuse future reviewers.

---

### F009 (A): graph.v1.json violates the patched per-group size rule

**File:** `phase1/outputs/graph.v1.json`
**Rule:** `1 ≤ len(claim_ids) ≤ max(15, ⌈N/20⌉)` where N=545, giving a cap of 28.

Seven groups exceed 28 claims: G005 (34), G012 (42), G013 (50), G014 (39), G015 (51), G016 (49), G019 (34).

The schema patch in F005 was applied to the schema document but graph.v1.json was not re-built or re-split to comply. The graph as emitted is non-conformant with the schema it is supposed to satisfy.

The graph_builder must re-run its clustering pass (steps 3–4 of the schema algorithm: split oversized clusters, then merge until ≤20 groups) to bring all groups within the 28-claim cap. With N=545 and 20 groups, the cap is mathematically satisfiable (20 × 28 = 560 > 545), so no architectural change is needed — only a re-split of the seven oversized groups.

**Severity: A** — the emitted artifact does not satisfy the schema it is validated against, per the schema's own statement that violations are "auto-Category-A."

---

## Summary

| Finding | Severity | Description |
|---|---|---|
| F001 | ~~B~~ | RESOLVED |
| F002 | ~~B~~ | RESOLVED |
| F003 | ~~A~~ | RESOLVED |
| F004 | ~~B~~ | RESOLVED |
| F005 | ~~B~~ | RESOLVED |
| F006 | ~~C~~ | RESOLVED |
| F007 | ~~C~~ | RESOLVED |
| F008 | C | Spurious bib entry violates bib header invariant |
| F009 | A | graph.v1.json group sizes violate patched schema rule |

Two new findings: one A, one C. F009 requires graph_builder to re-split oversized groups. F008 requires removing or legitimizing the DBLP passthrough entry.
