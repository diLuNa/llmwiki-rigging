---
title: "Skinning"
tags: [skinning, lbs, dqs, deformation, math]
---

## Definition
Skinning is the process of deforming a character mesh in response to an underlying skeleton. Each vertex is influenced by one or more joints; the joint transforms are blended to produce the final vertex position. Skinning is distinct from shape-based deformation (blendshapes, correctives) — it handles the continuous transformation of mesh vertices under joint motion rather than the discrete interpolation of sculpted targets.

## Variants / Taxonomy

### Linear Blend Skinning (LBS)
[[concepts/linear-blend-skinning]] — the standard production method. Each vertex $\mathbf{v}$ is a weighted average of the joint-transformed copies:

```
v' = Σⱼ wⱼ (Tⱼ · v)
```

Fast, simple, GPU-friendly. Artifacts: candy-wrapper twist collapse, volume loss at extreme bends.

### Dual Quaternion Skinning (DQS)
[[concepts/dual-quaternion-skinning]] — blends joint transforms in dual quaternion space instead of matrix space. Eliminates candy-wrapper. Slight volume inflation at joint extremes ("bulging") — correctable with iterative blending.

### Center of Rotation (CoR) Skinning
Computes a per-vertex optimal center of rotation that minimizes skinning error vs. LBS, stored as a precomputed correction. Near-equivalent quality to DQS with fewer artifacts.

### Implicit Skinning
Represents the character surface as an implicit function; composites joint-local implicit primitives. Handles contact and self-intersection naturally but expensive at production scale.

### Neural Skinning
Learned skinning models that predict vertex positions from joint transforms via neural networks. Examples: Neural Blend Shapes (Li et al., SIGGRAPH 2021 — [[papers/li-2021-neural-blend-shapes]]), which learns pose-dependent corrective shapes on top of LBS.

### Cage-Based Deformation
[[concepts/cage-deformation]] — the skin deforms relative to a coarse control cage rather than directly from skeleton joints. Harmonic, Green, and Somigliana coordinates generalize the cage-to-mesh mapping.

### Geometric Skinning (Bounded Biharmonic Weights)
[[concepts/bounded-biharmonic-weights]] — computes smooth, bounded skinning weights that satisfy the Laplace equation. Standard for computing weights from geometry automatically.

## Key Papers
- [[papers/magnenat-thalmann-1988-lbs]] — original LBS formulation (if ingested)
- [[papers/kavan-2008-dqs]] — dual quaternion skinning (SIGGRAPH 2008)
- [[papers/jacobson-2011-bbw]] — bounded biharmonic weights; auto-computed smooth weights (SIGGRAPH 2011)
- [[papers/le-2014-skeletal-rigging]] — Smooth Skinning Decomposition (SSDR / Dem Bones); fits skinning to mesh sequences
- [[papers/li-2021-neural-blend-shapes]] — neural blend shapes; learned pose-dependent correctives on LBS (SIGGRAPH 2021)

## Connections
- [[concepts/linear-blend-skinning]] — detailed LBS page
- [[concepts/dual-quaternion-skinning]] — detailed DQS page
- [[concepts/bounded-biharmonic-weights]] — automatic weight computation
- [[concepts/correctives]] — corrective shapes compensate for skinning artifacts
- [[concepts/pose-space-deformation]] — corrective framework driven by pose parameters
- [[concepts/rig-inversion]] — inverse problem: recovering rig parameters from a skinned mesh

## Notes
- In practice, production characters combine LBS for the skeleton drive with corrective blendshapes for artifact suppression. DQS is used selectively for extreme twist joints (forearm, neck).
- Skin weight painting is time-intensive; bounded biharmonic weights and Dem Bones automate the process from reference mesh sequences.
- The skinning equation is the forward rig function $f(\beta)$ in the rig inversion literature — all inverse rig methods assume some form of skinning model as the base deformer.
