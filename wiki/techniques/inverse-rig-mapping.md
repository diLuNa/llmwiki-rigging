---
title: "Inverse Rig Mapping — Analytically Learning the Rig Jacobian"
tags: [rig-generation, pose-space, math, python, vex, houdini, kine-fx]
---

## Overview

**Inverse rig mapping** solves the problem of recovering high-level rig control parameters from skeleton joint transforms. Given a target pose — from mocap retargeting, a crowd system, or a pose library — find the rig parameter vector β such that the rig's forward function F(β) produces joint transforms closest to that target.

The naive approach evaluates the rig thousands of times per frame to estimate a numerical Jacobian. Gustafson, Lo & Kanyuk (Pixar, SIGGRAPH Talks 2020) solve this by **learning an analytic approximation of the rig function offline**, making per-frame Jacobian evaluation effectively free, and enabling real-time inversion of hero-quality rigs.

Source paper: [[papers/gustafson-2020-inverse-rig]]  
Python implementation: [[python/inverse_rig_mapping.py]]  
VEX implementation: [[vex/inverse-rig-mapping.vex]]

---

## The Problem

A production rig maps high-level abstract controls to skeleton poses:

```
F : β ∈ ℝⁿ → [J₀, J₁, ..., Jₖ]    (joint local transforms)
```

β might encode slider positions, blend weights, custom attributes — not joint angles. Motion systems (crowds, retargeting, physics simulation) produce joint angles; the rig expects β. The inversion is needed whenever you want to:

- Apply a procedural skeleton edit and transfer it to the full rig for polish
- Drive a hero rig from mocap that came in as joint rotations
- Pose-match a hero rig to a crowd or physics skeleton

Iterative least-squares inversion (Gauss-Newton) requires the Jacobian:

```
J[i, k] = ∂(pose[i]) / ∂(β[k])
```

Computing this numerically means evaluating F once per parameter per iteration — thousands of rig evaluations per frame on a large rig. The paper reports **~5000× speedup** from using an analytic Jacobian instead.

---

## The Key Insight: Operators

Most rig parameters, **when varied in isolation with all others at zero**, do something simple: they rotate one joint about a fixed axis at a constant rate, or translate one joint along a fixed direction. The paper calls these **operators**:

| Operator | Forward function | dMatrix/dParam |
|----------|-----------------|----------------|
| `RotationOp(axis, rate)` | `R(β) = exp([axis]× · rate · β)` | `R · [axis]× · rate` |
| `TranslationOp(direction)` | `T(β) = I + direction · β` | constant `direction` in translation column |
| `ForearmTwistOp(joints, fractions)` | per-joint `R(frac·β)` | per-joint `R · [axis]× · rate · frac` |

If you can identify which operator each parameter is, you have a **closed-form Jacobian** — no rig evaluations needed at runtime.

---

## The Three Stages

### Stage 1: Classification (Offline)

For each parameter β_i, hold all others at zero and sample several values λ:

```python
beta = zeros(n_params)
for λ in [0.1, 0.3, 0.5, 0.7, 1.0]:
    beta[i] = λ
    pose = rig(beta)
    M_rel_j(λ) = pose[j] @ inv(pose0[j])   # relative effect on joint j
```

`M_rel_j(λ)` is a curve of transforms parameterized by λ. Classify by asking:

**RotationOp test:** Is `M_rel` a pure rotation? Is the rotation axis consistent across all λ? Is the angle proportional to λ?

```python
rot_vecs = [log_map(M_rel(λ)) for λ in lambdas]
angles   = [norm(rv) for rv in rot_vecs]
# Proportionality: angle / λ ≈ constant (std < 5% of mean)
# Axis consistency: all rot_vecs point in same direction (dot ≈ ±1)
```

**TranslationOp test:** Is `M_rel[:3,:3] ≈ I`? Is the translation proportional to λ?

