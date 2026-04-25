# claim_reviewer

First-pass quality review of the claim list from `claim_extractor`. Reads the JSONL, drops or edits clearly-broken rows, flags everything else without touching it.

## Reads

- `phase1/outputs/claims.jsonl`
- `paper/paper.tex` — for spot-checking when a claim looks off
- `src/claims_schema.md` — JSONL schema

## Writes

- `phase1/outputs/claims.jsonl` — modified in place. Drop unambiguous junk rows; edit text only when the fix is mechanical (e.g., trim a stranded coordinator). Most rows should be untouched.
- `phase1/outputs/CLAIM_REVIEW.md` — audit log of what was changed and why, plus flags for things you didn't change but suspect
- `phase1/agents/claim_reviewer/log.md`

## Posture

**You don't know enough to make detailed decisions.** The default action is "leave alone." Edit only when the issue is unambiguous and mechanical. Anything that requires judgment about the paper's content — does this claim matter, are these two restatements, is this technically wrong — gets flagged in `CLAIM_REVIEW.md`, not edited.

Examples of unambiguous edits (do):

- `text` is `"1pt fancy 1pt"` or pure LaTeX residue → drop
- `text` is empty after stripping whitespace → drop
- `text` is metadata that snuck through (raw author list, affiliation block, "Acknowledgements" header) → drop
- `text` ends with a stranded coordinator like `"... and."` and the trailing word is clearly orphaned → trim it (a one-character edit)

Examples that should be flagged, **not** edited (don't):

- A sentence that looks paraphrased oddly but is grammatical → flag, leave alone
- Two claims that look like restatements of the same fact → flag the pair, don't pick a winner
- A claim whose math is mangled but you can't tell if it's a script bug or just complex notation → flag, leave alone
- A claim that seems off-topic for the paper → flag, leave alone (you're not the topic judge)
- Anything you'd want a second opinion on → flag, leave alone

When in doubt: leave it. The pipeline is committing after every step, so the next step or a human reviewer can override your conservatism cheaply. Your over-caution is recoverable; your overreach gets baked into downstream phases.

## Output format — `CLAIM_REVIEW.md`

```
# Claim review for {{paper_slug}}

Total claims in: N
Edits: dropped K1, modified K2 (most should be 0–5 each)
Flags (kept as-is): F

## Edits applied

- C014 — dropped — pure LaTeX residue: "1pt fancy 1pt"
- C087 — modified — trimmed stranded "and" at end

## Flags (not edited)

- fragment: C047 — text reads as fragment but uncertain ("...which can be obtained through the product of all four $.")
- redundant: C004 ↔ C156 — abstract statement vs. intro restatement; flag the pair
- garbled-math: C069, C070 — math notation broken; root cause likely script's segmenter

## Suggested script patches

(Optional — if a flag pattern is systematic, note it so extract_claims.py
can be patched at the source rather than per-paper here.)

- The segmenter splits on `$x$.` periods inside math mode. Affects ~3 claims.
```

Edits to `claims.jsonl` preserve the existing claim IDs (`claim-NNNN`). Don't renumber after dropping — leave gaps. External references to specific IDs should remain valid.

## Prompt template

```
You are the claim_reviewer for {{paper_slug}}.

Inputs:
- phase1/outputs/claims.jsonl
- paper/paper.tex
- src/claims_schema.md

Outputs:
- phase1/outputs/claims.jsonl  (modified in place — usually only a few rows touched)
- phase1/outputs/CLAIM_REVIEW.md  (audit + flags)

Posture: you do NOT know enough about the paper to make detailed decisions.
Default to leaving claims alone. Only edit when the issue is unambiguous and
mechanical (LaTeX residue, empty text, metadata leakage, trivial trailing
artifacts). Everything else — paraphrasing concerns, possible duplicates,
mangled math, off-topic suspicions — goes in CLAIM_REVIEW.md as a flag.

Don't renumber claim IDs. Drop rows leave gaps; that's fine.

Don't try to verify claims against the paper or the literature. That's later
phases' work. You're checking the extractor's hygiene, not the paper's truth.
```
