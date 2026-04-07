---
title: "Mesh-Tension Driven Expression-Based Wrinkles for Synthetic Faces"
authors: [Raman, Chirag; Hewitt, Charlie; Wood, Erroll; Baltrusaitis, Tadas]
venue: CVPR 2022 (approx.)
year: 2022
tags: [correctives, blendshapes, neural, simulation]
source: raw/papers/MeshTensionDrivenWrinkles.pdf
---

## Summary
A method for adding dynamic, expression-dependent skin wrinkles to synthetic face renders, improving downstream computer vision task performance. The core contribution is a formal definition of *mesh tension* — a scalar measure of local surface deformation — used to blend between neutral and wrinkled texture maps (albedo + displacement) captured from high-resolution expression scans.

## Problem
Synthetic face rendering pipelines (like Wood et al. 2021) generate realistic neutral faces but apply static textures regardless of the expression being deformed. Real faces exhibit complex dynamic wrinkles in response to muscle activations. Missing wrinkles in synthetic training data reduces the realism gap and degrades downstream CV model performance.

## Method
**Mesh tension:** Defined per-vertex as a scalar measuring how much the local surface is compressed or stretched relative to the neutral pose. Computed from the 2D surface metric change — concretely, the ratio of local area or edge lengths in the deformed mesh vs. the neutral mesh. High tension → surface compressed → likely to wrinkle.

**Wrinkle maps from scans:** High-resolution expression scans (albedo + displacement) are captured for a set of target expressions per identity. Each scan yields a wrinkle map (the difference between the posed and neutral appearance). Multiple wrinkle maps are stored per identity.

**Synthesis:** For an arbitrary expression (not in the scan set):
1. Compute per-vertex mesh tension.
2. Use tension values to weight blend between the neutral texture and the closest wrinkle maps.
3. The blended map is applied to the rendered face.

**Result:** Wrinkles appear where the face is compressed, scale in intensity with compression, and generalize beyond the scanned poses.

## Key Results
- Training a face landmark localization model on wrinkled synthetic data improves accuracy vs. training on wrinkle-free synthetic data.
- Demonstrates that realism at the wrinkle level measurably impacts downstream CV task quality.
- Introduces the 300W-winks evaluation subset and Pexels dataset for evaluation under extreme expressions.

## Limitations
- Mesh tension is a simplified proxy for the true biomechanical stress driving wrinkle formation.
- Wrinkle maps are captured per identity — requires scan sessions; doesn't generalize zero-shot to new identities.
- Blending is a linear interpolation in texture space and may not capture wrinkle nonlinearity.

## Connections
- [[papers/cutler-2007-art-directed-wrinkles]] — same stress-driven wrinkle blending concept, applied to animated films rather than synthetic data
- [[papers/mancewicz-2014-delta-mush]] — surface smoothing as complement to wrinkle addition
- [[concepts/pose-space-deformation]] — related paradigm of pose-driven texture blending
- [[concepts/blendshapes]] — wrinkle maps as a texture-space blendshape analog

## Implementation Notes
Mesh tension in VEX: for each point, compute the ratio of current edge lengths to rest edge lengths over incident edges, then aggregate (mean or max) to a scalar. A simple approximation:

```vex
float tension = 0;
int n = neighbourcount(0, @ptnum);
for (int i = 0; i < n; i++) {
    int nb = neighbour(0, @ptnum, i);
    float rest_len = length(point(1,"P",nb) - point(1,"P",@ptnum));  // rest mesh
    float curr_len = length(point(0,"P",nb) - @P);
    tension += (curr_len / max(rest_len, 1e-6)) - 1.0;
}
tension = max(0, -tension / n);   // compression (negative stretch) is positive tension
```

Negative values (stretch) can drive a separate stretch-wrinkle map if desired.
