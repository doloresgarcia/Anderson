# critical_reviewer phase 1 ROUND 2 — log

## Inputs read

- `agents/critical_reviewer.md`
- `methodology/04-review.md`
- `methodology/05-artifacts.md`
- `conventions/claim_taxonomy.md`
- `conventions/graph_schema.md`
- `conventions/confidence.md`
- `phase1/CLAUDE.md`
- `phase1/review/critical.md` (round 1 — F01–F12)
- `phase1/review/ARBITRATION.md` (round 1 — F01 deferral note)
- `phase1/agents/fixer/log.md` (full)
- `phase1/agents/graph_builder/log.md` (full, including round-2 rebuild section)
- `phase1/outputs/CLAIMS.md` (post-fix)
- `phase1/outputs/LITERATURE.md` (post-fix)
- `phase1/outputs/references.bib` (unchanged per fixer)
- `phase1/outputs/graph.v1.json` (rebuilt round 2)
- `phase1/outputs/graph.v1.skeleton.json` (frozen)
- `phase1/outputs/FINDINGS.md` (with new §8)
- `paper/paper.txt` (line lookups for provenance sampling)

## Outputs written

- `phase1/review/critical_round2.md`
- `phase1/agents/critical_reviewer/round2_plan.md`
- `phase1/agents/critical_reviewer/round2_log.md` (this file)

## Auto-A trigger checks (mechanical)

### a. Bibtex resolution

```python
keys_in_lit = set(re.findall(r'\[@([A-Za-z0-9:_\-]+)\]', LITERATURE_MD))
keys_in_bib = set(re.findall(r'@\w+\{([^,]+),', REFERENCES_BIB))
unresolved = keys_in_lit - keys_in_bib
```

Result: 34 keys in LITERATURE.md, 45 in references.bib, **`unresolved = ∅`**.
No new keys introduced (consistent with fixer log: F07/F08 were re-tags only,
no bibtex churn). PASS.

### b. graph.v1.json schema validation

Loaded the rebuilt JSON and re-ran every rule from `conventions/graph_schema.md`:

- `len(groups) = 20 ≤ 20` ✓
- every group's `len(claim_ids)` in `[1, 15]` (max = 14 at G014, min = 7 at G020) ✓
- every claim's `parent` resolves to an existing group, and the claim id is in
  that group's `claim_ids` ✓
- claim id set in graph = group-listed id set in graph (bidirectional set
  equality) ✓
- `edges = []` → endpoint, self-loop, inferred-low-contradicts ban all
  vacuously satisfied ✓
- every claim's `color = #95A5A6` (matches `NOT_CHECKED` in palette) ✓
- C188 and C189 absent from claim list ✓
- C218 and C219 present with `parent = G002` ✓
- C036, C044, C060, C148 carry `confidence: "low"` on the claim node ✓

PASS.

### c. CLAIMS.md provenance sample

Sampled 12 rows (mix of unchanged and fixer-touched). For each, looked up
`paper.txt` at the row's `line` value and verified verbatim presence of the
quoted sentence's first ~35 chars within ±3 lines:

| claim_id | line | match | note |
|---|---|---|---|
| C001 | 56 | yes | unchanged, verbatim |
| C006 | 95 | yes | unchanged, verbatim (LITERATURE retagged but text identical) |
| C036 | 207 | yes | unchanged sentence; only confidence demoted (high→low) |
| C044 | 232 | yes | unchanged sentence; only confidence demoted |
| C060 | 328 | yes | unchanged sentence; only confidence demoted |
| C100 | 429 | yes | unchanged, verbatim |
| C129 | 546 | yes | unchanged, verbatim |
| C148 | 680 | yes | unchanged sentence; only confidence demoted |
| C217 | 952 | yes | unchanged, verbatim |
| C015 | 108 | **paraphrase** | sentence "We extend amplitude regression to handle high-multiplicity LHC events." — paper line 108 says "we extend the amplitude regression analysis…"; the phrase "high-multiplicity" does not appear at line 108 (it occurs in §3 around line 381). Paraphrase introduced by F04 split. See finding G02 below. |
| C218 | 108 | **paraphrase** | sentence "We improve classification by introducing a new pre-training scheme." — paper line 108 says "improve the classification through pre-training and multi-class tagging." Paraphrase drops "multi-class tagging." See G02. |
| C219 | 108 | **paraphrase** | sentence "We deliver a competitive Lorentz-equivariant generative network." — paper line 108 says "deliver a competitive generative network for Monte Carlo event generation." Paraphrase adds the descriptor "Lorentz-equivariant" not in the source contributions sentence. See G02. |

