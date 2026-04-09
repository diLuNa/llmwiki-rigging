2# VEX Snippets Index

All Houdini VEX snippets extracted from wiki papers.
Each snippet is a self-contained Geometry Wrangle SOP unless noted otherwise.

---

## Kelvinlets (de Goes & James 2018 / 2019)

Source papers: [[papers/degoes-2018-kelvinlets]] · [[papers/degoes-2019-sharp-kelvinlets]]

| File | Algorithm | Eq. | Decay | Notes |
|------|-----------|-----|-------|-------|
| [kelvinlet-grab.vex](kelvinlet-grab.vex) | Regularized Kelvinlet grab brush | Eq. 6–7 | O(1/r) | Core brush; Poisson ratio controls volume |
| [kelvinlet-multiscale.vex](kelvinlet-multiscale.vex) | Bi-scale & tri-scale extrapolation | Eq. 8–11 | O(1/r³), O(1/r⁵) | `mode` param: 0=single, 1=bi, 2=tri |
| [kelvinlet-affine.vex](kelvinlet-affine.vex) | Twist / Scale / Pinch brushes | Eq. 14–17 | O(1/r²) | `brush_type`: 0=twist, 1=scale, 2=pinch |
| [kelvinlet-constrained.vex](kelvinlet-constrained.vex) | Multi-point constrained deformation | Eq. 18 | — | Pass 2 only; includes Python Pass 1 solve |
| [kelvinlet-cusped.vex](kelvinlet-cusped.vex) | Cusped Kelvinlet (spiky profile) | Eq. 10 | O(1/r) | From Sharp Kelvinlets paper |
| [kelvinlet-laplacian.vex](kelvinlet-laplacian.vex) | Laplacian & Bi-Laplacian Kelvinlet | Eq. 15–16 | O(1/r³), O(1/r⁹) | `order`: 1=Laplacian, 2=Bi-Laplacian |
| [kelvinlet-sharp.vex](kelvinlet-sharp.vex) | Cusped Laplacian & Cusped Bi-Laplacian | Eq. 17–18 | O(1/r³), O(1/r⁹) | Full Sharp Kelvinlets; `smooth_blend` mixes cusped↔smooth |

### Quick-start parameter guide

All grab-type snippets share this detail attribute interface:

| Attribute | Type | Default | Meaning |
|-----------|------|---------|---------|
| `brush_center` | vector | `{0,0,0}` | Brush tip world position |
| `brush_disp` | vector | `{0,1,0}` | Desired displacement at brush center |
| `epsilon` | float | `1.0` | Brush radius (regularization scale) |
| `nu` | float | `0.5` | Poisson ratio: 0=compressible, 0.5=incompressible |
| `mode` | int | `2` | Multiscale mode (multiscale snippet only) |

Affine brushes use `brush_force` instead of `brush_disp` plus type-specific attributes (see file headers).

### Key formulas

**Regularized Kelvinlet (core expression):**
```vex
float A = (1.0 - ba)/re + 0.5*eps*eps/re3;
float B = ba/re3;
vector disp = c * eps * (A * u_tip + B * dot(r, u_tip) * r);
```
where `ba = 1/(4*(1-nu))`, `c = 2/(3 - 2*ba)`, `re = sqrt(dot(r,r) + eps*eps)`.

**Bi-scale (faster decay, simpler than tri):**
```vex
float eps2 = 1.1 * eps1;
float norm = 1.0 / (1.0/eps1 - 1.0/eps2);
disp = c * norm * (KMAT(r, u_tip, eps1) - KMAT(r, u_tip, eps2));
```

**Laplacian Kelvinlet A/B:**
```vex
float re7 = pow(re, 7.0);
float A = (15.0*eps4 - 2.0*ba*re*re*(5.0*eps2 + 2.0*r2)) / (2.0*re7);
float B = 3.0*ba*(7.0*eps2 + 2.0*r2) / re7;
```

**Bi-Laplacian Kelvinlet A/B:**
```vex
float re11 = pow(re, 11.0);
float A = 105.0*eps4 * (3.0*(eps2 - 2.0*r2) - 2.0*ba*re*re) / (2.0*re11);
float B = 945.0*ba*eps4 / re11;
```

---

## Curvenet / Profile Curves (de Goes, Sheffler & Fleischer 2022)

Source paper: [[papers/degoes-2022-profile-curves]]

| File | Algorithm | Eq. | Notes |
|------|-----------|-----|-------|
| [curvenet-frames.vex](curvenet-frames.vex) | Scaled frame + deformation gradient per segment | Eq. 1 | F = sum of outer products of posed/rest axis vectors scaled by stretch ratios |
| [curvenet-polygon-laplacian.vex](curvenet-polygon-laplacian.vex) | Cut-aware polygonal Laplacian L_f | Appendix Eq. 7–10 | Handles arbitrary polygons incl. crack edges; reduces to cotan for triangles |
| [curvenet-deform.vex](curvenet-deform.vex) | Surface deformation evaluation (adjusted sample positions xc + face transforms yh) | Eq. 5–6 | Pass A: transform cut-faces; Pass B: adjusted curvenet constraints; Python Poisson solve included |

### Quick-start parameter guide

**curvenet-frames.vex** (per-primitive, each prim = one curvenet segment):

