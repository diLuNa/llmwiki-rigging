---
title: "ImFace: A Nonlinear 3D Morphable Face Model With Implicit Neural Representations"
authors: [Zheng, Mingwu; Yang, Hongyu; Huang, Di; Chen, Liming]
venue: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2022)
year: 2022
tags: [neural, digital-human, blendshapes, rig-generation]
source: raw/papers/Zheng_ImFace_A_Nonlinear_3D_Morphable_Face_Model_With_Implicit_Neural_CVPR_2022_paper.pdf
---

## Summary
ImFace represents 3D face geometry as a neural implicit function (signed distance field) rather than a mesh. It learns separate deformation fields for identity and expression using individual latent codes, enabling nonlinear decoupling of identity and expression in a continuous, resolution-independent representation. Unlike mesh-based 3DMMs (FLAME, CoMA), ImFace can represent sharp geometric details without fixed vertex counts or correspondences.

## Problem
Mesh-based 3DMMs require fixed topology and vertex correspondences across all subjects. Linear 3DMMs (PCA) cannot represent nonlinear variations (extreme expressions, fine wrinkles). Neural mesh autoencoders (CoMA) are constrained by fixed mesh resolution and topology. A representation that is simultaneously nonlinear, resolution-free, and capable of decoupling identity from expression is needed.

## Method
ImFace represents the face as an implicit function $f_\theta: \mathbb{R}^3 \times z_\text{id} \times z_\text{exp} \to \mathbb{R}$ where the output is the signed distance to the face surface.

**Dual latent codes:**
- $z_\text{id} \in \mathbb{R}^{d_\text{id}}$ — identity code (encodes who the person is)
- $z_\text{exp} \in \mathbb{R}^{d_\text{exp}}$ — expression code (encodes facial expression)

**Two-stage deformation:**
Rather than directly conditioning the SDF on both codes, ImFace uses a deformation-based approach:
1. **Expression deformation field**: $\mathcal{D}_\text{exp}(x; z_\text{exp}) \to \Delta x$ — warps a canonical identity space to the target expression space.
2. **Identity deformation field**: $\mathcal{D}_\text{id}(x; z_\text{id}) \to \Delta x$ — warps a mean face to the target identity.
3. **SDF evaluation**: the warped point is passed to a base SDF network to get the signed distance.

This composition: base SDF ∘ identity deformation ∘ expression deformation — ensures the deformations are applied in canonical space, avoiding entanglement between identity and expression.

**Training:** Supervised on 3D scan datasets (BU-3DFE, FaceWarehouse). Loss: SDF reconstruction + deformation regularity + latent code regularization.

## Key Results
- Better identity-expression disentanglement than FLAME and CoMA.
- Represents fine-scale details (wrinkles, pores) by increasing implicit resolution — no re-training needed.
- Smooth, plausible expression interpolation in latent space.
- Can be fitted to 2D landmarks and depth maps.

## Limitations
- Mesh extraction (marching cubes) is needed for animation use; not directly compatible with LBS pipelines.
- Slower than mesh-based models at inference (ray marching or marching cubes).
- Does not output skinning weights — harder to integrate with skeleton-driven rigs.

## Connections
- [[papers/ranjan-2018-coma]] — CoMA is the mesh-based predecessor; ImFace replaces fixed topology with implicit fields
- [[papers/li-2017-flame]] — FLAME is the linear 3DMM being outperformed; ImFace uses similar latent structure
- [[papers/zheng-2023-imface-pp]] — ImFace++ extends this work
- [[papers/loper-2015-smpl]] — SMPL body equivalent; ImFace is face-specific
- [[concepts/digital-human-appearance]] — implicit face model for high-fidelity digital human representation
- [[concepts/blendshapes]] — expression latent $z_\text{exp}$ is an alternative to explicit blendshape weights
