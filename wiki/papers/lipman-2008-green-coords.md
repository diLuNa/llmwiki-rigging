---
title: "Green Coordinates"
authors: [Lipman, Yaron; Levin, David; Cohen-Or, Daniel]
venue: SIGGRAPH 2008
year: 2008
tags: [cage-deformation, deformation, math, skinning]
source: ~no local pdf~
---

## Summary
Introduces Green Coordinates — a cage deformation scheme where interior points are expressed as a combination of both cage vertex positions *and* cage face normals. The resulting deformation is similarity-invariant (preserves local shape under similarity transforms of the cage) and detail-preserving, significantly outperforming mean-value coordinates for character deformation.

## Problem
Mean-value coordinates and related cage deformers produce undesirable shearing when cage faces are non-uniformly scaled. Artists want a cage deformer that preserves local shape details — the cage should act like a similarity transformation locally, not an arbitrary affine map.

## Method
Derives coordinates from Green's third integral identity applied to harmonic functions in the cage interior. Each interior point $\mathbf{x}$ is expressed as:

```math
\mathbf{x}' = \sum_j \phi_j(\mathbf{x})\,\mathbf{v}_j' + \sum_k \psi_k(\mathbf{x})\,s_k\,\mathbf{n}_k'
```

where $\phi_j$ are vertex coordinates, $\psi_k$ are face coordinates, $\mathbf{v}_j'$ are deformed cage vertices, $\mathbf{n}_k'$ are deformed face normals, and $s_k$ is the local scale factor of face $k$.

Key properties:
- **Similarity invariant**: if the cage undergoes a similarity transformation, so does every interior point.
- **Detail preserving**: the face-normal term captures local shape orientation.
- **Closed-form**: no volumetric solve required; coordinates computed analytically per face triangle.
- Coordinates can be negative outside the cage.

## Key Results
- Visually superior to MVC for character deformation under large cage deformations.
- Handles complex characters with fine surface detail.
- Demonstrated on 2D and 3D characters.

## Limitations
- Coordinates are not guaranteed non-negative (can produce artifacts outside the cage).
- No volume control — bulging requires post-processing (addressed by [[papers/chen-2023-somigliana]]).
- Shearing can still occur under non-similarity deformations.

## Connections
- [[papers/chen-2023-somigliana]] — Somigliana Coordinates generalize Green Coordinates with volume control
- [[papers/degoes-2024-stochastic-bary]] — stochastic evaluation of Green Coordinates and others
- [[papers/joshi-2007-harmonic-coords]] — alternative cage coordinates using Laplace equation
- [[concepts/cage-deformation]]
- [[authors/lipman-yaron]]

## Quotes
> The deformed shape reproduces similarity transformations of the cage exactly, ensuring that local shape details are preserved.