| Attribute | Type | Where | Meaning |
|-----------|------|-------|---------|
| `Q` | vector | point | Posed world-space position |
| `rest_normal` | vector | prim | Parallel-transported normal in rest pose |
| `pose_normal` | vector | prim | Parallel-transported normal in posed pose |
| `rest_width` | float | prim | Ribbon width in rest pose |
| `pose_width` | float | prim | Ribbon width in posed pose |

**curvenet-polygon-laplacian.vex** (per-primitive on surface mesh):
- Reads `P` from points.
- Writes `Lf` (float array, n×n row-major), `af_norm` (float), `nf` (vector) to the primitive.
- Use `n_verts` prim attribute to know the square dimension of `Lf`.

### Key formulas

**Deformation gradient (Eq. 1):**
```vex
matrix3 Ft = set(st * t1.x * t0, st * t1.y * t0, st * t1.z * t0);
matrix3 Fb = set(sb * b1.x * b0, sb * b1.y * b0, sb * b1.z * b0);
matrix3 Fn = set(sn * n1.x * n0, sn * n1.y * n0, sn * n1.z * n0);
matrix3 F  = Ft + Fb + Fn;   // st=l1/l0, sb=w1/w0, sn=h1/h0
```

**Gradient operator column j (Appendix Eq. 7):**
```vex
vector avg_e = 0.5 * (Ef[j] + Ef[(j-1+n)%n]);
vector Gf_col_j = (-1.0 / af_norm) * cross(nf, avg_e);
```

**Adjusted curvenet constraint position (§4.3):**
```vex
vector pi = qi - Fi * (rest_qi - rest_pi);  // offset-preserving projection
```

---

## Cage Deformation

Source papers: [[papers/lipman-2008-green-coords]] · [[papers/chen-2023-somigliana]]

| File | Algorithm | Eq. | Notes |
|------|-----------|-----|-------|
| [cage-green-coords.vex](cage-green-coords.vex) | Green Coordinates — face weights ψ_f + deformation eval | Lipman 2008 | Closed-form solid angle ψ_f; vertex weights φ_i reference Python BEM |
| [cage-somigliana-kernels.vex](cage-somigliana-kernels.vex) | Somigliana Coordinates — K and T kernel precomputation | Eq. 3–4, 8 | Outputs per-point T_i and K_j matrix arrays via quadrature over cage |
| [cage-somigliana-deform.vex](cage-somigliana-deform.vex) | Somigliana corotational deformation + bulging | Eq. 10–15 | Per-face polar decomp, bulging β/η, traction balance, Eq. 11 solve |

### Quick-start parameter guide

**cage-somigliana-kernels.vex** (precomputation, over points on interior mesh):

| Attribute | Type | Where | Meaning |
|-----------|------|-------|---------|
| `nu` | float | detail | Poisson ratio ν ∈ [0, 0.5) |
| `somi_quad_n` | int | detail | Quadrature points per triangle edge (default 5; paper uses ~87 for 7500 pts/face) |

**cage-somigliana-deform.vex** (runtime, over points):

| Attribute | Type | Where | Meaning |
|-----------|------|-------|---------|
| `nu` | float | detail | Poisson ratio (must match precomputation) |
| `gamma` | float | detail | Bulging scale γ (0 = no bulge, 10–30 = strong swell) |
| `variant` | int | detail | 0 = global rotation, 1 = local per-face rotation |
| `rest_P` | vector | point (cage) | Rest cage vertex positions |

### Key formulas

**Kelvinlet kernel K (Eq. 3, displacement fundamental solution):**
```vex
float a = 1.0 / (mu * 5.0 * PI);   // 3D: (2d-1)=5
float b = a / (4.0 * (1.0 - nu));
matrix3 K = (a-b)/r * matrix3(1) + b/r3 * rrt;  // rrt = outer(r,r)
```

**Traction kernel T (Eq. 4):**
```vex
matrix3 T = coeff1 * (dot(n,r)*matrix3(1) + outer(n,r) - outer(r,n))
           + coeff2 * dot(n,r) * rrt;   // coeff1=(a-2b)/r³, coeff2=6b/r⁵
```

**Corotational deformation (Eq. 11):**
```vex
x_new = invert(T_sum) * rhs;   // T_sum = Σ R_i T_i Rᵢᵀ
// rhs = Σ R_i T_i Rᵢᵀ v'_i  +  Σ R_j K_j Rⱼᵀ τ̃_j
```

**Green Coordinates face weight (solid angle):**
```vex
float num = dot(r1, cross(r2, r3));
float den = d1*d2*d3 + dot(r2,r3)*d1 + dot(r1,r3)*d2 + dot(r1,r2)*d3;
float psi_f = -2.0*atan2(num, den) / (4.0*PI);
```

---

## Bounded Biharmonic Weights (Jacobson et al. 2011)

Source paper: [[papers/jacobson-2011-bbw]]

| File | Algorithm | Notes |
|------|-----------|-------|
| [bbw-cotan-laplacian.vex](bbw-cotan-laplacian.vex) | Cotangent Laplacian assembly (per-triangle half-weights → sparse triplets) | Includes full Python BBW QP solve (SciPy / cvxpy) |
| [bbw-mass-matrix.vex](bbw-mass-matrix.vex) | Lumped mass matrix M_i = (1/3) × sum of incident triangle areas | Required for biharmonic H = LᵀM⁻¹L |
| [bbw-lbs-apply.vex](bbw-lbs-apply.vex) | Runtime LBS deformation using stored BBW weight attributes | Handles any handle type (bones, cages, points) |
| [bbw-harmonic-weights.vex](bbw-harmonic-weights.vex) | Harmonic weight diffusion (Laplacian smoother, linear baseline) | Use for initialization or comparison; iterate 50–200× |

