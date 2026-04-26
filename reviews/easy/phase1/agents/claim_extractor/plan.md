# Claim Extraction Plan — easy

## Paper Overview
- Title: "A Lorentz-Equivariant Transformer for All of the LHC"
- Authors: Brehmer, Bresó, de Haan, Plehn, Qu, Spinner, Thaler
- Type: Machine learning for particle physics
- Pages: 1-29 (with references and appendices)

## Extraction Strategy

### Scope
The paper presents L-GATr, a Lorentz-equivariant transformer architecture for high-energy physics applications. It includes:
1. Theoretical framework (geometric algebra, equivariance properties)
2. Three case studies: amplitude regression, jet tagging, event generation
3. Benchmarking against baselines
4. Training details and hyperparameters

### Claim Categories Identified

#### result (empirical findings, performance metrics)
- Claims about L-GATr performance on specific tasks
- Comparative results vs baselines (accuracy, AUC, rejection rates)
- Scaling behavior analysis
- Performance on datasets (top tagging, JetClass, event generation)

#### method (architectural choices, procedures)
- Descriptions of L-GATr network construction
- Layer definitions (Linear, Attention, LayerNorm, Activation)
- Symmetry breaking mechanisms
- Reference vector approaches
- Training procedures for each task
- Loss functions and optimization choices

#### prior_work (attributed claims)
- Results from referenced papers
- Established techniques cited as background

#### background_fact (domain knowledge without attribution)
- Physical principles (Lorentz invariance, geometric algebra)
- Standard ML concepts
- Physical symmetry structures

#### assumption
- Data cut constraints
- Dataset splits
- Initialization strategies
- Network architecture assumptions

#### interpretation
- Explanations of why L-GATr performs better
- Causal inferences from results
- Analysis of contributing factors

#### definition
- Mathematical definitions (spacetime algebra, multivector, bivector)
- Formal specifications (geometric product, Lorentz transformation)

### Granularity Rules Applied
- One claim per proposition (compound sentences split)
- Include subject and verifiable predicate
- Exclude bare descriptive statements ("Section X presents...")
- Extract claims from table captions and figure descriptions
- Split cited contributions into separate typed claims

### Confidence Heuristics
- `high`: Direct empirical results with specific numbers, single-proposition sentences
- `medium`: Type selections between categories, split compound sentences, hedged statements
- `low`: Required substantial paraphrase, grammatical ambiguity, judgment calls

### Coverage Plan
1. **Abstract & Introduction (Pages 1-3)**: Goal statements, motivation, prior work summary
2. **Section 2 - Architecture (Pages 3-8)**: Mathematical definitions, layer definitions, scaling analysis
3. **Section 3 - Amplitude Regression (Pages 9-11)**: Training setup, performance results, comparative analysis
4. **Section 4 - Jet Tagging (Pages 11-14)**: Dataset, results on top tagging and multiclass (JetClass), pre-training
5. **Section 5 - Event Generation (Pages 15-20)**: CFM setup, symmetry breaking, performance results
6. **Section 6 - Outlook (Page 21)**: Summary statements
7. **Appendix A (Pages 27-29)**: Training hyperparameters and implementation details

### Notes on Source PDF
- The source PDF was corrupted (paper_corrupted.pdf)
- Extracted text shows some formatting inconsistencies but is overall readable
- No obvious OCR errors detected that would affect claim extraction
- Page breaks marked with `=== PAGE N ===` markers are reliable for provenance

### Exclusions
- Pure numerical tables (Table 2, Table 3, etc.) without interpretive text
- Section headings and table of contents
- Acknowledgement section
- Code availability statements (not claims, descriptive only)
