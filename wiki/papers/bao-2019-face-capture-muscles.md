---
title: "High-Fidelity Facial Capture Using Anatomical Muscles"
authors: [Bao, Michael R.; Cong, Matthew; Sifakis, Eftychios; Fedkiw, Ronald]
venue: CVPR 2019
year: 2019
tags: [muscles, facial-capture, simulation, digital-human]
source: raw/papers/bao-2019-face-capture-muscles.pdf
---

## Summary
Replaces blendshape weights as the capture parameter space with **muscle activation values** from the ILM anatomy simulation model. A convolutional encoder maps input video/image frames to muscle activation estimates; the activations then drive the FEM simulation to produce the captured expression. Introduces learned priors over muscle activation sequences to produce anatomically plausible, temporally smooth capture. CVPR 2019.

## Problem
Standard face capture solves for blendshape weights or 3DMM parameters from images — these have no direct anatomical meaning and can produce implausible combinations. Muscle activation space is anatomically grounded (bounded to $[0,1]$, with known biomechanical coupling between muscles) and naturally prevents unphysical expressions.

## Method
**System overview:**
1. **Input:** video sequence of subject's face
2. **CNN encoder:** ResNet-based image encoder → predicted muscle activations $\hat{\mathbf{a}} \in [0,1]^M$
3. **Anatomical prior:** learned prior over muscle activation sequences (temporal LSTM) ensures activations follow physiologically plausible patterns; co-activation probabilities modeled
4. **FEM forward model:** predicted activations fed into anatomy simulation → surface mesh deformation
5. **Loss:** photometric consistency (rendered mesh vs. input image) + anatomical prior regularization

**Co-activation prior:** some muscle pairs are rarely activated simultaneously (e.g., zygomaticus major and corrugator). Prior encodes these correlations as a learned Gaussian process in activation space.

**Temporal smoothing:** LSTM over activation sequence discourages unphysical rapid activation transients.

## Key Results
Demonstrated superior anatomical plausibility vs. blendshape-weight capture on the same footage. Muscle activations correlate with EMG measurements. Produces compelling expressions for challenging cases (extreme mouth opens, asymmetric expressions) where blendshape weights produce artifacts. CVPR 2019.

## Limitations
Requires the ILM anatomy model to be available per subject (expensive MRI pipeline). CNN encoder trained on synthetic rendered data — domain gap to real video. Quasistatic assumption: frame-by-frame independent solves, no temporal dynamics. Inference speed bottlenecked by FEM solve in the training loop.

## Connections
- [[papers/cong-2015-anatomy-pipeline]] — anatomy model that defines the muscle activation space
- [[papers/cong-2016-art-directed-blendshapes]] — alternative: capture blendshape weights then convert to simulation
- [[papers/sifakis-2005-anatomy-muscles]] — original muscle activation recovery from mocap markers
- [[papers/terzopoulos-1993-facial-analysis]] — conceptual origin: capture via model inversion
- [[concepts/muscles]] — muscle activation as capture parameter space
- [[concepts/rig-inversion]] — this is neural rig inversion in muscle activation space
- [[authors/cong-matthew]]
- [[authors/sifakis-eftychios]]
- [[authors/fedkiw-ronald]]
