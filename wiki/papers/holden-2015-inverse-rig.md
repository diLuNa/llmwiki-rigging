---
title: "Learning an Inverse Rig Mapping for Character Animation"
authors: [Holden, Daniel; Saito, Jun; Komura, Taku]
venue: SCA (Symposium on Computer Animation) 2015
year: 2015
tags: [rig-generation, neural, pose-space, math]
source: ~no local pdf~
---

## Summary
Learns a nonlinear inverse rig mapping (skeleton pose → rig parameters) using a feedforward neural network trained on sampled rig evaluations. Enables real-time rig inversion without Jacobian computation, at the cost of approximation error for out-of-distribution poses.

## Problem
Rig inversion (finding rig parameters that reproduce a given skeleton pose) typically requires iterative optimization with expensive Jacobian evaluation. A learned direct mapping avoids the Jacobian entirely.

## Method
Samples the rig's forward mapping $f: \mathbf{q} \to \mathbf{x}$ across the rig's parameter space, producing a training set of $(\mathbf{q}, \mathbf{x})$ pairs. Trains a multilayer perceptron to approximate $f^{-1}: \mathbf{x} \to \mathbf{q}$. At runtime, a single forward pass of the network provides the approximate rig parameters.

Key considerations:
- Rig parameter space is typically high-dimensional; sampling must cover the space densely.
- Network must generalize smoothly to unseen poses.
- Follow-up work (Holden et al. 2017) improves with nonlinear regression.

## Key Results
- Real-time rig inversion.
- Good accuracy within the training distribution.
- Foundation for subsequent Pixar work on analytic Jacobian learning [[papers/gustafson-2020-inverse-rig]].

## Limitations
- Accuracy degrades for poses far from the training distribution.
- Training data collection scales poorly with rig parameter count.
- Network must be retrained when the rig changes.

## Connections
- [[papers/gustafson-2020-inverse-rig]] — Pixar's follow-up; analytic Jacobian approach
- [[papers/hahn-2012-rig-space-physics]] — rig Jacobian used in physics projection
- [[concepts/rig-inversion]]
- [[authors/holden-daniel]]
