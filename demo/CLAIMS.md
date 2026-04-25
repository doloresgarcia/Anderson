# CLAIMS — EfficientFlow demo

| claim_id | type | sentence | hedged | confidence | page | line | section | provenance |
|----------|------|----------|--------|------------|------|------|---------|------------|
| C001 | result | "EfficientFlow, a sparse attention mechanism that achieves 87.3% F1 on the GLUE benchmark" | false | high |  | 7 | abstract | paper.txt:7 |
| C002 | result | "reducing memory consumption by 40% relative to standard attention" | false | high |  | 8 | abstract | paper.txt:8 |
| C003 | method | "we route tokens through a learned sparse pattern that scales linearly with sequence length" | false | high |  | 10 | abstract | paper.txt:10 |
| C004 | prior_work | "Building on Chen et al. (2024)" | false | medium |  | 9 | abstract | paper.txt:9 |
| C005 | interpretation | "Our method demonstrates that attention sparsity is sufficient for emergent reasoning capability in transformer language models." | false | medium |  | 11 | abstract | paper.txt:11 |
| C006 | background_fact | "Standard attention has O(n^2) complexity in sequence length n" | false | high |  | 17 | 1 | paper.txt:17 |
| C007 | method | "We use a 12-layer transformer with 768 hidden dimensions" | false | high |  | 26 | 2 | paper.txt:26 |
| C008 | method | "We propose EfficientFlow, which routes each query token to k=8 key tokens selected by a small router network." | false | high |  | 24 | 2 | paper.txt:24 |
| C009 | result | "EfficientFlow achieves an average score of 78.4% across 9 tasks" | false | high |  | 32 | 3 | paper.txt:32 |
| C010 | result | "a 0.4% improvement over the standard attention baseline" | false | medium |  | 33 | 3 | paper.txt:33 |
| C011 | result | "Memory consumption drops 40% at sequence length 4096." | false | high |  | 35 | 3 | paper.txt:35 |
| C012 | interpretation | "Our results suggest that learned sparsity recovers most of the performance of dense attention." | true | medium |  | 41 | 4 | paper.txt:41 |
| C013 | interpretation | "We thus prove that sparsity is sufficient for emergent reasoning." | false | high |  | 44 | 4 | paper.txt:44 |
