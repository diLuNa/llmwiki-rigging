---
title: "Mesh Wrap / Topology Transfer"
tags: [mesh-wrap, deformation, rig-generation]
---

## Definition
Mesh wrap (also called topology transfer or retopologizing transfer) is the process of adapting the vertex connectivity of a source mesh to match the shape of a target geometry, while preserving the source mesh's patch layout and edge flow structure. The output mesh has the source's topology but the target's shape.

## Variants / Taxonomy
- **ICP-based wrap**: iterative closest-point alignment; fails for large non-rigid deformations.
- **Affine-invariant coordinate wrap** [[papers/degoes-2019-mesh-wrap]]: uses coordinates invariant to local affine transformations; robust under large shape differences; preserves patch layout.
- **Template fitting / non-rigid ICP**: statistical shape model or energy-based deformation field.
- **Neural wrap**: learn deformation field from training data; requires paired examples.

## Key Papers
- [[papers/degoes-2019-mesh-wrap]] — affine-invariant coordinates; wrapped 600 Pixar characters
- [[papers/degoes-2020-garment-refit]] — applies the same affine-invariant idea to garment refitting

## Connections
- [[concepts/linear-blend-skinning]] — sharing a mesh topology enables sharing skinning weights
- [[concepts/pose-space-deformation]] — shared topology enables corrective transfer

## Notes
Practical motivation for mesh wrap in production:
- **Shared rig topology**: if all humanoid characters share the same mesh connectivity, they can share skinning weights, blend shape targets, and USD skeletal schemas.
- **Asset reuse**: wrap garments, facial patches, and accessories from one character to another.
- **Character variants**: hero → crowd variant mesh sharing.

In Houdini, mesh wrap is available via the `Labs Instant Meshes` SOP (topology-agnostic) or via custom constraint-based deformation SOPs for topology-preserving wraps.
