# Graph schema

Defines the structure of `graph.v*.json`, the rendering of `graph.final.html`,
the canonical color palette used across every Anderson visual artifact, and the
clustering algorithm `graph_builder` uses to keep the visualization at ≤20
groups regardless of paper size.

The design follows established patterns from the claim-graph and argumentation
literature (Dung-style argumentation frameworks; SciClaim's coarse-grained
node + fine-grained attribute pattern; Cytoscape's compound-node convention)
and deliberately keeps both vocabularies small to maximize agent consistency.

## Two node kinds

### `group` — compound node, visual container

A thematic cluster of related claims. Cap of **20 groups** per paper. Groups
have no verdict of their own — their displayed verdict aggregates from their
child claims (rule below).

| field | required | meaning |
|---|---|---|
| `id` | yes | `G001`, `G002`, … |
| `kind` | yes | literal `"group"` |
| `title` | yes | 2–3 words for HTML display, e.g. `"novel attention"` |
| `caption` | yes | one-sentence summary of what the group's claims collectively assert |
| `claim_ids` | yes | list of child claim ids, denormalized for renderer convenience |
| `dominant_type` | yes | most common claim type within, or `"mixed"` if no type > 60% |
| `verdict` | derived | aggregated from children — `CLEAR`, `FLAGGED`, `INCONCLUSIVE`, `NOT_CHECKED` |
| `color` | derived | hex from palette below, derived from verdict |
| `section` | yes | best-effort paper section, or `"multiple"` |
| `page_range` | yes | `[first_page, last_page]` of constituent claims |

### `claim` — atomic node

One per row in `CLAIMS.md`. Lives inside a `group` (its `parent`).

| field | required | meaning |
|---|---|---|
| `id` | yes | `C001`, `C002`, … (matches `CLAIMS.md`) |
| `kind` | yes | literal `"claim"` |
| `parent` | yes | id of the group this claim belongs to |
| `type` | yes | from `conventions/claim_taxonomy.md` |
| `sentence` | yes | literal proposition, in quotes |
| `hedged` | yes | boolean, from `CLAIMS.md` |
| `confidence` | yes | extraction confidence, `high`/`medium`/`low` |
| `verdict` | v2+ | from `VERIFICATION.md`, or `NOT_CHECKED` if absent |
| `verdict_confidence` | v2+ | `high`/`medium`/`low`, from verifier |
| `verdict_reason` | v2+ | INCONCLUSIVE reason code, when applicable |
| `color` | derived | hex from palette below |
| `page` | yes | page number |
| `line` | yes | line in `paper.txt` |
| `section` | yes | paper section |
| `evidence` | v2+ | list of pointers from `VERIFICATION.md` |

## Three edge kinds

**Edges connect claims, not groups.** Group-level connections in the rendered
HTML are aggregated from claim-level edges by the renderer; the canonical data
is at the claim level.

All edges are **directed** with strict semantics. LLM agents tend to fabricate
symmetric "related-to" edges if direction is left underspecified; the schema
forbids that.

### `supports`

`A → B` means **"A is evidence for B."** A's truth raises confidence in B's
truth. The reverse is not implied — `B → A` is a separate edge if it holds.

Typical use: a numerical `result` claim → the higher-level `interpretation`
claim it backs.

### `depends_on`

`A → B` means **"A's truth requires B's truth."** If B is false, A is undefined
or false. This is a pre-condition, distinct from `supports`.

Typical use: a `result` claim → the `assumption` claim its derivation requires;
or a `method` claim → the `definition` it relies on.

### `contradicts`

`A → B` means **"A's truth makes B false."** Per Dung-style asymmetric
semantics: A undermines B. The reverse is *not* implied; a symmetric mutual
contradiction is two edges.

Typical use: an internal inconsistency where one section's number contradicts
another's; or a `prior_work` citation that turns out to disagree with the
paper's own claim.

### Edge fields

| field | required | meaning |
|---|---|---|
| `id` | yes | `E001`, … |
| `source` | yes | claim id |
| `target` | yes | claim id |
| `kind` | yes | `supports` / `depends_on` / `contradicts` |
| `confidence` | yes | `high`/`medium`/`low`, per `conventions/confidence.md` |
| `provenance` | yes | a `paper.txt:line` pointer, OR the literal `"inferred"` if the relationship was inferred by the agent rather than explicitly stated |

## Canonical color palette

**Used everywhere — graph nodes, highlighted PDF, REPORT.md inline tables.**
One source of truth.

| name | hex | meaning |
|---|---|---|
| green | `#2ECC71` | all checked claims `CLEAR` |
| yellow | `#F1C40F` | at least one `INCONCLUSIVE`, no `FLAGGED` |
| red | `#E74C3C` | at least one `FLAGGED` |
| gray | `#95A5A6` | none checked / all `skip` |

Properties:

- **Colorblind-safe enough.** Green and red are distinguishable by lightness
  in deuteranopia/protanopia simulations; yellow is distinct from both.
- **Highlighted PDF restriction.** The PDF only renders red and yellow as
  highlights. `green` and `gray` translate to "no highlight" — there is no
  positive marking for verified or unchecked sentences (would be visual
  noise).
- **REPORT.md.** Markdown does not support inline color, but section ordering
  and prose mirrors the palette: red findings first, then yellow, then green
  summary, then gray ("not checked").

Edges in the HTML are neutral gray (`#7F8C8D`). Edge *kind* is encoded by line
style, not color:

- `supports` — solid
- `depends_on` — dashed
- `contradicts` — double line, slightly thicker

## Verdict aggregation

### Per claim

Map directly from `VERIFICATION.md`:

- claim has a verdict in `VERIFICATION.md` → `claim.verdict` = that verdict
- claim has no row → `claim.verdict` = `NOT_CHECKED`
- `claim.color` from the palette: `CLEAR` → green, `FLAGGED` → red,
  `INCONCLUSIVE` → yellow, `NOT_CHECKED` → gray.

### Per group

```
if any child verdict is FLAGGED:                       group = FLAGGED,         red
elif any child verdict is INCONCLUSIVE:             group = INCONCLUSIVE, yellow
elif every child verdict is CLEAR:                   group = CLEAR,         green
else (mix of CLEAR and NOT_CHECKED, or all NOT_CHECKED):
                                                    group = NOT_CHECKED,  gray
```

A single FLAGGED anywhere is intentionally enough to color a whole group red —
the goal is to draw the reader's eye to the failure, not to average it out.

## Clustering algorithm

`graph_builder` runs this to produce ≤20 groups from the `N` claims in
`CLAIMS.md`. Deterministic given the same input.

```
1. Degenerate case. If N ≤ 20: each claim is its own group. Stop.

2. Initial clusters. Group claims by (paper_section, claim_type). This is the
   coarsest natural partition. Typical paper has 5–8 sections × 7 types →
   ~30–50 initial clusters.

3. Split oversized clusters. For any cluster with > 15 claims, split by
   sub-section. If a single section/type cluster still has > 15 claims after
   that, split by paragraph proximity (consecutive claims first).

4. Merge until ≤ 20 clusters.
   while len(clusters) > 20:
     pick the two clusters with smallest combined size that share either
     section or type; merge them. Tie-break by section adjacency
     (claims in adjacent paper sections merge before claims in distant ones).

5. Floor. If len(clusters) < 5 AND any cluster has > 5 claims:
   split the largest cluster by sub-topic (claim sentence similarity).
   This is the only step that requires the agent to make a judgment call —
   document the split criterion in graph_builder's log.md.

6. Title and caption per cluster.
   - title: 2–3 words. Extract the dominant noun phrase from the most central
     claim's sentence. No punctuation, no acronyms unless the paper uses them.
   - caption: one sentence ≤ 25 words summarizing what the cluster collectively
     asserts. Not a paraphrase of any single claim.

7. Cross-cluster edges. Carry over claim-to-claim edges from the extractor's
   structural pass. Do not introduce new edges at clustering time.
```

The algorithm is deliberately heuristic at step 5 — agent judgment is allowed,
but logged. Steps 1–4 and 6 are mechanical.

## JSON schema (concrete)

```json
{
  "schema_version": "1",
  "paper": {
    "slug": "demo-paper",
    "title": "...",
    "doi": "...",
    "arxiv": "..."
  },
  "groups": [
    {
      "id": "G001",
      "kind": "group",
      "title": "novel attention",
      "caption": "The paper proposes a sparse attention mechanism that scales linearly with sequence length.",
      "claim_ids": ["C001", "C002", "C003"],
      "dominant_type": "method",
      "verdict": "INCONCLUSIVE",
      "color": "#F1C40F",
      "section": "3.1",
      "page_range": [4, 5]
    }
  ],
  "claims": [
    {
      "id": "C001",
      "kind": "claim",
      "parent": "G001",
      "type": "method",
      "sentence": "We replace standard attention with a sparse variant.",
      "hedged": false,
      "confidence": "high",
      "verdict": "CLEAR",
      "verdict_confidence": "high",
      "color": "#2ECC71",
      "page": 4,
      "line": 87,
      "section": "3.1",
      "evidence": ["paper.txt:87", "paper.txt:142"]
    }
  ],
  "edges": [
    {
      "id": "E001",
      "source": "C002",
      "target": "C001",
      "kind": "supports",
      "confidence": "high",
      "provenance": "paper.txt:144"
    },
    {
      "id": "E002",
      "source": "C003",
      "target": "C001",
      "kind": "depends_on",
      "confidence": "medium",
      "provenance": "inferred"
    }
  ]
}
```

## HTML output (`graph.final.html`)

A single self-contained file. No external network requests at view time.

**Library.** Cytoscape.js (MIT). Inline-embedded in the HTML. Selected because
it is the only mature graph viz with native compound-node support.

**Layout.** `cose-bilkent` (force-directed with compound-node awareness),
falling back to `breadthfirst` if the graph is small (< 8 groups).

**Default state.**

- Group nodes visible, child claims collapsed.
- Group nodes rendered as rounded rectangles, ~140px wide.
- Group label = `title`.
- Group fill = `color` from palette.
- Edges between groups shown as aggregated arcs (one per edge kind), labeled
  with count, e.g. `supports ×3`.

**On hover (group).** Tooltip shows:

- caption (1 sentence)
- claim count
- verdict breakdown: `2 CLEAR, 1 INCONCLUSIVE, 0 FLAGGED, 0 NOT_CHECKED`

**On click (group).** Expand to show child claims as small nodes inside the
group. Edges between claims (rather than aggregated group edges) become
visible. Click again to collapse.

**On hover (claim).** Tooltip shows:

- full sentence
- type, hedged, confidence
- verdict (and reason if INCONCLUSIVE)
- evidence pointers

**On click (claim).** Open a margin panel with the full claim record and a
link to the corresponding `VERIFICATION.md` anchor.

## Versioning

| file | phase | what's new |
|---|---|---|
| `graph.v1.skeleton.json` | 1 | claims-only skeleton, no literature edges yet. |
| `graph.v1.json` | 1 | groups, claims, structural edges. All claim verdicts = `NOT_CHECKED`. |
| `graph.v2.json` | 2 | claim verdicts + verdict_confidence + evidence populated; group verdicts re-aggregated. |
| `graph.final.json` | 3 | same data as v2, frozen for the report. |
| `graph.final.html` | 3 | interactive viz, rendered by `src/render_graph.py`. |

Each version is a new file. **Never overwrite a previous version.**

## Validation rules

Every emitted JSON is checked. Failure of any rule is auto-Category-A:

- `len(groups) ≤ 20`
- every `group` has `1 ≤ len(claim_ids) ≤ 15`
- every `claim.parent` resolves to a `group`, and the claim's id is in that
  group's `claim_ids`
- every `edge.source` and `edge.target` resolves to a `claim` node
- no edge has source == target
- every node carries provenance or has `confidence ≤ medium`
- color hex matches the verdict per the palette table
- no edge of kind `contradicts` has confidence `low` and `provenance: "inferred"`
  (an inferred contradiction without a paper anchor is too weak — promote to
  `medium` confidence with a real anchor or drop the edge)

## When to extend

Stay minimal until a real reviewer finding forces the change. Likely future
extensions, deferred:

- **`external_reference` node type** for `prior_work` claims that don't fit
  cleanly inside a group. Only if citation-heavy papers cluster poorly in
  practice.
- **Additional edge kinds** (`extends`, `refines`, `motivates`). Empirical
  argumentation work shows agents conflate these with `supports`; add only
  if reviewers consistently flag the conflation.
- **Toulmin `warrant` attribute** on edges (the unstated reasoning that
  connects A and B). Useful for auditing but expensive to extract reliably.
- **Edge weights / probabilities.** The discrete confidence scale is
  intentionally coarse; if downstream uses (centrality, propagation) need
  finer ordering, add then — not now.

Do not split node or edge types preemptively. Three edge kinds with sharp
semantics outperform six with fuzzy ones.
