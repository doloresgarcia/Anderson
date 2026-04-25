# Verification

Defines the closed list of verification methods, the default mapping from claim
type to method, evidence standards per verdict, and the external-source
hierarchy used when sources disagree.

The `strategist` reads this file to assign a method per claim. The `verifier`
reads this file to know what counts as PASS / FAIL / INCONCLUSIVE for the method
it was assigned. Verdict confidence (`high` / `medium` / `low`) follows
`conventions/confidence.md`.

## Method catalog

Six methods. Closed list. Anything that doesn't fit gets `skip` plus a note.

### `internal_consistency`

Checks the claim against the rest of the same paper.

- **Reads.** `paper/paper.txt`, plus the specific sections, figures, tables, and
  captions referenced by the claim.
- **Procedure.**
  1. Locate the claim in the paper.
  2. Search the paper for related statements: same numbers, same defined terms,
     same assertions made in different words.
  3. Note agreement, disagreement, or silence.
- **PASS.** No internal contradictions; if the claim refers to a number/figure
  elsewhere in the paper, the cross-reference matches.
- **FAIL.** A different section of the paper directly contradicts the claim, or
  a defined term is used inconsistently with its definition.
- **INCONCLUSIVE.** The paper neither confirms nor contradicts the claim from
  other parts; or the claim depends on supplementary material the verifier
  cannot access.

### `numerical_recheck`

For numerical claims, re-derive or verify the number from the paper's own
data, tables, or figures.

- **Reads.** The claim, plus the paper's tables/figures/equations the number
  derives from.
- **Procedure.**
  1. Identify what number is asserted and at what stated precision.
  2. Locate the source: a table cell, a figure annotation, an equation result.
  3. Compute or read off the value at the same precision.
  4. Compare.
- **PASS.** The number agrees with the source within stated precision (or
  within reasonable rounding if precision is not stated).
- **FAIL.** The number disagrees beyond stated precision *and* the disagreement
  is not explained elsewhere in the paper.
- **INCONCLUSIVE.** The source is in a figure that cannot be read off precisely,
  or the precision is ambiguous, or the derivation requires data not in the
  paper.

### `citation_audit`

For `prior_work` claims, confirm the cited reference actually contains the
proposition attributed to it.

- **Reads.** The claim, the cited reference's abstract/full-text, and the
  citation context in `paper.txt`.
- **Procedure.**
  1. Resolve the bibtex key in `references.bib` to a real record.
  2. Retrieve the reference (or its abstract if the body is paywalled).
  3. Search the reference for the asserted proposition or a near-paraphrase.
- **PASS.** The reference contains the proposition or a clearly equivalent
  statement.
- **FAIL.** The reference does not contain the proposition, OR contains a
  contradicting statement, OR the bibtex key does not resolve to a real record
  (this is a separate auto-FAIL — see "fabricated citations" below).
- **INCONCLUSIVE.** The reference is paywalled and the abstract is not
  determinative; the asserted proposition is plausibly in the body but cannot
  be confirmed.

### `external_corroboration`

Checks the claim against authoritative external sources, ranked per the
external-source hierarchy below.

- **Reads.** The claim, plus retrieved external sources from the
  literature_searcher's candidates and any additional searches the verifier
  runs.
- **Procedure.**
  1. Identify the highest-tier sources relevant to the claim.
  2. Look for direct agreement or contradiction.
- **PASS.** A higher-tier source agrees with the claim, with no equally-high
  source contradicting.
- **FAIL.** A higher-tier source contradicts the claim, with no equally-high
  source agreeing.
- **INCONCLUSIVE.** Sources at the same tier disagree (a "tie" — see hierarchy
  below); or no relevant external source is retrievable.

### `proof_audit`

For mathematical claims (typically `result` claims that are theorems, or
`definition` claims that anchor proofs).

- **Reads.** The claim, the proof in the paper, any lemmas it cites.
- **Procedure.**
  1. Identify the theorem statement and the proof.
  2. Walk through each step. For each step, classify as: trivially correct,
     correct given a cited lemma, requires checking, or appears wrong.
  3. For "requires checking" steps, verify locally; for "cited lemma" steps,
     check the lemma exists and is correctly applied.
- **PASS.** Every step is trivially correct, correctly cites a verifiable
  lemma, or has been verified.
- **FAIL.** A step does not follow, or a cited lemma does not say what is
  attributed to it.
- **INCONCLUSIVE.** A step requires more domain expertise than the verifier
  has; the proof depends on supplementary material not retrievable; the proof
  is sketched rather than complete.

### `skip`

Explicit non-verification. The verifier emits an `INCONCLUSIVE` verdict with a
specific reason.

Reasons that warrant `skip`:

- claim is an `interpretation` with no testable content
- claim is an `assumption` not used non-trivially in the paper
- claim is `future_work` style ("we plan to extend …")
- the strategist's `STRATEGY.md` row explicitly assigns `skip`

