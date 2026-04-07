---
title: "SMPL: A Skinned Multi-Person Linear Model"
authors: [Loper, Matthew; Mahmood, Naureen; Romero, Javier; Pons-Moll, Gerard; Black, Michael J.]
venue: ACM Transactions on Graphics (SIGGRAPH Asia 2015)
year: 2015
tags: [skinning, lbs, blendshapes, pose-space, correctives, neural, body-model]
source: ~no local PDF~
---

## Summary
SMPL is a skinned vertex-based body model that accurately represents a wide variety of body shapes in natural human poses. It combines a shape PCA basis, SMPL-style pose-dependent blend shapes (learned linear correctives), and standard LBS — all learned from a large 3D scan database. SMPL is now the de facto standard parametric human body model for vision, animation, and generative research.

## Problem
Prior 3D morphable body models (Anguelov 2005 SCAPE) are not compatible with standard graphics pipelines: they use non-linear representations and are difficult to integrate into existing animation tools. A model that is simultaneously accurate, pose-dependent, and compatible with LBS-based rigs is needed.

## Method
The SMPL model defines a function $M(\beta, \theta)$ that maps shape parameters $\beta \in \mathbb{R}^{10}$ and pose parameters $\theta \in \mathbb{R}^{72}$ (24 joints × 3 axis-angle) to a posed mesh of 6890 vertices.

**Shape blend shapes:**
```math
B_S(\beta) = \sum_{n=1}^{|\beta|} \beta_n S_n
```
$S_n \in \mathbb{R}^{3N}$ are learned PCA directions from a corpus of registered body scans.

**Pose blend shapes** (linear correctives, learning joint-angle–dependent skin deformations):
```math
B_P(\theta) = \sum_{n=1}^{9K} (R_n(\theta) - R_n(\theta^*)) P_n
```
$R_n(\theta)$ are elements of the rotation matrices for each joint; $P_n \in \mathbb{R}^{3N}$ are learned blend shape directions. This is the same formulation later adopted by FLAME and Animatomy.

**Joint locations:**
$$J(\beta) = \mathcal{J}(\bar{T} + B_S(\beta))$$
Joint regressor $\mathcal{J}$ predicts joint positions from the shaped template.

**LBS skinning:**
$$M(\beta, \theta) = W(T_P(\beta, \theta), J(\beta), \theta, \mathcal{W})$$
where $T_P = \bar{T} + B_S(\beta) + B_P(\theta)$ and $\mathcal{W}$ are learned blend weights.

All parameters ($S_n$, $P_n$, $\mathcal{J}$, $\mathcal{W}$) are learned jointly from registered mesh sequences.

## Key Results
- Matches body shapes across gender, age, BMI with a compact 10-dim shape space.
- Pose-dependent deformations correctly model muscle bulging and skin deformation at joints.
- Compatible with standard DCC tools (Maya, Blender, Houdini) as a standard rigged mesh.
- Foundation for FLAME (face), MANO (hand), SMPL-X (full body with face+hands).

## Limitations
- LBS artifacts remain at extreme poses (mitigated but not eliminated by pose blend shapes).
- 10 shape components can't capture all individual variation.
- Clothing and hair not modeled; topology is fixed at 6890 vertices.

## Connections
- [[papers/lewis-2000-psd]] — pose-space deformation; SMPL's pose blend shapes are a learned version of PSD
- [[papers/jacobson-2011-bbw]] — LBS weight learning; SMPL learns skinning weights from data
- [[papers/li-2017-flame]] — FLAME applies the same architecture to the face
- [[concepts/linear-blend-skinning]] — SMPL evaluates LBS at runtime
- [[concepts/pose-space-deformation]] — pose blend shapes $B_P(\theta)$ are learned PSD correctives
- [[concepts/blendshapes]] — shape + expression basis shares the blendshape paradigm

## Implementation Notes
SMPL is available as a Python package (smplx library, MPI-IS). The core forward pass is:
```python
# Pytorch: given betas (B,10), thetas (B,72)
v_shaped = smpl.v_template + smpl.shapedirs @ betas      # + B_S
J = smpl.J_regressor @ v_shaped                          # joint positions
pose_feature = (R - I).flatten()                         # 9K-dim
v_posed = v_shaped + smpl.posedirs @ pose_feature        # + B_P
v_skinned = lbs(v_posed, J, thetas, smpl.lbs_weights)   # LBS
```
In Houdini: import as .obj + weight attributes; use the standard Bone Capture Biharmonic for weight matching, or load SMPL weights directly as point attributes.