Row-by-row read of the changed entries against the source confirmed the
identity and provenance line for each unchanged row. The three paraphrased
rows were introduced by the F04 split (per the fixer log) — this is permitted
by `conventions/claim_taxonomy.md` (the contributions-list expansion rule)
but the *paraphrase quality* is a separate concern (see new findings).

No row was found whose `line` value disagreed with the paper. All 9 unchanged
rows match verbatim. The 3 split-derived rows are paraphrases of the
contributions sentence on line 108 (intended by F04). **No auto-A
provenance failure.**

### d. Output files list

Listing of `phase1/outputs/`:

```
CLAIMS.md
FINDINGS.md
LITERATURE.md
graph.v1.json
graph.v1.skeleton.json
references.bib
```

Six files — exactly the declared phase-1 deliverable set per
`phase1/CLAUDE.md`. No extra files. Round-1 F02 concern (build_v1.py in the
agent working dir): `find phase1/agents -name "*.py"` returns nothing; the
script now lives at `src/build_graph_v1.py` (and `src/build_graph_v1_round2.py`
for the round-2 rebuild). Working-directory contents of
`phase1/agents/graph_builder/` are now only `log.md` and `plan.md`. PASS.

### Auto-A summary

**No auto-A trigger fired.**

## Round-1 finding resolution audit

Each F-row was confirmed by independent inspection of the post-fixer artifacts
(not by trusting the fixer's log). See the table in `critical_round2.md` §
"Round-1 finding resolution audit."

- **F01 (page numbers).** FINDINGS.md §8 ("Deferred to phase 3") contains the
  required deferral text: "Page-number recovery (F01)…The arbiter (phase-1
  round-1 ARBITRATION.md) explicitly accepts F01 being open for the round-2
  review provided this deferral is recorded here." This matches the round-1
  arbiter's stated condition. **DEFERRED — accepted.**
- **F02 (build_v1.py).** Confirmed: no Python file in
  `phase1/agents/graph_builder/`; equivalent script at
  `src/build_graph_v1.py`. **RESOLVED.**
- **F03 (no low-confidence rows).** Confirmed: C036, C044, C060, C148 now
  show `low` in CLAIMS.md and on the corresponding nodes in graph.v1.json
  (`confidences = {high: 149, medium: 64, low: 4}` mechanically computed).
  **RESOLVED.**
- **F04 (C015 split).** Confirmed: C015 row now reads "We extend amplitude
  regression to handle high-multiplicity LHC events." (first sub-claim) and
  two new rows C218, C219 appended for the second and third sub-claims.
  Group G002's `claim_ids` updated. **RESOLVED structurally.** Paraphrase
  quality is a separate new finding (G02).
- **F05 (C188/C189 dropped).** Confirmed: neither id appears in CLAIMS.md,
  LITERATURE.md, or graph.v1.json. The id gap at C188/C189 is preserved
  intentionally per fixer log. **RESOLVED.**
- **F06 (over-confident expressivity claims).** Subsumed by F03's
  demotions of C036, C044, C060 to `low`. **RESOLVED.**
- **F07 (C006 over-attributed `supports`).** Confirmed: C006's three bullets
  all retagged from `supports`/`high` and `supports`/`medium` to
  `related`/`medium`; phase-2 note added pointing to `Spinner:2024hjm` §4 or
  `Bogatskiy:2020tje` for the order-of-magnitude figure. **RESOLVED.**