### Quick-start parameter guide

**bbw-cotan-laplacian.vex** (per-prim, single-threaded):
- Run on rest-pose triangle mesh. Disable multi-threading on the wrangle.
- Outputs detail arrays `L_row[]`, `L_col[]`, `L_val[]` for Python sparse assembly.
- Follow with Python solve (embedded in file comments) to get BBW weight attributes `bbw_0`, `bbw_1`, …

**bbw-mass-matrix.vex** (per-point):
- Outputs `@bbw_area` = M_i (lumped area per vertex).
- Run before the Python solve; used to form H = LᵀM⁻¹L.

**bbw-lbs-apply.vex** (per-point, runtime):

| Attribute | Type | Where | Meaning |
|-----------|------|-------|---------|
| `bbw_N` | int | detail | Number of handles K |
| `bbw_k` | float | point | BBW weight for handle k (k = 0…K-1) |
| `bbw_xform_k` | matrix | detail | Delta transform for handle k: `pose_k * inv(rest_k)` |

**bbw-harmonic-weights.vex** (per-point, iterated):
- Requires `bbw_N` (detail int), `bbw_w` (point float array), `bbw_fixed` (point int).
- Initialize boundary conditions, then iterate this wrangle 50–200 times in a For-Each SOP.

### Key formulas

**Cotangent weight for an angle (BBW Appendix):**
```vex
// For edge (p1,p2) — angle opposite at p0:
vector e01 = p1 - p0,  e02 = p2 - p0;
float cot0 = dot(e01, e02) / length(cross(e01, e02));
// Laplacian entry: L[p1,p2] += -0.5 * cot0   (this triangle's contribution)
```

**Biharmonic energy (minimized in BBW):**
```math
\min_{w_j} \; w_j^\top (L^\top M^{-1} L) \, w_j \quad
\text{s.t.} \quad w_j \ge 0,\; \mathbf{1}^\top w = 1,\; w_j|_{\text{handles}} = I
```

**Runtime LBS (bbw-lbs-apply.vex core):**
```vex
vector blended = {0,0,0};
for (int k = 0; k < K; k++) {
    float w = point(0, sprintf("bbw_%d",k), @ptnum);
    matrix T = detail(0, sprintf("bbw_xform_%d",k), ident());
    blended += w * (@P * T);   // row-vector convention
}
@P = blended;
```

---

## Animatomy — Anatomy-Inspired Facial Rig (Choi et al. SIGGRAPH Asia 2022)

Source paper: [[papers/choi-2022-animatomy]]

| File | Algorithm | § | Notes |
|------|-----------|---|-------|
| [animatomy-muscle-strain.vex](animatomy-muscle-strain.vex) | Muscle strain γ = (s − s̄)/s̄ per fiber curve | §5.1 | Per-prim on polyline curves; init pass sets @rest_length |
| [animatomy-strain-blendshapes.vex](animatomy-strain-blendshapes.vex) | Strain blendshapes B_E = E · γ (linear basis) | §5.3 | Column-major E storage; Python AE pass for nonlinear path |
| [animatomy-pose-correctives.vex](animatomy-pose-correctives.vex) | FLAME-style pose correctives B_P = Σ(R_k − R*_k)P_k | §5.2 | K=3 joints, 30 components; delta per axis accumulated |
| [animatomy-jaw-rbf.vex](animatomy-jaw-rbf.vex) | Jaw RBF proxy χ(p) = Σψᵢgᵢ/Σgᵢ (M=50 Gaussians) | §5.5 | Run on 1-pt geometry; outputs jaw_translation + jaw_rotation |
| [animatomy-full-model.vex](animatomy-full-model.vex) | Full forward model M(θ,γ) = W(T + B_P + B_E, J, θ, W) | §5 | Combines B_P + B_E + LBS in one pass; expression transfer note |

### Quick-start parameter guide

**Complete forward pass pipeline:**
```
jaw controls → animatomy-jaw-rbf     (RBF proxy → jaw_translation, jaw_rotation)
muscle curves → animatomy-muscle-strain  (init: @rest_length; runtime: @strain γ)
pose joints  → animatomy-pose-correctives   (joint delta rotations → B_P per vertex)
strain γ     → [Python AE] → latent → [Python decode] → strain deltas
             or animatomy-strain-blendshapes (linear path: B_E = E·γ)
all deltas   → animatomy-full-model    (T + B_P + B_E → LBS → @P)
```

| Attribute | Type | Where | Meaning |
|-----------|------|-------|---------|
| `rest_length` | float | prim (curve) | Arc length of rest muscle fiber |
| `strain` | float | prim (curve) | Current strain γ = (s − s̄)/s̄ |
| `n_muscles` | int | detail | Number of muscle curves (178 for Avatar face) |
| `E_basis` | float[] | detail | Strain basis matrix E, column-major, size = n_muscles × n_pts × 3 |
| `P_basis` | float[] | detail | Pose corrective basis P_k, size = K × n_pts × 3 |
| `bbw_N` | int | detail | Number of LBS handles K |