**ForearmTwistOp test:** Multiple joints affected, all rotating about the same axis, with rates proportional to a monotonically increasing sequence (cumulative fractions).

Parameters that fit no pattern within tolerance σ are **discarded** — their pose effect is too nonlinear to model analytically.

### Stage 2: Sorting (Offline)

Matrix multiplication is non-commutative: operator order matters when two parameters affect the **same joint**. The pairwise test (Eq. 6 from paper):

> X precedes Y in composition if and only if varying Y does not change X's apparent effect.

```python
# Test: does Y change what X does?
LHS = (Y_zero ∘ X_alpha) @ inv(Y_zero ∘ X_zero)
RHS = (Y_beta ∘ X_alpha) @ inv(Y_beta ∘ X_zero)
X_precedes_Y = allclose(LHS, RHS)
```

In words: zero Y, measure what X does. Then set Y nonzero, measure what X does again. If they're the same, X is applied first. Run this for all pairs affecting the same joint; sort by insertion.

### Stage 3: Inversion (Runtime, Real-Time)

With operators classified and sorted, the analytic Jacobian is:

```python
# For RotationOp at joint j with param k:
R    = rotation_matrix(op.axis, op.rate * beta[k])
dR   = R @ skew(op.axis) * op.rate        # dR/d(beta_k)
dRV  = log_map_jacobian(R) @ vee(dR)      # d(rotvec)/d(beta_k)
J[3j:3j+3, k] = dRV
```

The **log-map Jacobian** (right Jacobian inverse of SO(3)) converts from matrix derivative to rotation-vector derivative:

```
J_r⁻¹ = I + ½[rv]× + a·[rv]×²
a = 1/θ² − sin(θ)/(2θ(1−cos(θ)))      (θ = ‖rv‖)
```

Falls back to `vee(dR)` at θ < 1e-8 (near-identity).

With the Jacobian available, **Gauss-Newton** solves the inversion:

```
JᵀJ · Δβ = Jᵀ · r         (normal equations)
r = target_pose − F̂(β)     (residual in rotation-vector space)
β ← β + Δβ
```

Iterate ~30 times. If the residual stalls (JᵀJ poorly conditioned), switch to **Levenberg-Marquardt**:

```
(JᵀJ + λ·diag(JᵀJ)) · Δβ = Jᵀ · r     (LM damping)
```

Because the approximation F̂ is stateless (no rig dependencies), all Jacobian columns are independent and can be computed in parallel — this is the primary source of speedup.

---

## Arm + Forearm + Hand Example

A seven-parameter arm rig with three procedural forearm twist joints demonstrates the full classification pipeline including **CompoundOp** — one parameter driving heterogeneous operators on multiple joints simultaneously:

```
Parameters: shoulder_rx, shoulder_ry, shoulder_rz, elbow_bend, hand_rx, hand_ry, hand_rz
Joints:     shoulder(0), elbow(1), forearm_1(2), forearm_2(3), forearm_3(4), hand(5)
```

**Forward kinematics:**

```python
R_shoulder = Rx(sx) @ Ry(sy) @ Rz(sz)   # ZYX Euler, 3 parameters
R_elbow    = Rx(eb)                       # pure Rx hinge, 1 parameter
inc        = hx / 3.0                     # forearm incremental twist
R_forearm1 = Rx(inc)                      # cumulative twist: hx/3
R_forearm2 = Rx(inc)                      # cumulative twist: 2*hx/3
R_forearm3 = Rx(inc)                      # cumulative twist: hx
R_hand     = Rx(hx) @ Ry(hy) @ Rz(hz)   # ZYX Euler, 3 parameters
```

The forearm joints are **procedural** — they are not driven by independent rig controls. Instead, `hand_rx` simultaneously drives a `ForearmTwistOp` (joints 2,3,4) and a `RotationOp` (joint 5). The classification algorithm detects this by sampling `hand_rx` in isolation: four joints respond, with rates 1/3, 1/3, 1/3, 1.0. The rate-grouping step produces a `CompoundOp` wrapping:

