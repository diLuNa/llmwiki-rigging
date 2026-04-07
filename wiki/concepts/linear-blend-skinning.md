---
title: "Linear Blend Skinning (LBS)"
tags: [skinning, lbs, deformation]
---

## Definition
The standard skinning algorithm. Each vertex position $v'$ is computed as a weighted sum of bone-transformed positions:

```math
v' = \sum_i w_i T_i v
```

where $w_i$ are skinning weights, $T_i$ are bone world transforms, and weights sum to 1.

## Artifacts
- **Candy-wrapper**: volume collapse at twisted joints (e.g. forearm). Caused by linear interpolation of rotation matrices.
- **Volume collapse at bends**: joint bending loses volume.
- Cannot reproduce non-rigid anatomical deformation.

## Variants / Taxonomy
- Standard LBS (matrix blend)
- Dual Quaternion Skinning — see [[concepts/dual-quaternion-skinning]]
- Spherical blend skinning (less common)

## Key Papers
- [[papers/kavan-2007-dqs]] — identifies and fixes candy-wrapper with DQS
- [[papers/loper-2015-smpl]] — SMPL is an LBS rig with learned weights and pose correctives
- [[papers/le-2012-ssdr]] — SSDR extracts LBS rigs from animation sequences automatically

## Connections
- [[concepts/dual-quaternion-skinning]]
- [[concepts/bounded-biharmonic-weights]] — computes the weights used in LBS
