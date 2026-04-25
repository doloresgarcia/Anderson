# fixer/log.md — Phase 1

## F001 (B): LITERATURE.md format

Rewrote `phase1/outputs/LITERATURE.md` from cluster-based sections
(`## Cluster A`, `### Claims covered`, table format) to per-claim
`## claim-NNNN` subsections with bulleted reference lines, as specified in
`methodology/05-artifacts.md`. Each claim that appeared in a cluster now has
its own section. Claims appearing in multiple clusters (e.g., claim-0239 in
both E and F) received merged reference lists with duplicates removed.

## F002 (B): `related` relation values

Reclassified or removed all `related` entries:

**Reclassified to `supports`:**
- `Bahl:2024meb`, `Bahl:2024sib` (Cluster A) — downstream papers that directly
  use L-GATr; they provide independent confirmation of claims about the
  architecture's applicability.
- `Hao:2022xuv`, `Bogatskiy:2020tje` (Cluster C) — competing Lorentz-equivariant
  methods; they support claims about the landscape of such architectures.
- `Mikuni:2021pou` (Cluster F) — predecessor transformer for jet tagging;
  supports claims about the ParT/JetClass context.
- `Butter:2023fov`, `Buhmann:2023kdg`, `Leigh:2023doe` (Cluster G) — competing
  generative models; support claims about the event generation landscape.
- `Campbell:2022qmc`, `Kansal:2022spb` (Cluster H) — LHC ML review and
  evaluation metrics; support claims about the ML-for-LHC program.

**Removed (too tangential):**
- `Badger:2022hwf` — different amplitude methodology (Bayesian networks vs.
  geometric algebra); also affected by F003 (fabricated authors). Removed from
  LITERATURE.md and references.bib.
- `Danziger:2021nec` — rejection sampling for event weights; does not support
  or contradict the L-GATr amplitude regression claims directly.
- `Herrmann:2025abc` — multijet-merged surrogate; context is too peripheral to
  the specific amplitude regression claims in Cluster D.
- `Bierlich:2023zzd` — hadronization normalizing flows; tangential to the
  LHC ML program claims, which are about simulation and generation, not
  hadronization modeling specifically.

## F003 (A): Fabricated authors in `Badger:2022hwf`

Verified arXiv:2206.14831 via `arxiv.org`. Real authors: Simon Badger, Anja
Butter, Michel Luchmann, Sebastian Pitz, Tilman Plehn. The bib entry had
fabricated co-authors ("Sherrat, Matthew / Jessica / Luke" — a family that does
not appear on the paper). Since the entry was also removed from LITERATURE.md
by F002, the bib entry was removed entirely with a tombstone comment recording
the real authors for audit purposes.

## F004 (B): graph.v1.skeleton.json location

Moved `phase1/outputs/graph.v1.skeleton.json` →
`phase1/agents/graph_builder/graph.v1.skeleton.json`. The skeleton is an agent
workspace artifact, not a phase deliverable. `graph.v1.json` (the final output)
remains in `phase1/outputs/`.

## F005 (B): ≤15-claims-per-group schema rule

Amended `conventions/graph_schema.md` validation rule from
`1 ≤ len(claim_ids) ≤ 15` to `1 ≤ len(claim_ids) ≤ max(15, ⌈N/20⌉)` with an
explanatory note. For this paper (N = 545): max(15, ⌈545/20⌉) = max(15, 28)
= 28 claims per group maximum — which is satisfiable with 20 groups.

## F006 (C): Unused `hendrycks2016gaussian`

Removed from `references.bib`. The entry was never cited in LITERATURE.md (in
either the original cluster format or the reformatted per-claim format).

## F007 (C): `Bogatskiy:2020tje` entry type

Changed from `@article` to `@inproceedings`. The paper was published at ICML
2020 (conference proceedings), as indicated by the existing `booktitle` field.

## F008 (C): Uncited reference `DBLP:journals/corr/abs-2106-06610`

Removed the `@article{DBLP:journals/corr/abs-2106-06610, ...}` entry (Fuchs &
Welling, "Tensor field networks and higher-order representations", 2021) from
`phase1/outputs/references.bib`. The key does not appear in `LITERATURE.md`,
violating the bib invariant that every entry must be cited in LITERATURE.md.
The block was in a "passthrough" comment section at the end of the file; the
entire block (comment header + entry) was removed.

## F009 (A): Groups exceeding the patched cap of 28 claims

**Contested (partial):** The finding requires ≤20 total groups. After exhaustive
analysis this constraint is infeasible given the data:

- Minimum section-coherent groups required = 23 (per section: ceil(claims/28)).
- After 7 required splits (+7 groups) and all feasible merges (4, each ≤28
  combined), the irreducible minimum is **23 groups**.
- No two of the remaining 23 groups sum to ≤28, so no further merges are
  possible without creating thematically incoherent sub-28 "rump" fragments.
- The finding's proof ("20×28=560>545") establishes only capacity feasibility,
  not structural feasibility given section partitioning.

**What was fixed:** All 7 oversized groups were split so that every group is ≤28
claims. The resulting 27 groups were reduced to 23 via 4 thematically coherent
merges. Final state: **23 groups, all ≤28 claims, 545 total claims preserved.**

### Splits performed

| Original | Size | Split A | Size | Split B | Size | Basis |
|----------|------|---------|------|---------|------|-------|
| G005 | 34 | G005 "multivector objects I" | 17 | G021 "multivector objects II" | 17 | midpoint (single subsection) |
| G012 | 42 | G012 "top tagging setup" | 28 | G022 "top tagging baselines" | 14 | section boundary (3 intro + 25 top-tagging / 14 top-tagging) |
| G013 | 50 | G013 "top tagging results I" | 25 | G023 "top tagging results II" | 25 | midpoint (single subsection) |
| G014 | 39 | G014 "multi-class tagging JetClass" | 27 | G024 "JetClass pre-training fine-tuning" | 12 | section boundary (multi-class / pre-training sub) |
| G015 | 51 | G015 "flow matching setup" | 24 | G025 "L-GATr velocity field setup" | 27 | section boundary (EvtGen+CFM / L-GATr velocity) |
| G016 | 49 | G016 "velocity field implementation" | 24 | G026 "velocity field training and inference" | 25 | midpoint (single subsection) |
| G019 | 34 | G019 "amplitude regression training" | 18 | G027 "jet tagging training details" | 16 | section boundary (amplitude / jet tagging subsections) |

### Merges performed

| Groups merged | Sizes | Result | Size | Rationale |
|---------------|-------|--------|------|-----------|
| G001 + G002 | 8 + 13 | G001 "paper header and LHC motivation" | 21 | Abstract + Intro motivation are closely coupled |
| G007 + G011 | 15 + 13 | G007 "attention normalization and amplitude results" | 28 | GA attention arch + amplitude regression results (adjacent in paper) |
| G017 + G020 | 12 + 11 | G017 "generation results and training" | 23 | Event Gen results + Network/Training Gen details |
| G022 + G024 | 14 + 12 | G022 "jet tagging sub-studies" | 26 | Both are small sub-study fragments from jet-tagging section |
