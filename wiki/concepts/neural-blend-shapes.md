---
title: "Neural Blend Shapes"
tags: [neural, blendshapes, correctives, skinning, pose-space]
---

## Definition
Neural blend shapes are a learned, pose-dependent deformation layer that replaces or augments hand-sculpted corrective blend shapes. A neural network predicts blend shape weights (or directly the corrective displacements) conditioned on the current pose — typically joint rotations or skeletal parameters — producing nonlinear deformations beyond what LBS alone can represent.

The term is most associated with Li et al. 2021, which learns skeleton, LBS weights, and neural blend shapes jointly from mesh sequences, requiring no manual rig or sculpting.

## Variants / Taxonomy

| Variant | Description |
|---|---|
| **Residual neural correctives** | LBS gives the base deformation; a small MLP or blend shape basis predicts the residual. Keeps LBS compatibility. |
| **Fully learned blend shapes** | Network outputs a set of learned basis shapes + pose-driven weights. Interpretable like PSD but auto-derived. |
| **Neural PSD replacement** | Replaces hand-sculpted pose-space deformations with network predictions, without changing the blend shape schema. |
| **Latent correctives** | Correctives are generated from a latent code jointly trained with identity/expression, used in face models. |

## Key Papers
- [[papers/li-2021-neural-blend-shapes]] — joint learning of skeleton, LBS weights, and neural correctives from mesh sequences
- [[papers/bailey-2020-fast-deep-facial]] — residual MLP over LBS for facial deformation
- [[papers/song-2020-differential-subspace]] — differential subspace approach to learned correctives
- [[papers/arcelin-2024-ml-deformer-crowds]] — production comparison of neural blend shape approaches for crowds

## Connections
- [[concepts/blendshapes]] — neural blend shapes are a learned generalization of FACS/PSD blend shapes
- [[concepts/pose-space-deformation]] — neural blend shapes replace or extend traditional PSD
- [[concepts/latent-generative-modelling]] — neural blend shapes operate in learned latent spaces
- [[concepts/skinning]] — LBS is typically the base deformation layer

## Notes
Neural blend shapes offer the precision of sculpted correctives at scale: they generalize to unseen poses, require no artist input per correction, and can capture subtle nonlinearities (twist, volume preservation). The trade-off vs. traditional PSD is reduced interpretability — individual blend shapes don't correspond to named poses — and the need for a training corpus of posed meshes.
