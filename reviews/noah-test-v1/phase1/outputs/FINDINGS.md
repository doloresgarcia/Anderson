# Phase 1 Findings — noah-test-v1
**Paper:** "A Lorentz-Equivariant Transformer for All of the LHC" (L-GATr)

---

## 1. Claim Inventory

545 claims total extracted from `paper/paper.tex`.

**By type:**

| type | count |
|---|---|
| prose | 418 |
| table_cell | 77 |
| equation | 33 |
| caption | 17 |

**Epistemic status:** The `epistemic_status` field is not populated by the current extractor; all 545 claims carry a null value. Phase 2 verifiers should not rely on this field for triage.

**Other flags:** 7 footnote claims. `first_person` and `has_numeric` fields are also unpopulated — the extractor does not emit them.

---

## 2. Claim Reviewer Findings

The reviewer made **no edits** (0 dropped, 0 modified). It raised **11 flags** in two categories.

**Fragment (1 claim):** claim-0066 opens with `\gamma^\mu$.` — the closing token of an inline math environment from the preceding equation. The prose that follows ("Pseudoscalars act as chirality projection operations…") is coherent. Root cause: sentence splitter cut inside inline math. Fix: detect sentences starting with a bare close-dollar and merge with the previous segment.

**Table-as-prose (9 claims):** claims 0140, 0278, 0323, 0346, 0352, 0462, 0514, 0515, 0543 are full comparison/results/hyperparameter table bodies rendered as concatenated prose strings with no natural-language sentence structure. Claims 0346 and 0352 additionally carry a `2c` prefix — residue from `\multicolumn{2}{c}{...}` macro stripping. Claims 0514 and 0515 appear to be two partial rows of the same table split across two JSONL records.

**Implication for phase 2:** These 9 claims will not verify cleanly. The relevant numerical results appear redundantly in proper `table_cell` rows; skip or deprioritise them.

---

## 3. Literature Coverage

The literature searcher read all 98 bank PDFs (first 2 pages each) and ran 13 targeted external searches. 50 distinct claims across 11 clusters received literature annotations.

| Cluster | Topic | Bank | External | Overall |
|---|---|---|---|---|
| A | L-GATr architecture | HIGH | HIGH | covered |
| B | GATr E(3) predecessor | none | HIGH | covered |
| C | Lorentz competitor networks | LOW | HIGH | covered |
| D | Amplitude regression | HIGH | MEDIUM | covered |
| E | Top tagging datasets/benchmarks | MEDIUM | HIGH | covered |
| F | ParT / JetClass / MIParT | LOW | HIGH | covered |
| G | Event generation | HIGH | — | covered |
| H | LHC ML overview | HIGH | MEDIUM | covered |
| I | Transformer foundations | none | HIGH | covered |
| J | Conditional flow matching | MEDIUM | HIGH | covered |
| K | Geometric algebra foundations | none | HIGH (Hestenes book) | covered |

No cluster was left entirely without coverage.

**Key gap — competitors absent from bank:** LorentzNet (2201.08187), PELICAN (2211.00454), CGENN (2305.11141), and ParT (2202.03772) — the four most-cited architectural competitors — are not in the literature bank. Clusters C and F depend entirely on external retrieval; phase 2 cannot bank-verify claims about these baselines.

**Minor gaps:** `Plehn:2022ftl` and `Butter:2017cot` were not retrieved (peripheral claims, excluded from LITERATURE.md). MIParT (He:2024eiw, 2407.08682) remains a preprint with no confirmed published version. Claims about specific MadGraph versions, Sherpa configurations, and MC generator settings have only tangential bank coverage.

---

## 4. Graph Structure

20 groups, 10 structural edges. Schema constraint conflict: with 545 claims and ≤ 20 groups, the minimum possible maximum group size is ⌈545/20⌉ = 28, making the ≤ 15-claim cap simultaneously unsatisfiable. The graph_builder prioritised the group-count constraint; 14/20 groups exceed the cap.

| ID | Title | Section | Claims |
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

**Edges (10 total, all `provenance: inferred`, `confidence: medium`):**
- 3 `supports`: result groups G011, G013, G017 → abstract claim G001/claim-0004
- 6 `depends_on`: task method claims → architecture (G006/claim-0108); architecture → multivector (G005/claim-0076); architecture → GA intro (G004/claim-0043)
- 1 `supports`: prior work reference → GA intro (G004/claim-0043)

No `contradicts` edges added.

---

## 5. Gaps and Risks for Phase 2

1. **Table-as-prose claims** (0140, 0278, 0323, 0346, 0352, 0462, 0514, 0515, 0543) — will not verify as prose assertions. Skip or handle separately.

2. **Unpopulated extractor fields** — `epistemic_status`, `first_person`, `has_numeric` are all null across all 545 claims. Phase 2 logic that branches on these fields will treat every claim identically.

3. **Competitor baselines not in bank** — LorentzNet, PELICAN, CGENN, ParT require external-only verification. Claims in G003, G012–G014 citing these networks will systematically fail bank lookup.

4. **Large groups** — G013 (50), G015 (51), G016 (49), G012 (42) each exceed the schema cap by 3×. Phase 2 agents should expect batches of 40–50 claims from these groups, not 10–15.

5. **Fragment claim-0066** — will likely fail sentence-level verification. Exclude from verification metrics; flag as malformed.

6. **`2c` prefix artifacts** — claims 0346 and 0352 start with `2c` (LaTeX `\multicolumn` residue). String-matching verifiers may misparse these.
