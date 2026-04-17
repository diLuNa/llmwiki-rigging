---
title: "Parallel Transport"
tags: [math, deformation, skinning, houdini, vex]
papers: [pinskiy-2010-sliding-deformation, degoes-2022-profile-curves]
---

## What Is Parallel Transport

**Parallel transport** moves a vector along a curve while keeping it "as constant as possible" — tangent-plane–projected at every step, with no extra twist beyond what the geometry itself forces.

On a smooth surface, the transported vector $V$ satisfies:

```math
\nabla_{\dot\gamma} V = 0
```

where $\nabla_{\dot\gamma}$ is the covariant derivative along the path $\gamma$. In plain terms: at each infinitesimal step, project the vector onto the new tangent plane and keep going. The result is path-dependent — different routes between two points yield different orientations — and the accumulated rotation around a closed loop equals the integral of Gaussian curvature enclosed (Gauss-Bonnet theorem).

In character rigging, parallel transport appears wherever a **local coordinate frame or direction must be propagated coherently** across a surface or along a curve without reference to a global up-vector.

---

## The Discrete Operation: `dihedral()`

The discrete analogue of one parallel-transport step is the **dihedral rotation** between two adjacent normals: the unique minimal-angle rotation that maps $N_i$ onto $N_{i+1}$.

```vex
matrix3 R = dihedral(N_i, N_i_plus_1);   // VEX built-in
vector  v_transported = v * R;            // transport v into the next frame
v_transported -= dot(v_transported, N_i_plus_1) * N_i_plus_1; // project onto new tangent plane
v_transported  = normalize(v_transported);
```

`dihedral(a, b)` returns the rotation matrix for the shortest arc from unit vector `a` to unit vector `b`. It is a rank-3 rotation of the form $R = I + \sin\theta\,[\hat{n}]_\times + (1-\cos\theta)\,[\hat{n}]_\times^2$ where $\hat{n} = (a \times b)/\|a \times b\|$.

**Two degenerate cases:**
- $N_i \approx N_{i+1}$ (flat): $R \approx I$, works fine.
- $N_i \approx -N_{i+1}$ (180° flip, sharp crease): the rotation axis is ambiguous. Guard with a dot-product check and fallback to a user-specified axis if needed.

---

## Application 1 — Along a Curve (Bishop Frame)

A chain of polyline segments defines a natural parallel-transport frame, called the **Bishop frame** (also *rotation-minimizing frame*). It avoids the Frenet frame's singularity at zero-curvature segments and the arbitrary flipping that comes with tracking a Frenet normal.

**Algorithm:**

```
1. Seed the initial normal n₀ perpendicular to the first tangent t₀.
2. For each subsequent segment i → i+1:
     R = dihedral(t_i, t_{i+1})
     n_{i+1} = normalize(n_i * R)
     b_{i+1} = normalize(cross(t_{i+1}, n_{i+1}))  // binormal
```

The result is a frame {t, n, b} at every vertex that has **zero torsion**: the normal twists only as much as the curve's geometry requires and no more.

**Torsion correction** (CurveNet): When a curve connects two feature points that each define a fixed normal direction, the pure Bishop frame may accumulate an unwanted net twist. CurveNet (de Goes et al. 2022) corrects this by blending an extra rotation $\theta$ around $t$ along the arc length:

```math
n_i \leftarrow R_\theta^{(\alpha_i)} \cdot n_i, \quad
\theta = \arctan2(\hat\Omega_k n_1 \cdot (n_k \times t_k),\; \hat\Omega_k n_1 \cdot n_k)
```

where $\alpha_i = s_i / s_\text{total}$ is the fractional arc length and $\hat\Omega_k$ is the rotation at the destination corner.

**VEX (curve, per-segment):** see [[vex/parallel-transport.vex]] Snippet A.

---

## Application 2 — Over a Mesh Surface (BFS Propagation)

When a local tangent-space direction must be represented consistently across many vertices (e.g. to define a sliding direction over a mesh patch), parallel transport generalizes to surface propagation via BFS.

**Algorithm:**

```
1. Seed the direction at a handle vertex: a₁ = b₁ (local tangent axis).
2. BFS outward through active vertices. For each vertex P with processed neighbour Nb:
     R = dihedral(N_nb, N_P)               // transport from Nb's tangent plane into P's
     a₁_contrib = normalize(a₁_nb * R)    // rotate + project
     a₁_contrib -= dot(a₁_contrib, N_P) * N_P
3. Average contributions from all processed neighbours; normalize.
4. Re-orthogonalize a₂ = normalize(b₂ - dot(b₂, a₁) * a₁).
```

