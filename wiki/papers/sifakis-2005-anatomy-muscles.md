---
title: "Automatic Determination of Facial Muscle Activations from Sparse Motion Capture Marker Data"
authors: [Sifakis, Eftychios; Neverov, Igor; Fedkiw, Ronald]
venue: SIGGRAPH 2005
year: 2005
tags: [muscles, facial-capture, simulation, digital-human]
source: knowledge
---

## Summary
Introduces the first production-quality physics-based face capture system: given sparse motion capture markers on a subject's face, automatically solve for the **muscle activation parameters** that, when fed into a quasistatic FEM flesh simulation, reproduce the observed marker positions. This closes the loop between physical face simulation (Teran et al. 2005) and performance capture, enabling face animation driven by anatomically grounded muscle activations. SIGGRAPH 2005.

## Problem
Prior performance capture worked directly in marker or blendshape space. Muscle activation space (physiologically grounded, compact, anatomically interpretable) had never been used as the capture parameter space. No method existed to solve the inverse problem: given observed surface deformations, recover the underlying muscle activations in a volumetric FEM face model.

## Method
**Anatomy model construction:**
1. MRI scan of subject → volumetric tetrahedral mesh
2. Segment MRI into tissue types: skin, fat, muscle, bone
3. Identify muscle fiber directions from MRI texture/segmentation
4. Assign Neo-Hookean material properties per tissue type; transversely isotropic for muscle fibers

**FEM simulation:** quasistatic FEM (Teran et al. 2005). Muscle activation via transversely isotropic active fiber model:
```math
\Psi_{muscle}(\mathbf{F}, a) = \Psi_{passive}(\mathbf{F}) + a \cdot \Psi_{active}(\lambda_f)
```

**Inverse solve:** given marker positions $\mathbf{m}_i^{obs}$, solve:
```math
\min_{\mathbf{a} \geq 0} \sum_i \| \mathbf{m}_i(\mathbf{a}) - \mathbf{m}_i^{obs} \|^2 + \lambda R(\mathbf{a})
```
where $\mathbf{m}_i(\mathbf{a})$ is the simulated marker position under activations $\mathbf{a}$, and $R$ is a regularizer (sparsity or smoothness). Jacobian $\partial \mathbf{m}_i / \partial \mathbf{a}_j$ computed by differentiating through the quasistatic solve.

## Key Results
First successful muscle activation recovery from mocap markers using a volumetric FEM model. Demonstrated on real subjects with optical mocap. Recovered activations are anatomically plausible (validated against EMG). Enabled physics-based face animation retargeting. Foundation for ILM's production face pipeline (Cong et al. 2015–2017). SIGGRAPH 2005.

## Limitations
Requires per-subject MRI scan to build the anatomy model. MRI-based tissue segmentation requires expert manual review. Quasistatic solve per-iteration is expensive (inverse solve has many iterations). Number of markers (typically 50–100) constrains the number of independently recoverable activation parameters. Assumes quasistatic equilibrium — no dynamic effects.

## Connections
- [[papers/teran-2005-quasistatic-flesh]] — FEM simulation engine used for the forward model
- [[papers/cong-2015-anatomy-pipeline]] — scales this to full production pipeline at ILM
- [[papers/cong-2016-art-directed-blendshapes]] — replaces direct FEM with blendshape approximation driven by same muscle activations
- [[papers/bao-2019-face-capture-muscles]] — extends to video-based capture with learned priors
- [[papers/terzopoulos-1993-facial-analysis]] — conceptual predecessor: inverse problem for spring-mass model
- [[concepts/muscles]] — production-scale anatomy-based face capture
- [[concepts/rig-inversion]] — this is rig inversion where the "rig" is a physics simulation
- [[authors/sifakis-eftychios]]
- [[authors/fedkiw-ronald]]