- `ForearmTwistOp(joints=[2,3,4], fractions=[1/3, 2/3, 1.0], axis=X, rate=1.0)` — equal-rate group
- `RotationOp(joint=5, axis=X, rate=1.0)` — single-joint group

**Classified operators:**

| Parameter | Operator type | Joints affected | Notes |
|-----------|--------------|-----------------|-------|
| shoulder_rx | RotationOp(X, rate=1.0) | joint 0 | |
| shoulder_ry | RotationOp(Y, rate=1.0) | joint 0 | |
| shoulder_rz | RotationOp(Z, rate=1.0) | joint 0 | |
| elbow_bend | RotationOp(X, rate=1.0) | joint 1 | |
| hand_rx | **CompoundOp** | joints 2,3,4,5 | ForearmTwistOp(2,3,4) + RotationOp(5) |
| hand_ry | RotationOp(Y, rate=1.0) | joint 5 | |
| hand_rz | RotationOp(Z, rate=1.0) | joint 5 | |

**Jacobian structure (18 × 7):**

```
               sh_rx  sh_ry  sh_rz  el_bend  hand_rx  hand_ry  hand_rz
joint 0 x:       1      0      0      0        0        0        0
joint 0 y:       0      1      0      0        0        0        0
joint 0 z:       0      0      1      0        0        0        0
joint 1 x:       0      0      0      1        0        0        0
joint 1 y:       0      0      0      0        0        0        0
joint 1 z:       0      0      0      0        0        0        0
joint 2 x:       0      0      0      0       1/3       0        0     ← forearm_1
joint 2 y:       0      0      0      0        0        0        0
joint 2 z:       0      0      0      0        0        0        0
joint 3 x:       0      0      0      0       1/3       0        0     ← forearm_2
joint 3 y:       0      0      0      0        0        0        0
joint 3 z:       0      0      0      0        0        0        0
joint 4 x:       0      0      0      0       1/3       0        0     ← forearm_3
joint 4 y:       0      0      0      0        0        0        0
joint 4 z:       0      0      0      0        0        0        0
joint 5 x:       0      0      0      0        1        0        0     ← hand
joint 5 y:       0      0      0      0        0        1        0
joint 5 z:       0      0      0      0        0        0        1
```

At rest (β = 0) all blocks are identity-diagonal except the `hand_rx` column (index 4), which has values 1/3 at the three forearm rx rows and 1.0 at the hand rx row. This makes `JᵀJ[4,4] = 3*(1/3)² + 1² = 4/3` — the only non-unit diagonal entry. Gauss-Seidel handles this correctly because the off-diagonal coupling of `hand_rx` with `hand_ry/rz` is zero (orthogonal axes at rest). At nonzero β, the log-map Jacobian chain rule captures ZYX Euler coupling analytically.

**Elbow rows 4, 5 are zero** — the elbow is a pure Rx hinge. The solver exploits this sparsity through the JᵀJ structure automatically.

---

## Python Usage

Source: [[python/inverse_rig_mapping.py]]

