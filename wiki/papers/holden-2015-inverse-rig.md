---
title: "Learning an Inverse Rig Mapping for Character Animation"
authors: [Holden, Daniel; Saito, Jun; Komura, Taku]
venue: SCA (Symposium on Computer Animation) 2015
year: 2015
tags: [rig-generation, neural, pose-space, math]
source: raw/papers/2786784.2786788.pdf
---

## Summary
First data-driven approach to rig inversion. Trains a multilayer perceptron to map skeleton joint positions directly to rig control parameters, using example animation sequences produced by artists. Enables real-time rig inversion without Jacobian computation. Demonstrated on quadruped, biped, deformable mesh, and facial rigs. The core limitation — training with a parameter-space loss fails when rigs are non-injective — directly motivated Marquis Bolduc 2022.

A substantially extended journal version adding Gaussian Process Regression and super-sampling exists: [[papers/holden-2017-inverse-rig-tvcg]] (IEEE TVCG 2017).

## Problem
Rig inversion (finding rig parameters that reproduce a given skeleton pose) typically requires iterative optimization with expensive Jacobian evaluation. A learned direct mapping avoids the Jacobian entirely and runs in real time, but requires representative training data.

The practical gap: motion synthesis, motion capture retargeting, and physics simulation all output skeleton joint angles or positions; character rigs are controlled by abstract high-level parameters. Without inversion, these techniques cannot be applied to production-rigged characters.

## Method
Collects training pairs $(\mathbf{x}, \mathbf{y})$ from artist-authored animation sequences, where $\mathbf{x} \in \mathbb{R}^{3j}$ is the global joint position vector and $\mathbf{y}$ is the corresponding rig parameter vector. Trains a feedforward MLP to approximate $f^{-1}: \mathbf{x} \to \mathbf{y}$. At runtime, a single network forward pass produces rig parameters in real time.

The paper represents the skeleton as global joint positions (not local angles), which makes the learning problem smoother and more transferable across characters with different rest poses.

Optional refinement: after the network prediction, a Newton step using finite-difference Jacobian of the rig function reduces residual in joint position space.

## Key Results
- Real-time rig inversion (< 1 ms per frame after training).
- Demonstrated on four rig types: quadruped (dog), biped (Stewart), deformable mesh (squirrel), facial rig.
- Mean vertex error on facial rig: ~9.2 mm on random poses (later comparison by Marquis Bolduc 2022).
- Foundation for all subsequent work in the rig inversion literature.

## Limitations
- Accuracy degrades for poses far from the training distribution.
- Requires artist-produced training animations; synthetic random parameter sampling poorly covers the rig's useful range.
- Non-injectivity: multiple rig parameter vectors may produce the same skeleton pose; the parameter-space loss averages over conflicting ground truths.
- Network must be retrained when the rig changes.

## Connections
- [[papers/holden-2017-inverse-rig-tvcg]] — extended journal version; adds GPR, super-sampling, larger evaluation
- [[papers/gustafson-2020-inverse-rig]] — Pixar's follow-up; analytic Jacobian approach eliminates need for training data
- [[papers/marquis-bolduc-2022-differentiable-rig]] — SIGGRAPH Asia 2022; directly addresses non-injectivity via mesh loss on differentiable rig approximation; 3–4× lower error
- [[papers/mirrored-anims-2025-rig-retargeting]] — analytic template rig inversion for retargeting; cites Holden as foundational prior work
- [[papers/hahn-2012-rig-space-physics]] — rig Jacobian used in physics projection
- [[concepts/rig-inversion]]
- [[authors/holden-daniel]]

## External Implementation
Filmakademie Baden-Württemberg student project (Technical Directing course, 2023) implemented the IRM tool in Maya using PyTorch GPR, following this paper's approach. Video: https://www.youtube.com/watch?v=N5rSmC9WJlQ (source: `raw/assets/Inverse Rig Mapping - Technical Directing - Animationsinstitut Filmakademie BW.md`)
