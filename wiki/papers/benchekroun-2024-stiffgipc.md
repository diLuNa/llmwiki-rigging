---
title: "StiffGIPC: Advancing GPU IPC for Stiff Affine-Deformable Simulation"
authors: [Benchekroun, Otman; Zhang, Jiayi; Chaudhuri, Siddhartha; Grinspun, Eitan; Zhou, Yi; Wang, Huamin; Jiang, Chenfanfu; Yang, Yin]
venue: ACM Transactions on Graphics (SIGGRAPH 2024)
year: 2024
tags: [simulation, contact, gpu-computing, deformable-objects, incremental-potential]
source: TBA
doi: 10.1145/3735126
---

## Summary
GPU-accelerated Incremental Potential Contact (IPC) method for robust, accurate simulation of stiff deformable materials with complex frictional contacts. Introduces connectivity-enhanced MAS preconditioner addressing efficiency bottlenecks in stiff material simulation while maintaining IPC robustness guarantees.

## Problem
IPC is robust and accurate but becomes inefficient for stiff materials (high Young's modulus). GPU acceleration is essential for production character animation but requires effective preconditioners for irregular mesh topologies.

## Method
- **GPU IPC foundation**: Parallel barrier-based contact formulation
- **Connectivity-enhanced MAS**: Preconditioner leveraging mesh adjacency structure
- **Stiffness scaling**: Adaptive parameter tuning for material stiffness ranges
- **Hybrid solver**: CPU-GPU load balancing for irregular geometries

## Key Results
- Significant speedups for stiff material simulation vs. standard IPC
- Maintains robustness and accuracy guarantees
- Handles large, irregular tetrahedral and triangular meshes
- Enables real-time or near-real-time character simulation

## Limitations
- Preconditioner quality depends on mesh regularity
- High stiffness may still require small timesteps
- Memory overhead for connectivity structures
- Requires careful parameter tuning per material type

## Connections
- [[papers/bouaziz-2014-projective-dynamics]] — related contact formulation
- [[papers/teran-2005-quasistatic-flesh]] — quasistatic soft tissue
- [[papers/lan-2025-jgs2]] — related GPU linear solver
- [[concepts/simulation]] — physics-based character animation
- [[papers/pfaff-2021-meshgraphnets]] — neural simulation alternatives

## Implementation Notes
- Connectivity-enhanced preconditioner critical for irregular meshes
- Stiffness scaling requires material-specific tuning
- Compatible with Houdini DOP solver integration
- Hybrid CPU-GPU approach needed for production pipelines

## External References
- ACM DL: [doi.org/10.1145/3735126](https://doi.org/10.1145/3735126)
- SIGGRAPH 2024 proceedings
