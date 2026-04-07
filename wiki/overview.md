# Rigging Research — Overview

*High-level synthesis of the field. Updated as new papers are ingested.*

---

## The Core Problem

Character deformation — making a mesh follow a skeleton convincingly — is a deceptively hard problem. The naive solution (Linear Blend Skinning) is fast and universal but produces well-known artifacts: candy-wrapper twisting at joints, volume collapse at extreme poses, and an inability to reproduce the complex secondary shapes of real anatomy. Decades of research have attacked these problems from multiple angles.

## Major Research Threads

### 1. Better Skinning Algorithms
The goal is a deformation function that's fast, artifact-free, and artist-friendly. The trajectory goes:

- **LBS** (1980s–) — fast, ubiquitous, wrong. Blends transformation matrices linearly; collapses volume.
- **DQS** (Kavan et al. 2007) — blends dual quaternions instead of matrices. Eliminates candy-wrapper, but introduces "bulging" artifacts at certain poses.
- **Implicit / volumetric skinning** — drives deformation by implicit fields; better volume preservation but higher cost.
- **Neural skinning** — learn deformation from data; impressive quality but opaque and hard to art-direct.

### 2. Corrective Shapes (Pose-Space Deformation)
Skinning alone can't reproduce anatomical complexity. The solution: add sculptor-authored delta meshes that activate as a function of pose. Lewis et al. 2000 (*Pose Space Deformation*) formalized this. The challenges are: how to interpolate correctives across pose space, how to transfer sculpts between poses (de Goes et al. 2020), and how to normalize blendshape weights for predictable behavior (the UsdSkel non-normalized convention).

### 3. Geometric Processing Tools
Supporting both threads is a body of geometric math:
- **Laplacian / bi-Laplacian smoothing** — relaxation operators for correcting sculpts after transfer.
- **Bounded Biharmonic Weights** (Jacobson et al. 2011) — computing smooth, bounded skinning weights from cage or skeleton.
- **Cotangent Laplacian** — the geometrically correct discrete version of the Laplacian.

### 4. Pipeline / Schema (USD)
As productions move to USD, rigging data (skeletons, weights, blendshapes) must be expressed in UsdSkel. This introduces specific schema conventions — particularly around blendshape weight normalization — that interact with the algorithmic choices above.

---

## Open Questions (as of initialization)

- How do neural deformation methods compose with traditional corrective workflows?
- What's the right architecture for USD-native blendshape pipelines in Houdini Solaris?
- Can VEX implementations of geometric operators (Laplacian, BBW approximations) match offline solver quality for production use?

---

## Key Papers by Thread

| Thread | Landmark Papers |
|--------|----------------|
| Skinning | [[papers/kavan-2007-dqs]], LBS (implicit, historical) |
| Correctives | [[papers/lewis-2000-psd]], [[papers/degoes-2020-sculpt]] |
| Geometry | [[papers/jacobson-2011-bbw]] |
| Pipeline | (to be added) |