### Key formulas

**Muscle strain (§5.1):**
```vex
float arc_len = 0;
for (int i = 0; i < npts-1; i++)
    arc_len += length(point(0,"P",pts[i+1]) - point(0,"P",pts[i]));
@strain = (arc_len - @rest_length) / max(@rest_length, 1e-8);
```

**Strain blendshapes (§5.3, linear path):**
```vex
// B_E[:,ptnum] = E * gamma   (E is n_pts×3 × n_muscles)
for (int i = 0; i < n_muscles; i++)
    disp[axis] += gamma[i] * E_basis[i*n_pts*3 + @ptnum*3 + axis];
```

**Pose correctives (§5.2, FLAME-style):**
```vex
// delta_k = R_curr[k] - R_rest[k]   (flattened 9-vector)
for (int k = 0; k < K; k++)
    pose_disp[axis] += delta_k[k] * P_basis[k*n_pts*3 + @ptnum*3 + axis];
```

**Jaw RBF (§5.5):**
```vex
float g_sum = 0;
for (int i = 0; i < M; i++) {
    float dist2 = dot(p - mu[i], p - mu[i]);
    g[i] = exp(-sigma[i]*sigma[i] * dist2);
    g_sum += g[i];
}
out[d] = sum(g[i] * psi[i*6 + d]) / g_sum;  // d=0..5: tx,ty,tz,rx,ry,rz
```

---

## Wrinkle Systems (Cutler et al. 2007 · Raman et al. 2022)

Source papers: [[papers/cutler-2007-art-directed-wrinkles]] · [[papers/raman-2022-mesh-tension-wrinkles]]

| File | Algorithm | Paper | Notes |
|------|-----------|-------|-------|
| [wrinkle-stress-vector.vex](wrinkle-stress-vector.vex) | 16-component stress vector (8 edge lengths + 8 angle cosines) | Cutler 2007 §5, Fig. 6 | Run on rest, reference poses, and animation frames |
| [wrinkle-proximity-metric.vex](wrinkle-proximity-metric.vex) | Proximity metric m*_j + box filter + persistence function (Eq. 1–2) | Cutler 2007 §5 | Three-pass: raw metric → box filter → persistence power |
| [wrinkle-curve-displacement.vex](wrinkle-curve-displacement.vex) | Gaussian displacement field from wrinkle curves (§4) | Cutler 2007 §4 | Inputs curve polylines; amplitude, radius, bend_angle per point |
| [wrinkle-blend.vex](wrinkle-blend.vex) | Weighted displacement blend d* = Σ w_j · d_j (Eq. 3) | Cutler 2007 §5, Eq. 3 | Reads proximity weights + stacked displacement array |
| [wrinkle-mesh-tension.vex](wrinkle-mesh-tension.vex) | Mesh tension (compression/expansion channels, softmax) | Raman 2022 §4 | Outputs tension_compress, tension_expand for texture blend weights |

### Quick-start parameter guide

**Complete Cutler 2007 pipeline:**
```
rest_mesh  → wrinkle-stress-vector → store @rest_stress
ref_pose_0 → wrinkle-stress-vector → wrinkle-curve-displacement → store stress + disp
ref_pose_1 → wrinkle-stress-vector → wrinkle-curve-displacement → store stress + disp
...
anim_frame → wrinkle-stress-vector
           → wrinkle-proximity-metric (pass 1: raw_m)
           → wrinkle-proximity-metric (pass 2: box filter, separate wrangle)
           → wrinkle-proximity-metric (pass 3: persistence weights w_j)
           → wrinkle-blend            (apply weighted displacements)
```

**wrinkle-curve-displacement.vex** (per-point, two inputs):

| Attribute | Type | Where | Meaning |
|-----------|------|-------|---------|
| `amplitude` | float | point (curve) | Peak displacement magnitude (scene units) |
| `radius` | float | point (curve) | Gaussian falloff radius |
| `bend_angle` | float | point (curve) | Normal tilt angle in radians (0 = pure normal, π/4 = 45° fold) |
| `global_scale` | float | channel | Overall amplitude multiplier |
| `blend_mode` | int | channel | 0 = additive, 1 = max |

**wrinkle-mesh-tension.vex** (per-point, two inputs):

| Attribute | Type | Where | Meaning |
|-----------|------|-------|---------|
| `compress_sensitivity` | float | channel | Scale factor for compression channel |
| `expand_sensitivity` | float | channel | Scale factor for expansion channel |

### Key formulas

**Stress vector (Cutler §5):**
```vex
// l_i = edge length to i-th neighbour
sv[i] = length(point(0,"P", neighbour(0,@ptnum,i)) - @P);
// c_i = cos(angle between adjacent edges)
sv[8+i] = dot(edges[i], edges[next]) / (sv[i] * sv[next]);
```

**Proximity metric per component (Eq. 1):**
```vex
float delta_ref_rest = abs(l_ref - l_rest);
float delta_anim_ref = abs(l_anim - l_ref);
// term = 1 at perfect ref match, 0 at rest level or beyond
float term = (delta_ref_rest > EPS && delta_anim_ref <= delta_ref_rest)
             ? 1.0 - delta_anim_ref / delta_ref_rest : 0.0;
```

