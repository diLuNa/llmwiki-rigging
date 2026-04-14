---
title: "Compressed Skinning for Facial Blendshapes"
authors: [Kavan, Ladislav; Doublestein, John; Prazak, Martin; Cioffi, Matthew; Roble, Doug]
venue: ACM Transactions on Graphics (SIGGRAPH 2024)
year: 2024
tags: [skinning, blendshapes, compression, facial-animation, lbs]
source: ~no local PDF~
doi: 10.1145/3641519.3657477
---

## Summary
Sparse linear blend skinning (LBS) formulation for facial blendshapes achieving ~90% sparsity (10% non-zero weights) while maintaining production quality. Enables efficient real-time evaluation and reduces memory footprint significantly. Method applicable to any blendshape-based facial rig.

## Problem
Traditional LBS for facial blendshapes uses dense weight matrices (every vertex affected by many shapes). Sparse weights reduce computation, memory, and improve rig interpretability. Challenge: find sparse weights without sacrificing quality or introducing artifacts.

## Method
- **Sparse optimization**: Solve for blendshape weights with L0/L1 sparsity constraints
- **Quality metrics**: Per-vertex error, temporal coherence, blend shape interpretability
- **Reconstruction**: Harmonic reconstruction for smooth sparse weight distribution

## Key Results
- 90% sparsity achievable with <2mm error on production characters
- 2-3× speedup in blendshape evaluation
- Significant memory savings (dense → sparse matrix storage)
- Successfully deployed in production (Meta)

## Limitations
- Sparsity depends on rig design; some rigs may not compress as well
- Training/optimization overhead (one-time cost)
- Very sparse weights (95%+) may hurt generalization to unseen expressions

## Connections
- [[papers/lewis-2014-blendshape-star]] — blendshape survey; traditional dense approach
- [[papers/li-2021-neural-blend-shapes]] — neural learned blendshapes
- [[papers/bailey-2020-fast-deep-facial]] — fast facial deformation via learned residuals
- [[papers/radzihovsky-2020-facebaker]] — facial rig approximation and compression
- [[concepts/blendshapes]] — blendshape fundamentals
- [[techniques/ml-deformer]] — related deformation approximation

## Implementation Notes
- Sparse LBS requires sparse matrix libraries for efficient evaluation
- Sparsity pattern can be precomputed; runtime is essentially unchanged
- Applicable to facial rigs, body secondary motion, cloth simulation

## External References
- ACM DL: [doi.org/10.1145/3641519.3657477](https://doi.org/10.1145/3641519.3657477)
- arXiv: [arxiv.org/abs/2406.11597](https://arxiv.org/abs/2406.11597)