- **F08 (C148 mis-relation for OT-CFM).** Confirmed: C148's
  `lipman2023flowmatching` bullet retagged from `supports medium` to
  `related medium`; explanatory note added flagging that vanilla CFM does
  not provide OT paths and that phase-2 verifier may flag the underlying
  claim wording. **RESOLVED.**

## New-findings hunt

### Over-edit / scope-creep audit on the fixer

I diffed the fixer's listed edits against the artifact state to look for
unannounced changes:

- F02 — moved `build_v1.py`. No collateral damage observed.
- F03/F06 — confidence demotions on C036, C044, C060, C148 only; verified
  by row-by-row diff of `confidence` column (other 213 rows unchanged in
  that column).
- F04 — C015 sentence updated; C218 and C219 appended at end of CLAIMS.md.
  Empty `## C218` and `## C219` headings appended at end of LITERATURE.md.
  No other rows touched.
- F05 — C188 and C189 removed from CLAIMS.md and LITERATURE.md; gap
  preserved (no renumbering).
- F07 — only C006's three bullets in LITERATURE.md changed; phase-2 note
  appended.
- F08 — only C148's one bullet in LITERATURE.md changed; phase-2 note
  appended.
- F01 — FINDINGS.md §8 added.

I did not find any unannounced mutation of unrelated rows or fields. The
fixer stayed within the declared scope.

### Cross-artifact claim-set consistency

- `CLAIMS.md` ids: `{C001..C187, C190..C219}` (217 rows). ✓
- `LITERATURE.md` headings: `{C001..C187, C190..C219}` (217 headings). ✓
- `graph.v1.json` claim ids: `{C001..C187, C190..C219}` (217 nodes). ✓
- All three artifacts agree on the claim id set exactly.

### Round-2 rebuild structural changes

Per the rebuild log, only **G002** changed: `claim_ids` membership
{−C188, −C189, +C218, +C219}, size unchanged (10), caption updated, and
`page_range` tightened from `[95, 855]` to `[95, 108]`. All other 19 groups
have byte-identical claim_ids, captions, page ranges, sections, dominant
types. Verified by direct field comparison. The change is justified by
the fixer's edits and is the minimum-impact rebuild. No structural
deviation from the schema's deterministic algorithm.

### FINDINGS.md staleness

FINDINGS.md was *not* re-emitted after the fixer's edits. Several numeric and
narrative statements are now stale:

| FINDINGS.md location | stated | actual (post-fix) | impact |
|---|---|---|---|
| §3 "Confidence distribution" table | high 153, medium 64, low 0 | high 149, medium 64, low 4 | numbers do not match |
| §3 narrative "no low-confidence rows" | true | now 4 low rows (C036, C044, C060, C148) | incorrect prose |
| §5 "Distribution by relation" table | supports 74, related 39, contradicts 0 | supports 70, related 43, contradicts 0 | F07 (3 retags) + F08 (1 retag) moved 4 from supports → related |
| §6.4 "C148 (`result`, `medium` confidence)" | medium | low (now) | inline confidence label outdated |
| §6.5 "Code-availability URL claims `C188`, `C189` were *kept*" | kept | dropped per F05 | sentence is now factually wrong |
| §6.5 "`C015` (paper's contributions) was kept whole" | kept | split per F04 (C015, C218, C219) | sentence is now factually wrong |

§2 (Total claims 217), §4 (group structure table), §5 (73 claims with refs,
113 bullets, 11 unused bib entries, 144 empty-bucket claims) all still match
the actual post-fixer state. §1 narrative still accurate at the level of
"217 claims… 20 groups… 0 edges." §7 phase-2 prompts still consistent. §8
deferral note correctly added.

This is a B-class finding: it weakens the report (downstream agents and
human reviewers will see incorrect counts) but does not block phase-1
advancement. Tagged G01 below.

### Paraphrase / content-drift in the F04 split

