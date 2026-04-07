---
title: "Learning Mesh-Based Simulation with Graph Networks"
authors: [Pfaff, Tobias; Fortunato, Meire; Sanchez-Gonzalez, Alvaro; Battaglia, Peter W.]
venue: International Conference on Learning Representations (ICLR 2021)
year: 2021
tags: [simulation, neural, mesh-graph-nets, cloth, muscles, volumes]
source: raw/papers/2010.03409v4.pdf
---

## Summary
MeshGraphNets is a graph neural network framework for learning physics simulation directly on mesh representations — including cloth, rigid bodies, and fluids. Unlike particle-based GNN simulators, it operates on adaptive triangular/tetrahedral meshes (the native representation in character cloth and FEM simulation), encoding both the mesh structure and world-space relationships into a heterogeneous graph. Trained on ground-truth simulations, MeshGraphNets rolls out accurate, fast predictions for unseen configurations.

## Problem
Production cloth and soft-body simulations require expensive iterative solvers (implicit integration, nonlinear FEM). Neural surrogates exist for particle-based systems but don't naturally handle the adaptive mesh topology used in production pipelines. A learned simulator that operates directly on the production mesh representation — and generalizes to varying mesh resolution and material parameters — would enable real-time or interactive physical feedback for cloth and secondary deformation in character pipelines.

## Method
The simulation state at time $t$ is encoded as a graph $\mathcal{G}_t = (V_M, E_M \cup E_W)$ where:
- **Mesh nodes** $V_M$: one per mesh vertex; node features include position, velocity, material properties, boundary conditions.
- **Mesh edges** $E_M$: mesh connectivity (triangle edges / tetrahedra edges); edge features encode relative position and rest-state geometry.
- **World edges** $E_W$: inter-object or self-collision edges added within a spatial radius; encode contact proximity.

**Encoder–Processor–Decoder architecture:**
1. **Encoder**: MLP embeds node/edge features into latent vectors.
2. **Processor**: $M$ rounds of message passing (graph network blocks):
   - Each block: update edge latents from endpoint node latents; aggregate messages at each node; update node latents.
   - Message passing operates over both $E_M$ and $E_W$.
3. **Decoder**: MLP maps per-node latents to per-node acceleration $\ddot{x}$; integrate to get next-step position $x_{t+1} = 2x_t - x_{t-1} + \Delta t^2 \ddot{x}$.

**Training**: supervised on rollouts from a traditional solver (e.g. cloth FEM, Eulerian fluid). Noise injection during training improves long-horizon stability.

**Multi-scale resolution**: world edges span multiple mesh resolutions via radius graph; the model adapts to locally refined meshes around contact regions.

## Key Results
- Generalizes across cloth, rigid bodies, and incompressible fluid simulation.
- Long-horizon rollouts remain stable (100+ steps without drift to failure).
- Handles adaptive mesh refinement: finer mesh near contacts, coarser elsewhere.
- Inference speed: orders of magnitude faster than traditional FEM solvers.
- Outperforms particle-based GNN simulators on mesh-topology tasks.

## Limitations
- Training requires a corpus of ground-truth simulation data from a traditional solver.
- Generalization degrades for material properties or mesh topologies far outside the training distribution.
- Self-contact handling is approximate (radius-based world edges, not exact collision detection).
- Currently slower than LBS for real-time use; faster than FEM but not yet interactive at full production mesh density.

## Connections
- [[papers/bouaziz-2014-projective-dynamics]] — traditional fast cloth/elastic solver; MeshGraphNets can be trained to mimic its output
- [[papers/hahn-2013-rig-space-secondary]] — rig-space secondary dynamics; MeshGraphNets is a potential learned replacement for the simulation step
- [[papers/hahn-2014-subspace-cloth]] — subspace cloth; MeshGraphNets avoids needing a manually chosen subspace
- [[papers/mcadams-2011-elasticity-skinning]] — character skin FEM; MeshGraphNets could replace or accelerate the elasticity solve
- [[concepts/secondary-motion]] — learned mesh simulation is a neural surrogate for secondary motion computation
- [[concepts/neo-hookean-simulation]] — the simulation being learned is often neo-Hookean or co-rotational FEM on the training side

## Implementation Notes
MeshGraphNets is available in PyTorch (unofficial) and JAX (DeepMind's original). Key integration point for character pipelines:

```python
# Given rest mesh V_rest, current V_t, V_{t-1}, boundary conditions bc:
graph = build_graph(V_t, V_rest, edges_mesh, edges_world)
accel = model(graph)               # (N, 3)
V_next = 2*V_t - V_prev + dt**2 * accel
```

For Houdini: run the model in Python SOP at each DOP timestep as a replacement for or correction to the Vellum solver. Build world edges using `xyzdist()` / `pcfind()` at each step. Pass boundary conditions (pinned vertices, wind) as node attributes.

**Training data generation**: run Houdini Vellum cloth at high quality on a varied set of garments/poses; export per-frame mesh positions as numpy arrays. Use a 5% noise injection on positions during training to prevent error accumulation.
