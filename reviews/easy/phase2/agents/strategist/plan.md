# Strategist — Plan

## Task

Score all 200 claims (C001–C200) on importance, checkability, and relevant
error categories for the Phase 2 checker agents. Write STRATEGY.md.

## Inputs read

- `reviews/easy/phase1/outputs/CLAIMS.md` — 200 claims
- `reviews/easy/phase1/outputs/LITERATURE.md` — 88 COVERED, 112 UNCOVERED
- `reviews/easy/phase1/outputs/FINDINGS.md` — phase-1 summary
- `reviews/easy/phase1/outputs/graph.v1.json` — 20 groups, 20 edges
- `src/conventions/error_categories.md` — five categories
- `src/conventions/verification.md` — placeholder; fallback to defaults

## Approach

### Importance scoring

- **high**: claims central to L-GATr's stated contribution
  (headline numerical/performance results, architectural correctness claims
  about equivariance, formal algebraic definitions, claims that recur in
  abstract/conclusion)
- **medium**: supporting methodology claims, contextual interpretation,
  dataset description, baseline characterization
- **low**: routine procedural statements, uncontroversial background, single
  implementation details with no downstream effect on conclusions

### Checkability scoring

- **high**: claim can be confronted with external evidence (literature, known
  mathematical facts, dataset specs), or with another claim in the paper
- **medium**: claim is partly checkable (ambiguous metrics, partially covered
  by literature)
- **low**: purely interpretive, novelty/intuition language, or impossible to
  verify without running experiments

### Category assignment rationale

The 112 UNCOVERED claims are prime `unreferenced` candidates; they lack any
independent external citation. Among these, claims making quantitative or
comparative assertions without citing a data source deserve the highest priority.

The algebraic definition claims (C018–C027, C031, C035, C041, C043, C045,
C049, C150, C151) have external support via hestenes1966/vaswani2017 but are
mathematical statements that can be wrong — `domain_violation` is the primary
risk.

Headline performance claims (C001, C004, C104, C112, C117, C129, C138, C181,
C183, C195, C197, C198) are both `unreferenced` (no independent source for the
paper's own novel numbers) and `literature_collision` risks (the paper's
numbers must not contradict baseline numbers already in the literature for
those same datasets).

Claims with strong cross-claim dependencies (abstract vs. results vs. appendix)
are `internal_contradiction` candidates.

Interpretive/novelty language ("first time", "significant") without a metric
is `ambiguous`.

## Selection rule

All importance=high claims appear in STRATEGY.md (required). Medium and low
claims are included in full to give checkers complete coverage.

## Output path

`reviews/easy/phase2/outputs/STRATEGY.md`
