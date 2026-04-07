---
title: "Multi-Modal Diffusion for Hand-Object Grasp Generation"
authors: [Cao, Jinkun; Liu, Jingyuan; Kitani, Kris; Zhou, Yi]
venue: arXiv / Adobe 2024
year: 2024
tags: [hand-animation, neural, motion-synthesis]
source: raw/papers/MultiModalGraspObject.pdf
---

## Summary
Multi-modal Grasp Diffusion (MGD) — a diffusion model that jointly generates hand pose and object shape for grasping, trained from heterogeneous data. Enables both conditional (given object, generate hand) and unconditional (joint hand+object) synthesis. Uses MANO hand model. Generalizes to unseen object geometries by leveraging large-scale 3D object datasets.

## Problem
Existing hand grasp generation methods are constrained to small hand-object datasets with full 3D annotations and specific hand parametric models (MANO vs. robotic). They cannot combine data from different sources or generalize to diverse object shapes.

## Method
**Multi-modal diffusion:** Joint latent diffusion model over (hand pose, object shape) space. Learns both prior (unconditional) and conditional posterior.

**Heterogeneous data:** Leverages large-scale 3D object datasets (ShapeNet etc.) combined with hand-object interaction datasets, despite incompatible annotation formats.

**Hand model:** MANO parametric hand model (blend skinning with non-rigid deformation).

**Generation modes:**
- Conditional: given object geometry → generate MANO hand parameters
- Unconditional: jointly generate hand + object

## Key Results
- Visual plausibility and diversity on held-out object shapes.
- Good generalization to unseen object geometries.
- Both conditional and unconditional generation modes work.

## Limitations
- Static grasps (no motion synthesis).
- MANO model constraint — output quality limited by MANO expressiveness.
- Plausibility metric; no user study on animator utility.

## Connections
- [[papers/zhang-2024-graspxl]] — complementary motion-based approach (RL policy vs. diffusion)
- [[concepts/hand-animation]] — parent concept