`skip` is not silent: it produces a `VERIFICATION.md` row with verdict
`INCONCLUSIVE` and reason `skip:<short reason>`. This is so phase 3 can report
*what was not checked*.

## Type → method default mapping

The strategist uses this mapping. Deviations require a one-line justification in
`STRATEGY.md`.

| claim type | default method | fallback |
|---|---|---|
| `result` | `numerical_recheck` | `external_corroboration` if a public benchmark |
| `result` (if a theorem) | `proof_audit` | `internal_consistency` |
| `method` | `internal_consistency` | — |
| `prior_work` | `citation_audit` | — |
| `background_fact` | `external_corroboration` | — |
| `assumption` | `skip` | `internal_consistency` if the assumption is load-bearing |
| `interpretation` | `skip` | `internal_consistency` if the interpretation is testable |
| `definition` | `internal_consistency` | — |

A claim may carry more than one method if appropriate (e.g. a `result` that is
both numerical *and* benchmarked elsewhere → `numerical_recheck` +
`external_corroboration`). In that case, the verdict is the worst of the two,
with confidence the lower of the two.

## Evidence standards

### What PASS requires

- A specific paper-internal reference (line, table cell, equation), OR
- A specific external reference (citation key + page/section), OR
- For `proof_audit`, an annotated walk through the proof.

A bare "the paper is internally consistent" without pointers is not a PASS —
demote to `INCONCLUSIVE` with reason `evidence_thin`.

### What FAIL requires

- A direct contradiction the verifier can quote, OR
- A numerical disagreement beyond stated precision, OR
- A canonical-tier external source flatly disagreeing, OR
- An unresolvable bibtex key (auto-FAIL — see below).

"It doesn't seem right" is `INCONCLUSIVE`, not FAIL. A FAIL must be
defensible by quoting evidence.

### What INCONCLUSIVE requires

A stated reason. Acceptable reasons:

- `paywalled` — relevant reference is behind a paywall
- `evidence_thin` — supports a verdict directionally but not decisively
- `ambiguous_wording` — the claim has more than one plausible reading
- `out_of_scope` — claim's verification needs domain expertise the verifier
  does not have (e.g. checking a 30-step physics derivation)
- `not_retrievable` — relevant external source returned by no search
- `skip:<reason>` — strategist explicitly skipped
- `verification_rules_gap` — no method in this catalog applies cleanly

## Fabricated citations (auto-FAIL)

If a `prior_work` claim cites a bibtex key that does not resolve to a real
record (no DOI, no arXiv ID, no retrievable record from the configured search
backend), the verdict is **automatically FAIL with confidence high**, regardless
of method. The reasoning string must say `fabricated_citation` and quote the
unresolvable key.

This is the most common failure mode of LLM-generated text the system is built
to catch. There is no INCONCLUSIVE escape: a key either resolves or it doesn't.

## External-source hierarchy

When external sources are required (`external_corroboration`, fallback for other
methods), the verifier ranks sources as:

1. **Domain canonical reference** — PDG (particle physics), IUPAC (chemistry),
   IAU (astronomy), authoritative review monographs in the field.
2. **Peer-reviewed journal article.**
3. **Peer-reviewed conference paper.**
4. **arXiv preprint, version ≥ v2** (revisions imply review).
5. **arXiv preprint, v1.**
6. **Technical report from a recognized institution** (e.g. CERN, ATLAS, NIST).
7. **Textbook or extensive review article**, when more current than the above.
8. **Blog post, tutorial, course notes, Wikipedia.**
9. **LLM training data — never a source.** Quoting "I know this is true" is
   not evidence. The verifier must locate a real record or mark
   `not_retrievable`.

Tier 7 (textbooks) is intentionally below journal articles for novel claims but
typically *outranks* arXiv preprints for well-established background facts. The
verifier picks based on the claim type: novel results lean toward the journal
side, background facts lean toward the canonical-reference / textbook side.

When sources at the same tier disagree, the verdict is `INCONCLUSIVE` with
reason `tied_sources`, not FAIL — Anderson is not a referee, and unresolved
disagreement at the field's top tier is genuinely inconclusive.

## Verifier output format

Every section in `VERIFICATION.md` carries:

- `claim_id`
- `VERDICT` ∈ {`PASS`, `FAIL`, `INCONCLUSIVE`}
- `method` from this catalog
- `confidence` from `conventions/confidence.md`
- `evidence` — list of pointers (`paper.txt:142`, `[@smith2020] §3.2`, …)
- `reasoning` — prose, ≤ 5 sentences

For INCONCLUSIVE, an extra `reason` field with one of the codes above.

## When to extend the catalog

Add a method only when an actual claim cannot be reasonably handled by any
existing method *and* the new method has a real procedure with mechanical PASS
criteria. Likely future additions, deferred:

- `dataset_recheck` — re-running the paper's evaluation on the same data
- `code_audit` — checking released code matches described methodology
- `replication` — running an independent re-implementation

These are out of scope for the current skeleton: they require execution
infrastructure beyond what Anderson currently provides.
