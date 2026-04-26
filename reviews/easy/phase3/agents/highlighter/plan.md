# Highlighter Plan for easy review

## Task
Highlight sentences in the paper PDF based on VERIFICATION.md verdicts from Phase 2.

## Inputs
- CLAIMS.md: 203 extracted claims with provenance (page, line)
- VERIFICATION.md: Verdicts for each claim (FLAGGED, CLEAR, INCONCLUSIVE) across 5 checkers (unreferenced, ambiguous, internal_contradiction, literature_collision, domain_violation)
- paper.pdf: The original paper to highlight
- error_categories.md: Color mapping and severity order

## Color Mapping
- Blue (#4285F4): unreferenced
- Amber (#FFBF00): ambiguous
- Orange (#FF6D00): internal_contradiction
- Red (#D32F2F): literature_collision
- Purple (#7B1FA2): domain_violation
- Yellow (#F1C40F): INCONCLUSIVE (no FLAGGED category)

Severity order (highest first): domain_violation > literature_collision > internal_contradiction > ambiguous > unreferenced

## Key findings from VERIFICATION.md
The VERIFICATION.md file contains detailed verdicts for all 203 claims across the five checker categories. Key observations:
- Many CLEAR verdicts (no highlight needed)
- Multiple FLAGGED and INCONCLUSIVE verdicts in ambiguous category (most common)
- FLAGGED unreferenced claims (C007, C060, C070, C094, C142, C162, C191)
- FLAGGED internal_contradiction claims (C004, C112, C183, C185)
- Needs to identify all FLAGGED or INCONCLUSIVE claims and apply appropriate highlighting

## Execution
1. Read the full VERIFICATION.md file to identify all FLAGGED/INCONCLUSIVE claims
2. For each flagged/inconclusive claim, determine:
   - Which error categories triggered (FLAGGED or INCONCLUSIVE)
   - The most severe category (for color selection)
   - Page and line from CLAIMS.md
3. Run highlight_paper.py with the review slug
4. Verify PDF output is created

## Expected Output
- reviews/easy/phase3/outputs/paper.highlighted.pdf
