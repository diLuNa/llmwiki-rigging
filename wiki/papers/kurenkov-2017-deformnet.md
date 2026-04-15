---
title: "DeformNet: Free-Form Deformation Network for 3D Shape Reconstruction from a Single Image"
authors: [Kurenkov, Andrey; Ji, Jingwei; Garg, Animesh; Mehta, Viraj; Gwak, JunYoung; Choy, Christopher; Savarese, Silvio]
venue: WACV 2018
year: 2018
tags: [neural, deformation, cage-deformation, rig-generation, math]
source: https://arxiv.org/abs/1708.04672
---

## Summary
Introduces a **differentiable FFD layer** as a building block for 3D reconstruction neural networks. A CNN encodes an input image and predicts displacements of a Bernstein trivariate control lattice; the FFD layer applies those displacements to a template shape to produce the reconstructed 3D output. The FFD layer is naturally differentiable with respect to control point positions, enabling end-to-end training on shape reconstruction losses (Chamfer distance, IoU). First use of learnable control point prediction for 3D deformation in a neural architecture.

## Problem
3D reconstruction from a single image can operate on voxel grids, point clouds, or mesh templates. Direct vertex prediction scales poorly; voxel grids are memory-intensive; point clouds lack surface structure. Deforming a high-quality template via FFD provides: smooth deformations, resolution-independent output, compact parameterization (few control points instead of many vertices), and differentiability through the Bernstein evaluation.

## Method

### Architecture
```
Image → CNN encoder → Control point displacements ΔP ∈ ℝ^{(l+1)×(m+1)×(n+1)×3}
                     → FFD layer (fixed Bernstein basis + ΔP)
                     → Deformed template points
```

The template is a high-quality source shape from a database (retrieved by nearest-neighbor matching).

### Differentiable FFD Layer
The deformed position of template point $\mathbf{X}$ with local coordinates $(s,t,u)$ is:

```math
\mathbf{P}_{def}(s,t,u) = \mathbf{P}_{ref}(s,t,u) + \sum_{i,j,k} B_i^l(s)\, B_j^m(t)\, B_k^n(u)\, \Delta\mathbf{P}_{ijk}
```

Because the Bernstein basis values $B_i^l(s)$ are **fixed** for a given template shape (computed once from its local coordinates), the deformed position is a **linear function of $\Delta\mathbf{P}$**. Gradients flow through the FFD layer analytically:

```
∂P_def / ∂ΔP_{ijk} = B_i^l(s) · B_j^m(t) · B_k^n(u)  (scalar)
```

This makes the entire pipeline differentiable end-to-end.

### Loss Functions
- **Point-cloud loss**: Chamfer distance between predicted and ground-truth point clouds
- **Earth-Mover's Distance**: For more uniformly distributed reconstructions
- Pretrained on ShapeNet categories

## Key Results
- Quantitatively matches or outperforms state-of-the-art 3D reconstruction methods on ShapeNet
- The FFD layer provides smooth, plausible deformations that point-cloud or voxel methods cannot guarantee
- Template retrieval step allows the system to benefit from high-quality 3D shape databases

## Limitations
- Reconstruction quality bounded by the template: shapes very different from any template in the database will be poorly reconstructed
- Bernstein basis has global support within the lattice — any control point movement affects the entire shape
- No explicit surface correspondence between template and target
- The FFD layer is a passive deformation module; the CNN must learn to produce physically plausible control point displacements without any geometric prior

## Connections
- [[papers/sederberg-1986-ffd]] — the FFD technique being made differentiable
- [[concepts/b-spline-volumes]] — technical foundation of the FFD layer
- [[papers/jack-2018-learning-ffd]] — concurrent differentiable FFD work for 3D reconstruction
- [[concepts/cage-deformation]] — FFD as a special case of cage deformation (regular lattice cage)

## Implementation Notes
- Project website: https://deformnet-site.github.io/DeformNet-website/
- The Bernstein basis matrix $\mathbf{B}$ (size: #template_points × #control_points_per_axis) is fixed per template and can be precomputed, making the FFD evaluation a simple matrix multiplication: `P_def = P_ref + B_s ⊗ B_t ⊗ B_u @ delta_P.reshape(-1, 3)`
- For B-spline variant (local support): replace Bernstein basis with B-spline basis; the evaluation is still linear in control points but sparse (most weights are zero for any given template point)

## Quotes
> "We present a differentiable layer for 3D data deformation [and] show that combining DeformNet with a FFD layer provides a powerful building block for deep learning on 3D data." (Abstract)
