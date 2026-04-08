---
title: "Learning Neural Blend Shapes for Character Animation"
authors: [Li, Peizhuo; Aberman, Kfir; Hanocka, Rana; Liu, Libin; Sorkine-Hornung, Olga; Liu, Gengdai]
venue: ACM Transactions on Graphics (SIGGRAPH 2021)
year: 2021
tags: [skinning, neural, blendshapes, correctives, rig-generation, lbs]
source: raw/papers/neural-blend-shapes-camera-ready.pdf
---

## Summary
Introduces a neural method that learns pose-dependent corrective blend shapes and skinning weights jointly from a mesh dataset — without any manual rig or sculpting. Given an unrigged character mesh and a set of reference poses, the network simultaneously predicts a skeleton, LBS skinning weights, and a small set of "neural blend shapes" that model nonlinear pose-dependent deformations. The result is a compact, real-time–capable deformation model compatible with standard LBS pipelines.

## Problem
Production-quality pose-space correctives (PSD) require manual sculpting by skilled artists for every pose, making them expensive and character-specific. Neural skinning methods (e.g. Bailey et al. 2018) improve quality but sacrifice artist controllability and LBS compatibility. An automatic method that learns high-quality pose-dependent deformations without manual sculpting — while staying compatible with standard skeleton rigs — is needed.

## Method
The model is structured in two branches over the same graph-encoded mesh $(V, F)$:

**Rigging branch** — learns a standard LBS rig:
- Encodes the mesh into per-vertex features $V_0 \in \mathbb{R}^{|V| \times D}$.
- Predicts joint offsets $O \in \mathbb{R}^{|J| \times 3}$ (skeleton fitting).
- Predicts skinning weights $W \in \mathbb{R}^{|V| \times |J|}$.
- Applies LBS to produce the driven mesh:
```math
\tilde{V}_R = T_R \odot V, \quad T_R^i = \sum_j W_{ij} T_j \quad \text{(Eq. 2–3)}
```

**Blend shape branch** — learns $K$ neural corrective blend shapes:
- Input: $[V_0 \;\|\; W]$ (rigging features concatenated with weights).
- Outputs: $K$ blend shape displacement vectors $\{B_k\}_{k=1}^K$, $B_k \in \mathbb{R}^{|V| \times 3}$.
- Outputs: $K$ small MLP weight functions $\{U_k\}_{k=1}^K$, one per joint.
- Final posed vertex:
```math
\tilde{V} = V + \sum_{j=1}^{|J|} \sum_{k=1}^{K} U_k^j \cdot B_k \quad \text{(Eq. 5)}
```
where $U_k^j$ is the per-joint scalar weight for blend shape $k$, predicted by an MLP from joint rotation $R_j$.

**Training:** supervised on paired $(pose, mesh)$ data from a reference rig. Loss: $\mathcal{L}_v = \|\tilde{V} - V^*\|^2$ (Eq. 4). No manual sculpts required — the network discovers what blend shapes are needed.

**Key design choices:**
- Residual formulation: LBS provides the base; neural blend shapes correct nonlinear residuals.
- Joint-local weights $U_k^j$: each blend shape is weighted per joint, enabling sparse, localized activation.
- $K \ll |V|$: compact basis (e.g. $K=8$) keeps evaluation fast.
- Compatible with any skeleton — the rigging branch fits the skeleton automatically.

## Key Results
- Outperforms Bailey et al. 2018 on nonlinear deformation accuracy.
- More realistic than standard LBS at elbows, shoulders, and wrists.
- No manual rig or sculpts: fully automated from mesh data.
- Compact: K=8 blend shapes sufficient for typical humanoid characters.
- Real-time capable: blend shape evaluation is a small MLP + weighted sum.

## Limitations
- Requires a dataset of paired (pose, mesh) samples from a reference rig or simulation.
- Per-character training: a new network must be trained per character.
- Neural blend shapes are not directly interpretable or artist-editable (unlike PSD sculpts).
- Performance at extreme out-of-distribution poses depends on training coverage.

## Connections
- [[papers/bailey-2018-deep-deformation]] — same residual-over-LBS formulation; neural blend shapes replace the dense MLP with a structured blend shape basis
- [[papers/lewis-2000-psd]] — pose-space deformation is the manual alternative; this automates the blend shape discovery
- [[papers/loper-2015-smpl]] — SMPL's learned blend shapes are a statistical version of the same idea; this method is character-specific
- [[papers/neumann-2013-sparse-deformation]] — learns localized blend shapes from data; similar problem, different approach (dictionary learning vs neural)
- [[papers/jacobson-2011-bbw]] — automatic skinning weights; neural blend shapes complement automatic BBW weights
- [[concepts/blendshapes]] — the discovered $B_k$ are learned corrective blendshapes
- [[concepts/linear-blend-skinning]] — the LBS base deformation on which correctives are applied
- [[concepts/pose-space-deformation]] — this is the automated, neural version of PSD
- [[authors/sorkine-olga]]
- [[authors/aberman-kfir]]

## Implementation Notes
The forward pass at runtime:
```python
# Assume network has been trained and we have:
#   B: (K, N, 3)  — blend shape displacements
#   mlp_U: list of K MLPs, each (|J| → scalar)
#   W: (N, |J|)   — skinning weights (from rigging branch, fixed)

# Given pose rotations R_joints (|J|, 3, 3):
U = torch.stack([mlp(R_joints) for mlp in mlp_U], dim=0)  # (K, |J|)
blend_disp = torch.einsum('kj,knc->nc', U, B)             # (N, 3)
V_lbs = lbs(V_rest, W, joint_transforms)                  # standard LBS
V_final = V_lbs + blend_disp
```

In Houdini: precompute $B_k$ as stored point attribute delta arrays; evaluate $U_k$ in Python (ONNX); sum in VEX.
