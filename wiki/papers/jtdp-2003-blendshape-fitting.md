---
title: "Blendshape Weight Estimation from Markers (Performance-Driven Facial Animation)"
authors: [(Authors uncertain — filename JTDP03, estimated 4 authors ~2003)]
venue: Unknown conference/journal (~2003)
year: 2003
tags: [blendshapes, correctives, facial-capture, rig-generation]
source: raw/papers/JTDP03.pdf
---

## Summary
An early paper on solving for blendshape weights from motion capture markers or 2D/3D landmark positions. Establishes the least-squares formulation for performance-driven facial animation: given a set of tracked marker positions $M_j$ and a blendshape rig $\{V_i\}$, find weights $\alpha_i$ minimizing the distance between the driven mesh and the tracked markers. Includes temporal regularization and constraint handling.

## Problem
Performance-driven facial animation requires mapping tracked facial landmarks/markers to rig control weights. With $n$ blendshapes and $m$ tracked markers, the system is generally overdetermined or underdetermined; a robust least-squares formulation with regularization is needed.

## Method
**Blendshape model (replacement convention):**
$$V(\alpha) = \sum_{i=1}^n \alpha_i V_i, \quad \sum \alpha_i = 1, \quad \alpha_i \geq 0$$

**Marker fitting objective:**
$$\min_\alpha \sum_j \|M_j - V_j(\alpha)\|^2 + \mu \|\nabla\alpha\|^2$$
where $M_j$ are measured marker positions, $V_j(\alpha)$ is the $j$-th marker vertex on the driven mesh, and $\mu \|\nabla\alpha\|^2$ is a temporal smoothness regularizer (finite differences on the weight trajectory).

**Facial similarity function** (for marker-to-vertex correspondence):
$$R(P_j) = \frac{\sum_{i=1}^m e^{-\|M_i - P_j\|} C_i}{\sum_{i=1}^m e^{-\|M_i - P_j\|}}$$
A softmax-weighted similarity used to establish correspondence between markers and mesh vertices.

**Solution strategy:**
- Constrained QP: $\sum \alpha_i = 1$, $\alpha_i \geq 0$
- Temporal regularization via finite differences $\|\nabla\alpha\|$ added to the QP objective
- Solved frame-by-frame with warm-start from previous frame solution

**Additional components noted in the paper:**
- Multi-scale approach: coarse-to-fine tracking
- Factorization of the blendshape matrix $B$ for efficient solve
- Marker subset selection for robustness to occlusion

## Limitations
- Limited technical detail available due to PDF text extraction quality.
- Author list uncertain; year estimated from filename.
- Works only within the blendshape space — cannot synthesize unseen expressions.

## Connections
- [[papers/lewis-2000-psd]] — PSD provides the theoretical basis; this paper applies it to live marker data
- [[papers/lewis-2014-blendshape-star]] — STAR survey covers performance-driven animation as a key application
- [[papers/faceit-diaz-barros]] — FACEIT is a modern video-based version of the same inverse problem
- [[papers/bermano-2013-facial-performance]] — related: performance enhancement using dynamic shape space analysis
- [[concepts/blendshapes]] — blendshape weight estimation is the core task
- [[concepts/rig-inversion]] — this is the prototypical rig inversion problem for faces
