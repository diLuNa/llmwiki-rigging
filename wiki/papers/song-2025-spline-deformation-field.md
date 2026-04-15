---
title: "Spline Deformation Field"
authors: [Song, Mingyang; Zhang, Yang; Mihajlovic, Marko; Tang, Siyu; Gross, Markus; Aydin, Tunc Ozan]
venue: SIGGRAPH 2025 Conference Papers
year: 2025
tags: [deformation, skinning, neural, simulation, math]
source: https://arxiv.org/abs/2507.07521
---

## Summary
Proposes a spline-based trajectory representation for modeling dense point motion in dynamic scenes. Instead of relying on neural networks to represent trajectories implicitly, the paper uses explicit spline curves where the number of knots directly controls degrees of freedom. This enables analytical computation of velocity and acceleration (via spline derivatives), better temporal coherence, and superior interpolation with sparse input observations. A complementary "low-rank time-variant spatial encoding" replaces conventional spatiotemporal coupling.

## Problem
Dynamic scene reconstruction from video requires modeling dense 3D point trajectories over time. Neural deformation fields (e.g., D-NeRF, HyperNeRF) implicitly encode motion but:
- Cannot analytically compute velocity/acceleration
- Produce temporally inconsistent reconstructions between frames
- Require expensive evaluation at every time step
- Decouple spatial structure from temporal dynamics (heuristic spatiotemporal coupling)

Linear blend skinning (LBS)-based deformation avoids some issues but introduces articulation artifacts and requires explicit skeleton fitting.

## Method

### Spline Trajectories
Each point $\mathbf{p}$ in the scene has a trajectory $\mathbf{p}(t)$ represented as a spline curve over time $t \in [0, T]$:

```math
\mathbf{p}(t) = \sum_{i} c_i \cdot B_{i,k}(t)
```

where $B_{i,k}$ are B-spline basis functions of degree $k$ over a knot sequence $t_0 < t_1 < \ldots < t_m$, and $c_i \in \mathbb{R}^3$ are control points (one per knot interval). The number of knots $m$ directly controls the trajectory's degrees of freedom — more knots = more complex motion.

**Analytic derivatives**: Velocity $\mathbf{v}(t) = d\mathbf{p}/dt$ and acceleration $\mathbf{a}(t) = d^2\mathbf{p}/dt^2$ are computed analytically from the B-spline derivative formulae — no finite differences required.

### Low-Rank Time-Variant Spatial Encoding
Rather than coupling space and time through a single spatiotemporal feature (as in HexPlane or K-planes), the paper introduces a spatial encoding that varies smoothly over time as a low-rank decomposition:

```
spatial feature(x, t) = Σ_r  f_r(x) · g_r(t)
```

where $f_r(x)$ are spatial basis features and $g_r(t)$ are temporal modulation functions. The rank $r$ controls the coupling expressiveness. This avoids the sharp temporal transitions of hash-grid approaches.

### Integration with Dynamic Representation
The spline trajectories and spatial encoding are combined:
1. For each point, a spline trajectory defines its canonical-to-deformed mapping over time
2. The spatial encoding enriches per-point features for appearance modeling
3. Training: minimize photometric reconstruction loss against input video frames

## Key Results
- Superior temporal interpolation: given sparse keyframe observations, spline trajectories generalize smoothly to intermediate times vs. neural implicit alternatives
- Competitive or better dynamic scene reconstruction quality vs. state-of-the-art methods (4D-GS, HexPlane, etc.)
- Analytical velocity/acceleration enables physically-informed regularization and downstream use in physics simulation
- Faster inference: spline evaluation is cheaper than neural network forward pass

## Limitations
- Number of knots is a hyperparameter: too few → underfitting complex motion; too many → overfitting or training instability
- Spline representation is per-scene: requires re-training for each new video, unlike generalizable neural approaches
- Not directly applicable to articulated character animation (no semantic skeleton or rig)
- Not yet demonstrated on production-scale character deformation pipelines

## Connections
- [[concepts/b-spline-volumes]] — shares the B-spline mathematical framework; this paper applies it in the time dimension rather than spatial volume
- [[concepts/skinning]] — alternative to LBS-based dynamic scene representation; explicitly avoids LBS articulation artifacts
- [[papers/sederberg-1986-ffd]] — foundational B-spline/Bernstein deformation; this paper's temporal spline is the 1D analog of FFD's trivariate volume

## Implementation Notes
- B-spline evaluation in time is trivially vectorizable across all scene points in parallel
- PyTorch B-spline: `torch-cubic-spline-grids` or `torchdiffeq` for differentiable spline fitting
- Knot placement strategy: uniform knots for constant-tempo motion; adaptive knots (clustering around high-acceleration frames) for complex motion
- For character animation: replace per-point spline trajectories with per-joint spline trajectories — the skeleton then drives skin via standard LBS but each joint's trajectory is spline-parameterized, eliminating foot-sliding and temporal jitter

## Quotes
> "The number of knots explicitly determines the degrees of freedom, enabling analytical computation of velocities and accelerations while improving spatial coherence." (Abstract)
