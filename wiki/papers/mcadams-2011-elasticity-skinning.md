---
title: "Efficient Elasticity for Character Skinning with Contact and Collisions"
authors: [McAdams, Aleka; Zhu, Yongning; Selle, Andrew; Empey, Mark; Tamstorf, Rasmus; Teran, Joseph; Sifakis, Eftychios]
venue: SIGGRAPH 2011
year: 2011
tags: [simulation, skinning, muscles, volumes, math]
source: ~no local pdf~
---

## Summary
Presents an efficient elastic simulation system for character skin and flesh that handles contact and self-collisions at production scale. Uses a multigrid solver and corotational FEM to achieve interactive rates on tet meshes embedded in character geometry.

## Problem
Physics-based skin simulation for characters requires handling: (1) large deformations from skeletal animation, (2) self-contact between skin surfaces, (3) flesh-bone collisions. Prior methods were too slow for production use or sacrificed quality.

## Method
- **Corotational FEM** on tetrahedral embedded mesh: decomposes deformation into rotation + linear strain, enabling efficient stiffness matrix construction.
- **Multigrid preconditioned conjugate gradient**: fast solver for the large sparse linear system per Newton step.
- **Contact handling**: penalty-based contact forces, with continuous collision detection for skin surfaces.
- **Parallelism**: per-element assembly and multigrid hierarchy are parallelized.

Cited in both the Kelvinlets paper and Somigliana as a reference for production-quality character elastic simulation.

## Key Results
- Production-quality elastic skin simulation at near-interactive rates.
- Demonstrated on complex characters with self-contact.
- Multigrid approach provides scalable performance.

## Limitations
- Corotational FEM loses accuracy under very large deformations (artifacts under extreme twists).
- Embedded mesh resolution limits fine-detail deformation.

## Connections
- [[papers/smith-2018-neo-hookean]] — stable Neo-Hookean replaces corotational for better volume preservation
- [[papers/kim-2022-dynamic-deformables]] — production FEM course
- [[papers/james-2020-phong-deformation]] — improves visual quality of embedded geometry
- [[concepts/neo-hookean-simulation]]
- [[authors/sifakis-eftychios]]
