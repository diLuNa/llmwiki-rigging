---
title: "GANtlitz: Ultra High Resolution Generative Model for Multi-Modal Face Textures"
authors: [Gruber, Andreas; Collins, Erin; Meka, Abhimitra; Mueller, Franziska; Sarkar, Kripasindhu; Orts-Escolano, Sergio; Prasso, Luca; Busch, Jan; Gross, Markus; Beeler, Thabo]
venue: Eurographics 2024 (Computer Graphics Forum)
year: 2024
tags: [neural, digital-human, appearance, facial-capture]
source: raw/papers/ComputerGraphicsForum-2024-Gruber-GANtlitzUltraHighResolutionGenerativeModelforMulti‐ModalFaceTextures.pdf
---

## Summary
A StyleGAN-based generative model for producing ultra high resolution (4K+) multi-modal face texture maps — albedo, specular attenuation, and displacement/normals — suitable for rendering photoreal digital humans in traditional pipelines. Addresses severe data scarcity and GPU memory constraints at extreme resolutions via discriminator augmentations and patch-based generation.

## Problem
High-resolution (4K) multi-modal face texture datasets are scarce and expensive to capture. Training GANs at this resolution on limited data causes mode collapse. Existing methods are limited to lower resolution or single modality (albedo only).

## Method
**Architecture:** StyleGAN backbone adapted for multi-modal output. Generates all texture modalities jointly (albedo, specular, displacement, normals) from a shared latent space, ensuring physical consistency between maps.

**Data scarcity handling:** Discriminator augmentations (similar to ADA) prevent overfitting when training on limited captured face data.

**Patch-based generation:** Memory-limited 4K generation addressed by synthesizing overlapping patches at full resolution, then compositing. Uses explicit positional encodings (StyleGANv3-style) to avoid aliasing and enable seamless tiling.

**Outputs:** Per-subject or unconditional generation of: albedo maps, specular attenuation maps, displacement maps, normal maps — all at 4K resolution, tiled for skin detail.

## Key Results
- Generates diverse, photoreal face texture sets at 4K resolution.
- Multi-modal consistency: albedo/specular/displacement are coherent per sample.
- Competitive or superior to state-of-the-art 1K resolution face texture generators.

## Limitations
- Generative (unconditional or weakly conditioned) — does not solve the harder problem of fitting textures to a specific captured individual in minutes.
- Static textures — no expression-dependent texture variation (see [[papers/raman-2022-mesh-tension-wrinkles]] for that).
- Requires high-quality multi-modal training data from capture rigs.

## Connections
- [[papers/weyrich-2006-skin-reflectance]] — same measurement modalities, this paper is the generative successor
- [[papers/raman-2022-mesh-tension-wrinkles]] — expression-driven texture variation on top of static base textures
- [[authors/prasso-luca]] — Luca Prasso is co-author
- [[authors/beeler-thabo]] — Thabo Beeler is co-author
- [[concepts/digital-human-appearance]]
