---
title: "FACEIT: Real-Time Performance-Driven Facial Animation with Blendshapes"
authors: [García Moreno-Figueroa, Jilliam; Stricker, Didier; (DFKI / MPI / HTWK)]
venue: ACM SIGGRAPH / Eurographics (year estimated ~2020–2022)
year: 2020
tags: [blendshapes, digital-human, neural, facial-capture, correctives]
source: raw/papers/FACEIT_DiazBarros_etal.pdf
---

## Summary
FACEIT is a real-time system for performance-driven facial animation that drives a blendshape rig from a live RGB video stream. It combines head pose estimation with expression transfer via energy minimization (NLLS) to solve for blendshape target weights frame-by-frame, enabling low-cost, passive (no markers) facial capture for virtual character animation.

## Problem
High-end facial capture requires marker-based setups or dedicated hardware cameras. Passive RGB approaches either lack robustness under varying lighting or require heavy compute. A real-time, marker-free system that drives production-quality blendshape rigs from a standard webcam is needed.

## Method
**Pipeline:**
1. **Neutral detection**: detect the performer's neutral expression and initial head pose from the first frames.
2. **Head pose estimation**: track head pose (6 DOF rigid transform) via landmark-based registration every frame.
3. **Expression transfer (energy minimization)**: given tracked 2D landmarks on the performer's face, solve for blendshape target weights $\alpha$ via:
$$\min_\alpha \sum_j \|M_j - \Pi(\sum_i \alpha_i V_i, \text{head\_pose})\|^2 + \mu \|\nabla\alpha\|^2$$
where $M_j$ are 2D landmark positions, $\Pi$ is the camera projection, $\sum_i \alpha_i V_i$ is the blendshape-driven 3D face model, and $\mu \|\nabla\alpha\|^2$ is a temporal smoothness regularizer.
4. **Asymmetric handling**: left/right face halves handled independently to capture asymmetric expressions.
5. **NLLS solve**: Non-Linear Least Squares (Levenberg-Marquardt) solves the optimization per-frame in real-time.

**Blendshape weight constraints:**
- $\alpha_i \in [0, 1]$ (normalized)
- $\sum_i \alpha_i = 1$ for replacement convention, or unconstrained for delta convention depending on rig

## Key Results
- Real-time performance on standard RGB camera input.
- Handles asymmetric expressions and head pose variation.
- Comparable quality to marker-based systems for a subset of expressions.

## Limitations
- Expression range limited by the blendshape space of the target rig.
- Occlusion (hand over face, glasses) degrades tracking.
- Camera-to-character mapping may require per-session calibration.

## Connections
- [[papers/lewis-2014-blendshape-star]] — STAR survey covering performance-driven animation as one application of blendshapes
- [[papers/choi-2022-animatomy]] — Animatomy's face system is the production rig that performance systems like FACEIT would drive
- [[papers/taylor-2017-speech-animation]] — audio-driven alternative to video-driven blendshape control
- [[papers/bermano-2013-facial-performance]] — earlier performance-based face enhancement in a shape space
- [[concepts/blendshapes]] — blendshape weights are the output of the FACEIT solve
- [[concepts/rig-inversion]] — FACEIT is a form of rig inversion from 2D landmarks

## Implementation Notes
The landmark-to-blendshape solve is the key component. In Python:
```python
from scipy.optimize import least_squares

def residuals(alpha, landmarks_2d, V_blendshapes, pose, K):
    V = sum(alpha[i] * V_blendshapes[i] for i in range(len(alpha)))
    proj = project(V, pose, K)          # 2D projection
    landmark_proj = proj[landmark_idx]  # select landmark vertices
    return (landmark_proj - landmarks_2d).flatten()

result = least_squares(residuals, x0=alpha_prev, bounds=(0, 1),
                       args=(landmarks, V_blend, pose, K_cam),
                       method='trf')   # TRF or LM
```
Real-time performance requires ~68 landmarks and ~50–100 blendshapes to keep the solve under 16ms.
