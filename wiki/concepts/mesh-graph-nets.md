---
title: "Mesh Graph Networks"
tags: [simulation, neural, mesh-graph-nets, cloth, volumes]
---

## Definition
Mesh Graph Networks (MeshGraphNets / MGN) are graph neural network frameworks that learn physics simulation directly on mesh representations. Unlike particle-based GNN simulators, they encode mesh connectivity as a graph and train a neural network to predict the next simulation state from the current one, enabling fast rollouts at inference time without iterative solvers.

The canonical architecture (Pfaff et al. 2021) uses an **Encode-Process-Decode** pipeline:

1. **Encoder** — maps node/edge features to latent embeddings via MLPs.
2. **Processor** — $K$ rounds of message-passing over the graph (mesh edges + world-space radius edges for contact).
3. **Decoder** — predicts per-node accelerations; positions integrated with a semi-implicit Euler step.

The graph is heterogeneous: *mesh edges* encode rest-state geometry and connectivity; *world edges* (radius-based) encode proximity/contact.

## Variants / Taxonomy

### Flat (single-scale)
- **MeshGraphNets** (Pfaff 2021) — baseline; propagation radius limited to $K$ hops per step.
- **MeshGraphNetRP** (Libao 2023) — GRU encoder for temporal history; physics-informed edge losses.

### Hierarchical / Multi-scale
- **MultiScale MeshGraphNets** (Fortunato 2022) — V-cycle over fine + auxiliary coarse mesh; achieves spatial convergence.
- **HOOD** (Grigorev 2023) — learned hierarchical pooling; self-supervised physics loss (no ground-truth sim data).

### Shape / Appearance (non-physics)
- **CoMA** (Ranjan 2018) — spectral Chebyshev conv + hierarchical pooling on fixed-topology face meshes; learns a nonlinear face shape space (not a time-stepping simulator, but the architectural ancestor).

### Production-mesh focus
- **N-Cloth** (Li 2022) — arbitrary-topology meshes (non-SMPL characters); shared cloth+obstacle latent space; scales to 100K triangles at 30–45 fps.

## Key Papers

- [[papers/pfaff-2021-meshgraphnets]] — canonical MGN; heterogeneous graph; cloth, rigid, fluid benchmarks
- [[papers/fortunato-2022-multiscale-mgn]] — V-cycle hierarchy; spatial convergence
- [[papers/grigorev-2023-hood]] — hierarchical + self-supervised; garment-agnostic; handles topology changes
- [[papers/libao-2023-meshgraphnetsrp]] — GRU encoder; physics-informed losses; better rigid-body generalization
- [[papers/li-2022-ncloth]] — arbitrary production mesh topology; 100K triangles at real-time
- [[papers/ranjan-2018-coma]] — spectral mesh conv for nonlinear 3D face shape (architectural precursor)

## Connections

- [[concepts/secondary-motion]] — MGN is the leading neural surrogate for secondary cloth/soft-tissue motion
- [[concepts/neo-hookean-simulation]] — the FEM simulation being learned is typically co-rotational or neo-Hookean on the training side
- [[concepts/digital-human-appearance]] — CoMA's nonlinear face space is used in digital human shape models (FLAME, DECA)
- [[concepts/blendshapes]] — CoMA latent codes are a nonlinear alternative to PCA blendshape weights

## Notes

**Propagation bottleneck:** A flat GNN with $K$ message-passing steps can propagate information at most $K$ edges per rollout step. On fine meshes this is too local — long-range forces (tension, global body motion) arrive too slowly, causing rubbery artefacts. MS-MGN and HOOD address this via multi-scale hierarchies.

**Self-supervision:** HOOD is the first cloth MGN to replace ground-truth simulation data with a differentiable physics loss (stretch + bending + collision + inertia). This removes the expensive offline simulation step from the training pipeline.

**Production applicability checklist:**
| Requirement | MGN | MS-MGN | HOOD | N-Cloth | MGN-RP |
|-------------|-----|--------|------|---------|--------|
| Arbitrary mesh topology | ✓ | ✓ | ✓ | ✓ | ✓ |
| Real-time inference | ~ | ~ | ✓ | ✓ | ~ |
| No GT sim data needed | ✗ | ✗ | ✓ | ✗ | ✗ |
| Multi-garment single model | ✗ | ✗ | ✓ | ✗ | ✗ |
| Temporal coherence | ✗ | ✗ | ✗ | ✗ | ✓ |
