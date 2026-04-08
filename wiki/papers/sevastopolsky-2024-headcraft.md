---
title: "HeadCraft: Modeling High-Detail Shape Variations for Animated 3DMMs"
authors: [Sevastopolsky, Artem; Grassal, Philip-William; Giebenhain, Simon; Athar, ShahRukh; Verdoliva, Luisa; Nießner, Matthias]
venue: 3DV 2025
year: 2025
tags: [neural, digital-human, blendshapes, rig-generation, appearance]
source: raw/papers/2312.14140.pdf
---

## Summary
HeadCraft adds a StyleGAN2-based generative model over UV displacement maps on top of NPHM, bridging the gap between statistical shape models (coarse, animatable) and scan-quality geometry (detailed, static). The model supports unconditional sampling of high-detail animated heads, fitting to partial scans (e.g., from a depth sensor), and semantically aware region editing — all while remaining fully animatable via NPHM's expression space.

## Problem
NPHM captures overall head shape well but its SDF representation smooths out fine geometric detail (pores, wrinkles, micro-geometry). Classic 3DMMs (FLAME) are even coarser. Meanwhile, scan-captured meshes have full detail but are static — not animatable. A model that is simultaneously high-detail *and* animatable is missing.

## Method
**Two-stage pipeline:**

1. **NPHM registration:** Fit NPHM to a training set of high-resolution scans, computing per-scan residual displacement maps (UV-parameterized delta from the NPHM surface to the scan surface).

2. **StyleGAN2 over displacements:** Train a StyleGAN2 on the UV displacement maps from stage 1. The GAN latent $\mathbf{w}$ controls fine-scale detail; the NPHM latent $\mathbf{z}_\text{id}$ controls coarse identity; NPHM expression code $\mathbf{z}_\text{exp}$ drives animation.

**At inference:** Sample or optimize $(\mathbf{z}_\text{id}, \mathbf{w}, \mathbf{z}_\text{exp})$ → evaluate NPHM for coarse shape + animated deformation → apply StyleGAN displacement → extract detailed animated mesh.

The UV displacement is computed in NPHM's canonical space, so it deforms consistently with expressions.

## Key Results
- High-detail head mesh generation with controllable animation.
- Fitting to partial scans while preserving fine detail.
- Semantic region editing (e.g., change nose shape only) compatible with NPHM animation.

## Limitations
- Two-stage pipeline: NPHM residuals require NPHM fitting, which needs multi-view scans.
- StyleGAN displacement is in canonical space — large expression changes may cause texture-space misalignment.
- Not yet validated on production character pipelines.

## Connections
- [[concepts/nonlinear-face-models]] — extends NPHM with generative detail; bridges shape model and scan quality
- [[papers/giebenhain-2023-nphm]] — NPHM provides the animatable backbone
- [[papers/giebenhain-2024-npga]] — NPGA uses NPHM for Gaussian avatars (complementary approach)
- [[authors/niessner-matthias]]
