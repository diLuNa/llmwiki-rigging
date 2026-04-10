# Python Snippets Index

All Python snippets extracted from wiki papers.
Each file is a self-contained NumPy module with a runnable `__main__` example.

---

## Kelvinlets (de Goes & James 2018 / 2019)

Source papers: [[papers/degoes-2018-kelvinlets]] · [[papers/degoes-2019-sharp-kelvinlets]]

| File | Functions | Eq. | Notes |
|------|-----------|-----|-------|
| [kelvinlet_core.py](kelvinlet_core.py) | `grab`, `grab_biscale`, `grab_triscale`, `apply_grab` | Eq. 6–11 | Vectorized over N points; `mode` param selects decay order |
| [kelvinlet_affine.py](kelvinlet_affine.py) | `twist`, `scale`, `pinch` | Eq. 14–17 | Locally affine brushes; `scale` is zero for nu=0.5 (incompressible) |
| [kelvinlet_constrained.py](kelvinlet_constrained.py) | `solve_forces`, `deform`, `apply_constrained` | Eq. 18 / §5 | Phase 1: numpy linear solve; Phase 2: superposed evaluation |
| [kelvinlet_sharp.py](kelvinlet_sharp.py) | `laplacian`, `bilaplacian`, `cusped_laplacian`, `cusped_bilaplacian`, `sharp_blend` | Eq. 15–18 | Sharp Kelvinlets; `sharp_blend` mixes cusped ↔ smooth |

### Quick-start

```python
import numpy as np
from kelvinlet_core import apply_grab

pts    = np.load("my_mesh.npy")          # (N, 3) vertex positions
result = apply_grab(pts,
                    center=[0, 0, 0],
                    disp=[0, 1, 0],
                    epsilon=2.0,
                    nu=0.45,
                    mode="tri")          # "single" | "bi" | "tri"
```

```python
from kelvinlet_constrained import apply_constrained

# Grab one point, pin two anchors
centers = [[0,0,0], [2,0,0], [-2,0,0]]
disps   = [[0,1.5,0], [0,0,0], [0,0,0]]
result  = apply_constrained(pts, centers, disps, epsilons=1.0, nu=0.4)
```

### Parameter guide

| Parameter | Typical range | Meaning |
|-----------|--------------|---------|
| `epsilon` | 0.5–5.0 (scene units) | Brush radius; controls spatial extent |
| `nu` | 0.3–0.5 | Poisson ratio; 0.5 = incompressible |
| `mode` | "single" / "bi" / "tri" | Far-field decay order: O(1/r), O(1/r³), O(1/r⁵) |
| `smooth_w` (sharp) | 0–1 | 0 = pure cusped (spiky), 1 = pure smooth |
| `family` (sharp) | "laplacian" / "bilaplacian" | Locality level |

### Key formulas

**Grab brush (Eq. 6–7):**
```python
re  = sqrt(dot(r,r) + eps²)
A   = (1-ba)/re + 0.5*eps²/re³
B   = ba/re³
u   = c*eps * (A*force + B*dot(r,force)*r)
```

**Bi-scale normalization (Eq. 8–9):**
```python
norm = 1 / (1/eps1 - 1/eps2)
u    = c * norm * (K(r, eps1) - K(r, eps2))
```

**Constrained solve (§5):**
```python
# 3n×3n system: K_ij = K_eps_i(x_j - x_i)
forces = np.linalg.solve(K_mat, disps.flatten()).reshape(n, 3)
```

---

## Forearm Partial Twist — Swing-Twist Decomposition

Source: General character rigging technique; see [[techniques/forearm-partial-twist]]

| File | Functions | Notes |
|------|-----------|-------|
| [forearm_partial_twist.py](forearm_partial_twist.py) | `swing_twist_decompose`, `partial_twist_xform`, `build_forearm_chain`, `relative_quaternion` | NumPy; includes Houdini Python SOP helper and runnable demo |

### Quick-start

```python
import numpy as np
from forearm_partial_twist import build_forearm_chain

# elbow_xf, hand_xf: (4,4) world-space transforms
xforms = build_forearm_chain(
    elbow_xf, hand_xf,
    twist_axis=np.array([1., 0., 0.]),
    fractions=(0.33, 0.66),       # two intermediate twist joints
)
# xforms[0] → ForearmTwist1 world transform
# xforms[1] → ForearmTwist2 world transform
```

### Key formulas

