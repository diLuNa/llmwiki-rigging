---
title: "Blendshapes"
tags: [blendshapes, correctives, facs, usd, pose-space]
---

## Definition
Blendshapes (also: morph targets, shape keys) encode deformation as per-vertex delta displacements relative to a base mesh. A scalar weight controls the blend amount.

```math
v' = v_{base} + \sum_i w_i \delta_i
```

## Normalization Conventions
Two major conventions:

- **Normalized (0–1)**: weights are clamped to [0,1]. Full shape at w=1. Cannot exceed the sculpted amount. Most DCC tools default to this.
- **Non-normalized (UsdSkel convention)**: weights are unbounded. Allows additive combinations and overshooting. Better for corrective workflows; weights can exceed 1 or be negative.

The non-normalized convention is important for USD/Houdini Solaris pipelines — see [[concepts/usdskel]].

## FACS
The Facial Action Coding System defines a standard vocabulary of facial blendshapes (Action Units). Common in facial rigging.

## Key Papers
- [[papers/lewis-2000-psd]] — PSD as framework for corrective blendshapes
- [[papers/lewis-2014-blendshape-star]] — comprehensive EG 2014 survey; canonical reference for conventions and taxonomy
- [[papers/loper-2015-smpl]] — SMPL pose blend shapes are learned corrective blendshapes
- [[papers/li-2017-flame]] — FLAME expression basis $B_E = E\psi$ is a PCA blendshape system
- [[papers/neumann-2013-sparse-deformation]] — learns sparse localized blendshapes from mesh sequences
- [[papers/wang-2015-linear-subspace]] — optimizes compact linear blendshape palettes from rig samples
- [[papers/li-2021-neural-blend-shapes]] — learns blendshape basis and weights jointly from rig data
- [[papers/jtdp-2003-blendshape-fitting]] — foundational marker-to-blendshape inverse solve (performance-driven)

## Connections
- [[concepts/pose-space-deformation]]
- [[concepts/usdskel]]
- [[papers/degoes-2020-sculpt]]
