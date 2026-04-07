---
title: "Neural Cloth Simulation"
authors: [Bertiche, Hugo; Madadi, Meysam; Escalera, Sergio]
venue: ACM Transactions on Graphics (SIGGRAPH Asia 2022)
year: 2022
tags: [simulation, neural, cloth, secondary-motion]
source: raw/papers/neural-cloth-sim-2022.pdf
---

## Summary
Neural Cloth Simulation is the first method to learn realistic cloth dynamics in a fully self-supervised way, requiring no ground-truth simulation data. The key architectural insight is a disentangled encoder: a static branch handles pose-dependent drape, and a dynamic branch (GRU-based, bias-free) handles inertial motion — zero input yields zero dynamic contribution, cleanly separating the two. A physics-based inertia loss enforces Newtonian mechanics, and a motion augmentation technique (shuffling dynamic latent codes during training) improves generalization. Inference runs at 206 fps on 250K-DoF garments with an artist-accessible motion-intensity dial.

## Problem
Supervised cloth learning requires thousands of expensive ground-truth simulations per garment/body/fabric. Prior unsupervised work (PBNS) is static-only; SNUG claims dynamics but has a fatal gradient-backpropagation flaw (gradients invert and close skirts). No prior work learns true cloth dynamics without simulation supervision.

## Method
**Input:** Body pose sequence $\{\theta_t\}$, encoded as per-joint 6D rotations + gravity direction (static descriptor) and first/second pose derivatives in local space (dynamic descriptor).

**Architecture — disentangled encoder:**
- Static encoder: 4 FC layers on current-frame descriptors → static latent $z_s$
- Dynamic encoder: 2 FC layers + GRU on dynamic descriptors → dynamic latent $z_d$
  - **No bias terms** in dynamic layers, so $z_d = 0$ when input is zero (static pose)
- Combined: $z = z_s + z_d$ → decoder → per-vertex deformation offsets

**Self-supervised physics loss:**
```math
\mathcal{L} = \mathcal{L}_\text{cloth} + \mathcal{L}_\text{bend} + \mathcal{L}_\text{collision} + \mathcal{L}_\text{inertia}
```

Inertia loss (critical for dynamics):
```math
\mathcal{L}_\text{inertia} = \frac{1}{2\Delta t^2} m \|x_t - x_t^\text{proj}\|^2
```
where $x_t^\text{proj} = 2x_{t-1} - x_{t-2}$ is the inertial projection. Gradients are **not** backpropagated through $x_{t-1}, x_{t-2}$ (causality preserved).

**Motion augmentation:** During training, dynamic latent codes $z_d$ from different sequences are shuffled while static losses remain active. Leverages the disentangled subspace to improve dynamic generalization without corrupting static quality.

**Motion intensity control:** At inference, scale $z_d$ by $w \in [0, 2]$: $w=0$ gives static drape, $w=1$ learned dynamics, $w=2$ exaggerated dynamics.

## Key Results
- 206.3 fps at 250K DoF (garment-specific network)
- First unsupervised method to produce true cloth dynamics (verified via inertia loss > PBNS and SNUG)
- Motion augmentation demonstrably improves generalization across motion styles
- Controllable motion intensity — useful as an art-direction tool

## Limitations
- Network is garment- and avatar-specific; retraining required per asset
- No self-collision handling
- Slower to train than supervised methods (1 hour–1 day vs 10 minutes for PBNS)
- Training stability sensitive to batch size

## Connections
- [[papers/pfaff-2021-meshgraphnets]] — MeshGraphNets is graph-based; Neural Cloth Sim uses MLP/GRU on a different graph-free architecture for body-specific garments
- [[papers/grigorev-2023-hood]] — HOOD also uses physics losses and is also self-supervised; HOOD is topology-general and uses hierarchical GNN vs this method's per-garment MLP
- [[papers/li-2022-ncloth]] — N-Cloth is supervised and topology-general; complementary approach
- [[papers/hahn-2014-subspace-cloth]] — classical subspace cloth simulation; this is the neural analogue
- [[concepts/secondary-motion]] — cloth dynamics as secondary character motion
