---
title: "Learning a Model of Facial Shape and Expression from 4D Scans"
authors: [Li, Tianye; Bolkart, Timo; Black, Michael J.; Li, Hao; Romero, Javier]
venue: ACM Transactions on Graphics (SIGGRAPH Asia 2017)
year: 2017
tags: [blendshapes, correctives, pose-space, rig-generation, body-model, digital-human]
source: raw/papers/flame_paper.pdf
---

## Summary
FLAME (Faces Learned with an Articulated Model and Expressions) is a statistical 3D face model trained on 33,000 scans from 3800 subjects and 4D expression sequences. It represents face shape, head pose, jaw articulation, and facial expressions in a single unified parametric model compatible with standard LBS-based rigs. FLAME's pose-corrective formulation is the basis adopted verbatim by Animatomy.

## Problem
Existing 3D morphable models (3DMM, Basel Face Model) separate shape from expression and do not model pose-dependent skin deformation or jaw articulation. Fitting these models to dynamic sequences is difficult, and the resulting models are not directly usable in production rigs.

## Method
FLAME defines a function:
```math
M(\beta, \theta, \psi) = W\!\left(\bar{T} + B_S(\beta) + B_P(\theta) + B_E(\psi),\; J(\beta),\; \theta,\; \mathcal{W}\right)
```
where:
- $\bar{T} \in \mathbb{R}^{3N}$ — mean face template (5023 vertices)
- $B_S(\beta) = \mathbf{S}\beta$ — shape blend shapes ($|\beta|=300$ PCA directions)
- $B_P(\theta) = \sum_{n=1}^{9K}(R_n(\theta) - R_n(\theta^*))\mathbf{P}_n$ — pose correctives for K=4 joints (global rotation, neck, jaw, left/right eyeballs); same formulation as SMPL
- $B_E(\psi) = \mathbf{E}\psi$ — expression blend shapes ($|\psi|=100$ PCA directions learned from expression sequences)
- $J(\beta)$ — joint positions regressed from shaped template
- $\mathcal{W}$ — learned LBS blend weights

All parameters learned jointly from registered 4D scans.

**Training data:**
- Shape: 3800 subjects, registered to template
- Expressions: 4D video sequences of 12 subjects performing expressions
- Pose correctives: learned from head-pose variation in sequences

## Key Results
- Compactly models shape (300), pose (15 DOF for face joints), and expression (100) variation.
- Jaw articulation with pose correctives correctly handles skin folding at chin and cheeks.
- Fits accurately to 2D landmark detections and 3D reconstructions.
- Foundation for SMPL-X (whole body with face), FaceWarehouse-style models, and many neural face reconstruction systems.
- Pose corrective formulation ($B_P$) directly adopted by Choi et al. (Animatomy) for production facial rigs.

## Limitations
- Linear expression space; can't represent extreme non-linear expressions or contact deformation.
- 5023 vertices — coarser than production face meshes; used as a statistical prior, not as a production mesh.
- Texture not included in the base FLAME model (separate FLAME-based texture models exist).

## Connections
- [[papers/loper-2015-smpl]] — FLAME applies the SMPL architecture to the face; pose correctives are identical
- [[papers/choi-2022-animatomy]] — Animatomy uses FLAME's pose corrective formulation (§5.2)
- [[papers/lewis-2000-psd]] — expression blend shapes $B_E$ are learned pose-space correctives
- [[papers/bagautdinov-2018-facial-cvae]] — VAE-based alternative for face shape; compared against FLAME
- [[concepts/blendshapes]] — $B_E$ is a PCA blendshape basis for expressions; $B_S$ for shape
- [[concepts/pose-space-deformation]] — $B_P(\theta)$ are learned pose-space deformations for jaw/neck
- [[concepts/linear-blend-skinning]] — FLAME uses LBS for articulation

## Implementation Notes
FLAME is available via MPI-IS (requires license agreement). Python forward pass:
```python
# Given beta (300,), theta (15,), psi (100,)
v_shaped = T_bar + S @ beta                             # shape
J        = J_regressor @ v_shaped                      # joints
R        = batch_rodrigues(theta)                       # joint rotations
v_posed  = v_shaped + P @ (R - R_rest).flatten()       # pose correctives
v_expr   = v_posed  + E @ psi                          # expression
v_final  = lbs(v_expr, J, theta, W)                    # LBS skinning
```
In Houdini: the expression layer `E @ psi` maps cleanly to blendshape-additive workflow (each column of E is a delta blendshape). The 100 expression components can be driven by FACS AUs via a learned mapping matrix.
