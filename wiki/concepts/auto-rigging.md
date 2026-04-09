---
title: "Auto-Rigging"
tags: [rig-generation, neural, skinning, auto-rigging, blendshapes]
---

## Definition
Auto-rigging refers to methods that automatically generate animation rigs (skeletons, skinning weights, or blendshape sets) from a character mesh, without manual artist intervention. The problem has two main sub-domains:

1. **Skeleton + skinning weight prediction** — given a bare 3D mesh, predict joint locations, bone connectivity, and per-vertex LBS weights.
2. **Facial blendshape auto-rigging** — given a neutral face mesh, generate a set of FACS-compatible blendshape targets (or a forward model that evaluates them).

## Variants / Taxonomy

### Template-based
Transfer rigs from a known template mesh via dense correspondences (e.g., deformation transfer). Requires matching topology or robust correspondence estimation. Fast and predictable but constrained to characters close to the template.

### Learning-based skeleton + weights
- Train a network on a dataset of rigged characters
- Predict joints (clustering displaced vertices), connectivity (MST on bond probabilities), and skinning weights (geodesic-distance-weighted softmax)
- Generalises to diverse morphologies if training set is diverse
- Representative: **RigNet** (Xu et al. SIGGRAPH 2020)

### Learning-based facial blendshape rigging
- Predict per-vertex displacements for each FACS pose from a neutral mesh
- Can use DiffusionNet for triangulation-agnostic processing
- FACS latent space regularized to semantic action units; residual dimensions capture fine nonlinear details
- Representative: **NFR** (Qin et al. SIGGRAPH 2023), **RigAnyFace** (Ma et al. NeurIPS 2025)

## Key Papers
- [[papers/xu-2020-rignet]] — end-to-end neural skeleton + skinning from mesh; GMEdgeNet
- [[papers/qin-2023-nfr]] — neural facial rigging for arbitrary mesh topology; FACS-conditioned NJF decoder
- [[papers/ma-2025-riganyface]] — extends NFR with disconnected components + 2D-supervised scaling
- [[papers/canrig-2026-neural-face-rigging]] — cross-attention neural face rigging; variable local control
- [[papers/hou-2024-neutral-facial-rigging]] — bidirectional rig gen + recognition from limited data
- [[papers/ming-2024-mesh-blendshapes]] — FACS-compatible blendshapes from video via neural inverse rendering; directly production-importable
- [[papers/cha-2025-neural-face-skinning]] — mesh-agnostic FACS-compatible skinning via FACS region supervision; handles highly stylized non-human characters (EG 2025)
- [[papers/le-2012-ssdr]] — SSDR: auto-extracts LBS rig from an animation sequence (inverse direction)
- [[papers/holden-2015-inverse-rig]] — inverse rig mapping from pose to rig parameters (related problem)

## Connections
- [[concepts/linear-blend-skinning]] — LBS is the skinning model auto-rigging targets
- [[concepts/blendshapes]] — FACS blendshapes are the output of facial auto-rigging
- [[concepts/rig-inversion]] — the inverse problem: from poses back to rig parameters
- [[concepts/bounded-biharmonic-weights]] — BBW is the geometric baseline that neural methods outperform

## Notes
- The ModelsResource-RigNet dataset (2,703 rigged characters) is the main benchmark for skeleton auto-rigging.
- ICT FaceKit (USC Institute for Creative Technologies) provides synthetic FACS-labeled meshes used by NFR and RigAnyFace.
- Production rigs often have far more detail than auto-rigs can provide (helper joints, deformer stacks) — auto-rigs are most useful as a starting point or for game/background characters.
