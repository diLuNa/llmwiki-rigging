---
title: "Delta Mush: Smoothing Deformations While Preserving Detail"
authors: [Mancewicz, Joe; Derksen, Matt L.; Rijpkema, Hans; Wilson, Christine A.]
venue: DigiPro 2014
year: 2014
tags: [skinning, smoothing, correctives, deformation, lbs]
source: ~no local pdf~
---

## Summary
Delta Mush is a deformation layer that smooths a base deformation (typically LBS) to remove skin-sliding and collapsing artifacts, then adds back the original surface detail as a delta offset in the smoothed frame. The result is smooth, volume-preserving deformation that retains fine surface detail without requiring corrective sculpts.

## Problem
LBS produces skin-sliding, candy-wrapper collapse, and sharp creases at joints. Corrective sculpts fix these issues but require enormous per-pose authoring effort. A single automatic operator that removes LBS artifacts while preserving surface detail would dramatically reduce rigging labor.

## Method
Two-step process per frame:
1. **Smooth step**: apply many iterations of Laplacian smoothing to the deformed mesh positions, producing a smooth (but detail-free) surface.
2. **Delta reapply step**: for each vertex, compute the offset (delta) from the smoothed surface to the original rest pose surface, expressed in the local tangent frame of the smoothed surface. Apply this delta to restore surface detail in the deformed configuration.

The delta is stored in a local frame (normal + tangent) so it moves correctly with the surface even under large deformations.

```
delta_i = vertex_rest_i - smooth_rest_i (in local frame at smooth_rest_i)
deformed_i = smooth_deformed_i + apply_delta(delta_i, frame_smooth_deformed_i)
```

## Key Results
- Eliminates most LBS candy-wrapper and volume-collapse artifacts automatically.
- Preserves surface wrinkles, pores, and other fine detail.
- Widely adopted in production; now a standard node in Maya, Houdini, and other DCCs.
- Dramatically reduces corrective sculpt authoring time.

## Limitations
- Does not strictly preserve volume (smoothing introduces volume changes).
- Smoothing can over-relax in low-detail regions, making them look too soft.
- Iteration count and smoothing amount require per-character tuning.
- Performance cost is proportional to mesh resolution × iteration count.

## Connections
- [[concepts/linear-blend-skinning]] — the deformation being corrected
- [[papers/le-2019-direct-delta-mush]] — theoretical reformulation as direct skinning weights
- [[papers/degoes-2018-patch-relax]] — related patch-aware relaxation for rigging cleanup
- [[concepts/laplacian-smoothing]] — the operator used in the smooth step

## Implementation Notes
In Houdini: Delta Mush is available as a SOP (Labs or built-in). The key parameters are number of smoothing iterations (typically 20–100) and the mix/envelope. Applying it as a deformer after the rig evaluation gives the best results.

In VEX: implement as two passes over the mesh — first Laplacian smooth, then delta reapply using per-vertex tangent frames.

## Quotes
> "Delta Mush allows animators to use simple, low-resolution skinning setups while achieving smooth, high-quality deformations that appear to require complex corrective shapes."
