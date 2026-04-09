---
title: "Efficient Geometry-aware 3D Generative Adversarial Networks"
authors: [Chan, Eric R.; Lin, Connor Z.; Chan, Matthew A.; Nagano, Koki; Pan, Boxiao; De Mello, Shalini; Gallo, Orazio; Guibas, Leonidas; Tremblay, Jonathan; Khamis, Sameh; Karras, Tero; Wetzstein, Gordon]
venue: CVPR 2022
year: 2022
tags: [neural, digital-human, appearance, rig-generation]
source: raw/papers/2112.07945.pdf
---

## Summary
EG3D introduces a hybrid explicit-implicit tri-plane backbone for high-resolution, multi-view-consistent 3D face generation from unstructured 2D photographs. Three axis-aligned feature planes encode a volumetric scene; a lightweight MLP decodes sampled features to density and color; a 2D super-resolution network produces full-resolution output. By integrating StyleGAN2 as the feature generator, EG3D achieves state-of-the-art 3D GAN quality at real-time rendering speeds. It defines the tri-plane representation that became the dominant backbone for subsequent neural avatar and face generation systems.

## Problem
Prior 3D-aware GANs use either implicit representations (slow, poor geometry) or explicit voxel grids (memory-expensive, low resolution). A representation that achieves the quality of StyleGAN2 2D images while maintaining multi-view-consistent 3D geometry — trained purely from unstructured 2D photo collections — is missing.

## Method
**Tri-plane representation:** Three orthogonal 2D feature planes $F_{xy}, F_{xz}, F_{yz} \in \mathbb{R}^{H \times W \times C}$. For a 3D query point $\mathbf{x}$, features are sampled from each plane by projection and bilinearly interpolated, then summed: $f(\mathbf{x}) = F_{xy}(\mathbf{x}_{xy}) + F_{xz}(\mathbf{x}_{xz}) + F_{yz}(\mathbf{x}_{yz})$.

**Generator backbone:** StyleGAN2 generates the three planes jointly from a latent code $\mathbf{w}$. The planes share a single generator, keeping parameter count manageable.

**Volume rendering + super-resolution:** A neural volume renderer samples the tri-plane along camera rays to produce a low-resolution RGBD image. A 2D super-resolution network upscales to final resolution.

**Camera conditioning:** The generator is conditioned on camera extrinsics, enabling controlled pose synthesis and consistent multi-view output.

## Key Results
- State-of-the-art FID on FFHQ (256×256) among 3D-aware GANs.
- Real-time rendering (tri-plane lookup is cheap; SR upscales efficiently).
- Disentangled control over geometry and appearance.
- Tri-plane backbone adopted by Next3D, NPGA, and dozens of subsequent avatar systems.

## Limitations
- Trained from 2D images only — no explicit 3D supervision. Geometry quality is GAN-grade, not scan-grade.
- Expression control requires additional conditioning (e.g., FLAME); base EG3D has no semantic expression control.
- Identity-specific fitting (inversion) requires optimization loops.

## Connections
- [[concepts/nonlinear-face-models]] — EG3D defines the generative 3D face representation most neural avatars build on
- [[papers/yu-2023-nofa]] — NOFA uses EG3D as its generative prior for one-shot avatar reconstruction
- [[papers/sun-2023-next3d]] — Next3D builds Generative Texture-Rasterized Tri-planes on top of EG3D
- [[papers/giebenhain-2024-npga]] — NPGA references tri-plane representations; EG3D is the lineage

## Implementation Notes
The tri-plane is the key engineering contribution: it replaces an expensive 3D feature volume with three 2D planes, reducing memory from $O(N^3)$ to $O(N^2)$ while retaining spatial expressiveness in all three axes (though with limited high-frequency capture along each plane's normal). The StyleGAN2 backbone generates all three planes simultaneously from a single latent.
