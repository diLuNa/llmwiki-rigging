---
title: "Bandage Smoothing — VEX Implementation"
tags: [vex, houdini, smoothing, correctives, bi-laplacian, hda]
---

## Overview
VEX implementation of the bandage smoothing operator from [[papers/degoes-2020-sculpt]]. Applies a bi-Laplacian ($L^2$) relaxation to a corrective delta shape, constrained to a user-defined vertex patch (the "bandage"). Boundary vertices are held fixed; interior vertices are smoothed until the energy $\|L^2 \delta\|^2$ is minimized.

Used after sculpt transfer to remove high-frequency noise and kinks introduced by the transfer process, while preserving the corrective's intent on the patch boundary.

## Algorithm

```vex
// Geometry Wrangle SOP — run over points
// Attributes in:  @P (current position), @delta (corrective displacement), 
//                 @bandage (int mask: 1 = interior, 0 = boundary/outside)
// Attribute out:  @delta (smoothed)

int    iters    = chi("iterations");   // typically 5–20
float  strength = chf("strength");     // blend: 0=none, 1=full

vector delta_orig = @delta;
vector delta_curr = @delta;

for (int i = 0; i < iters; i++) {
    if (@bandage == 1) {  // interior vertices only
        // Laplacian step: average neighbours
        int npts[] = neighbours(0, @ptnum);
        vector lap = {0, 0, 0};
        foreach (int nb; npts) {
            vector nb_delta = point(0, "delta", nb);
            lap += nb_delta;
        }
        lap /= len(npts);

        // Bi-Laplacian: apply Laplacian to the Laplacian result
        vector bi_lap = lap;  // one Laplacian step per iteration
        // (Full L^2 requires a two-pass approach; see notes)

        delta_curr = lerp(delta_curr, bi_lap, strength / iters);
        setpointattrib(0, "delta", @ptnum, delta_curr, "set");
    }
}

@P = @P - delta_orig + delta_curr;  // apply smoothed delta
```

## Two-Pass Bi-Laplacian (Production Quality)

For correct bi-Laplacian behavior, use two sequential Wrangle nodes:

**Pass 1 — Laplacian:**
```vex
// Compute L(delta) for each interior point
if (@bandage == 1) {
    int npts[] = neighbours(0, @ptnum);
    vector lap = {0, 0, 0};
    foreach (int nb; npts) lap += point(0, "delta", nb);
    @laplacian_delta = lap / len(npts) - @delta;  // Laplacian of the delta
}
```

**Pass 2 — Laplacian of Laplacian:**
```vex
// Apply Laplacian to the laplacian_delta field
if (@bandage == 1) {
    int npts[] = neighbours(0, @ptnum);
    vector lap2 = {0, 0, 0};
    foreach (int nb; npts) lap2 += point(0, "laplacian_delta", nb);
    @delta -= chf("strength") * (lap2 / len(npts) - @laplacian_delta);
}
```

Repeat both passes for `iterations` count.

## Cotangent Weights (Geometry-Aware Variant)

Replace uniform averaging with cotangent-weighted averaging for geometry-aware smoothing (less dependent on mesh density). Cotangent weights $w_{ij}$ for edge $(i,j)$:

```math
w_{ij} = \frac{\cot\alpha_{ij} + \cot\beta_{ij}}{2}
```

where $\alpha_{ij}, \beta_{ij}$ are the angles opposite edge $(i,j)$ in the two adjacent triangles.

```vex
// Cotangent-weighted Laplacian
int npts[] = neighbours(0, @ptnum);
vector lap = {0, 0, 0};
float w_total = 0;
for (int k = 0; k < len(npts); k++) {
    int nb = npts[k];
    float cot_weight = abs(point(0, "cot_weight", nb));  // pre-computed
    lap += cot_weight * point(0, "delta", nb);
    w_total += cot_weight;
}
if (w_total > 1e-6) lap /= w_total;
```

## HDA Setup

| Input | Description |
|-------|-------------|
| Input 0 | Geometry with `@delta` (corrective displacement) attribute |
| Input 1 | Bandage selection group (convert to `@bandage` int point attribute) |

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `iterations` | int | 10 | Number of relaxation steps |
| `strength` | float | 1.0 | Overall smoothing strength |
| `use_cotangent` | toggle | off | Geometry-aware cotangent weights |

## Notes
- The bandage boundary (ring of fixed vertices surrounding the patch) is critical — without it, smoothing leaks into surrounding geometry and destroys the corrective's overall shape.
- Iterative Gauss-Seidel (in-place updates) converges faster than Jacobi (simultaneous updates) for the same number of iterations; VEX's sequential point iteration is naturally Gauss-Seidel.
- For very large patches (hundreds of vertices), consider solving via sparse linear system (Python SOP with scipy.sparse) for exact bi-Laplacian minimization rather than iterative approximation.

## Related
- [[papers/degoes-2020-sculpt]] — source paper; bandage smoothing is §3.2
- [[concepts/laplacian-smoothing]] — underlying operator theory
- [[techniques/sculpt-transfer-vex]] — bandage smoothing is typically applied after sculpt transfer
- [[comparisons/smoothing-operators]] — comparison of Laplacian vs bi-Laplacian vs cotangent
