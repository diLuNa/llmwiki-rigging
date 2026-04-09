---
title: "Analysis and Synthesis of Facial Image Sequences Using Physical and Anatomical Models"
authors: [Terzopoulos, Demetri; Waters, Keith]
venue: IEEE Transactions on Pattern Analysis and Machine Intelligence 15(6)
year: 1993
tags: [muscles, digital-human, facial-capture]
source: knowledge
---

## Summary
Extends the 1990 physically-based face model to a complete **analysis-synthesis** framework. The analysis module tracks facial feature points in image sequences and inverts the physical model to solve for muscle activation parameters. The recovered activations drive the synthesis module to reproduce or retarget the captured expression to a different identity's model. This is the conceptual origin of physics-model-based performance capture.

## Problem
The 1990 Terzopoulos-Waters model was purely forward (synthesis only). No method existed for automatically recovering muscle activations from observed facial images — required for performance capture and expression transfer between subjects.

## Method
**Analysis pipeline:**
1. Track 2D facial feature points (lips, eyes, nose bridge) across video frames using optical flow or template matching
2. Project tracked points into 3D via the shape model
3. Optimize muscle activation parameters $\mathbf{a} \in [0,1]^M$ to minimize reprojection error:
```math
\min_{\mathbf{a}} \sum_i \| \mathbf{x}_i - \hat{\mathbf{x}}_i(\mathbf{a}) \|^2
```
where $\hat{\mathbf{x}}_i(\mathbf{a})$ is the predicted 2D location of point $i$ given activations $\mathbf{a}$.
4. Solve via gradient descent or Newton methods; Jacobian computed by differentiating the spring simulation.

**Synthesis pipeline:** Feed recovered activations $\mathbf{a}$ into the physical simulation to generate full-face mesh deformation. Can replace identity geometry to retarget expression.

## Key Results
First model-based facial performance capture from monocular video. Demonstrated expression transfer: activations fitted from one subject, applied to a different identity's model. Validated against electromyography (EMG) muscle measurements for some subjects. IEEE TPAMI 15(6), 1993.

## Limitations
Requires accurate tracking of feature points (failure in hair occlusion, lighting changes). Optimization is non-convex; requires good initialization near neutral. Sensitivity to the physical model's parameter calibration. Does not model asymmetric muscle activations between left/right.

## Connections
- [[papers/terzopoulos-1990-physically-based-face]] — direct predecessor (synthesis model used here)
- [[papers/waters-1987-muscle-model]] — muscle actuators in the physical model
- [[papers/bao-2019-face-capture-muscles]] — modern equivalent: muscle activation space as capture parameterization
- [[papers/cong-2015-anatomy-pipeline]] — ILM: anatomy model from MRI + physics inversion for capture
- [[concepts/muscles]] — analysis-synthesis framework for muscle-based capture
- [[concepts/rig-inversion]] — this is the original rig inversion for a physical face model
- [[authors/terzopoulos-demetri]]
- [[authors/waters-keith]]

## Implementation Notes
The key insight is differentiating through the spring simulation to get $\partial \hat{\mathbf{x}}_i / \partial \mathbf{a}_j$ — the Jacobian mapping activation changes to predicted point positions. For a linear spring system this Jacobian is analytically tractable. In practice the Jacobian is sparse (each muscle affects only vertices in its influence zone).