**Gaussian wrinkle profile (§4):**
```vex
float weight = amp * exp(-0.5 * dist*dist / (radius*radius));
vector disp  = weight * normalize(cos(bend)*Nsurf + sin(bend)*curve_tangent);
```

**Mesh tension (Raman 2022):**
```vex
float mean_strain = sum((curr_len/rest_len) - 1.0) / nbcount;
tension_compress = clamp(-mean_strain, 0, 1);   // squeeze → wrinkle
tension_expand   = clamp( mean_strain, 0, 1);   // stretch → thin
```

---

## Sliding Deformation — Shape Preserving Per-Vertex Displacement (Pinskiy 2010)

Source paper: [[papers/pinskiy-2010-sliding-deformation]]

| File | Algorithm | §  | Notes |
|------|-----------|-----|-------|
| [sliding-tangent-basis.vex](sliding-tangent-basis.vex) | Local tangent basis {b1,b2} + per-neighbour exponential map Q' in ΨP | §3.1 | Run once on rest mesh; normal-curve approx for geodesic distance |
| [sliding-direction-propagate.vex](sliding-direction-propagate.vex) | BFS parallel transport of global direction {a1,a2} via `dihedral()` | §3.2, Eq. 4 | Iterate in For-Each SOP; @slide_done flag prevents re-processing |
| [sliding-displace.vex](sliding-displace.vex) | Cubic falloff tangential displacement + `xyzdist()` surface re-projection | §3.3, Eq. 5–8 | Two inputs: animated mesh + rest mesh for snapping |

### Quick-start parameter guide

**Full pipeline:**
```
rest_mesh → sliding-tangent-basis     (precompute {b1,b2}, stencil_uv, slide_N)
          → [set handle_pt, slide_radius, disp_d, falloff_power on detail]
          → initialize handle: slide_a1/a2=b1/b2, slide_done=1
          → For-Each (N iters) → sliding-direction-propagate  (BFS spread)
          → sliding-displace                                   (apply + snap)
```

| Attribute | Type | Meaning |
|-----------|------|---------|
| `handle_pt` | int (detail) | Index of handle (brush-centre nearest vertex) |
| `slide_radius` | float (detail) | Support region radius in world units |
| `disp_d` | vector (detail) | World-space displacement d (end_locator - start_locator) |
| `falloff_power` | float (detail) | Cubic falloff power p (default 3); or use painted `slide_weight` |
| `slide_active` | int (point) | 1 if within radius |
| `slide_done` | int (point) | 1 once {a1,a2} has been propagated to this vertex |

### Key formulas

**Exponential map image in ΨP (§3.1, first-ring approx):**
```vex
vector dQ_tan = dQ - dot(dQ, Nv) * Nv;   // project Q-P onto tangent plane
float u = dot(dQ_tan, b1);               // 2D local coords
float v = dot(dQ_tan, b2);
```

**Parallel transport via dihedral (§3.2):**
```vex
matrix3 R = dihedral(N_neighbour, N_current);  // minimal rotation N→N
vector  a1_transported = a1_neighbour * R;     // parallel-transport a1
```

**Displacement with falloff (§3.3, Eq. 7):**
```vex
float fo = pow(1.0 - pow(r/R, p), p);          // cubic falloff
vector dp = fo * (s * a1p + t * a2p);          // local tangent displacement
@P = snap_to_surface(@P + dp, rest_mesh);      // re-project
```

---

## Mesh Wrap — Affine-Invariant Coordinates (de Goes & Martinez 2019)

Source paper: [[papers/degoes-2019-mesh-wrap]]

| File | Algorithm | Eq. | Notes |
|------|-----------|-----|-------|
| [mesh-wrap-affine-coords.vex](mesh-wrap-affine-coords.vex) | Stencil dYi assembly + Wi nullspace (precomputation) | §4 | VEX gathers stencil; Python SVD computes Wi; Python builds sparse L |
| [mesh-wrap-project-score.vex](mesh-wrap-project-score.vex) | Closest-point projection Π(xi) + score mi = 1/(1 + µ‖pi−xi‖²) | §3 | Uses xyzdist(); µ ramped 0.1 → 100 over rounds |
| [mesh-wrap-distortion-energy.vex](mesh-wrap-distortion-energy.vex) | Per-vertex distortion ‖dXi Wi‖²_F (diagnostic / convergence) | §4 | Reads Wi_flat from source; evaluates current wrap quality |
| [mesh-wrap-solve.vex](mesh-wrap-solve.vex) | Apply solved X after Python Cholesky; full solve in comments (Eq. 2) | §5, Eq. 2 | Full Python sparse solve: (L + µM²+ κB²)X = rhs |

### Quick-start parameter guide

**Complete pipeline:**
```
SOURCE mesh S → mesh-wrap-affine-coords   (VEX: stencil dYi)
              → Python: Wi = null(dYi), build L
              → [repeat until convergence]
WRAP mesh M   → mesh-wrap-project-score   (VEX: pi, mi each iter)
              → Python: solve (L + µM² + κB²) X = rhs
              → mesh-wrap-solve            (VEX: @P = solved_P)
```

| Parameter | Typical value | Meaning |
|-----------|--------------|---------|
| `mu` | 0.1 → 1 → 10 → 100 | Fitting stiffness; ramped ×10 every 10 iters |
| `kappa` | 0.1 | Curve correspondence weight (fixed) |
| max iters | 100 (5 rounds × 10) | Stop when max(dist) < 1e-4 |

