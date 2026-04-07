---
title: "N-Cloth: Predicting 3D Cloth Deformation with Mesh-Based Networks"
authors: [Li, Yudi; Tang, Min; Yang, Yun; Huang, Zi; Tong, Ruofeng; Yang, Shuangcai; Li, Yao; Manocha, Dinesh]
venue: Eurographics 2022 / Computer Graphics Forum
year: 2022
tags: [simulation, neural, mesh-graph-nets, cloth, skinning]
source: raw/papers/ncloth-2022.pdf
---

## Summary
N-Cloth is a graph-convolution-based network for predicting 3D cloth deformation on characters with arbitrary mesh topology — both SMPL bodies and non-parametric characters. It encodes cloth and obstacle meshes into a shared latent space to reduce non-linearity, then decodes to predicted vertex positions. The method handles meshes up to 100K triangles and runs at 30–45 fps on an RTX 3090.

## Problem
Existing learning-based cloth methods assume fixed-topology skinned bodies (SMPL) or simple obstacle geometries. Production characters use diverse, non-SMPL meshes. Scaling to 100K-triangle garments with temporal coherence at real-time speeds on arbitrary topology is unsolved.

## Method
**Graph representation:** Cloth and obstacle meshes converted to graphs. Node features encode positions, normals, velocities. Edge features encode relative geometry.

**Latent space encoding:** Graph convolution layers map cloth and obstacle graph features into a shared latent space. Reducing the non-linearity of raw mesh-space deformations in this shared embedding improves prediction accuracy for novel poses.

**Prediction:** Decoder maps latent features back to per-vertex deformation offsets. Temporal coherence is maintained through previous-frame context.

Graph convolution (standard form):
```math
h_v^{(l+1)} = \sigma\!\left(W^{(l)}\!\left[h_v^{(l)};\; \text{AGG}\!\left(\{h_u^{(l)} : u \in \mathcal{N}(v)\}\right)\right]\right)
```

**Generalization:** Training covers SMPL characters, non-SMPL characters, rigid bodies. Test meshes differ from training data.

## Key Results
- 30–45 fps on RTX 3090 for cloth meshes up to 100K triangles
- Tested on jackets on non-SMPL bodies, robes at 100K triangles, T-shirts on SMPL
- All test meshes unseen during training — demonstrates topology generalization
- Handles SMPL, non-SMPL, and rigid body obstacles in the same framework

## Limitations
- Self-collision not explicitly handled
- Generalization range defined by training distribution; very out-of-distribution garment shapes may fail
- No physics-based loss; relies on ground-truth simulation data for training (unlike HOOD/Neural Cloth Sim)

## Connections
- [[papers/pfaff-2021-meshgraphnets]] — same graph network paradigm applied to cloth on characters
- [[papers/grigorev-2023-hood]] — HOOD uses physics loss and hierarchical graph vs N-Cloth's supervised latent approach
- [[papers/bertiche-2022-neural-cloth-sim]] — unsupervised alternative; N-Cloth is supervised
- [[papers/loper-2015-smpl]] — SMPL is one of the obstacle body models used
- [[concepts/secondary-motion]] — cloth deformation as secondary motion on animated characters
