---
title: "Fast Automatic Skinning Transformations"
authors: [Jacobson, Alec; Baran, Ilya; Kavan, Ladislav; Popović, Jovan; Sorkine, Olga]
venue: SIGGRAPH 2012
year: 2012
tags: [skinning, lbs, math, rig-generation]
source: ~no local pdf~
---

## Summary
Proposes Automatic Skinning Transformations (FAST) — a method that automatically computes per-bone rigid transformation sequences that minimize an elastic energy, producing natural LBS deformations without any weight painting or corrective sculpting. The approach handles volume preservation and avoids candy-wrapper artifacts inherently.

## Problem
LBS requires both skinning weights and bone transforms. Standard pipeline: animate bone transforms, apply weights. But the interaction between weights and transforms is complex — good weights with bad transforms still look bad. FAST jointly optimizes transforms to minimize elastic deformation energy, given fixed weights.

## Method
Given user-specified rest poses and a set of handle constraints, solves for rigid transformations $T_j$ at each bone that minimize:

```math
E = \sum_{\text{elements}} w_e \| \sum_j w_{ej} T_j - \text{target} \|^2
```

This is a sequence of local SVD problems (analogous to ARAP [[papers/sorkine-2007-arap]]) interleaved with global position solves. The weights are precomputed BBW weights [[papers/jacobson-2011-bbw]].

## Key Results
- Automatic, high-quality deformations with no correctives.
- Handles volume preservation and volume loss artifacts better than standard LBS.
- Real-time after precomputation.
- Demonstrated on complex characters with many handles.

## Limitations
- Requires a global solve per frame (more expensive than simple LBS).
- Works best when handles are well-placed; auto-placement still requires user guidance.

## Connections
- [[papers/jacobson-2011-bbw]] — BBW weights used as input
- [[papers/sorkine-2007-arap]] — ARAP-like local-global structure
- [[concepts/linear-blend-skinning]]
- [[authors/jacobson-alec]]
- [[authors/kavan-ladislav]]
- [[authors/sorkine-olga]]
