## domain_violation

### claim-0052 — FLAGGED — confidence: high
- evidence: paper.txt:133
- violated_principle: The geometric product of two elements of the same grade is not generally commutative. Two grade-k elements (k ≥ 1) do not commute unless they satisfy special algebraic conditions (e.g., vectors are collinear). For vectors: xy = {x,y}/2 + [x,y]/2 but yx = {x,y}/2 − [x,y]/2, so xy = yx only if [x,y] = 0.
- canonical_source: Doran & Lasenby, *Geometric Algebra for Physicists* (Cambridge University Press, 2003), §2.4; Hestenes, *Space-Time Algebra* (1966).
- reasoning: The paper states "the geometric product preserves commutativity when acting on elements of the same grade." This is false. Grade-sameness does not imply commutativity in geometric algebra. Only grade-0 scalars commute with all elements automatically.

### claim-0058 — FLAGGED — confidence: high
- evidence: paper.txt:142
- violated_principle: The difference between G(1,3) (spacetime algebra) and the Dirac algebra is not merely the field of the underlying vector space (R vs C). Over R, C(1,3) ≅ M(2,H) (2×2 matrices over the quaternions), while the standard Dirac algebra is M(4,C). These are non-isomorphic as real algebras with different representations and centers.
- canonical_source: Lounesto, *Clifford Algebras and Spinors* (Cambridge University Press, 2nd ed., 2001), §15; Doran & Lasenby, *Geometric Algebra for Physicists* (2003), §2.5.
- reasoning: The paper states "the only difference being that the spacetime algebra is defined over R^4, whereas the Dirac algebra is defined over C^4." This is an oversimplification that misrepresents the algebraic relationship and would mislead readers about the structural connection.

### claim-0099 — FLAGGED — confidence: high
- evidence: paper.txt:229
- violated_principle: The sandwich product vxv^{-1} with v in the Clifford/Spin/Pin group is grade-preserving by the fundamental theorem of the versor representation. This holds for any v in the group — boosts, rotations, and all their compositions preserve grades.
- canonical_source: Lounesto, *Clifford Algebras and Spinors* (Cambridge University Press, 2001), §17 (versor representation); Doran & Lasenby, *Geometric Algebra for Physicists* (2003), §5.2.
- reasoning: The paper states "in practice grade mixing can occur through the combined action of boosts and rotations on composite multivector states." A product of group elements v₁v₂ is still in the group, and (v₁v₂)x(v₁v₂)^{-1} is still grade-preserving. This contradicts settled algebra.
- cross_reference: claim-0098 ("Lorentz transformations will never mix grades") is the correct statement of the grade-preservation theorem. claim-0099's qualification contradicts it.

### claim-0082 — INCONCLUSIVE — confidence: medium
- reason: The characterization of the interference term 2Re(M_E* M_O) as "a pseudoscalar function of the 4-momenta" is internally consistent with the paper's algebraic formalism (it maps to the γ^5 grade), but whether this constitutes a domain violation depends on interpretation. Insufficient certainty to flag.

### claim-0163 — INCONCLUSIVE — confidence: medium
- reason: The stabilizer of the null vector (1,0,0,±1) under the Lorentz group is the little group ISO(2) (the Euclidean group of the 2D plane), not simply SO(2) as stated. However, in the physical context of beam-axis reference vectors, the relevant symmetry is azimuthal SO(2), which may be what the authors mean. Expert scrutiny warranted but not a clear-cut domain violation.

### claim-0043 — CLEAR — confidence: high
### claim-0047 — CLEAR — confidence: high
### claim-0048 — CLEAR — confidence: high
### claim-0050 — CLEAR — confidence: high
### claim-0051 — CLEAR — confidence: high
### claim-0053 — CLEAR — confidence: high
### claim-0055 — CLEAR — confidence: high
### claim-0057 — CLEAR — confidence: high
### claim-0061 — CLEAR — confidence: high
### claim-0062 — CLEAR — confidence: medium
### claim-0063 — CLEAR — confidence: high
### claim-0071 — CLEAR — confidence: high
### claim-0076 — CLEAR — confidence: high
### claim-0080 — CLEAR — confidence: high
### claim-0086 — CLEAR — confidence: high
### claim-0088 — CLEAR — confidence: high
### claim-0089 — CLEAR — confidence: medium
### claim-0091 — CLEAR — confidence: high
### claim-0096 — CLEAR — confidence: high
### claim-0097 — CLEAR — confidence: high
### claim-0098 — CLEAR — confidence: high
### claim-0100 — CLEAR — confidence: high
### claim-0101 — CLEAR — confidence: high
### claim-0106 — CLEAR — confidence: high
### claim-0108 — CLEAR — confidence: high
### claim-0117 — CLEAR — confidence: high
### claim-0119 — CLEAR — confidence: high
### claim-0122 — CLEAR — confidence: high
### claim-0123 — CLEAR — confidence: high
### claim-0127 — CLEAR — confidence: high
### claim-0128 — CLEAR — confidence: high
### claim-0133 — CLEAR — confidence: high
### claim-0138 — CLEAR — confidence: high
### claim-0147 — CLEAR — confidence: medium
### claim-0148 — CLEAR — confidence: high
### claim-0152 — CLEAR — confidence: high
### claim-0189 — CLEAR — confidence: high
### claim-0196 — CLEAR — confidence: high
### claim-0204 — CLEAR — confidence: medium
### claim-0382 — CLEAR — confidence: high
### claim-0396 — CLEAR — confidence: high
### claim-0399 — CLEAR — confidence: high
### claim-0401 — CLEAR — confidence: high
### claim-0402 — CLEAR — confidence: high
### claim-0403 — CLEAR — confidence: high
### claim-0473 — CLEAR — confidence: medium
### claim-0504 — CLEAR — confidence: high
### claim-0508 — CLEAR — confidence: high

Remaining low-importance prose claims (definitions, hedged, footnotes, non-algebra topics): CLEAR (batch).
