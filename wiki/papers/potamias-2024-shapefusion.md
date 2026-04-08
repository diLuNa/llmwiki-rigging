---
title: "ShapeFusion: A 3D Diffusion Model for Localized Shape Editing"
authors: [Potamias, Rolandos Alexandros; Tarasiou, Michail; Ploumpis, Stylianos; Zafeiriou, Stefanos]
venue: ECCV 2024
year: 2024
tags: [neural, digital-human, blendshapes, rig-generation, math]
source: raw/papers/2403.19773.pdf
---

## Summary
ShapeFusion trains a DDPM diffusion model over FLAME-topology meshes with a masked diffusion strategy, enabling fully localized shape edits — any arbitrary facial region, not just predefined FACS zones — while completely preserving unmasked geometry. Applications include FACS-localized expression manipulation, cross-identity region transplantation, and scan fitting. Offers more interpretable edits and faster inference than optimization-based parametric model fitting.

## Problem
Linear 3DMMs and PCA blendshapes suffer from orthogonality constraints that couple global and local shape — editing one region leaks into others. FLAME's blendshape basis cannot represent truly localized edits without affecting the rest of the face. Existing diffusion models for shapes operate globally. A generative model that supports *any* localized edit region with strict masking constraints is missing.

## Method
**Base representation:** FLAME-registered mesh vertices $V \in \mathbb{R}^{N \times 3}$ as the shape domain.

**Diffusion model:** DDPM over mesh vertex coordinates. The backbone is a graph neural network operating on FLAME's mesh connectivity.

**Masked diffusion training:** At each training step, a random binary vertex mask $\mathbf{m}$ is sampled. The noising process applies only to masked vertices; unmasked vertices are held fixed. The denoising network is conditioned on:
- The fixed (unmasked) vertex positions as context.
- The mask itself.

At inference: given a source mesh and a user-defined edit region mask, the diffusion process generates plausible geometry for the masked region conditioned on the surrounding fixed geometry.

**Applications:**
- FACS expression manipulation: mask the AU region, condition on neutral + expression code.
- Region transplantation: mask target face region, condition on source identity shape.
- Scan completion / fitting: mask missing geometry, inpaint from surrounding context.

## Key Results
- More interpretable and localized edits than PCA/FLAME blendshapes.
- Generates diverse shape variations within the masked region (generative, not deterministic).
- Faster inference than optimization-based morphable model fitting.
- Works for arbitrary masks — not limited to predefined FACS AUs.

## Limitations
- Constrained to FLAME topology — not generalizable to arbitrary mesh topology.
- Stochastic output: for animation control, determinism is usually needed; diffusion is better suited for authoring/augmentation than real-time expression control.
- Diffusion model requires many inference steps (though accelerated samplers help).

## Connections
- [[concepts/nonlinear-face-models]] — diffusion model over FLAME mesh; localized nonlinear shape editing
- [[concepts/facial-blendshape-rigs]] — alternative to manual blendshape sculpting for localized expression generation
- [[concepts/blendshapes]] — addresses the coupling limitation of PCA blendshape bases
- [[papers/li-2017-flame]] — FLAME provides the mesh topology and registration framework
- [[papers/zou-2024-4d-expression-diffusion]] — concurrent: diffusion for 4D expression dynamics (temporal sequences)

## Implementation Notes
The mask-conditioned denoising network is the core contribution. Architecturally this is a GNN DDPM where input node features include vertex position, mask flag, and fixed-region context embeddings. At training, random morphological masks on the FLAME mesh ensure the model learns all possible region combinations. The result is a shape inpainting model in 3D mesh space.