**Swing-Twist decomposition:**
```python
imag    = q[:3]                         # imaginary part (axis × sin θ/2)
proj    = np.dot(imag, twist_axis) * twist_axis
q_twist = normalize([proj[0], proj[1], proj[2], q[3]])
```

**Partial twist via slerp:**
```python
q_partial = slerp(identity_q, q_twist, t)   # t in [0,1]
```

---

## Rigid Body Resting Analysis (Baktash et al. — ACM ToG / SIGGRAPH 2025)

Source paper: [[papers/baktash-2025-resting-rigid-bodies]]

| File | Functions | Notes |
|------|-----------|-------|
| [rigid_body_rest.py](rigid_body_rest.py) | `support_function`, `potential_energy`, `convex_hull_gauss_map`, `check_face_stability`, `compute_spherical_voronoi_areas`, `resting_probabilities`, `drop_trajectory`, `inverse_design_target_probs`, `run_in_houdini_python_sop` | scipy ConvexHull + SphericalVoronoi; Houdini SOP helper; runnable demo (unit cube + tetrahedron) |

### Quick-start

```python
import numpy as np
from rigid_body_rest import resting_probabilities

# Any convex mesh: (N,3) vertex positions + COM
vertices = np.array([...])          # convex polyhedron vertices
com      = vertices.mean(axis=0)    # approximate COM

result = resting_probabilities(vertices, com)
for i, (p, s) in enumerate(zip(result['prob'], result['stable'])):
    if s:
        print(f"Face {i}: probability = {p:.3f}")
```

### Key functions

| Function | Inputs | Outputs | Notes |
|----------|--------|---------|-------|
| `support_function(vertices, directions)` | (N,3), (M,3) | h (M,), idx (M,) | h(n) = max_x n·x; vectorized |
| `potential_energy(vertices, normals)` | (N,3), (M,3) | V (M,) | V(n) = h(-n); COM height |
| `convex_hull_gauss_map(vertices)` | (N,3) | hull, face_normals, face_areas, com | scipy ConvexHull wrapper |
| `check_face_stability(hull, vertices, com)` | hull, (N,3), (3,) | stable (F,), margins (F,) | COM inside face → 2D cross-product test |
| `compute_spherical_voronoi_areas(face_normals)` | (F,3) | areas (F,) | scipy SphericalVoronoi; dedup for parallel faces |
| `resting_probabilities(vertices, com)` | (N,3), (3,) | dict | Full pipeline; prob[i] = Voronoi_area[i] / 4π if stable |
| `drop_trajectory(vertices, com, n0, steps, step_size)` | (N,3), (3,), (3,), int, float | (T,3) path on S² | Gradient descent on V(n); snaps to face normal |
| `inverse_design_target_probs(vertices, com, target_face_idx, target_probs, iters, lr)` | … | (verts_opt, loss_history) | Numerical gradient descent on vertex positions |
| `run_in_houdini_python_sop(node)` | hou.Node | — | Writes stable, rest_prob, margin prim attrs; voronoi_area detail array |

### Key formulas

**Support function:**
```python
h = directions @ vertices.T      # (M, N) dot products
h_vals = h.max(axis=1)           # (M,) support values
```

**Spherical Voronoi (scipy):**
```python
from scipy.spatial import SphericalVoronoi
sv = SphericalVoronoi(face_normals, radius=1.0, center=np.zeros(3))
sv.sort_vertices_of_regions()
areas = np.array([sv.calculate_areas()[i] for i in range(len(sv.regions))])
```

**Drop trajectory step (tangent gradient):**
```python
grad_V = -(vertices[hull.simplices[best_face]].mean(axis=0))  # approximate
grad_tan = grad_V - np.dot(grad_V, n_curr) * n_curr           # project to S²
n_next = normalize(n_curr - step_size * grad_tan)
```

---

## Health summary

- **4** modules — Kelvinlets: grab (single/bi/tri), affine (twist/scale/pinch), constrained solve, sharp family
- **1** module  — Forearm Partial Twist: swing-twist decomposition, partial twist xform, chain builder, Houdini SOP helper
- **1** module  — Rigid Body Resting Analysis: support function, Gauss map, stability check, Voronoi areas, resting probabilities, drop trajectory, inverse design, Houdini SOP helper
- **Total: 6 modules, 26 functions across 3 papers + 1 general technique**
- All modules: NumPy + SciPy only (scipy.spatial for ConvexHull and SphericalVoronoi)
- Each has a runnable `__main__` example
