---
title: "HOOD: Hierarchical Graphs for Generalized Modelling of Clothing Dynamics"
authors: [Grigorev, Artur; Thomaszewski, Bernhard; Black, Michael J.; Hilliges, Otmar]
venue: CVPR 2023
year: 2023
tags: [simulation, neural, mesh-graph-nets, cloth, secondary-motion]
source: raw/papers/hood-2023.pdf
---

## Summary
HOOD is a self-supervised GNN for real-time clothing dynamics that uses hierarchical message-passing to overcome the slow-propagation bottleneck of flat MeshGraphNets. A physics-based loss (stretching, bending, collision, friction, inertia) replaces ground-truth simulation data. A single trained network handles diverse garment types (shirts, dresses, pants), body shapes, material parameters, and even dynamic topology changes (zipping/unzipping) without retraining.

## Problem
Standard MeshGraphNets with $K$ message-passing steps can propagate information at most $K$ edges per step — on fine garment meshes this is far too local for realistic dynamics, producing over-stretching artefacts and rubbery appearance. Retraining per garment is expensive.

## Method
**Graph:** Garment vertices + edges, augmented with "body edges" connecting each garment node to its nearest body surface vertex. Node features: type, velocity, surface normal, mass. Edge features: relative positions in current and canonical geometry.

**Hierarchical message passing (L levels):**
```math
e_{ij}^{l} \leftarrow f^l_{v\to e}(e_{ij}^l,\; v_i^0,\; v_j^0) \qquad
v_i \leftarrow f_{e\to v}\!\left(v_i,\; \textstyle\sum_j e_{ij}^{\text{body}},\; \sum_j e_{ij}^1,\;\ldots,\; \sum_j e_{ij}^L\right)
```
Coarser levels carry long-range signals; fine levels handle local contact. Achieves effective propagation radius of 48 edges vs 15 for a flat 15-step scheme at equal compute.

**Self-supervised physics loss:**
```math
\mathcal{L} = \mathcal{L}_{\text{stretch}} + \mathcal{L}_{\text{bend}} + \mathcal{L}_{\text{gravity}} + \mathcal{L}_{\text{friction}} + \mathcal{L}_{\text{collision}} + \mathcal{L}_{\text{inertia}}
```
Stretching uses the St. Venant-Kirchhoff material model; bending uses discrete curvature; collision uses a cubic penalty. Material parameters (Lamé constants, bending stiffness, density) are sampled log-uniformly during training so the network generalises across fabrics.

**Training:** Fully self-supervised — no ground-truth simulations needed. Autoregressive rollout length gradually increases from 1 to 5 steps during training.

## Key Results
- Perceptual study (30 participants): preferred over SNUG and SSCH; on par with physics solver ARCSim
- Hierarchical (L=2) outperforms flat 15-step baseline: loss 1.48 vs 2.92
- Handles garment topology changes at inference time (zip/unzip, size edits)
- Single model covers shirt, tank top, dress, pants, shorts across diverse body shapes and materials

## Limitations
- No garment-garment self-collision; penetrations can appear in bunched fabric
- Fails when body velocities exceed the training distribution
- Initialization from skinning-approximated garment meshes introduces a bias toward body-fitted shapes

## Connections
- [[papers/pfaff-2021-meshgraphnets]] — direct extension; HOOD adds hierarchical levels to fix message-propagation bottleneck
- [[papers/fortunato-2022-multiscale-mgn]] — concurrent multi-scale approach; HOOD learns inter-level transitions implicitly vs explicit interpolation in MS-MGN
- [[papers/bertiche-2022-neural-cloth-sim]] — both use physics-based self-supervised losses; Neural Cloth Sim adds unsupervised dynamics disentanglement
- [[papers/hahn-2014-subspace-cloth]] — earlier non-neural subspace cloth on characters
- [[papers/libao-2023-meshgraphnetsrp]] — another MeshGraphNets extension; GRU history vs hierarchical graph
- [[concepts/secondary-motion]] — clothing dynamics as secondary motion on characters
- [[authors/black-michael]]
