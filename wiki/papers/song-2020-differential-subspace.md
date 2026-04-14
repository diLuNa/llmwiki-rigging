---
title: "Accurate Face Rig Approximation with Deep Differential Subspace Reconstruction"
authors: [Song, Steven L.; Shi, Weiqi; Reed, Michael]
venue: ACM Transactions on Graphics (SIGGRAPH 2020)
year: 2020
tags: [neural, blendshapes, facial-capture, real-time, correctives, math]
source: ~no local PDF~
doi: 10.1145/3386569.3392491
---

## Summary
Alternative to CNN-based facial rig approximation (Bailey 2020). Uses differential coordinates to learn localized shape deformations in a learned reconstruction subspace. Produces smoother per-vertex error distribution than CNN approaches, enabling higher quality approximations at similar computational cost. Blue Sky Studios production-tested method.

## Problem
CNN-based approximation (Bailey 2020) works well but can produce uneven error distribution — some regions approximated perfectly, others with visible artifacts. Differential coordinate-based approach offers tighter control over geometric quality. Also addresses training data requirements: can work with sparser pose sampling.

## Method

### Differential Coordinate Representation
Uses **differential coordinates** (Laplacian) rather than absolute vertex positions:
```math
\delta_i = v_i - \frac{1}{|N(i)|} \sum_{j \in N(i)} v_j
```
where $N(i)$ are neighbors of vertex $i$ in the mesh. Differential coordinates capture local shape detail and curvature.

### Decomposition
1. **Linear component**: LBS (absolute positions from skeleton)
2. **Differential residual**: Learn per-vertex differential coordinate offsets via neural network
3. **Reconstruction**: Convert differential coordinates back to absolute positions via harmonic reconstruction

### Architecture
- **Input**: Pose parameters (blend shape weights, joint angles)
- **Encoder**: Compress pose vector via PCA or learned bottleneck
- **Decoder**: Predict per-vertex differential coordinate deltas
- **Loss**: Reconstructed position error in 3D space (not differential space directly)
- **Regularization**: Optional smoothness term on differential coordinates

### Key Insight
Differential coordinates naturally encode **local geometric constraints**. Learning corrections in differential space produces meshes that respect neighbor relationships, yielding smoother surfaces than unconstrained per-vertex predictions. Harmonic reconstruction from (modified) differential coordinates is well-conditioned and fast.

## Key Results
- **Comparable speed to CNN**: Real-time evaluation on hero facial geometry
- **Superior error distribution**: Artifacts distributed evenly across surface rather than localized
- **Sparser training data**: Works well with fewer example poses than CNN approach
- **Production validated**: Successfully used in Blue Sky Studios character pipeline
- **Generalization**: Slightly better extrapolation than Bailey CNN on unseen poses

## Limitations
- Requires mesh connectivity information — not applicable to point clouds or unstructured data
- Differential reconstruction adds computation vs raw coordinate prediction
- Still requires representative training pose set (though sparser than CNN)
- Learned subspace may not fully capture all localized effects (e.g., dynamic wrinkles)

## Connections
- [[papers/bailey-2020-fast-deep-facial]] — concurrent 2020 work; alternative to CNN decomposition
- [[papers/radzihovsky-2020-facebaker]] — Pixar; compares multiple approaches including this one
- [[papers/li-2021-neural-blend-shapes]] — later work; joint skeleton + weights + neural correctives
- [[concepts/laplacian-smoothing]] — differential coordinates and Laplacian mesh processing
- [[concepts/pose-space-deformation]] — pose → deformation framework
- [[techniques/ml-deformer]] — Houdini tool implementing multiple neural facial approximation methods
- [[authors/song-steven]] — first author

## Implementation Notes
- **Differential coordinate extraction**: Cotangent Laplacian or simple uniform averaging
- **Reconstruction**: Sparse linear solve via Cholesky decomposition or iterative method
- **PCA dimensionality**: Typically 10–50 dimensions for pose parameters
- **Network architecture**: 3–4 fully connected hidden layers, output = 3N (for N-vertex mesh)
- **Training loss**: MSE on reconstructed 3D positions (not differential coordinates directly)
- **Inference pipeline**: 
  1. Evaluate LBS (absolute positions)
  2. Run network to get differential residuals
  3. Add residuals to LBS differential coordinates
  4. Reconstruct absolute positions from (modified) differential coords
  5. Output final vertex positions

## External References
- ACM DL: [doi.org/10.1145/3386569.3392491](https://doi.org/10.1145/3386569.3392491)
- Blue Sky Studios production validated
