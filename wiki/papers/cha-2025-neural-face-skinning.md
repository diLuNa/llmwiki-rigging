---
title: "Neural Face Skinning for Mesh-agnostic Facial Expression Cloning"
authors: [Cha, Sihun; Yoon, Serin; Seo, Kwanggyoon; Noh, Junyong]
venue: Computer Graphics Forum (Eurographics 2025)
year: 2025
tags: [neural, blendshapes, rig-generation, skinning, digital-human, auto-rigging]
source: raw/papers/2505.22416.pdf
---

## Summary
Neural Face Skinning predicts per-vertex skinning weights for an arbitrary target mesh via indirect supervision from FACS segmentation labels, combining a global latent deformation model with a local skinning-weight decoder to enable high-fidelity expression cloning across meshes of completely different topologies and proportions — including highly stylized non-human characters. The method is the most production-rigging-relevant recent paper in cross-mesh expression retargeting: it generates a proper skinning-based rig for any target mesh driven by FACS-interpretable controls.

## Problem
Expression retargeting between meshes of very different topologies (e.g., FLAME face → stylized cartoon character) requires either manual blendshape authoring or methods that assume geometric correspondence. Methods like NFR and RigAnyFace work well on near-human topologies but struggle with heavy stylization. A mesh-agnostic method that generates FACS-compatible skinning weights without requiring geometric correspondence or manual authoring is missing.

## Method
**Global + local decomposition:**
- *Global model*: learns a latent deformation basis shared across face regions — captures large-scale expression structure.
- *Local skinning decoder*: predicts per-vertex skinning weights $W \in \mathbb{R}^{N \times K}$ for $K$ FACS-inspired control regions. The skinning weights localize the global deformation to semantically meaningful face areas.

**FACS segmentation supervision:**
Rather than supervising on 3D ground-truth blendshapes (which require correspondence), the method uses FACS region segmentation labels as indirect supervision — constraining which controls influence which regions. This makes the approach topology-agnostic.

**Interpretable FACS controls:**
Output rig is driven by FACS-compatible control parameters. The skinning weights ensure each control acts on the correct facial region, enabling direct artist editing.

## Key Results
- State-of-the-art expression fidelity and deformation transfer accuracy vs NFR and prior retargeting methods.
- Generalizes to highly stylized characters (non-human proportions, non-FLAME topology).
- FACS-interpretable controls — directly usable by animators.
- Eurographics 2025.

## Limitations
- Submitted May 2025 — conference version may differ from arXiv.
- Skinning-based rig; complex expressions requiring volume preservation need additional correctives.
- FACS segmentation supervision requires some label data on training meshes.

## Connections
- [[concepts/nonlinear-face-models]] — mesh-agnostic neural expression cloning; most production-relevant retargeting paper
- [[concepts/auto-rigging]] — automatically generates skinning-based FACS rig for arbitrary target mesh
- [[concepts/blendshapes]] — FACS-compatible output controls
- [[concepts/linear-blend-skinning]] — skinning weights drive the local deformation model
- [[papers/qin-2023-nfr]] — NFR is the primary baseline (also topology-agnostic facial auto-rigging)
- [[papers/ma-2025-riganyface]] — RigAnyFace targets FACS blendshapes (not skinning); complementary approach
- [[papers/sol-2025-blendshape-retargeting]] — sol-2025 also targets cross-identity retargeting via VAE
