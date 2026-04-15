---
title: "B-Spline Volumes (Free-Form Deformation)"
tags: [skinning, deformation, math, cage-deformation, simulation, muscles]
---

## Definition
A B-spline (or Bernstein) volume embeds a 3D region in a trivariate polynomial control lattice. Any point $\mathbf{P}$ inside the volume is expressed as a weighted sum of the lattice control points $\mathbf{P}_{ijk}$:

```math
\mathbf{P}(s,t,u) = \sum_{i=0}^{l} \sum_{j=0}^{m} \sum_{k=0}^{n} B_{i,p}(s)\, B_{j,q}(t)\, B_{k,r}(u)\, \mathbf{P}_{ijk}
```

where $(s,t,u) \in [0,1]^3$ are local coordinates within the volume, $B_{i,p}$ are B-spline (or Bernstein) basis functions of degree $p$, and the lattice has $(l+1) \times (m+1) \times (n+1)$ control points.

Moving control points $\mathbf{P}_{ijk}$ deforms the ambient space continuously and differentiably — embedded geometry (surface meshes, particles, other volumes) follows via evaluation of the same polynomial at their pre-computed local coordinates.

## Variants / Taxonomy

### Free-Form Deformation (FFD) — Bernstein / B-spline lattice
[[papers/sederberg-1986-ffd]] (SIGGRAPH 1986) — the foundational technique. Uses a trivariate Bernstein polynomial lattice. A user positions the lattice around an object, moves control points, and the object deforms smoothly. Degree is fixed ($p=q=r$ typically 3 for cubic). Has no local support beyond the whole lattice cell.

Generalized to B-spline volumes shortly after, providing local support (moving one control point affects only nearby regions) and allowing non-uniform knot vectors for varying detail density.

### B-Spline Solid as Muscle Primitive
[[papers/ng-thow-hing-1997-bspline-solid]] — volumetric muscle shape primitives parameterized as trivariate B-spline solids. The 3D parameterization $(s,t,u)$ allows:
- Defining internal fibre bundle directions along iso-parametric curves
- Data-fitting from medical contour data or profile curves
- Applying spring-mass dynamics to the control lattice for deformable animation
- Volume preservation through constraints on the Jacobian determinant of the deformation

### Differentiable / Learnable FFD
[[papers/kurenkov-2017-deformnet]] — implements FFD as a differentiable neural layer. The Bernstein trivariate polynomial is a smooth function of control points; gradients flow through it during backpropagation. A CNN predicts control point displacements from an image; the FFD layer applies them to a template shape for 3D reconstruction.

[[papers/jack-2018-learning-ffd]] — similar differentiable FFD approach; learns free-form deformations of a template mesh for single-image 3D object reconstruction.

Key insight: because B-spline/Bernstein evaluation is a linear map from control points to embedded point positions, the Jacobian $\partial \mathbf{P} / \partial \mathbf{P}_{ijk} = B_{i,p}(s) B_{j,q}(t) B_{k,r}(u)$ is analytically computable — making FFD one of the earliest naturally differentiable deformation representations.

### Spline Deformation Fields for Dynamic Scenes
[[papers/song-2025-spline-deformation-field]] (SIGGRAPH 2025) — models dense point trajectories over time using splines, where the number of knots controls degrees of freedom. Analytic velocity/acceleration from spline derivatives; avoids LBS-style deformation artifacts. Low-rank time-variant spatial encoding replaces heuristic spatiotemporal coupling.

### Hexahedral FEM Lattices (related)
Flesh simulation (e.g., [[papers/smith-2018-stable-neohookean]]) drives hexahedral FEM lattices from skeletal bones. These are volumetric in the same spirit but discretized by FEM rather than B-spline basis functions — trilinear interpolation (degree 1 hexahedra) rather than higher-degree B-splines.

## Mathematical Details

### Local Coordinate Computation
For a point $\mathbf{X}$ in world space, its local coordinates $(s,t,u)$ are found by inverting the reference-state mapping — typically solved once offline by Newton iteration or analytic inversion.

### Jacobian and Volume Preservation
The deformation gradient at $(s,t,u)$:

```math
\mathbf{F}(s,t,u) = \frac{\partial \mathbf{P}}{\partial \mathbf{X}} = \sum_{ijk} \nabla_{s,t,u}(B_{i}B_{j}B_{k}) \otimes \mathbf{P}_{ijk}
```

Volume preservation: $\det(\mathbf{F}) = 1$ everywhere. Enforced as a constraint or through incompressible FEM energies.

### Muscle Fibre Orientation (Ng-Thow-Hing)
The $u$-direction parametric lines define fibre bundles. Fibre direction at any point = $\partial \mathbf{P}/\partial u$ (normalized). Contractile force is applied along this direction.

## Key Papers
- [[papers/sederberg-1986-ffd]] — foundational FFD; Bernstein trivariate volume; SIGGRAPH 1986
- [[papers/ng-thow-hing-1997-bspline-solid]] — B-spline solid as muscle primitive; spring-mass dynamics; fibre orientation; CAS 1997
- [[papers/kurenkov-2017-deformnet]] — differentiable FFD layer; CNN predicts control point displacements; WACV 2018
- [[papers/jack-2018-learning-ffd]] — learning FFD for single-image 3D reconstruction; ACCV 2018
- [[papers/song-2025-spline-deformation-field]] — spline deformation field for dynamic scenes; SIGGRAPH 2025

