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

## Health summary

- **4** modules — Kelvinlets: grab (single/bi/tri), affine (twist/scale/pinch), constrained solve, sharp family
- **1** module  — Forearm Partial Twist: swing-twist decomposition, partial twist xform, chain builder, Houdini SOP helper
- **Total: 5 modules, 17 functions across 2 papers + 1 general technique**
- All modules: NumPy only, no dependencies beyond standard scientific Python
- Each has a runnable `__main__` example
