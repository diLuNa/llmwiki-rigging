---
title: "Exoskeleton: Curve Network Abstraction for 3D Shapes"
authors: [de Goes, Fernando; Goldenstein, Siome; Desbrun, Mathieu; Velho, Luiz]
venue: Computers & Graphics 2011
year: 2011
tags: [rig-generation, deformation, skinning, math]
source: ~no local pdf~
---

## Summary
Introduces the Exoskeleton representation — a curve network that forms a topological skeleton abstracting a 3D shape's structure. The exoskeleton captures the shape's connectivity and profile curves, serving as a precursor to the curvenet rigging concept.

## Problem
Skeleton-based shape abstraction and character rigging typically use point skeletons (joint hierarchies). Curve-based skeletons better capture the profile and silhouette structure of organic shapes and enable more expressive deformation control.

## Method
Constructs a curve network on the surface that:
- Captures the topological skeleton of the shape (one curve per handle/limb).
- Follows the principal curvature directions of the surface.
- Can be used for shape editing by deforming the curve network and recovering a surface consistent with the new curves.

The curve network is computed automatically from the shape's topology and curvature structure, with user refinement allowed.

## Key Results
- Compact curve-network abstraction for complex 3D shapes.
- Demonstrated on organic characters.
- Conceptual precursor to [[papers/degoes-2022-profile-curves]] curvenet rigging.

## Limitations
- Automated curve network construction can fail on shapes with ambiguous topology.
- Does not directly produce animation controls — that development came later with curvenet rigging.

## Connections
- [[papers/degoes-2022-profile-curves]] — direct descendant: curvenet rigging
- [[concepts/curvenet-rigging]]
- [[authors/degoes-fernando]]
- [[authors/desbrun-mathieu]]
