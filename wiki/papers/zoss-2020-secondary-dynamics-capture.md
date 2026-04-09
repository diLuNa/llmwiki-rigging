---
title: "Empirical Capture of Secondary Dynamics from Single-View Video"
authors: [Zoss, Gaspard; Chandran, Prashanth; Gotardo, Paulo; Beeler, Thabo; Bradley, Derek]
venue: ACM Transactions on Graphics (SIGGRAPH 2020)
year: 2020
tags: [simulation, facial-capture, digital-human, secondary-motion]
source: raw/papers/zoss-2020-secondary-dynamics-capture.pdf
---

## Summary
Presents a method to **automatically capture secondary facial dynamics** (soft-tissue jiggle, lip flutter, cheek oscillation) from single-view video using an analysis-by-synthesis approach. A physics-based dynamics model (damped spring system) per face region is fitted to the residual motion between a tracked blendshape rig and the observed video. The fitted dynamics model can then be applied to any new animation on the same character, automatically adding secondary motion. Disney Research Zürich. SIGGRAPH 2020.

## Problem
Secondary dynamics (skin jiggle, lip/cheek bounce) are physically real but tedious for animators to add manually. Existing physics simulation approaches require setting stiffness/damping parameters per character, which requires expert calibration. A data-driven approach from real video could extract and re-apply these dynamics automatically.

## Method
**Analysis pipeline:**
1. Track face from single-view video → blendshape rig parameters (smooth, quasi-static tracking)
2. Compute residual: $\mathbf{r}(t) = \mathbf{x}_{video}(t) - \mathbf{x}_{rig}(t)$ — the part of the video motion not explained by the smooth rig
3. Model residual per-region as driven by a **damped mass-spring system**:
```math
m\ddot{x} + c\dot{x} + kx = f_{drive}(t)
```
where $f_{drive}$ is derived from the rig parameter velocity
4. Fit $(m, c, k)$ per region to minimize residual reconstruction error
5. Output: region-specific dynamic parameters $(m, c, k)$

**Synthesis pipeline:** Given new animation (different sequence on same character), compute rig parameter velocities → drive the fitted spring systems → add resulting secondary displacements to the rendered mesh.

## Key Results
Demonstrated on real subjects: captured jiggle parameters closely match ground-truth video dynamics. Secondary dynamics can be transferred to new animation sequences, including cases without video (new scripted sequences). Results are artist-adjustable by modifying $(m, c, k)$ parameters. SIGGRAPH 2020.

## Limitations
Per-region damped spring is a simplified dynamics model — cannot capture the full coupled nonlinear tissue dynamics. Single-view video limits depth recovery of secondary motion. Fitted parameters are subject-specific and not transferable to different characters. No modeling of contact-driven secondary effects (e.g., jaw impact on cheek).

## Connections
- [[papers/bradley-2017-blendshape-physics]] — earlier Disney Research work: physics on top of blendshapes (quasistatic, not dynamic)
- [[papers/chandran-2024-anatomically-constrained-face]] — same Disney Research group; implicit physical face model
- [[papers/yang-2023-implicit-physical-face]] — related Disney Research work
- [[papers/hahn-2013-rig-space-secondary]] — rig-space physics for secondary dynamics
- [[concepts/secondary-motion]] — empirical secondary dynamics capture
- [[concepts/muscles]] — context: secondary tissue dynamics is downstream of muscle activation
- [[authors/zoss-gaspard]]
- [[authors/chandran-prashanth]]
- [[authors/beeler-thabo]]
