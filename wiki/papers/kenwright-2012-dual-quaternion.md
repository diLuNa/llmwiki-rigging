---
title: "A Beginners Guide to Dual-Quaternions: What They Are, How They Work, and How to Use Them for 3D Character Hierarchies"
authors: [Kenwright, Ben]
venue: WSCG 2012
year: 2012
tags: [skinning, dqs, math]
source: raw/papers/dual-quaternion.pdf
---

## Summary
A tutorial introduction to dual quaternions and their application to character skeleton hierarchies. Explains dual number theory, how quaternions extend to dual quaternions, how dual quaternions represent rigid transforms (rotation + translation jointly), and how to implement them in code. Companion reading to the Kavan et al. 2007 DQS paper.

## Problem
Matrices are the standard representation for rigid transforms in character rigs, but dual quaternions offer a more compact, interpolation-friendly alternative. Most practitioners lack the mathematical background to understand or implement dual quaternions from scratch.

## Method
**Tutorial structure:**
1. Quaternion review — rotation representation, SLERP.
2. Dual numbers — extending reals with a nilpotent unit ε (ε² = 0).
3. Dual quaternions — quaternion with dual-number coefficients; encodes rotation in real part, translation in dual part.
4. Rigid transform encoding: `q̂ = q_r + ε·(0.5·t·q_r)` where q_r is rotation quaternion and t is translation.
5. Composition and inverse: multiplication, normalization.
6. Blending: linear blend of unit dual quaternions (DLB) — the basis of DQS skinning.
7. Code examples: C/C++ struct and operations.

**Key identity:** `DQ = (cos(θ/2) + sin(θ/2)·n̂) + ε·(0.5·t·DQ_rotation)`

## Key Results
This is a tutorial, not a research contribution. Provides clear step-by-step derivations and code for practitioners.

## Limitations
- Tutorial only; no novel contributions.
- Does not discuss DQS artifact (antipodality) or the cord artifact at joints with large rotation ranges.
- Predates Le & Lewis 2019 Direct Delta Mush which subsumes DQS for many use cases.

## Connections
- [[papers/kavan-2007-dqs]] — the primary research paper this tutorial explains
- [[concepts/dual-quaternion-skinning]] — concept page for DQS
- [[papers/le-2019-direct-delta-mush]] — more recent alternative

