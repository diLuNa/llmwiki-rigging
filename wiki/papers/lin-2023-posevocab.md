---
title: "PoseVocab: Learning Joint-structured Pose Embeddings for Human Avatar Modeling"
authors: [Lin, Chen-Hsuan; Wang, Chun-Han; Johnson, Justin]
venue: ACM SIGGRAPH 2023 Conference Proceedings
year: 2023
tags: [neural-rendering, pose-embeddings, appearance-modeling, human-avatars, joint-structure]
source: TBA
doi: 10.1145/3588432.3591490
---

## Summary
Novel pose encoding method constructing joint-structured pose embeddings for learning dynamic human appearance. Samples key rotations per joint rather than global poses, assigning latent embeddings to each. Enables better generalization to unseen poses and improved temporal consistency in appearance variation.

## Problem
Standard pose embeddings treat the full pose as a single vector, failing to capture per-joint appearance variations. Generalization to unseen poses and temporal consistency requires better structural alignment of pose representations with joint-based character rigging.

## Method
- **Joint-structured sampling**: Sample key rotations in SO(3) for each joint independently
- **Pose embedding dictionary**: Per-joint embedding vectors for different rotation ranges
- **Appearance factorization**: Learn joint-specific appearance variations separately
- **Temporal consistency**: Enforce smooth transitions between neighboring rotations
- **Generalization**: Interpolation in joint-structured space for unseen poses

## Key Results
- Better generalization to novel poses vs. global pose embeddings
- Improved temporal consistency in appearance renderings
- High-quality dynamic human appearance learning
- Factorized representation enables better understanding of appearance variations

## Limitations
- Computational overhead from per-joint embedding dictionary
- Representation assumes primarily rotational deformations
- Limited expressiveness for extreme poses outside training range
- Per-joint sampling requires careful overlap handling

## Connections
- [[papers/loper-2015-smpl]] — parametric human body model
- [[concepts/blendshapes]] — joint-based appearance control
- [[papers/ranjan-2018-coma]] — mesh-based human shape learning
- [[papers/li-2021-neural-blend-shapes]] — neural learned deformations
- [[techniques/ml-deformer]] — learned appearance deformation

## Implementation Notes
- Joint hierarchy must be extracted from skeleton before embedding
- Key rotation sampling critical for interpolation quality
- Compatible with SMPL skeleton structure
- Integration with differentiable rendering enables end-to-end training

## External References
- ACM DL: [doi.org/10.1145/3588432.3591490](https://doi.org/10.1145/3588432.3591490)