```python
import numpy as np
from inverse_rig_mapping import ArmRig, LearnedRigApproximation, RigInverter

# 1. Define rig (or wrap your own via rig_fn callable)
rig = ArmRig()
# Params:  shoulder_rx, shoulder_ry, shoulder_rz, elbow_bend, hand_rx, hand_ry, hand_rz
# Joints:  shoulder(0), elbow(1), forearm_1(2), forearm_2(3), forearm_3(4), hand(5)
# hand_rx is a CompoundOp: drives forearm_1/2/3 (ForearmTwistOp) AND hand (RotationOp)

# 2. Offline: classify operators + sort composition order
#    Classification auto-detects the CompoundOp from rate-grouping:
#    forearm joints respond at rate=1/3, hand at rate=1.0 → CompoundOp
approx = LearnedRigApproximation.train(
    rig.evaluate, rig.num_params, rig.num_joints,
    test_lambdas=[0.1, 0.3, 0.5, 0.7, 1.0],
    sigma=1e-3
)

# 3. Create inverter
inverter = RigInverter(approx)

# 4. Per-frame: invert a target pose
beta_target = np.array([0.3, 0.1, -0.2, 0.8, 0.2, -0.1, 0.4])
target_joints = rig.evaluate(beta_target)   # list of 6 × (4×4) matrices (incl. forearm joints)

beta_solved, info = inverter.invert(target_joints)
# info: {'iters': 3, 'residual': 1.8e-9, 'method': 'GN'}

# Validate
print(np.linalg.norm(beta_solved - beta_target))   # → < 1e-5 for linear rig
```

**Custom rig integration:**

```python
# rig_fn(beta: np.ndarray) must return List[np.ndarray] of (4×4) local transforms
def my_rig_fn(beta):
    # Call your DCC or evaluation system here
    return [joint.local_matrix for joint in evaluate_rig(beta)]

approx = LearnedRigApproximation.train(my_rig_fn, n_params=150, n_joints=80)
```

---

## Houdini VEX Usage (KineFX)

Source: [[vex/inverse-rig-mapping.vex]]

Three snippets covering the full pipeline:

**Snippet A — Python SOP (offline setup):**

```python
# Run once; writes Jacobian columns as detail float[] attributes
from inverse_rig_mapping import ArmRig, LearnedRigApproximation
import numpy as np

rig    = ArmRig()
approx = LearnedRigApproximation.train(rig.evaluate, rig.num_params, rig.num_joints)
J      = approx.jacobian(np.zeros(rig.num_params))   # (15, 5)

geo = hou.pwd().geometry()
geo.setGlobalAttribValue("n_params", rig.num_params)
geo.setGlobalAttribValue("n_joints", rig.num_joints)
for k in range(rig.num_params):
    geo.setGlobalAttribValue(f"jac_col_{k}", J[:, k].tolist())
geo.setGlobalAttribValue("pose_rest", approx.evaluate(np.zeros(rig.num_params)).tolist())
```

**Snippet B — KineFX Geometry Wrangle (per frame):**

```vex
// Reads: n_params, n_joints, jac_col_k, target_pose, pose_rest
// Writes: beta_solved, shoulder_rx/ry/rz, elbow_bend, forearm_twist

// Gauss-Newton: JᵀJ · Δβ = Jᵀ · r
// r = target_pose - pose_rest  (linearized at rest)
// Solved via Gauss-Seidel iterations (avoids matrix inversion in VEX)
```

**Snippet C — Standalone arm + forearm + hand example (no setup needed):**

```vex
// Hardcoded 18×7 Jacobian for the 7-param arm+forearm+hand rig.
// 6 joints: shoulder(0), elbow(1), forearm_1(2), forearm_2(3), forearm_3(4), hand(5)
// Set "target_pose" (18 floats) on a 1-point geometry.
// Outputs beta_solved, shoulder_rx/ry/rz, elbow_bend, hand_rx/ry/rz, residual.
Jc[ 0 * 7 + 0] = 1.0;        // shoulder_rx → joint 0 x
Jc[ 1 * 7 + 1] = 1.0;        // shoulder_ry → joint 0 y
Jc[ 2 * 7 + 2] = 1.0;        // shoulder_rz → joint 0 z
Jc[ 3 * 7 + 3] = 1.0;        // elbow_bend  → joint 1 x  (ry/rz rows 4,5 stay zero)
Jc[ 6 * 7 + 4] = 1.0/3.0;   // hand_rx → forearm_1 x   (CompoundOp ForearmTwistOp)
Jc[ 9 * 7 + 4] = 1.0/3.0;   // hand_rx → forearm_2 x   (CompoundOp ForearmTwistOp)
Jc[12 * 7 + 4] = 1.0/3.0;   // hand_rx → forearm_3 x   (CompoundOp ForearmTwistOp)
Jc[15 * 7 + 4] = 1.0;        // hand_rx → hand x        (CompoundOp RotationOp)
Jc[16 * 7 + 5] = 1.0;        // hand_ry → hand y
Jc[17 * 7 + 6] = 1.0;        // hand_rz → hand z
// JᵀJ[4,4] = 3*(1/3)² + 1² = 4/3  (hand_rx column is non-unit diagonal)
```

