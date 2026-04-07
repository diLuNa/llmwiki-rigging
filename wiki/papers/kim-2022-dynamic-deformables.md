---
title: "Dynamic Deformables: Implementation and Production Practicalities (Now With Code!)"
authors: [Kim, Theodore; Eberle, David]
venue: SIGGRAPH Course 2022
year: 2022
tags: [simulation, muscles, volumes, math, python]
source: raw/papers/2022.SiggraphCourses.KE.pdf
---

## Summary
A comprehensive, self-contained course on implementing production-quality dynamic deformation solvers, covering the Neo-Hookean formulation, efficient Hessian construction, collision handling, two-way coupling, and production practicalities from Pixar's Fizz simulator. Includes open-source C++ implementations.

## Problem
Academic papers on FEM simulation omit engineering details critical for production use: robust collision detection, solver acceleration, inversion handling, and two-way body–cloth coupling. No unified practical reference existed.

## Method
Covers:
- **Neo-Hookean formulation** (building on [[papers/smith-2018-neo-hookean]]): unified treatment of stable Neo-Hookean with closed-form eigendecomposition of force gradients.
- **System assembly**: vectorized element processing, GPU-friendly data layouts.
- **Solver**: preconditioned conjugate gradient, warm starting, line search.
- **Collision detection and response**: discrete collision, continuous collision, self-collision.
- **Two-way coupling**: cloth–body interaction via implicit constraints (Onward, 2020).
- Timeline of adoption in Pixar's Fizz: cloth (Coco 2017), 3D solids (Cars 3 2017), coupling (Onward 2020).

## Key Results
- Open-source C++ implementation covering most described algorithms.
- Production validation: Boo's shirt (*Monsters, Inc.* 2001) through *Onward* (2020).
- Unified treatment not available in individual SIGGRAPH papers.

## Limitations
- Focus on quasistatic and implicit time integration; explicit methods not covered in depth.
- Cloth model specifics are Fizz-centric.

## Connections
- [[papers/smith-2018-neo-hookean]] — the core hyperelastic formulation
- [[papers/james-2020-phong-deformation]] — embedded deformation used with these solvers
- [[concepts/neo-hookean-simulation]]
- [[authors/kim-theodore]]

## Implementation Notes
The course notes are the best single reference for implementing a production FEM solver. The open-source C++ code covers: stable Neo-Hookean energy + gradient + Hessian, projected Newton, and basic collision. Start here before reading individual papers.