### Key formulas

**Affine-invariant coordinates (§4) — nullspace of stencil differences:**
```vex
// dYi[:,k] = yj_k - yi    (source stencil differences, 3×n)
// Wi = right null-vectors of dYi  (n × (n-3), via Python SVD)
// Property: dYi Wi = 0
```

**Score per vertex (§3):**
```vex
float dist2 = dot(proj_pos - @P, proj_pos - @P);
float score = 1.0 / (1.0 + mu * dist2);   // 1 on target, →0 far away
```

**Distortion energy at vertex i (§4):**
```vex
// C = dXi * Wi   (3 × (n-3))
// Ei = ||C||²_F  = sum of squared entries
// Global: X^T L X = sum_i Ei
```

**Global solve (§5, Eq. 2):**
```python
A   = L + mu * M.T @ M + kappa * B.T @ B
rhs = mu * M.T @ M @ P_proj + kappa * B.T @ Q
X   = spla.spsolve(A, rhs)   # per coordinate axis
```

---

## Blendshape Fitting — JTDP03 · FACEIT · Lewis 2014 STAR

Source papers: [[papers/jtdp-2003-blendshape-fitting]] · [[papers/faceit-diaz-barros]] · [[papers/lewis-2014-blendshape-star]]

| File | Algorithm | Source | Notes |
|------|-----------|--------|-------|
| [blendshape-eval.vex](blendshape-eval.vex) | Forward blendshape evaluation: delta (additive) + replacement conventions | Lewis 2014 STAR, Eq. 1–4 | `CONVENTION` param: 0=additive, 1=replacement |
| [blendshape-marker-softmax.vex](blendshape-marker-softmax.vex) | Softmax marker-to-vertex correspondence R(P_j) | JTDP03, Facial Similarity | Per-vertex; outputs `marker_similarity` float attr |
| [blendshape-qp-fit.vex](blendshape-qp-fit.vex) | QP blendshape weight solve from 3D markers + weight application | JTDP03 | Python SLSQP solve embedded; VEX apply pass |
| [blendshape-nlls-faceit.vex](blendshape-nlls-faceit.vex) | 2D landmark projection + NLLS weight solve (Levenberg-Marquardt) | FACEIT ~2020 | VEX camera projection; Python `least_squares` solve |
| [blendshape-corrective-psd.vex](blendshape-corrective-psd.vex) | Corrective shape weight evaluation: product, min, Gaussian RBF | Lewis 2014 STAR §3; Lewis 2000 PSD | `mode` param: 0=product, 1=min, 2=RBF |

### Quick-start parameter guide

**Forward evaluation pipeline:**
```
neutral_mesh  (input 0) + target_shapes (inputs 1..N)
detail attr "weights" (float[N]) → blendshape-eval.vex → @P updated
```

**Corrective pipeline (on top of primary eval):**
```
primary_weights → blendshape-corrective-psd → "corrective_weights" detail attr
corrective_shapes → blendshape-eval.vex (delta mode) → add to primary @P
```

**Performance-driven pipeline (3D markers, JTDP03):**
```
tracked_markers → blendshape-marker-softmax  (marker_similarity per vertex)
               → assemble V_j matrix in Python
               → blendshape-qp-fit (Python SLSQP) → "alpha_star" detail attr
               → blendshape-qp-fit (VEX apply pass) → @P
```

**Performance-driven pipeline (2D video, FACEIT):**
```
video frame + camera intrinsics
→ blendshape-nlls-faceit (VEX: uv_proj per vertex)
→ blendshape-nlls-faceit (Python: least_squares) → "alpha_star" detail attr
→ blendshape-qp-fit (VEX apply pass) → @P
```

| Attribute | Type | Where | Meaning |
|-----------|------|-------|---------|
| `weights` | float[] | detail | Primary blendshape weights w[0..N-1] |
| `alpha_star` | float[] | detail | Solved weights from QP/NLLS |
| `alpha_prev` | float[] | detail | Previous-frame weights (warm-start + temporal regularisation) |
| `temporal_weight` | float | detail | μ — temporal smoothness regulariser (default 0.01) |
| `marker_pos` | vector[] | detail | 3D marker positions M_i |
| `marker_conf` | float[] | detail | Per-marker confidence C_i (default 1.0) |
| `num_markers` | int | detail | Number of tracked markers |
| `sigma` | float | channel | Distance scale for softmax (default ~1.0) |
| `cam_K` | float[9] | detail | Camera intrinsic matrix (row-major 3×3) |
| `cam_R` | float[9] | detail | Camera rotation (row-major 3×3) |
| `cam_t` | vector | detail | Camera translation |
| `corr_drivers_m` | int[] | detail | Driver indices for corrective m |
| `corr_exponents_m` | float[] | detail | Exponents per driver for product rule |
| `corr_centre_m` | float[] | detail | RBF centre in driver weight space |
| `corr_sigma_m` | float | detail | RBF bandwidth for corrective m |

### Key formulas

**Delta blendshape (Lewis 2014 STAR, Eq. 3–4):**
```vex
vector acc = {0,0,0};
for (int k = 0; k < N; k++)
    acc += weights[k] * (target_pos[k] - base_pos);   // B * w
@P = base_pos + acc;
```

