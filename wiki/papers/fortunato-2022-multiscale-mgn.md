---
title: "MultiScale MeshGraphNets"
authors: [Fortunato, Meire; Pfaff, Tobias; Wirnsberger, Peter; Pritzel, Alexander; Battaglia, Peter]
venue: AI4Science Workshop at ICML 2022
year: 2022
tags: [simulation, neural, mesh-graph-nets, cloth, volumes]
source: raw/papers/multiscale-meshgraphnets-2022.pdf
---

## Summary
MultiScale MeshGraphNets (MS-MGN) introduces a two-level hierarchical graph architecture over the original MeshGraphNets to solve the message-propagation bottleneck: as mesh resolution increases, flat GNNs need proportionally more steps to propagate information across the same physical distance. MS-MGN adds a coarse auxiliary mesh and four update operators (fine, coarse, downsample, upsample) arranged in a V-cycle, borrowing from classical multigrid solvers. Combined with high-accuracy training labels (from finer-mesh reference simulations), MS-MGN achieves spatial convergence — accuracy improves as mesh resolution increases — which flat MeshGraphNets cannot do.

## Problem
Standard MeshGraphNets exhibit flat error plateaus at fine mesh resolutions: adding more vertices requires proportionally more message-passing steps to keep the same physical propagation radius, so compute scales quadratically. The method also cannot improve beyond reference solver accuracy at a given resolution.

## Method
**Two-level graph:** Fine graph $G^h$ (simulation mesh) + coarse graph $G^l$ (auxiliary coarser mesh). Four learnable update operators, each an MLP with residual connections:

| Operator | Input | Output |
|----------|-------|--------|
| $f^{E,h}, f^{V,h}$ | fine edges/nodes | fine node update |
| $f^{E,l}, f^{V,l}$ | coarse edges/nodes | coarse node update |
| $f^{E,h\to l}, f^{V,h\to l}$ | fine→coarse edges | downsample |
| $f^{E,l\to h}, f^{V,l\to h}$ | coarse→fine edges | upsample |

**V-cycle:** fine update → downsample → coarse update → upsample → fine update. Multiple V-cycles can be stacked. Coarse-level updates propagate long-range information cheaply; fine-level handles local detail.

**High-accuracy labels:** Instead of using reference solver output at the target resolution, labels are interpolated from higher-resolution simulations. The network implicitly learns subgrid dynamics and can exceed classical solver accuracy at a given resolution.

## Key Results
- MS-MGN with 25 message-passing steps tracks the reference solver's spatial convergence curve; flat MGN error stagnates
- Combined with high-accuracy labels, error falls below reference solver across all tested resolutions
- Reduces long-range spatial error (low Fourier eigenvalues) compared to baseline
- Coarser auxiliary mesh must be conformal to simulation domain; uniform grids perform strictly worse

## Limitations
- Error accumulation persists on long rollouts; not eliminated, only reduced
- Experiments focus on CylinderFlow fluid; generalization to complex character geometries is extrapolated, not demonstrated
- Coarse mesh design (conformal vs uniform) significantly impacts results; no automatic coarsening strategy given

## Connections
- [[papers/pfaff-2021-meshgraphnets]] — direct extension; MS-MGN is the official DeepMind follow-up
- [[papers/grigorev-2023-hood]] — HOOD uses a similar hierarchical idea for garment dynamics; learns inter-level transitions implicitly
- [[papers/libao-2023-meshgraphnetsrp]] — another extension (GRU + physics losses) for cloth
- [[concepts/secondary-motion]] — multi-scale mesh simulation applicable to character secondary motion
