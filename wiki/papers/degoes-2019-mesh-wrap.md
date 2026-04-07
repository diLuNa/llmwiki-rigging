---
title: "Mesh Wrap based on Affine-Invariant Coordinates"
authors: [de Goes, Fernando; Martinez, Alonso]
venue: SIGGRAPH Talks 2019
year: 2019
tags: [mesh-wrap, deformation, rig-generation, math]
source: raw/papers/2019.SiggraphTalks.GM.pdf
---

## Summary
A mesh connectivity transfer (wrapping) method using affine-invariant mesh coordinates to robustly adapt one mesh's topology to another target shape, even under large locally non-rigid deformations. Used at Pixar to wrap 600 humanoid characters to a shared reference mesh.

## Problem
Traditional mesh wrap tools (ICP-based) fail under large locally non-rigid deformations common in character libraries (different body proportions, facial structures). Artists need to share mesh topology across characters for downstream USD/rig compatibility.

## Method
Enriches an iterative closest-point framework with **affine-invariant coordinates** that parametrize edge spans of the source tessellation. These coordinates are invariant to locally affine (linear) transformations, so the method tracks patch layout robustly under large shape change. Interactive workflow supports curve-correspondence authoring to guide the wrap.

## Key Results
- Successfully wrapped 600 humanoid characters spanning 15 years of Pixar production.
- Preserves patch layout and edge flow of the source mesh.
- Interactive curve-correspondence UI for authoring control.

## Limitations
- Requires curve correspondence authoring for very dissimilar shapes.
- Limited to shapes with broadly similar topology class (humanoid → humanoid).

## Connections
- [[papers/degoes-2018-patch-relax]] — related mesh layout preservation technique
- [[concepts/mesh-wrap]]
- [[authors/degoes-fernando]]

## Implementation Notes
Affine-invariant coordinates are related to mean-value coordinates but constructed to be invariant under the local affine transformation estimated at each vertex. The ICP loop alternates between coordinate-based deformation and closest-point matching.
