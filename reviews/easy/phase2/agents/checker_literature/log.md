# checker_literature log — review: easy

## Dispatch summary

- Date: 2026-04-26
- Claims examined: 88 COVERED (C001–C200 with at least one external candidate in LITERATURE.md)
- Claims with no candidates (UNCOVERED): 112 — these receive no literature_collision verdict per contract (absence of literature is not a collision)
- Verdicts: 87 CLEAR, 1 FLAGGED, 0 INCONCLUSIVE

## Sources read

- `reviews/easy/phase1/outputs/CLAIMS.md` (200 claims)
- `reviews/easy/phase1/outputs/LITERATURE.md` (88 COVERED, 112 UNCOVERED)
- `reviews/easy/phase1/outputs/references.bib` (35 entries)
- `reviews/easy/paper/paper.txt` (2425 lines; selected sections read)
- `reviews/easy/phase2/outputs/STRATEGY.md`
- `src/conventions/error_categories.md`
- `src/conventions/confidence.md`
- `src/methodology/05-artifacts.md`
- External fetches: arXiv abstract pages for lipman2022flowmatching (2210.02747), brehmer2023gatr (2305.18415), butter2023jetdiffusion (2305.10475), qu2022part (2202.03772), gong2022lorentznet (2201.08187); Zenodo record 2603256; Cambridge MLG blog on flow matching
- Web searches: flow matching convention; butter2023jetdiffusion methods

## Key findings

### C157 — FLAGGED (the only collision found)

The paper (paper.txt:1421-1422) says:
> "They share the generative CFM setup, which is currently the leading technique in precision generation of partonic LHC events [77]"

Reference [77] = @butter2023jetdiffusion = "Jet Diffusion versus JetGPT — Modern Networks for the LHC" (arXiv:2305.10475, SciPost Phys. Core 8, 026 (2025)).

Investigation: The abstract and title of butter2023jetdiffusion explicitly introduce "two diffusion models and an autoregressive transformer." The paper compares these against normalizing flows. The conclusion is that "LHC physics [is expected] to benefit from dedicated use cases for normalizing flows, diffusion models, and autoregressive transformers." Conditional flow matching (CFM) is not mentioned in the abstract. No external search result or abstract reference supports that this paper discusses or establishes CFM as the leading technique. The reference is misused as support for a claim it does not make.

This is a Category `literature_collision`: the paper attributes a claim about CFM leadership to a source that does not address CFM.

### Flow matching convention (C151-C155) — CLEAR

The paper uses x0=data (t=0), x1=latent/noise (t=1). Lipman et al. (2210.02747) use x0=noise (t=0), x1=data (t=1). This is a notation difference only. The paper defines its convention explicitly and applies the general CFM mathematics correctly with that convention. Confirmed from: Cambridge MLG blog on flow matching ("samples at the final timepoint (t=1) represent the data distribution" in Lipman's convention). The paper's convention is internally consistent and no mathematical conflict exists. All C151-C155 are CLEAR.

### Dataset specifications (C113, C115, C122-C126) — CLEAR

All verified:
- Top tagging dataset (kasieczka2019dataset): 2M jets, pT=550-650 GeV, train/val/test = 1.2M/0.4M/0.4M — confirmed via Zenodo record 2603256
- JetClass (qu2022part): 100M jets, 10 classes, pT=500-1000 GeV, |η|<2.0, MadGraph+Pythia+Delphes CMS card, 4 input feature categories — confirmed from arXiv abstract 2202.03772

### GATr relation (C014, C015) — CLEAR

Confirmed via arXiv abstract 2305.18415 that GATr is designed for E(3) (Euclidean translations, rotations, reflections) and uses projective geometric algebra. The paper's characterisation at paper.txt:117-120 is faithful.

### Hestenes 1966 claims (C018-C035) — CLEAR

All claims citing hestenes1966 are for foundational geometric algebra definitions (geometric product, spacetime algebra, multivector decomposition, sandwich product for Lorentz transformations) that are standard results from that textbook. No external verification was needed beyond confirming the bib record resolves to the correct book.

## UNCOVERED claims — no literature_collision verdict required

The following 112 claims had no external candidates in LITERATURE.md:
C004, C016, C017, C029, C031, C036, C037, C039, C041-C044 (partial), C046-C050, C053-C072, C075-C078, C082, C086, C094, C096-C097, C099-C101, C103-C104, C106-C109, C112, C117-C121, C127-C128, C130-C131, C133-C134, C136-C137, C138-C139, C143, C146-C148, C158-C162, C164-C167, C168-C170, C171-C179, C180-C182, C184-C186, C188-C189, C191-C200.

For UNCOVERED claims, absence of literature is not a collision. These claims may be flagged by other checkers (checker_unreferenced, checker_contradiction, checker_domain) but are out of scope for literature_collision unless a real conflicting source is independently identified. No such source was identified for any of these claims during this check.

## Notes on specific high-priority uncovered claims

The following UNCOVERED high-importance claims (from STRATEGY.md Tier 1) were inspected for potential literature collisions via web search but no relevant contradicting sources were found:
- C112 ("L-GATr sets a new record for jet tagging"): Not contradicted by published baselines at the time of this review. Table 2 shows L-GATr-f.t. achieving best AUC and 1/εB metrics among listed architectures.
- C181 ("enabling percent-level precision in angular correlations for the first time"): A strong novelty claim. No prior published work on Lorentz-equivariant generative networks for LHC events was identified that contradicts this; the claim is UNCOVERED and may require unreferenced checking.
- C129: The improvement over ParT/MIParT in JetClass is self-reported and consistent with the paper's Table 4. No conflicting published baseline numbers detected.

## References not in bib

None. All cited sources in LITERATURE.md resolve to entries in references.bib.
