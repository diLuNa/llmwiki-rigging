---
title: "Mesh Variational Autoencoders with RIMD Features for 3D Shape Synthesis"
authors: [(Authors uncertain — arXiv 1709.04307)]
venue: arXiv preprint (September 2017) / CVPR 2018 (likely)
year: 2017
tags: [neural, digital-human, blendshapes, rig-generation, math]
source: raw/papers/1709.04307v3.pdf
---

## Summary
Learns a variational autoencoder for 3D mesh generation using Rotation-Invariant Mesh Difference (RIMD) features — rotation matrix differences and symmetric strain matrices between adjacent vertex pairs. The RIMD representation is intrinsically invariant to rigid body motion, making the learned latent space encode only shape deformation, not pose. Applied to 3D face shape synthesis and interpolation.

## Problem
Standard mesh autoencoders encode absolute vertex positions, conflating pose (rigid body motion) with shape (intrinsic deformation). A representation invariant to rigid transforms would allow the latent space to encode only meaningful shape differences, improving interpolation and generation quality.

## Method
**RIMD feature extraction:**

For each vertex $v_i$ and its neighbors $j \in \mathcal{N}_i$, the local deformation from a reference mesh is described by:
- **Relative rotation** $dR_{ij} = R_i^T R_j \in SO(3)$, encoded as its matrix logarithm (3 values)
- **Symmetric strain** $S_i$ (polar decomposition: $T_i = R_i S_i$), encoded as 6 values

Feature vector $f_i = \{log(dR_{ij}), S_i\}_{j \in \mathcal{N}_i}$ — rigid-motion invariant.

**VAE in RIMD space:**
- Encode mesh $\mathcal{M}$ → RIMD features $\tilde{f}$ → latent $z$ via graph encoder
- Decode $z$ → reconstructed RIMD features $\hat{f}$ → recover mesh vertices via RIMD reconstruction
- Loss: $\mathcal{L} = \frac{\alpha}{2M}\sum_j \sum_i (\hat{f}_{ij} - \tilde{f}_{ij})^2 + D_{KL}(q(z|\tilde{f}) \| p(z))$

**Mesh reconstruction from RIMD:**
Given predicted $\{dR_{ij}, S_i\}$, recover absolute vertex positions by solving a linear system (global consistency requires a reference vertex).

## Key Results
- Interpolation in RIMD-VAE latent space produces pose-invariant shape blending.
- Better reconstruction of non-rigid deformation than absolute-position VAE baselines.
- Demonstrated on facial expression synthesis and 3D body shape generation.

## Limitations
- RIMD feature computation and reconstruction adds overhead vs. direct position encoding.
- Global pose is discarded — must be re-applied separately for animation.
- Author list uncertain (PDF text extraction quality limited).

## Connections
- [[papers/ranjan-2018-coma]] — CoMA uses a similar mesh VAE architecture but with absolute positions and Chebyshev spectral convolution
- [[papers/sorkine-2007-arap]] — RIMD features relate to ARAP's per-triangle rotation estimation
- [[papers/loper-2015-smpl]] — SMPL's shape PCA is the linear baseline; RIMD-VAE replaces PCA with a nonlinear VAE
- [[concepts/blendshapes]] — the RIMD latent space serves as a nonlinear alternative to explicit blendshape weights
