---
title: "MeshGraphNetRP: Improving Generalization of GNN-based Cloth Simulation"
authors: [Libao, Emmanuel Ian; Lee, Myeongjin; Kim, Sumin; Lee, Sung-Hee]
venue: ACM MIG 2023 (Motion, Interaction and Games)
year: 2023
tags: [simulation, neural, mesh-graph-nets, cloth]
source: raw/papers/3623264.3624441.pdf
---

## Summary
MeshGraphNetRP extends Pfaff et al.'s MeshGraphNets for cloth simulation with two modifications: replacing the MLP encoder with a GRU-based RNN encoder to capture temporal dynamics over a 10-step history, and adding physics-informed edge features (stretch, bending angle, kinetic energy) as additional losses. These changes improve generalization to translation, rotation, and unseen cloth topologies while maintaining real-time performance.

## Problem
MeshGraphNets fail to accurately predict cloth dynamics under complex rigid-body motions (translation, rotation of handles). GRU history improves oscillatory behaviour; physics feature supervision improves stability without hand-tuned contact handling.

## Method
**Architecture:** Encode-Process-Decode (from MeshGraphNets).

*Encoder* modified from MLP to GRU with $h=9$ prior time steps. Node features include velocity, node type, external force, kinetic energy $KE_i = \frac{1}{2}m_i\|v_i\|^2$. Edge features include current and rest-state 3D vectors (not UV), stretch $\|d_k\|-\|d_k^\text{rest}\|$, and bending angle $\theta_k$.

*Processor*: 15 message-passing steps.

*Decoder*: MLP → acceleration integrated via Verlet: $p^{t+1} = a + 2p^t - p^{t-1}$.

**Loss:**
```math
\mathcal{L} = \mathcal{L}_{acc} + \lambda_{KE}\mathcal{L}_{KE} + \lambda_{ev}\mathcal{L}_{ev} + \lambda_{el}\mathcal{L}_{el} + \lambda_\theta\mathcal{L}_\theta
```
($\lambda_{ev}=\lambda_{el}=30$, $\lambda_{KE}=1$, $\lambda_\theta=0.5$).

Scheduled sampling during training (rollout probability decays 1→0). Local coordinate transformation for rotation invariance. Gaussian noise $\sigma=0.3$ added to training positions.

## Key Results
- 37 ms/frame on RTX 3080 for 1024-vertex meshes (real-time capable)
- Position RMSE 3.167×10⁻² vs MeshGraphNets baseline
- Generalises to unseen topologies, motion directions, and speeds within training range
- RNN encoder confirmed critical for oscillatory cloth behaviour (ablation)

## Limitations
- No collision handling with external objects
- Fails at speeds exceeding training distribution
- Planar cloth topologies only (no complex garment shapes)
- Rest-state assumption breaks when cloth corners are lifted

## Connections
- [[papers/pfaff-2021-meshgraphnets]] — direct extension; replaces MLP encoder with GRU, adds physics losses
- [[papers/hahn-2014-subspace-cloth]] — subspace cloth simulation: alternative (non-neural) real-time approach
- [[concepts/secondary-motion]] — cloth dynamics as secondary motion on characters