The BFS order determines which path is taken to each vertex. On a surface with significant Gaussian curvature, the result is path-dependent (holonomy), so the direction field will not be integrable globally. For typical rigging use cases (localized deformation regions), this is not a problem.

**Full VEX pipeline:** [[vex/sliding-direction-propagate.vex]] (Pinskiy 2010 specific)
**General single-step:** [[vex/parallel-transport.vex]] Snippet B

---

## Bishop Frame vs Frenet Frame

| Property | Frenet Frame | Bishop Frame (Parallel Transport) |
|----------|-------------|----------------------------------|
| Normal definition | $n = \hat\kappa / \|\hat\kappa\|$ (curvature direction) | propagated from seed via dihedral |
| Singularity | flips at inflection points (κ = 0) | none |
| Torsion | tracks natural torsion of curve | zero (twist-free by construction) |
| Net twist around closed loop | matches geometric torsion | holonomy of Gaussian curvature |
| Seeding | automatic (first Frenet normal) | requires initial normal choice |
| Suitable for | general differential geometry | rigs, polyline deformers, UV parameterization |

For production rigs the Bishop frame is almost always preferred: it is numerically stable, never flips, and produces visually cleaner roll behavior on limbs and spine controls.

---

## Application 3 — Forearm Twist Distribution

The [[techniques/forearm-partial-twist]] technique distributes a single twist parameter across N intermediate joints. The intermediate joints' rotation axes are found by parallel-transporting the forearm bone's local X axis along the limb chain. Each step:

```vex
matrix3 R   = dihedral(current_rest_tangent, next_rest_tangent);
vector  axis = normalize(current_axis * R);
```

This ensures the distributed twist axes remain consistent with the geometry of the arm even when the elbow bends, preventing candy-wrapper artifacts.

---

## Holonomy and Path Dependence

The rotation accumulated when parallel-transporting a vector around a closed loop is the **holonomy** of that loop, equal to the integral of Gaussian curvature $K$ enclosed:

```math
\Delta\theta = \iint_\Omega K \, dA
```

For a flat surface ($K = 0$ everywhere), holonomy is zero — parallel transport is path-independent and globally consistent. For curved surfaces (a sphere, a shoulder blade, a cloth wrinkle), different BFS paths yield different results.

**Practical consequence for rigging:** limit parallel-transport propagation to regions small enough that curvature accumulation is visually negligible. For large-scale direction fields (spine curves, limb axes), work with the skeletal chain (Application 1) rather than the surface mesh (Application 2).

---

## Application 4 — Vertex-Connectivity Approach (Houdini / MOPs)

The `dihedral()`-based approach in Snippets A/B uses point indices to walk the polyline. This fails cleanly on closed curves where the last point has no next neighbour. A more robust alternative uses Houdini's KineFX vertex-connectivity library to determine the previous and next points via the half-edge graph, treating the polyline like a joint chain.

**Setup:** `#include <kinefx_hierarchy.h>` in a Primitive Wrangle. Key functions:
- `getchildren(geo, ptnum)` — returns array of downstream-connected point numbers
- `getparent(geo, ptnum)` — returns upstream-connected point number (-1 if none)

**Three tangent computation modes:**

| Mode | Code | Best for |
|------|------|----------|
| Forward | `normalize(P_child - P_i)` | Default; matches motion direction along curve |
| Backward | `normalize(P_parent - P_i) * -1` | When curve is authored end-to-start |
| Averaged | `normalize(lerp(T_fwd, T_bwd, 0.5))` | Sharp-corner curves; smoother roll through bends |

**Normal transport loop** (alternate formulation using binormal + acos):

```vex
for (int i = 0; i < len(normals)-1; i++) {
    vector binormal = cross(tangents[i], tangents[i+1]);
    if (length2(binormal) == 0) {
        normals[i+1] = normals[i];   // parallel tangents, no rotation needed
    } else {
        binormal = normalize(binormal);
        float theta = acos(dot(tangents[i], tangents[i+1]));
        matrix3 m = ident();
        rotate(m, theta, binormal);
        normals[i+1] = m * normals[i];   // column-vector convention (rotate() built-in)
    }
}
```

Note: this uses `m * v` (column-vector convention from `rotate()`) rather than `v * R` (row-vector convention from `dihedral()`). Both produce valid rotations; do not mix the two conventions in the same loop.

**Output as quaternion `orient` attribute** (instead of separate T/N/B vectors):

```vex
matrix3 m = maketransform(tangent, normal);   // forward=tangent, up=normal
vector4 orient = quaternion(m);
setpointattrib(0, "orient", pts[i], orient, "set");
```

