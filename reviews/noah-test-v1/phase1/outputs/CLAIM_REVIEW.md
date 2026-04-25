# Claim review for noah-test-v1

Total claims in: 545
Edits: dropped 0, modified 0
Flags (kept as-is): 11

## Edits applied

None.

## Flags (not edited)

### fragment

- fragment: claim-0066 — text opens with `\gamma^\mu$.` which is the closing of the inline math from the preceding equation environment (line 162). The sentence was segmented mid-expression; the leading token is LaTeX residue. The remainder ("Pseudoscalars act as chirality projection operations…") is coherent prose. Dropping would lose real content — flag for manual repair or extractor fix.

### table-as-prose

These claims are entire comparison/results/hyperparameter table bodies rendered as a single prose string. They contain no natural-language sentence structure — only column headers, network names, and numeric values concatenated with spaces. They will not be useful as prose claims for downstream verification. Flag for the extractor to handle as `table_cell` rows or to suppress.

- table-as-prose: claim-0140 (line 311) — Layer-type comparison table (Transformer vs. L-GATr) rendered as one prose string; contains full LaTeX formulas for Linear, Attention, LayerNorm, Activation, GP layers.
- table-as-prose: claim-0278 (line 462) — Top tagging results table (Network / Accuracy / AUC / 1/ε_B columns); multiple baselines concatenated.
- table-as-prose: claim-0323 (line 509) — Symmetry-breaking ablation table for top tagging (Beam / Time / Embedding / Extra features / AUC / 1/ε_B); multiple rows concatenated.
- table-as-prose: claim-0346 (line 553) — JetClass multi-class tagging results table header + body row (ParticleNet, ParT, MIParT, L-GATr); starts with malformed `2c` prefix (LaTeX `\multicolumn` residue).
- table-as-prose: claim-0352 (line 585) — JetClass multi-class tagging results table with model-size variants; also starts with `2c` prefix (LaTeX `\multicolumn` residue).
- table-as-prose: claim-0462 (line 779) — Symmetry-breaking ablation table for event generation (Beam / Time / Embedding / NLL / AUC).
- table-as-prose: claim-0514 (line 893) — Hyperparameter table for amplitude regression baselines (partial rows: activation, parameters, optimizer, learning rate, batch size, scheduler, patience).
- table-as-prose: claim-0515 (line 898) — Hyperparameter table continuation (iterations row only); appears to be a split of the same table as claim-0514.
- table-as-prose: claim-0543 (line 957) — Hyperparameter table for event generation (MLP / Transformer / L-GATr and E(3)-GATr).

## Suggested script patches

- The `2c` prefix on claim-0346 and claim-0352 is residue from a LaTeX `\multicolumn{2}{c}{...}` cell — the extractor is picking up the `2c` argument when stripping the macro. A targeted regex on `\multicolumn` before sentence splitting would eliminate this.
- claim-0514 and claim-0515 appear to be two rows from the same table split into two prose claims rather than one (or suppressed entirely). The table parser may be emitting partial rows as prose when it fails to parse them as `\result`/`\bestresult` macros.
- claim-0066 pattern (sentence split inside inline math) could be fixed by detecting when a segmented sentence starts with `\<macro>$` (close-dollar without open-dollar) and merging it with the previous sentence.
