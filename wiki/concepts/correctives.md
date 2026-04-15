---
title: "Corrective Shapes / Corrective Blendshapes"
tags: [correctives, blendshapes, pose-space, skinning]
---

## Definition
Corrective shapes (also called corrective blendshapes or delta shapes) are mesh offsets added on top of a base deformation to fix artifacts that the base system cannot represent. In character rigging, the base is typically LBS or DQS; correctives add pose-dependent deltas that activate based on joint angles, blendshape weights, or other rig parameters.

```
v_final = v_lbs + Σᵢ w_i(β) · Δᵢ
```

where $\Delta_i$ is a sculpted vertex offset and $w_i(\beta)$ is a weight driven by rig controls.

## Variants / Taxonomy

### By trigger type
- **Pose-space deformation (PSD)** [[papers/lewis-2000-psd]]: corrective weight is a function of joint rotation; interpolates sculpted targets across pose space via RBF or local regression.
- **Blendshape correctives**: weight is a product of primary blendshape weights ($w_i w_j$ for pairwise, $w_i w_j w_k$ for triple, etc.). Used heavily in facial rigs — see quartic blendshape models in [[papers/rackovic-2023-highfidelity-inverse-rig]].
- **Delta mush** [[techniques/dem-bones]]: smooth-then-difference; no explicit sculpt, computed from mesh data.
- **ML deformer correctives** [[techniques/ml-deformer]]: neural network residuals on top of LBS, trained from simulation or artist sculpts.

### By model order
- **Linear / additive**: single shape active at one extreme pose. Simplest; limited to isolated joint poses.
- **Pairwise (quadratic)**: corrective active when two controls are simultaneously nonzero, e.g., $w_i w_j$. Captures interactions missed by independent shapes.
- **Triple (cubic)** and **Quartic**: higher-order interactions; necessary for realistic facial muscle coupling. Enumeration grows combinatorially — production rigs use sparse selection of "important" corrective pairs/triples.

### By authoring method
- **Hand-sculpted**: artist sculpts the corrective mesh at the target pose, delta extracted automatically.
- **Simulation-baked**: run cloth/muscle/FEM sim in the target pose, extract vertex delta vs. LBS output.
- **Learned residuals**: neural network trained to predict vertex offsets from pose (ML deformer / neural blend shapes approach).

## Key Papers
- [[papers/lewis-2000-psd]] — pose-space deformation; foundational work on sculpted correctives driven by joint angles (SIGGRAPH 2000)
- [[papers/lewis-2014-blendshape-star]] — STAR survey covering corrective blendshape taxonomy and FACS-driven facial systems (EG 2014)
- [[papers/neumann-2013-sparse-deformation]] — sparse localized deformation components; learns minimal corrective basis from motion data (SIGGRAPH Asia 2013)
- [[papers/raman-2022-mesh-tension-wrinkles]] — mesh-tension driven correctives for dynamic wrinkle expressions (CVPR 2022)
- [[papers/rackovic-2023-highfidelity-inverse-rig]] — inverse rig over quartic corrective blendshape model; coordinate descent solver
- [[papers/rackovic-2023-accurate-interpretable-inverse-rig]] — SQP/MM solvers for quadratic corrective inversion; up to 45% RMSE gain
- [[papers/an-2024-refined-inverse-rigging]] — temporal-smooth inverse rig over quartic correctives; MetaHuman 80+400 model

## Connections
- [[concepts/blendshapes]] — correctives are a subset of the blendshape system
- [[concepts/pose-space-deformation]] — the driving framework for non-facial correctives
- [[concepts/linear-blend-skinning]] — correctives compensate for LBS candy-wrapper and volume-loss artifacts
- [[concepts/wrinkle-systems]] — wrinkles are typically corrective shapes triggered by tension or pose

## Notes
- **Candy-wrapper artifact**: LBS collapses volume at highly-twisted joints (forearm, shoulder); corrective blendshapes or DQS are the primary fixes.
- **Combinatorial explosion**: a rig with 80 base blendshapes has $\binom{80}{2} = 3160$ possible pairwise correctives and $\binom{80}{3} \approx 82,000$ triple correctives. Production rigs select only a sparse subset based on perceptual importance — typically 400–600 corrective terms for a full head rig.
- **Inversion challenge**: the quadratic/quartic coupling of corrective weights makes blendshape rig inversion (finding weights from a target mesh) a non-convex problem. See [[concepts/rig-inversion]] for the taxonomy of solvers.
