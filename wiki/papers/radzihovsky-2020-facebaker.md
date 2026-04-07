---
title: "FaceBaker: Baking Character Facial Rigs with Machine Learning"
authors: [Radzihovsky, Sarah; de Goes, Fernando; Meyer, Mark]
venue: SIGGRAPH Talks 2020
year: 2020
tags: [neural, blendshapes, rig-generation, correctives]
source: raw/papers/2020.SiggraphTalks.RGM.pdf
---

## Summary
Approximates facial mesh deformations from complex procedural rigs using machine learning, producing a portable, fast-to-evaluate "baked" rig that reduces compute, extends character longevity without rig upkeep, and enables export to external platforms.

## Problem
Film-quality facial rigs are procedural systems with hundreds of controls and layers of corrective sculpts; they are slow to evaluate and tied to proprietary pipelines. Approximating them enables real-time playback, crowd use, and platform portability.

## Method
Trains a neural network (or similar ML model) mapping rig-control vectors to per-vertex mesh displacements. Key design choices:
- Per-character training on densely sampled rig evaluations.
- Network architecture captures nonlinear rig behavior that PCA/blendshape linearization would miss.
- Qualitative and quantitative evaluation against ground-truth rig output on hero characters.

## Key Results
- Outperforms existing deformation approximation methods (at time of publication) for facial rigs.
- Demonstrated on multiple Pixar feature film characters.
- Achieves real-time evaluation rates.

## Limitations
- Approximation error at extreme or unusual control combinations.
- Requires per-character training (dataset collection + training time).
- Does not generalize across characters without retraining.

## Connections
- [[papers/gustafson-2020-inverse-rig]] — complementary: inverse mapping (rig params from skeleton)
- [[concepts/blendshapes]] — baked output is effectively a learned blendshape-like model
- [[authors/degoes-fernando]]

## Implementation Notes
The baked representation is typically a learned linear or nonlinear model over rig-control space. Simpler rigs may be well approximated by PCA+residual; complex facial rigs benefit from neural approaches. Consider per-region (eyes, mouth, cheeks) models for better accuracy.
