# checker_domain log — review: easy

Date: 2026-04-26

## Sources read
- `reviews/easy/phase1/outputs/CLAIMS.md` (C001–C200)
- `reviews/easy/paper/paper.txt`
- `reviews/easy/paper/paper.meta.json`
- `reviews/easy/phase2/outputs/STRATEGY.md`
- `src/conventions/error_categories.md`
- `src/conventions/confidence.md`
- `src/methodology/05-artifacts.md`
- Memory: `.claude/agent-memory/checker_domain/MEMORY.md`

## Approach
All 200 claims were reviewed. The strategy flagged algebraic/architectural
claims (C019–C027, C032, C034, C035, C038–C050, C055–C056, C058, C063–C068,
C094, C150–C155, C162, C172) as primary domain-violation candidates. Other
claims were also screened.

## Key decisions

### C068 — FLAGGED
The paper claims xV± = (1,0,0,±1) breaks Lorentz equivariance to "SO(3)
equivariance under spatial rotations." Group-theoretically, including both a
timelike vector (1,0,0,0) and a spacelike beam vector (0,0,0,1) as implicit
reference directions (via the linear combinations xV± = (1,0,0,±1) = (1,0,0,0)
± (0,0,0,1)) fixes BOTH the time direction and the beam direction. The subgroup
of the Lorentz group that preserves both vectors simultaneously is
Stab{(1,0,0,0)} ∩ Stab{(0,0,0,1)} = SO(3) ∩ {rotations around z and boosts
along z} = SO(2) (rotations around the beam axis only).

The paper's claimed preserved subgroup is SO(3), which is incorrect. SO(3)
would require that all spatial rotations (including those that rotate the beam
direction) be preserved, but the beam direction is explicitly fixed. Only
rotations around the beam axis (SO(2)) are preserved.

The paper even acknowledges that "these multivectors are linear combinations of
vectors pointing in the time and beam directions," which correctly identifies
that both directions are fixed — but then incorrectly states the resulting
preserved subgroup as SO(3) rather than SO(2).

Confidence: medium (the group theory is standard, but the paper's description
is somewhat informal and there is a possibility the authors intended a different
meaning of "SO(3)" that I am not seeing; however, taken at face value, the
claim is wrong).

### CFM convention (C151, C153, C155) — CLEAR
This paper uses the same convention as the "hard" review paper (same group:
Plehn et al.): x0=data (t→0), x1=latent (t→1). This is the reverse of
Lipman 2022 canonical convention but is internally consistent. Not a domain
violation.

### γ5 factor of i (C026) — CLEAR
The standard QFT definition is γ5 = iγ0γ1γ2γ3 (to ensure hermiticity). The
paper uses γ5 = γ0γ1γ2γ3 (real spacetime algebra, no factor of i). The paper
correctly notes the "missing factor i" as the difference between the complex
Dirac algebra and the real spacetime algebra. Verified against Wikipedia /
Peskin & Schroeder.

### G_{1,3} inner product zero/negative contributions (C046) — CLEAR
Standard property of indefinite-metric Clifford algebra. Noted in memory.

### Non-compact group normalization (C162) — CLEAR
Standard Haar measure theorem. The Lorentz group is non-compact, so no
normalizable Lorentz-invariant probability measure exists.

### Geometric product decomposition (C019) — CLEAR
Verified against standard GA textbooks (Hestenes 1966).

### Boost formula (C034) — CLEAR
σ03² = +1 (timelike bivector), so exp(ωσ03/2) = cosh(ω/2) + σ03 sinh(ω/2).
The resulting Lorentz boost formula is correct.

### Grade non-mixing under Lorentz transformations (C035) — CLEAR
Standard property of pin/spin group action in Clifford algebra.

### Linear layer completeness claim (C041) — CLEAR
By Schur's lemma, the most general equivariant linear map within a single
channel is a scalar multiple of the identity on each irreducible subspace
(= each grade). The γ5 term extends this to the special orthochronous group.

### Scalar-gated activation (C049) — CLEAR
Multiplying by a Lorentz scalar preserves grade structure; equivariance holds.
Confirmed from memory (hard review).

### Equivariance of geometric product (C050) — CLEAR
GP(vxv⁻¹, vyv⁻¹) = v·GP(x,y)·v⁻¹ follows trivially from associativity of
the geometric product.

## Claims not examined in depth (low domain-violation risk)
Background claims about LHC ML (C005–C013, C089–C093, C110–C112),
implementation details (C075–C088), dataset descriptions (C113–C116, C122–C126),
pre-training/fine-tuning procedures (C132–C137), and all interpretation claims
that are the authors' own assessments were screened and found to present no
domain violation candidates.