## Connections
- [[concepts/cage-deformation]] — cages are a related paradigm: a coarse polyhedral cage instead of a regular lattice; same "embed object, deform container" idea
- [[concepts/skinning]] — alternative to skeleton-driven skinning; the volume can be driven by control points rather than bone transforms
- [[concepts/muscles]] — B-spline solids are used as muscle shape primitives in anatomical modeling
- [[concepts/simulation]] — FEM flesh simulations use volumetric hex/tet discretizations that share the "drive surface via embedded volume" concept
- [[techniques/inverse-rig-mapping]] — a B-spline volume driven by a skeleton can serve as the rig function $F(\beta)$ being inverted

## Implementations

| Tool | Language | Type | URL |
|------|----------|------|-----|
| **PyGeM** | Python | FFD + RBF + IDW, CAD/mesh morphing | https://github.com/mathLab/PyGeM |
| **FFD.jl** | Julia | B-spline FFD for aerodynamic shape optimization | https://github.com/OptimalDesignLab/FFD.jl |
| **DeformNet** | Python/PyTorch | Differentiable FFD layer (Bernstein) | https://github.com/deformnet-site/DeformNet |
| **CGAL** | C++ | Trivariate B-spline volume support | https://doc.cgal.org |

### PyGeM Quick Usage
```python
from pygem import FFD

# Create FFD box around mesh vertices
ffd = FFD([2, 2, 2])              # 2×2×2 control lattice (8 points)
ffd.read_parameters('params.prm') # load control point displacements

# Deform mesh vertices
deformed = ffd(mesh.vertices)
```

### Differentiable FFD in PyTorch
```python
import torch
from torch import nn

class BernsteinFFD(nn.Module):
    """Differentiable trivariate Bernstein FFD layer."""
    def __init__(self, l=4, m=4, n=4):
        super().__init__()
        self.l, self.m, self.n = l, m, n
        # Learnable control point displacements
        self.dP = nn.Parameter(torch.zeros(l+1, m+1, n+1, 3))
    
    def bernstein(self, n, i, t):
        """B_{i,n}(t) = C(n,i) * t^i * (1-t)^(n-i)"""
        from math import comb
        return comb(n, i) * (t ** i) * ((1-t) ** (n-i))
    
    def forward(self, points_stu):
        """
        points_stu: (N, 3) local coordinates in [0,1]^3
        returns: (N, 3) world-space displacements
        """
        s, t, u = points_stu[:, 0], points_stu[:, 1], points_stu[:, 2]
        disp = torch.zeros_like(points_stu)
        for i in range(self.l+1):
            Bi = self.bernstein(self.l, i, s)
            for j in range(self.m+1):
                Bj = self.bernstein(self.m, j, t)
                for k in range(self.n+1):
                    Bk = self.bernstein(self.n, k, u)
                    w = (Bi * Bj * Bk).unsqueeze(-1)  # (N,1)
                    disp += w * self.dP[i, j, k]
        return disp
```

## Production Workflow (Character Rigging Context)

B-spline volume deformers appear in production in several roles:

1. **FFD cage over a region**: Wrap a control lattice around a shoulder, knee, or face region. Skeleton drives control points via weighted rig connections; the lattice deforms the mesh smoothly in that region. Advantage over direct skinning: avoids candy-wrapper at twist.

2. **Muscle volume**: Each muscle is a B-spline solid parameterized by anatomical data. Contraction is modeled by changing control points in the $u$-direction (along fibre). The outer surface of the solid is rendered or transferred to the skin mesh.

3. **FEM pre-computation**: Hex lattice driven by skeleton; simulation computes equilibrium deformation; result transferred to skin mesh as corrective or as direct deform. Used in [[papers/smith-2018-stable-neohookean]] for Pixar characters.

4. **Learned deformation**: Train a network to predict control point displacements from pose parameters. At runtime, network runs once; FFD evaluation is analytic. Intermediate between direct neural displacement and classical rig.

## Gotchas

- **Local coordinate inversion**: Finding $(s,t,u)$ for a mesh vertex requires nonlinear solve. Do once offline, store as attributes.
- **Degree vs. resolution**: Higher polynomial degree = smoother but more globally coupled. More control points = more local but more DOF to manage.
- **Volume preservation**: Standard B-spline FFD does not preserve volume automatically. Add a volumetric FEM energy or explicit $\det(F)=1$ penalty.
- **Boundary conditions**: Points outside the control lattice are typically not deformed (or extrapolated linearly). Important for partial coverage rigs.

## Notes
FFD was the dominant secondary deformer paradigm before cage deformation methods (harmonic, Green, Somigliana) displaced it. It remains in use for:
- Art-directability (control lattice is intuitive to move)
- Local deformation zones (partial coverage)
- Driven lattices (rig parameters → control points → mesh)
