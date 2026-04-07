---
title: "Controllable Neural Style Transfer for Dynamic Meshes"
authors: [Haetinger, Guilherme G.; Tang, Jingwei; Ortiz, Raphael; Kanyuk, Paul; Azevedo, Vinicius C.]
venue: SIGGRAPH 2024
year: 2024
tags: [neural, deformation, simulation]
source: raw/papers/2024.SiggraphPapers.HTOKA.pdf
---

## Summary
A neural style transfer pipeline for 3D meshes that applies 2D image styles to both static and dynamic (simulated) assets, replacing the Gram-Matrix loss with Neural Neighbor formulation for sharper results and using an implicit reparametrization to handle large mesh deformations.

## Problem
Stylized animation requires 3D assets to match 2D design aesthetics. Existing neural style transfer for meshes suffers from artifacts (blurriness, texture swimming) and breaks on large deformations common in simulation outputs (cloth, liquid).

## Method
Key contributions:
1. **Neural Neighbor loss**: replaces Gram-Matrix style loss with a nearest-neighbor match in neural feature space, producing sharper and artifact-free stylization.
2. **Implicit reparametrization**: optimized mesh positions are expressed through an implicit formulation (position field conditioned on a deformation), enabling stylization to be consistent across frames of a deforming mesh.
3. Compatible with cloth and liquid simulation outputs.

## Key Results
- Sharper, artifact-free stylization vs. Gram-Matrix baseline.
- Consistent stylization on dynamic cloth and liquid simulation.
- Demonstrated on Disney/Pixar assets.

## Limitations
- Optimization-based; not real-time (per-asset optimization).
- Neural Neighbor loss is more expensive than Gram-Matrix.

## Connections
- [[authors/kanyuk-paul]]

## Implementation Notes
The implicit reparametrization idea (expressing positions through a deformation field) is related to neural radiance fields and implicit surfaces — a useful pattern when you need consistent attributes across a deforming mesh in other contexts (e.g., consistent UV baking on animated characters).