The F04 split added three paraphrased sentences for the contributions list
at line 108 of `paper.txt`. Per `conventions/claim_taxonomy.md`, the split
itself is correct ("Cited contributions of the present paper… expands into
N claims"). But the paraphrases introduced details not in the source
contributions sentence:

- **C015** "We extend amplitude regression to handle high-multiplicity LHC
  events." — paper line 108 says "we extend the amplitude regression
  analysis." The string "high-multiplicity" does not appear anywhere on
  line 108; it appears later in §3 (line 381). The paraphrase is a fair
  summary, but it inserts a scope qualifier ("high-multiplicity LHC
  events") that the contributions sentence does not literally contain.
- **C218** "We improve classification by introducing a new pre-training
  scheme." — paper line 108 says "improve the classification through
  pre-training and multi-class tagging." The paraphrase drops "multi-class
  tagging" entirely, narrowing the contribution.
- **C219** "We deliver a competitive Lorentz-equivariant generative
  network." — paper line 108 says "competitive generative network for
  Monte Carlo event generation." The paraphrase inserts the descriptor
  "Lorentz-equivariant" (correct in context, but not in this contributions
  sentence) and drops "for Monte Carlo event generation."

Per `conventions/confidence.md`, "low — best guess; agent had to
paraphrase, **infer**, or choose under genuine ambiguity" and
"medium — type sits between two categories OR the row was split from a
compound sentence OR the propositional content is hedged." The split-from-
compound-sentence anchor justifies `medium` in principle, but only if the
paraphrase faithfully preserves the sentence's content. C015 inserts a
scope qualifier; C218 drops "multi-class tagging" (a contribution the
paper explicitly enumerates); C219 substitutes a different descriptor.
Either the paraphrases should be tightened to remove inserted/dropped
content, or the confidence on these rows should be `low` rather than
`medium` to reflect the genuine paraphrase work involved.

This is a B-class finding (weakening: the verifier in phase 2 will check
sub-claims that don't match what the contributions sentence literally
asserts). Tagged G02 below.

### LITERATURE.md format note

F07 and F08 added inline "Note:" lines under the per-claim heading
(`## C006`, `## C148`). The artifact format spec in
`methodology/05-artifacts.md` shows only bullet lines under each heading.
The fixer's log explicitly flagged this as a known scaffolding choice:
"the artifact format spec in `methodology/05-artifacts.md` is silent on
free-form notes; treating them as orchestrator-facing scaffolding is
consistent with the existing FINDINGS.md §6 style." That is defensible
but worth recording, since downstream parsers (e.g. phase-2 strategist)
that read LITERATURE.md by regex on bullet lines will simply ignore the
notes — fine — but a strict parser might reject them. C-level — record,
do not block. Tagged G03 below.

### Other checks performed

- No new bibtex keys → no new fabrication risk to assess.
- No edges in the graph → vacuous edge audit.
- All paper title and authors fields in graph.v1.json unchanged (still
  derived from CLAIMS.md heading; F09 was de-scoped).
- All 11 unused bib entries from round 1 are still unused (F10 was
  de-scoped).
- C111 still tagged `result high` (F11 was de-scoped); not a new finding.
- FINDINGS.md §5 wording about LITERATURE.md vs paper.txt unused-cite
  distinction unchanged (F12 was de-scoped); not a new finding.

## Findings (this round)

- A: 0
- B: 2  (G01: stale FINDINGS.md numbers; G02: paraphrase drift in F04 split)
- C: 1  (G03: free-form "Note:" lines in LITERATURE.md format)

## Verdict recommendation

Recommended verdict: **ITERATE (round 3)** — two B-class findings exist and
neither has been previously fixed. Per `methodology/04-review.md`:

```
elif any B and not previously fixed: → ITERATE
```

The remediation is small: re-emit FINDINGS.md from the post-fixer artifacts
(mechanical regen) and either tighten the C015/C218/C219 paraphrases to
faithfully match line 108 OR demote the three rows to `confidence = low`
with a one-line justification in the fixer log. C-level G03 may be
de-scoped or addressed in passing.

If the arbiter decides the two B findings are minor enough to defer
(analogous to F01's deferral), they can be tracked in FINDINGS.md and the
phase passed; that is an arbiter call, not mine.
