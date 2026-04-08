---
title: "Learning Neural Parametric Head Models"
authors: [Giebenhain, Simon; Kirschstein, Tobias; Georgopoulos, Markos; Rünz, Martin; Agapito, Lourdes; Nießner, Matthias]
venue: CVPR 2023
year: 2023
tags: [neural, digital-human, blendshapes, rig-generation, implicit-surfaces]
source: raw/papers/2212.02761.pdf
---

## Summary
NPHM (Neural Parametric Head Model) replaces the linear PCA shape basis of FLAME with an ensemble of local implicit neural fields (SDFs), each centered on a facial anchor point. Identity is encoded as a signed distance field in a canonical space; expressions are applied via a learned neural deformation field. Trained on 5,200+ complete head scans (including hair, teeth, ears), NPHM captures detail and topology that FLAME's fixed mesh cannot represent.

## Problem
FLAME and other linear 3DMMs are limited to the variation expressible by a small PCA basis trained on registered meshes — they cannot model hair, teeth, ears, or sharp non-Gaussian shape variation. A head model that captures full-head geometry with controllable identity and expression separation, and scales to fine-grained anatomical detail, is needed for high-fidelity avatars and downstream systems.

## Method
**Hybrid neural field architecture:**

- **Identity SDF** $f_\text{id}(\mathbf{x}; \mathbf{z}_\text{id})$: MLP maps 3D query point + identity latent code to signed distance. Represented as an *ensemble* of local fields each centered on a facial anchor point — finer local control than a single global network.
- **Expression deformation field** $f_\text{exp}(\mathbf{x}; \mathbf{z}_\text{exp})$: maps a canonical-space query point to a displacement vector, applied on top of the identity field. Disentangled from identity by training.
- **Local anchor ensemble:** Anchors placed at facial landmarks (eye corners, nose tip, mouth corners, etc.). Each local field has limited spatial support, allowing independent per-region fitting without global interference.

Training: 5,200+ head scans from 255 identities. Scans include full head geometry. No fixed mesh topology required — purely implicit.

## Key Results
- Outperforms FLAME in fitting accuracy (lower Chamfer distance) on held-out scans.
- Faithfully reconstructs hair, teeth, ears — all absent from FLAME.
- Latent space enables smooth expression interpolation and identity transfer.
- Became the backbone expression space for NPGA ([[papers/giebenhain-2024-npga]]) and HeadCraft ([[papers/sevastopolsky-2024-headcraft]]).

## Limitations
- Implicit representation; not directly compatible with mesh-based production pipelines without marching cubes extraction.
- Requires dense multi-view scanning for training data — not an in-the-wild model.
- Inference requires SDF evaluation at many query points; slower than linear blendshape evaluation.

## Connections
- [[concepts/nonlinear-face-models]] — NPHM is the leading neural replacement for FLAME's linear shape basis
- [[concepts/implicit-surfaces]] — identity represented as SDF ensemble
- [[papers/giebenhain-2024-npga]] — NPGA conditions Gaussian avatars on NPHM expression space
- [[papers/sevastopolsky-2024-headcraft]] — HeadCraft adds StyleGAN displacement on top of NPHM
- [[papers/li-2017-flame]] — the linear model NPHM replaces
- [[authors/niessner-matthias]]

## Implementation Notes
The local anchor ensemble is key: rather than a single global SDF MLP (which struggles with the complexity of a full head), NPHM decomposes the head into regions each with their own smaller network. This is analogous to localized blendshape influence regions but in implicit space.

For production use, the SDF must be isosurface-extracted (marching cubes) to get a mesh — topology will vary per-expression. Not plug-and-play with USD/UsdSkel.

## Quotes
> "We introduce a neural parametric representation that disentangles identity and expressions in disjoint latent spaces."
