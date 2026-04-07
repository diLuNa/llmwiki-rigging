---
title: "Generating 3D Faces using Convolutional Mesh Autoencoders"
authors: [Ranjan, Anurag; Bolkart, Timo; Sanyal, Soubhik; Black, Michael J.]
venue: European Conference on Computer Vision (ECCV 2018)
year: 2018
tags: [neural, digital-human, blendshapes, rig-generation, mesh-graph-nets]
source: raw/papers/1807.10267v3.pdf
---

## Summary
CoMA introduces convolutional autoencoders that operate directly on 3D mesh surfaces using spectral graph convolutions and hierarchical mesh pooling. Trained on a large facial expression dataset, CoMA learns a compact, nonlinear face space that outperforms PCA-based 3DMMs for interpolation, extrapolation, and expression generation — while remaining compatible with the fixed mesh topology of production face rigs.

## Problem
Linear 3D morphable models (3DMM, PCA-based) cannot represent extreme expressions or fine-scale details with a compact basis. Full mesh autoencoders using standard CNNs require UV parameterization (distortion, seam artifacts). A mesh-native, nonlinear model that generalizes like a neural network but works directly on 3D mesh topology is needed.

## Method
**Graph Laplacian and spectral convolution:**

Given mesh $(V, F)$ with adjacency $A$, degree matrix $D$, Laplacian $L = D - A$. Spectral convolution with a $K$-th order Chebyshev polynomial filter:
```math
g_\theta(L) = \sum_{k=0}^{K-1} \theta_k T_k(\tilde{L}), \quad \tilde{L} = \frac{2L}{\lambda_{\max}} - I_n
```
Applied to feature matrix $x \in \mathbb{R}^{n \times F_{in}}$:
```math
y_j = \sum_{i=1}^{F_{in}} g_{\theta_{i,j}}(L) x_i \in \mathbb{R}^n
```

**Hierarchical mesh pooling/upsampling:**
- Downsampling matrix $Q_d \in \{0,1\}^{n \times m}$: selects vertices by mesh simplification (edge contraction). Discarded vertices get barycentric weights from retained neighbors.
- Upsampling matrix $Q_u \in \mathbb{R}^{m \times n}$: inverse barycentric mapping.
- Alternating pooling → features go from $n \times F$ to $m \times F$ tensors.

**Autoencoder architecture:**
- Encoder: 4 × [Cheb-Conv + Pool] → FC(32) → latent $z \in \mathbb{R}^8$
- Decoder: FC(32) → 4 × [Upsample + Cheb-Conv] → $5023 \times 3$ (FLAME mesh)
- Trained with MSE reconstruction loss on vertex positions.

## Key Results
- Latent space of dimension 8 captures the full expression space of the COMA dataset (12 extreme expressions).
- Extrapolates to unseen expressions better than PCA.
- Interpolation in latent space produces smooth, plausible intermediate expressions.
- Scales to large meshes (5023 vertices) without UV parameterization artifacts.

## Limitations
- Fixed mesh topology: requires all training meshes to be in correspondence.
- Spectral convolution is sensitive to mesh resolution changes (filters must be recomputed per mesh).
- Does not handle texture; purely geometry.
- Latent space dimension 8 is sufficient for expression but too small for cross-identity variation.

## Connections
- [[papers/li-2017-flame]] — CoMA uses the FLAME mesh topology (5023 vertices); FLAME is the linear predecessor
- [[papers/zheng-2022-imface]] — ImFace extends CoMA-style ideas to implicit neural representations
- [[papers/loper-2015-smpl]] — SMPL is the body equivalent; CoMA is face-specific
- [[papers/pfaff-2021-meshgraphnets]] — related architecture (graph nets on meshes); different task (simulation vs generation)
- [[authors/black-michael]] — senior author, leads MPI-IS body/face model work

## Implementation Notes
CoMA is publicly available (MPI-IS GitHub). The key Houdini integration point:
- Export the trained encoder as ONNX; encode source face mesh to latent $z$.
- Decode to get mesh vertex positions.
- Use as a nonlinear blendshape space: $z$ replaces the blendshape weight vector $w$.

The Chebyshev convolution at $K=6$ approximates localized spectral filters without computing full eigendecomposition — practical for meshes up to ~50k vertices.
