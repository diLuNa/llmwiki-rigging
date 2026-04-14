---
title: "JGS2: Near Second-order Converging Jacobi/Gauss-Seidel for GPU Elastodynamics"
authors: [Lan, Lei; Lu, Zixuan; Yuan, Chun; Xu, Weiwei; Su, Hao; Wang, Huamin; Jiang, Chenfanfu; Yang, Yin]
venue: ACM Transactions on Graphics (SIGGRAPH 2025)
year: 2025
tags: [simulation, deformable-objects, gpu-computing, elastodynamics, linear-solvers]
source: arXiv:TBA
doi: 10.1145/3721238.3730770
---

## Summary
Parallel randomized Gauss-Seidel method for GPU-accelerated simulation of deformable objects (skin, cloth, soft tissue). Achieves convergence rates comparable to fullspace Newton's method while maintaining GPU parallelizability. Addresses overshoot problem through theoretically optimal second-order solution.

## Problem
GPU simulation of 3D deformable objects requires efficient parallel linear solvers. Standard iterative methods (Jacobi) lack convergence speed; Newton methods require expensive matrix inversions. Balancing convergence speed with parallelizability is critical for real-time character animation.

## Method
- **Randomized Gauss-Seidel**: Probabilistic local solve ordering enabling parallel GPU execution
- **Overshoot mitigation**: Energy-based formulation preventing aggressive local minimization
- **Adaptive preconditioning**: Connectivity-enhanced MAS preconditioner for irregular meshes
- **Second-order convergence**: Theoretical analysis achieving near-Newton convergence rates

## Key Results
- Convergence rates comparable to fullspace Newton methods
- Significant speedups on GPU vs. Jacobi iteration
- Handles large, irregular tetrahedral and triangular meshes
- Enables real-time soft-body character deformation

## Limitations
- Convergence depends on preconditioner quality
- Memory overhead for irregular mesh structures
- Stiffness (condition number) affects convergence speed
- Requires careful parameter tuning per scene

## Connections
- [[concepts/simulation]] — physics-based character deformation
- [[papers/teran-2005-quasistatic-flesh]] — quasistatic flesh simulation
- [[papers/mcadams-2011-elasticity-skinning]] — elasticity in character animation
- [[techniques/ml-deformer]] — learned alternatives to simulation
- [[papers/pfaff-2021-meshgraphnets]] — neural physics simulation

## Implementation Notes
- Particularly effective for stiff materials (muscle, skin, cartilage)
- Parallelizable across GPU thread blocks for irregular meshes
- Preconditioner selection critical for convergence
- Compatible with Houdini geometry, standard FEM discretizations

## External References
- arXiv: [arxiv.org/abs/TBA](https://arxiv.org/abs/TBA)
- Project page: [wanghmin.github.io/publication/lan-2025-jgs](https://wanghmin.github.io/publication/lan-2025-jgs/)
- ACM DL: [doi.org/10.1145/3721238.3730770](https://doi.org/10.1145/3721238.3730770)