---

## Gotchas & Limitations

### 1. Approximation error for nonlinear parameters
The analytic approximation is exact only for parameters that are truly linear-in-angle. Parameters that drive sigmoid blends, multiple axes simultaneously, or have discontinuities will be either misclassified (wrong operator type) or discarded. Post-inversion residual indicates the quality — a residual above ~0.05 rad suggests poor approximation coverage.

### 2. Composition order matters for same-joint parameters
If two parameters both affect joint 0, their order changes the result. The sorting step (Stage 2) handles this, but if the rig's internal order changes (e.g., after a rig update), the approximation must be retrained.

### 3. Discarded parameters create a gap
Parameters that fail classification are not modeled. Their effect on pose is unrecoverable by the inverter. If a discarded parameter is important (e.g., a volume-preservation control), the inversion will leave a systematic residual in the joints it drives.

### 4. Jacobian linearization is at current β
The analytic Jacobian is computed at the current parameter estimate, not globally. For large parameter ranges (β > 1.5 rad), re-linearizing each Gauss-Newton iteration improves convergence. The `RigInverter.invert()` does this automatically.

### 5. VEX has no native linear solver
For n_params > ~10, Gauss-Seidel on the normal equations becomes slow. In Houdini, prefer pushing the solve to a Python SOP for large rigs, and using VEX only for the forward approximation evaluation.

---

## Performance Notes

From Gustafson et al. (Pixar crowds pipeline):

| Step | Cost |
|------|------|
| Offline classification | `n_params × n_lambdas` rig evaluations (~seconds) |
| Offline sorting | `O(n_params²)` rig evaluations |
| Per-frame Jacobian | Analytic, negligible (all columns parallelizable) |
| Per-frame Gauss-Newton | ~2ms per character (30 iterations × small linear solve) |
| Speedup vs. numerical Jacobian | **~5000×** |

The speedup scales with `n_params`: a 200-parameter rig that previously needed 200 rig evaluations per Gauss-Newton iteration now needs zero.

---

## Comparison With Related Approaches

| Approach | Jacobian | Training | Accuracy | Runtime |
|----------|----------|----------|----------|---------|
| **Analytic rig approximation (this technique)** | Analytic, free | Offline sampling + classification | Exact for linear params | ~2ms |
| Numerical Jacobian (finite difference) | `n_params` rig evals/iter | None | Exact | Slow (×n_params) |
| Neural approximation (FaceBaker [[papers/radzihovsky-2020-facebaker]]) | Autodiff | Large training set | Approximate | Fast (GPU) |
| Dem Bones / SSDR [[techniques/dem-bones]] | Not applicable | Pose sequence | N/A (different problem) | Offline |
| ML Deformer [[techniques/ml-deformer]] | Not applicable | Supervised mesh pairs | Approximate | Inference-time |

---

## Related

- [[papers/gustafson-2020-inverse-rig]] — source paper
- [[python/inverse_rig_mapping.py]] — full Python implementation
- [[vex/inverse-rig-mapping.vex]] — Houdini VEX implementation (3 snippets)
- [[techniques/forearm-partial-twist]] — the forearm twist technique used in the arm example
- [[papers/radzihovsky-2020-facebaker]] — neural alternative for facial rigs
- [[concepts/rig-inversion]] — concept page
