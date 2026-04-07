---
title: "Real-time Skeletal Skinning with Optimized Centers of Rotation"
authors: [Le, Binh; Hodgins, Jessica]
venue: ACM SIGGRAPH 2016
year: 2016
tags: [skinning, lbs, correctives]
source: ~no local PDF~
---

## Summary
Eliminates the candy-wrapper / collapse artifact of LBS by computing per-vertex **optimal centers of rotation** (CoR) analytically from the blend weights. At runtime, each vertex rotates around its CoR using the weighted-average rotation, producing volume-preserving deformation without switching to dual quaternions or adding corrective shapes.

## Problem
LBS collapses volume at joints with opposing bone rotations (candy-wrapper). DQS avoids collapse but introduces a bulge artifact and non-commutativity issues. Correctives are expensive to author. A purely weight-driven solution that needs no extra data would be ideal.

## Method
**Key insight:** For a vertex influenced by two joints rotating in opposite directions, the "center of rotation" — the point that maps to itself under the weighted blend of joint transforms — can be computed analytically from the blend weights and bone rest positions.

**Optimal CoR precomputation (offline):**
Given blend weights $w_i$ per joint $i$, for each vertex $\mathbf{v}$:
```math
\mathbf{c}_v = \frac{\sum_{i<j} w_i w_j (\mathbf{c}_i + \mathbf{c}_j)}{\sum_{i<j} w_i w_j}
```
where $\mathbf{c}_i$ are joint positions. This is the minimizer of candy-wrapper over all possible rotation centers in the blend weight space.

**Runtime deformation:**
1. Compute weighted-average rotation $\bar{R}_v$ via quaternion SLERP/averaging over blend weights.
2. Translate vertex relative to its CoR, apply $\bar{R}_v$, translate back.
3. Apply the weighted-average translation term separately.

This replaces the standard LBS linear combination of full transforms.

**Result:** Rotation blending around the optimal center naturally preserves volume without explicit volume correction.

## Key Results
- Eliminates candy-wrapper collapse at joints under opposing rotations.
- No DQS bulge artifact.
- Same blend-weight input as LBS — no authoring overhead.
- Real-time performance (precomputed CoR; runtime cost nearly identical to LBS).
- Demonstrated on standard character benchmarks (arm twist, hip twist).

## Limitations
- CoR computation assumes rigid joint transforms — does not handle non-rigid (scale) transforms well.
- Blend weight quality still determines output quality; bad weights still produce bad CoRs.
- Does not handle skin sliding or fascia effects.

## Connections
- [[papers/kavan-2007-dqs]] — DQS is the main prior approach; CoR avoids DQS bulge
- [[papers/le-2019-direct-delta-mush]] — same first author; DDM is a more general framework
- [[papers/jacobson-2011-bbw]] — blend weights this method builds on
- [[concepts/linear-blend-skinning]] — the baseline this improves
- [[concepts/dual-quaternion-skinning]] — the main competitor
- [[authors/le-binh]] — first author