**Marker similarity softmax (JTDP03):**
```vex
// For vertex P_j and N markers M_i with confidence C_i:
float R = sum_i(exp(-dist(M_i,P_j)/sigma) * C_i)
        / sum_i(exp(-dist(M_i,P_j)/sigma));
```

**QP objective (JTDP03):**
```math
\min_\alpha \sum_j \|M_j - V_j(\alpha)\|^2 + \mu \|\nabla\alpha\|^2
\quad \text{s.t.} \quad \sum_i \alpha_i = 1,\; \alpha_i \geq 0
```

**FACEIT 2D landmark objective:**
```math
\min_\alpha \sum_j \|L_j - \Pi(V_j(\alpha), \text{pose})\|^2 + \mu \|\nabla\alpha\|^2
```

**Product corrective (Lewis 2014 STAR §3):**
```vex
float w_corr = 1.0;
for (int k = 0; k < K; k++)
    w_corr *= pow(primary_w[drivers[k]], exponents[k]);
```

---

## RBF (Radial Basis Functions) — Lewis 2000, Animatomy §5.5, MetaHuman, Waters 1987

Source papers: [[papers/lewis-2000-psd]] · [[papers/choi-2022-animatomy]] · [[papers/epic-2021-metahuman-rig]] · [[papers/waters-1987-muscle-model]]

| File | Algorithm | Source | Notes |
|------|-----------|--------|-------|
| [rbf-kernels.vex](rbf-kernels.vex) | Complete RBF kernel library: Gaussian, multiquadric, inv-MQ, TPS, linear, cubic, Wendland C2 | Buhmann 2003; Lewis 2000 | `rbf_kernel` int selects; includes kernel selection guide table |
| [rbf-gram-matrix.vex](rbf-gram-matrix.vex) | Offline Gram matrix assembly Φ_ij = φ(‖x_i−x_j‖) + Python solve Φλ = f | Lewis 2000 §2 | Single-threaded; Python Tikhonov solve embedded in comments |
| [rbf-eval.vex](rbf-eval.vex) | Runtime: f(x) = Σ λ_i φ(‖x−x_i‖); normalized mode for Animatomy jaw proxy | Lewis 2000, Animatomy §5.5 | `rbf_normalize=1` → Shepard-style; handles any dimension D and output K |
| [rbf-psd-pose.vex](rbf-psd-pose.vex) | Pose parameterization: blendshape weights (mode 0), quaternions (mode 1), rotation matrix delta R−R* (mode 2) | Lewis 2000; SMPL §3.1; Animatomy §5.2 | Three modes; outputs detail "pose_vec" as RBF input |
| [rbf-psd-correctives.vex](rbf-psd-correctives.vex) | Full PSD corrective evaluation: per-corrective Gaussian RBF → weight → apply delta to @P | Lewis 2000 §2; epic-2021 MetaHuman | Handles n_corr correctives with per-corrective driver subsets; performance skip <1e-5 |
| [rbf-scattered-interp.vex](rbf-scattered-interp.vex) | 3D scattered data interpolation; Waters muscle influence zones (linear + sphincter) inline | Waters 1987; Buhmann 2003 | Shepard fallback if no solve; Waters linear/sphincter muscles in comments |

### Quick-start: Pose Space Deformation (Lewis 2000 / MetaHuman style)

```
OFFLINE (rig build):
  example_poses geometry (N points, "pose_vec" float[D], "target_val" float[K])
  → rbf-gram-matrix.vex   (VEX: Gram matrix assembly)
  → Python: solve Φλ = F  → "lambda_vec" float[K] per example point

RUNTIME (every frame):
  current_rig_state → rbf-psd-pose.vex     (mode 0: "pose_vec" = primary weights)
  rbf_centers + rbf_lambdas (from offline)
  → rbf-psd-correctives.vex               (per corrective RBF eval + apply delta)
```

### Quick-start: General Scattered Interpolation (Shepard, no solve needed)

```
scattered_sites (input 1, "data_val" float[K] per point, no "rbf_lambdas" needed)
query_mesh      (input 0)
  → rbf-scattered-interp.vex  (rbf_normalize=1 for Shepard)
  → "rbf_interp" float[K] per query vertex
```

### Key formulas

**Gaussian kernel (Lewis 2000 — standard for PSD):**
```vex
float phi = exp(-(eps*eps) * dist2);   // dist2 = ||pose - center||²
```

**Full RBF evaluation:**
```vex
float w_m = 0;
for (int i = 0; i < N; i++)
    w_m += lambda[i] * exp(-(eps*eps) * dist2(query_pose, center[i]));
w_m = clamp(w_m, 0.0, 1.0);
@P += w_m * corrective_delta[@ptnum];
```

**Normalized Gaussian (Animatomy jaw, rbf-eval.vex with normalize=1):**
```vex
float phi_i = exp(-(sigma_i*sigma_i) * dot(p - mu_i, p - mu_i));
out += lambda_i * phi_i;
phi_sum += phi_i;
out /= phi_sum;   // prevents drift outside training set
```

**Pose vector: rotation matrix delta (SMPL/Animatomy mode 2):**
```vex
pv[9*k..9*k+8] = R_curr[k] - R_rest[k];   // 9-vector per joint k
```

**Waters linear muscle (from rbf-scattered-interp.vex):**
```vex
float w = max(0.0, 1.0 - dist(@P, origin) / d_max);
@P += w * activation * normalize(insertion - origin) * scale;
```

