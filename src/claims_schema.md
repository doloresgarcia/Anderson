# `claims.jsonl` Schema

One JSON record per line. Produced by `src/extract_claims.py` from a LaTeX paper, then optionally edited in place by the `claim_reviewer` agent. Lean schema — fields are present only when meaningful for that record's `type`.

## Fields by claim type

### Always present

| Field | Type | What it is |
|---|---|---|
| `id` | string | `claim-NNNN` — sequential, ordered by document position. IDs are stable across reviewer edits; if the reviewer drops a row, the gap remains (no renumbering). |
| `type` | string | `prose` \| `equation` \| `caption` \| `table_cell` |
| `text` | string | The claim text — what downstream agents read |
| `section_path` | string[] | Section/subsection titles, root → leaf. Empty if the claim appears before any `\section`. |
| `line` | int | 1-indexed line number in `paper.tex` |

### `prose` claims

| Field | Type | Meaning |
|---|---|---|
| `cite_keys` | string[] | Bibtex keys cited in the source sentence (e.g. `["Smith:2020"]`). Often empty. |
| `is_first_person` | bool | `we`, `our`, `us`, `ours` appear in the sentence — typically signals an authored claim |
| `is_numeric` | bool | A number/percentage appears in the sentence |
| `is_footnote` | bool | Claim came from inside a `\footnote{}` |
| `is_definition` | bool | Sentence matches a definition pattern (`let X denote`, `we define`, `is defined as`, …) |
| `epistemic` | string | `asserted` \| `hedged` (sentence contains hedge words like *may, might, suggests*) \| `conditional` (sentence starts with *if, when, suppose*) |

### `equation` claims

| Field | Type | Meaning |
|---|---|---|
| `env` | string | `align` \| `align*` \| `equation` \| `gather` \| `multline` |

The `text` field is the raw LaTeX source of the equation environment.

### `caption` claims

| Field | Type | Meaning |
|---|---|---|
| `env` | string | `figure` \| `figure*` \| `table` \| `table*` |

### `table_cell` claims

Parsed from `\result{val}{err}` and `\bestresult{val}{err}` macros in tables.

| Field | Type | Meaning |
|---|---|---|
| `value` | string | First arg — measurement value, e.g. `"295"` |
| `error` | string | Second arg — uncertainty, e.g. `"5"`. Omitted if absent. |
| `best` | bool | `true` if the macro was `\bestresult` (highlighted as best in row) |

The `text` field is `"value ± error"` (or just `value` if no error).

## Practical filters

```bash
# Authored numerical results (prime fact-check candidates)
jq -c 'select(.type=="prose" and .is_first_person and .is_numeric)' claims.jsonl

# Hedged or conditional claims (less assertive; lower-priority for verification)
jq -c 'select(.epistemic != "asserted")' claims.jsonl

# Claims citing prior work
jq -c 'select((.cite_keys // []) | length > 0)' claims.jsonl

# Definitions (often skip these for verification)
jq -c 'select(.is_definition)' claims.jsonl

# Numerical results from tables
jq -c 'select(.type=="table_cell")' claims.jsonl

# Counts by type
jq -r '.type' claims.jsonl | sort | uniq -c
```

## Notes

- **Provenance is line-level.** Use `paper.tex:{line}` when you need to point to source. Char-level offsets aren't tracked.
- **`section_path` is a list, not a string.** Use `(.section_path | join(" / "))` if you want a flat string.
- **Cross-references** (`\ref{X}`, `\eqref{X}`, `\Cref{X}`) become a literal `<ref>` placeholder in `text` so sentences don't fragment at "In Tab.~". The original key is gone from the JSONL but recoverable from `paper.tex` at the line.
- **Footnotes** are emitted as separate prose claims with `is_footnote: true` rather than folded into the surrounding paragraph.
- **No coreference resolution.** Pronouns like *"It improves accuracy"* reach the JSONL with the antecedent unresolved.
- **Filtered out before emission**: transitions ("In Section X, we now turn to…"), roadmap sentences ("In this paper, we…"), and sentences shorter than four words. These don't appear in the output.