**Degenerate seed normal guard:** if `dot(normals[0], tangents[0]) > 0.999`, the seed normal is nearly parallel to the first tangent — warn the user and/or override. This commonly happens on vertical straight lines and circles.

**Per-point roll/pitch/yaw** (applied after frame computation, using `@__curveu` from Resample SOP):

```vex
vector twist_axis = qrotate(p@orient, {0,0,1});   // local Z = roll
float twist_amount = ch("twist_amount") * chramp("twist_ramp", @__curveu);
vector4 twist_q = quaternion(radians(twist_amount), twist_axis);
p@orient = qmultiply(twist_q, p@orient);
```

**VEX:** see [[vex/parallel-transport.vex]] Snippet C.

**External reference:** [Revisiting Parallel Transport — toadstorm.com (2026-04-16)](https://www.toadstorm.com/blog/?p=1168) — practical re-implementation of MOPs Orient Curve using vertex connectivity and three tangent modes.

---

## VEX Reference

| Snippet | Purpose | File |
|---------|---------|------|
| A — curve chain | Bishop frame (`dihedral()`); optional torsion correction; outputs `@pt_T/N/B` | [[vex/parallel-transport.vex]] |
| B — single mesh step | One `dihedral()` transport step from neighbour to current vertex | [[vex/parallel-transport.vex]] |
| C — kinefx connectivity | Bishop frame via `kinefx_hierarchy.h`; three tangent modes; `orient` output | [[vex/parallel-transport.vex]] |
| BFS mesh (Pinskiy) | Full BFS propagation with @slide_done flag | [[vex/sliding-direction-propagate.vex]] |
| CurveNet frames | Bishop + torsion correction for CurveNet profile curves | [[vex/curvenet-frames.vex]] |

---

## Gotchas

- **Near-antipodal normals** ($N_i \cdot N_{i+1} \approx -1$): `dihedral()` is undefined. This happens at hard creases. Guard with `if (dot(Na, Nb) < -0.999) { /* fallback */ }` and use a fixed reference axis (e.g. world Y) for the seam edge.
- **Closed curves and point indices**: the point-index approach (Snippet A) extrapolates the last tangent and does not know the first vertex is connected to the last. Use the `kinefx_hierarchy.h` connectivity approach (Snippet C) for closed curves.
- **BFS initialization order matters**: the handle vertex must be initialized before the loop runs, and `@slide_done` must be initialized to 0 on all other vertices. A separate initialization wrangle (not inside the loop) is the cleanest pattern.
- **Re-projection after transport**: after rotating a vector with `dihedral()`, the result may have a small residual component along the new normal (floating-point accumulation). Always re-project: `v -= dot(v, N) * N`.
- **Bishop frame needs a seed normal**: the first normal must be chosen explicitly. Common choice: `n₀ = normalize(cross(t₀, world_up))`, with a fallback to `cross(t₀, world_right)` if $t_0 \approx \pm Y$.
- **Seed normal parallel to tangent**: if `dot(n₀, t₀) ≈ 1`, the seed is degenerate (happens on vertical lines and circles). Check and warn: `if (dot(seed, T[0]) > 0.999) { /* warn or override */ }`.
- **Closed curves holonomy**: a Bishop frame propagated around a closed polyline will not close up unless the curve's total torsion is zero. The closing gap is the holonomy angle. CurveNet distributes this gap uniformly via the torsion correction.
- **`dihedral()` vs `rotate()` convention**: `dihedral()` returns a row-vector matrix (`v * R`). The `rotate()` built-in creates a column-vector matrix (`m * v`). Do not mix them in the same code path.
- **Sharp corners and tangent averaging**: on curves with sudden direction changes, forward-only tangents produce sudden frame flips. Use the averaged tangent mode (Snippet C) to smooth the transition.

---

## Connections

- [[concepts/b-spline-volumes]] — FFD lattice frame is also parallel-transported for muscle primitives
- [[concepts/rig-inversion]] — rig Jacobian computation requires consistent frame conventions along chains
- [[concepts/skinning]] — LBS deformation gradient implicitly transports local skin frames
- [[papers/pinskiy-2010-sliding-deformation]] — BFS mesh application; sliding displacement in local frame
- [[papers/degoes-2022-profile-curves]] — curve application; Bishop + torsion correction in CurveNet
- [[techniques/forearm-partial-twist]] — twist axis chain uses dihedral transport along bone chain
- [[techniques/bandage-smoothing-vex]] — cotangent Laplacian respects tangent-plane structure implicitly
