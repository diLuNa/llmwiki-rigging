---
title: "Go Green: General Regularized Green's Functions for Elasticity"
authors: [Chen, Jiong; Desbrun, Mathieu]
venue: SIGGRAPH 2022
year: 2022
tags: [cage-deformation, deformation, elasticity, math]
source: ~no local pdf~
---

## Summary
Introduces a general framework for constructing regularized elasticity-based deformation kernels (Green's functions) that unifies Kelvinlets, Somigliana coordinates, and Green Coordinates under one theoretical umbrella. Provides a principled way to design new deformation operators with controllable locality and elastic behavior.

## Problem
Kelvinlets, Green Coordinates, and related methods each use different elasticity fundamental solutions with different approximations and regularizations. No unified framework explained why each works, what their limitations are, or how to design new variants.

## Method
Constructs regularized Green's functions for general elastic operators via:
- A regularization scheme that controls the spatial locality of the kernel.
- A corotational formulation that ensures deformation is rotation-aware (no shearing on rigid motion).
- A unifying boundary integral formulation that encompasses Kelvinlets (volume forces), Somigliana (boundary tractions), and Green Coordinates (boundary displacements) as special cases.

The framework enables designing new kernels by choosing the elastic operator, boundary type, and regularization independently.

## Key Results
- Unified theory for elasticity-based deformation methods.
- New kernel variants with properties not achievable by prior methods individually.
- Direct predecessor to [[papers/chen-2023-somigliana]].

## Limitations
- Primarily theoretical; practical implementation details depend on the chosen kernel.
- Numerical quadrature required for evaluation in general cases.

## Connections
- [[papers/chen-2023-somigliana]] — Somigliana Coordinates is the primary application of this framework
- [[papers/degoes-2018-kelvinlets]] — Kelvinlets arise as a special case
- [[papers/lipman-2008-green-coords]] — Green Coordinates arise as another special case
- [[concepts/cage-deformation]]
- [[concepts/kelvinlets]]
- [[authors/chen-jiong]]
- [[authors/desbrun-mathieu]]