**Tikhonov regularization (Python solve):**
```python
Phi_reg = Phi + 1e-5 * np.eye(N)
Lambdas = np.linalg.solve(Phi_reg, F)   # F = target values at examples
```

### Kernel selection guide

| Kernel | Type | Key property | Best use in rigging |
|--------|------|-------------|---------------------|
| Gaussian | PD | Smooth, narrow | PSD correctives (Lewis 2000, MetaHuman) |
| Inv. multiquadric | PD | Smooth, wide | General interpolation |
| Wendland C2 | PD + compact | Sparse Gram matrix | Large N (>50 example poses) |
| Cubic r³ | Semi-PD | Simple, stable | Deformation fields |
| Linear r | Semi-PD | Minimal | Rough region maps |
| TPS (r² ln r) | Semi-PD + poly | Minimal bending | 2D expression retargeting |
| Normalized Gauss | Partition-of-unity | No drift | Jaw proxy, region blends |

---

## Forearm Twist — Swing-Twist Decomposition

Source: General character rigging technique (game/film industry standard); see [[techniques/forearm-partial-twist]] · [[concepts/linear-blend-skinning]]

| File | Algorithm | Notes |
|------|-----------|-------|
| [forearm-partial-twist.vex](forearm-partial-twist.vex) | Swing-Twist quaternion decomposition → partial forearm pronation/supination | `twist_fraction` ∈ [0,1]: 0.33 = upper forearm, 0.66 = lower, 1.0 = wrist |

### Problem

When the hand rotates around the forearm axis (pronation/supination), a naive single-joint wrist produces a sharp candy-wrapper twist at the wrist. The fix: insert one or two intermediate forearm joints that each receive a *fraction* of the total twist, so the deformation rolls gradually along the arm.

### Quick-start parameter guide

Setup: **Geometry Wrangle SOP on a 1-point geometry** (not per-vertex).

| Attribute | Type | Where | Meaning |
|-----------|------|-------|---------|
| `elbow_xform` | matrix4 | detail | Elbow joint world-space transform |
| `hand_xform` | matrix4 | detail | Hand/wrist joint world-space transform |
| `twist_fraction` | float | detail | 0 = no twist (elbow), 1 = full wrist twist |
| `twist_axis` | vector | detail | Bone roll axis in elbow local space (default `{1,0,0}`) |
| `use_inputs` | int | detail | 1 = read xforms from SOP inputs 1 & 2 instead of detail attrs |

**Output:** `forearm_xform` (matrix4), `forearm_r` (euler), `forearm_t` (position) on detail.

**Typical chain:**
```
UpperArm → Elbow → ForearmTwist1 (t=0.33) → ForearmTwist2 (t=0.66) → Wrist (t=1.0) → Hand
```

Run this snippet twice (once per twist joint) with different `twist_fraction` values.

### Key formulas

**Swing-Twist decomposition (any quaternion Q around axis A):**
```vex
vector imag   = set(q.x, q.y, q.z);       // imaginary part (axis × sin θ/2)
float  proj   = dot(imag, A);              // projection length
vector proj_v = proj * A;                  // projected onto twist axis
vector4 twist_q = normalize({proj_v.x, proj_v.y, proj_v.z, q.w});
// swing_q = q * conjugate(twist_q)  (ignored here)
```

**Partial twist via slerp:**
```vex
vector4 identity_q    = {0, 0, 0, 1};
vector4 partial_twist = slerp(identity_q, twist_q, t);
// Hemisphere check (prevent long-path slerp):
if (dot(partial_twist, identity_q) < 0)
    partial_twist = -partial_twist;
```

**Final joint transform:**
```vex
matrix3 final_rot3 = elbow_rot * qconvert(partial_twist);
vector  joint_pos  = lerp(elbow_pos, hand_pos, t);
```

---

## Health summary

- **7** snippets — Regularized Kelvinlets + Sharp Kelvinlets (all algorithms)
- **3** snippets — Curvenet / Profile Curves (frames, Laplacian, deform+solve)
- **3** snippets — Cage deformation: Green Coordinates + Somigliana Coordinates
- **4** snippets — Bounded Biharmonic Weights (cotan Laplacian, mass matrix, LBS, harmonic)
- **5** snippets — Animatomy: muscle strain, strain blendshapes, pose correctives, jaw RBF, full model
- **5** snippets — Wrinkle Systems: stress vector, proximity metric, curve displacement, blend, mesh tension
- **3** snippets — Sliding Deformation (tangent basis, direction propagation, surface displacement)
- **4** snippets — Mesh Wrap: affine-invariant coordinates, projection, distortion, solve
- **5** snippets — Blendshape Fitting: eval (delta + replacement), marker softmax, QP fit, NLLS/FACEIT, PSD correctives
- **6** snippets — RBF Techniques: kernel library, Gram matrix+solve, runtime eval, pose parameterization, PSD correctives, scattered interpolation
- **1** snippet  — Forearm Twist: swing-twist decomposition for pronation/supination correction
- **Total: 46 snippets across 13 papers + 1 general technique**

Not yet implemented: Dynamic Kelvinlets (2018), Delta Mush, ARAP, Stochastic Barycentric Coordinates, CoR Skinning, Rig-Space Secondary Motion.
