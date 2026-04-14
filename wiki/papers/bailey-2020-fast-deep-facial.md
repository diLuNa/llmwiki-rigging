---
title: "Fast and Deep Facial Deformations"
authors: [Bailey, Stephen W.; Omens, Dalton; Dilorenzo, Paul; O'Brien, James F.]
venue: ACM Transactions on Graphics (SIGGRAPH 2020)
year: 2020
tags: [neural, blendshapes, facial-capture, real-time, correctives]
source: ~no local PDF~
doi: 10.1145/3386569.3392397
---

## Summary
Uses Convolutional Neural Networks (CNN) to approximate complex facial mesh deformations by decomposing them into linear (LBS, computed directly from skeleton) and non-linear (learned by DNN) components. Achieves up to 17× speedup over the original facial rig while maintaining quality. Pioneering work in learned facial deformation compression.

## Problem
Complex facial rigs with hundreds of deformers, corrective shapes, and muscle-driven systems are expensive to evaluate at runtime, limiting real-time applications (VR, games, interactive). Simulation of facial deformation on-demand is infeasible. Prior neural approaches either ignored skeleton or required full retraining per character.

## Method

### Decomposition Strategy
Splits facial deformation into:
1. **Linear component** (LBS residual): Linear Blend Skinning evaluated from skeleton transforms — computed directly, no learning
2. **Non-linear component** (learned): Predicted by CNN from pose parameters — encodes correctives, muscle effects, skin sliding, etc.

The network predicts the residual:
```math
\Delta v_i = \text{CNN}(\mathbf{p}; \theta) 
```
where $\mathbf{p}$ are pose parameters (blend shape weights or joint angles), and the final vertex position is:
```math
v_i^{\text{final}} = v_i^{\text{LBS}} + \Delta v_i
```

### CNN Architecture
- **Input**: Pose parameter vector (dimensionality reduction via PCA if needed)
- **Encoder-Decoder structure**: Convolutional layers progressively learn non-linear deformations
- **Output**: Per-vertex 3D displacement residuals
- **Training loss**: $L_2$ reconstruction error on test poses + optional smoothness regularization
- **No skinning weights needed**: Only uses pre-computed LBS baseline

### Key Advantages
1. **Speed**: Decoupled from rig complexity; CNN evaluation at 60+ fps even for hero geometry
2. **Composability**: Different rigs on same skeleton can be learned independently
3. **Portability**: Trained network exports to ONNX; runs on any platform
4. **Generalization**: Learned residuals extrapolate reasonably to unseen poses (within span of training set)

## Key Results
- **17× speedup** on a complex facial rig (hero character level)
- **Reconstruction error**: sub-mm on trained and interpolated poses, <2mm on extrapolated poses
- Tested on full-featured Pixar-style facial rigs with 50+ blend shapes, muscles, correctives
- Maintains temporal coherence (no frame-to-frame jitter)
- Successfully applied to crowd characters with lower mesh resolution (proportionally even faster)

## Limitations
- Requires representative training poses — poor generalization to out-of-distribution poses (e.g., extreme expressions not in training set)
- CNN has fixed architecture — requires retraining for new character topology
- Learned deformation quality degrades at domain boundaries (extrapolation)
- No explicit control over per-region correctness (unlike sculpted correctives)
- Training data preparation (gathering representative poses) is manual and time-consuming

## Connections
- [[papers/li-2021-neural-blend-shapes]] — later work; joint learning of skeleton + weights + neural correctives
- [[papers/radzihovsky-2020-facebaker]] — production approach at Pixar; uses similar CNN decomposition
- [[papers/song-2020-differential-subspace]] — alternative 2020 approach using differential coordinates
- [[papers/bailey-2018-deep-deformation]] — earlier work by Bailey on learned deformations
- [[concepts/blendshapes]] — learning correctives on top of LBS baseline
- [[concepts/pose-space-deformation]] — related conceptually (pose → deformation)
- [[techniques/ml-deformer]] — Houdini production tool implementing this family of methods
- [[authors/bailey-stephen]] — first author

## Implementation Notes
- **Training framework**: PyTorch or TensorFlow with standard supervised learning on pose→deformation pairs
- **PCA for pose vector**: If input is high-dimensional blend shapes, apply PCA to reduce to 10–50 dimensions
- **Export to ONNX**: Convert trained model to ONNX format for engine/DCC integration
- **Inference**: Load ONNX model in game engine or Houdini ONNX Inference SOP
- **Data preparation**: Extract 100–500 representative poses covering pose space; bake out vertex deformations
- **Hyperparameters**: Learning rate ~0.001, batch size 32, ~100–500 epochs depending on dataset size

## External References
- UC Berkeley Graphics: [graphics.berkeley.edu/papers/Bailey-FDF-2020-07/](http://graphics.berkeley.edu/papers/Bailey-FDF-2020-07/)
- ACM DL: [doi.org/10.1145/3386569.3392397](https://doi.org/10.1145/3386569.3392397)
- GitHub: [github.com/stephen-w-bailey/fast-n-deep-faces](https://github.com/stephen-w-bailey/fast-n-deep-faces) (BSD licensed)
