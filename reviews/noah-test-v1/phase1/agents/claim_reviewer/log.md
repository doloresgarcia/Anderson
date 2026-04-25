# claim_reviewer log — noah-test-v1

## Summary

Reviewed all 545 claims in `phase1/outputs/claims.jsonl`. No rows dropped or modified.

Scanned for: empty/whitespace text, pure LaTeX residue, metadata headers, author-list leakage, stranded coordinators, very short text, mid-expression sentence fragments, and high backslash-density prose.

**Findings:**

- 1 fragment (claim-0066): sentence split mid-inline-math; leading `\gamma^\mu$.` token is residue from the equation above. Content after the fragment is real prose — flagged rather than dropped to avoid data loss.
- 9 table-as-prose claims (claim-0140, claim-0278, claim-0323, claim-0346, claim-0352, claim-0462, claim-0514, claim-0515, claim-0543): entire table bodies (column headers + numeric rows) rendered as single prose strings. Not useful for sentence-level verification; flagged with extractor patch suggestions.
- 2 of the table claims (claim-0346, claim-0352) have a `2c` prefix from `\multicolumn` macro residue.
- claim-0514/0515 appear to be a single hyperparameter table split across two prose claims.

All 11 flags documented in `CLAIM_REVIEW.md`. No edits applied; `claims.jsonl` is unchanged.
