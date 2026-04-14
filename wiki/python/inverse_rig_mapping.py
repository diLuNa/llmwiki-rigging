"""
inverse_rig_mapping.py
======================
Implementation of: "Analytically Learning an Inverse Rig Mapping"
  Gustafson, Lo, Kanyuk — SIGGRAPH Talks 2020  (Pixar Animation Studios)

Core Pipeline
─────────────
1. CLASSIFICATION  (offline)
   Sample the rig function F(β) → pose by varying each parameter β_i
   individually. Analytically identify each parameter's operator type
   (RotationOp | TranslationOp) and fit its axis/rate.

2. SORTING  (offline)
   Determine the composition order of operators using pairwise tests.
   Key insight: if X precedes Y, then varying Y should not change the
   apparent effect of X, i.e. (Y₀ ∘ X_α)(Y₀ ∘ X₀)⁻¹ = (Yβ ∘ X_α)(Yβ ∘ X₀)⁻¹.

3. INVERSION  (runtime, real-time)
   Gauss-Newton on the analytic approximation F̂(β).
   Because F̂ is stateless, all Jacobian columns can be parallelised.
   Fallback to Levenberg-Marquardt if GN stalls.

Arm + Hand + Forearm Partial Twist Example
──────────────────────────────────────────
   Rig parameters : shoulder_rx, shoulder_ry, shoulder_rz,
                    elbow_bend,
                    hand_rx, hand_ry, hand_rz
   Skeleton joints: shoulder, elbow, forearm_1, forearm_2, forearm_3, hand  (6 joints)

   shoulder:   ZYX Euler (Rx @ Ry @ Rz)
   elbow:      pure bend about local X
   forearm_1/2/3: procedural — each receives hand_rx / 3 (partial twist extraction)
   hand:       ZYX Euler (Rx @ Ry @ Rz)

   The forearm joints are driven by the hand_rx parameter (the X-axis component of
   the hand rotation, which approximates the twist around the forearm bone axis).
   hand_rx is therefore a CompoundOp: it drives ForearmTwistOp(joints 2,3,4) AND
   RotationOp(joint 5) simultaneously.

Usage
─────
   rig   = ArmRig()
   model = LearnedRigApproximation.train(rig.evaluate, rig.num_params, rig.num_joints)
   inv   = RigInverter(model)

   target = rig.evaluate([0.3, 0.1, -0.2, 0.8, 0.2, -0.1, 0.4])
   solved = inv.invert(target)                           # recover rig params
"""

from __future__ import annotations
import numpy as np
from scipy.spatial.transform import Rotation
from dataclasses import dataclass
from typing import Optional, List, Callable, Tuple

# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _skew(u: np.ndarray) -> np.ndarray:
    """3×3 skew-symmetric (cross-product) matrix of unit vector u."""
    return np.array([[ 0,    -u[2],  u[1]],
                     [ u[2],  0,    -u[0]],
                     [-u[1],  u[0],  0   ]], dtype=float)


def _rot_matrix(axis: np.ndarray, angle: float) -> np.ndarray:
    """4×4 rotation matrix: angle (radians) about axis (unit vector)."""
    M = np.eye(4)
    M[:3, :3] = Rotation.from_rotvec(angle * axis).as_matrix()
    return M


def _mat_to_rotvec(M44: np.ndarray) -> np.ndarray:
    """Extract rotation vector from the upper-left 3×3 of a 4×4 matrix."""
    return Rotation.from_matrix(M44[:3, :3]).as_rotvec()


def _pose_to_vec(pose: List[np.ndarray]) -> np.ndarray:
    """Flatten list of per-joint rotation vectors → 1-D array (3*n_joints,)."""
    return np.concatenate([_mat_to_rotvec(M) for M in pose])


def _vec_to_pose_shape(vec: np.ndarray) -> List[np.ndarray]:
    """Unflatten rotation-vector array → list of 4×4 rotation matrices."""
    n = len(vec) // 3
    out = []
    for i in range(n):
        rv = vec[3*i: 3*i+3]
        M = np.eye(4)
        M[:3, :3] = Rotation.from_rotvec(rv).as_matrix()
        out.append(M)
    return out


# ══════════════════════════════════════════════════════════════════════════════
# Operator Types (analytic rig approximation primitives)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class RotationOp:
    """
    Rotation about a fixed axis, linearly proportional to the parameter.
      matrix(p) = Rot(axis, rate * p)
    Affects joint `joint_idx` only. `rate` is radians per unit parameter.
    """
    joint_idx: int
    axis:      np.ndarray   # unit vector in local joint frame
    rate:      float        # radians / unit parameter


    def matrix(self, param: float) -> np.ndarray:
        return _rot_matrix(self.axis, self.rate * param)


    def dmatrix_dparam(self, param: float) -> np.ndarray:
        """
        Analytic d/dparam of the 4×4 rotation matrix.
          dR/dθ = R · [axis]_×    →    dR/dparam = R · [axis]_× · rate
        """
        angle = self.rate * param
        R  = Rotation.from_rotvec(angle * self.axis).as_matrix()
        dR = R @ _skew(self.axis) * self.rate
        dM = np.zeros((4, 4))
        dM[:3, :3] = dR
        return dM


@dataclass
class TranslationOp:
    """
    Translation proportional to the parameter.
      matrix(p) = T(direction * p)
    Affects joint `joint_idx` only.
    """
    joint_idx: int
    direction: np.ndarray   # translation per unit parameter (local units)


    def matrix(self, param: float) -> np.ndarray:
        M = np.eye(4)
        M[:3, 3] = self.direction * param
        return M


    def dmatrix_dparam(self, param: float) -> np.ndarray:
        dM = np.zeros((4, 4))
        dM[:3, 3] = self.direction
        return dM


@dataclass
class ForearmTwistOp:
    """
    Special composite operator: distributes rotation across multiple joints
    with per-joint fractions (partial-twist / pronation-supination rig).

    Each joint k receives:
      local Rot(axis, rate * fractions[k] * param)

    This is NOT decomposable to a single RotationOp because it acts on
    multiple joints simultaneously. Classified separately.
    """
    joint_indices: List[int]
    fractions:     List[float]  # e.g. [1/3, 2/3, 1.0]  (cumulative world)
    axis:          np.ndarray   # unit twist axis (typically X in forearm frame)
    rate:          float        # radians / unit parameter (full twist)

    def local_fractions(self) -> List[float]:
        """Convert cumulative fractions to incremental local fractions."""
        fracs = list(self.fractions)
        inc = [fracs[0]] + [fracs[i] - fracs[i-1] for i in range(1, len(fracs))]
        return inc

    def matrices(self, param: float) -> List[Tuple[int, np.ndarray]]:
        """Return list of (joint_idx, 4×4 matrix) pairs."""
        out = []
        for j_idx, frac in zip(self.joint_indices, self.local_fractions()):
            M = _rot_matrix(self.axis, self.rate * frac * param)
            out.append((j_idx, M))
        return out

    def dmatrices_dparam(self, param: float) -> List[Tuple[int, np.ndarray]]:
        """Return analytic Jacobian contributions for each affected joint."""
        out = []
        for j_idx, frac in zip(self.joint_indices, self.local_fractions()):
            angle = self.rate * frac * param
            R     = Rotation.from_rotvec(angle * self.axis).as_matrix()
            dR    = R @ _skew(self.axis) * (self.rate * frac)
            dM    = np.zeros((4, 4))
            dM[:3, :3] = dR
            out.append((j_idx, dM))
        return out


@dataclass
class CompoundOp:
    """
    One rig parameter driving multiple operators simultaneously.

    Used when a single parameter has heterogeneous effects: e.g. hand_rx drives
    a ForearmTwistOp (partial twist across forearm_1/2/3) AND a RotationOp on
    the hand joint.  sub_ops is an ordered list of RotationOp / TranslationOp /
    ForearmTwistOp, all evaluated at the same scalar parameter value.

    The set of joint indices across sub_ops must be disjoint (each joint appears
    in exactly one sub_op).
    """
    sub_ops: List  # heterogeneous list; each element is a single-param op

    def _apply(self, local_mats: List[np.ndarray], param: float) -> None:
        """Apply all sub-ops to local_mats in-place."""
        for sub_op in self.sub_ops:
            if isinstance(sub_op, (RotationOp, TranslationOp)):
                M = sub_op.matrix(param)
                local_mats[sub_op.joint_idx] = local_mats[sub_op.joint_idx] @ M
            elif isinstance(sub_op, ForearmTwistOp):
                for j_idx, M in sub_op.matrices(param):
                    local_mats[j_idx] = local_mats[j_idx] @ M

    def jacobian_contributions(
            self, local_mats: List[np.ndarray], param: float
    ) -> List[Tuple[int, np.ndarray]]:
        """
        Return list of (joint_idx, d_rotvec) for every affected joint.
        Caller accumulates these into the Jacobian column.
        """
        out = []
        for sub_op in self.sub_ops:
            if isinstance(sub_op, (RotationOp, TranslationOp)):
                ji   = sub_op.joint_idx
                dM   = sub_op.dmatrix_dparam(param)
                A    = local_mats[ji] @ np.linalg.inv(sub_op.matrix(param))
                dLoc = A @ dM
                out.append((ji, _dmat_to_drotvec(local_mats[ji], dLoc)))
            elif isinstance(sub_op, ForearmTwistOp):
                for ki, (ji, dM) in enumerate(sub_op.dmatrices_dparam(param)):
                    cur_M = sub_op.matrices(param)[ki][1]
                    A    = local_mats[ji] @ np.linalg.inv(cur_M)
                    dLoc = A @ dM
                    out.append((ji, _dmat_to_drotvec(local_mats[ji], dLoc)))
        return out


# ══════════════════════════════════════════════════════════════════════════════
# Learned Rig Approximation
# ══════════════════════════════════════════════════════════════════════════════

class LearnedRigApproximation:
    """
    Analytic approximation F̂(β) of the rig function F(β).

    Stores one operator per rig parameter (or one ForearmTwistOp per
    multi-joint twist parameter).  Composition order is determined by
    the sorting step; for parameters acting on different joints, order
    does not matter.

    Construction via .train() (offline).
    Evaluation / Jacobian / inversion at runtime.
    """

    def __init__(self,
                 ops:        List,        # list of Op objects, indexed by param
                 n_joints:   int,
                 zero_pose:  np.ndarray,  # flat pose vector at β = 0
                 param_names: Optional[List[str]] = None):
        self.ops         = ops
        self.n_joints    = n_joints
        self.zero_pose   = zero_pose
        self.param_names = param_names or [f"p{i}" for i in range(len(ops))]

    # ──────────────────────────────────────────────────────────────────────────
    # Evaluation
    # ──────────────────────────────────────────────────────────────────────────

    def evaluate(self, beta: np.ndarray) -> np.ndarray:
        """
        Evaluate F̂(β) → flat rotation-vector pose (3 * n_joints,).
        Starts from zero_pose, applies each operator in order.
        """
        local = [np.eye(4) for _ in range(self.n_joints)]

        for i, op in enumerate(self.ops):
            if op is None:
                continue
            p = beta[i]
            if isinstance(op, (RotationOp, TranslationOp)):
                local[op.joint_idx] = local[op.joint_idx] @ op.matrix(p)
            elif isinstance(op, ForearmTwistOp):
                for j_idx, M in op.matrices(p):
                    local[j_idx] = local[j_idx] @ M
            elif isinstance(op, CompoundOp):
                op._apply(local, p)

        return _pose_to_vec(local)

    # ──────────────────────────────────────────────────────────────────────────
    # Jacobian (analytic)
    # ──────────────────────────────────────────────────────────────────────────

    def jacobian(self, beta: np.ndarray) -> np.ndarray:
        """
        Compute the (3*n_joints × n_params) Jacobian analytically.
        J[i, j] = ∂(pose_flat[i]) / ∂(beta[j])

        Each column is computed independently (parallelisable in production).
        """
        n_dof   = 3 * self.n_joints
        n_p     = len(beta)
        J       = np.zeros((n_dof, n_p))

        # Forward pass: build current local matrices (needed for dR chain rule)
        local = [np.eye(4) for _ in range(self.n_joints)]
        for i, op in enumerate(self.ops):
            if op is None:
                continue
            p = beta[i]
            if isinstance(op, (RotationOp, TranslationOp)):
                local[op.joint_idx] = local[op.joint_idx] @ op.matrix(p)
            elif isinstance(op, ForearmTwistOp):
                for j_idx, M in op.matrices(p):
                    local[j_idx] = local[j_idx] @ M
            elif isinstance(op, CompoundOp):
                op._apply(local, p)

        # Backward pass: one Jacobian column per parameter
        for j, op in enumerate(self.ops):
            if op is None:
                continue
            p = beta[j]
            if isinstance(op, (RotationOp, TranslationOp)):
                ji   = op.joint_idx
                dM   = op.dmatrix_dparam(p)
                A    = local[ji] @ np.linalg.inv(op.matrix(p))
                dLoc = A @ dM
                J[3*ji: 3*ji+3, j] = _dmat_to_drotvec(local[ji], dLoc)

            elif isinstance(op, ForearmTwistOp):
                mats = op.matrices(p)
                for ki, (ji, dM) in enumerate(op.dmatrices_dparam(p)):
                    A    = local[ji] @ np.linalg.inv(mats[ki][1])
                    dLoc = A @ dM
                    J[3*ji: 3*ji+3, j] = _dmat_to_drotvec(local[ji], dLoc)

            elif isinstance(op, CompoundOp):
                for ji, dRV in op.jacobian_contributions(local, p):
                    J[3*ji: 3*ji+3, j] += dRV   # += handles multiple sub_ops on same joint

        return J

    # ──────────────────────────────────────────────────────────────────────────
    # Finite-difference Jacobian (used during classification validation)
    # ──────────────────────────────────────────────────────────────────────────

    def jacobian_fd(self, beta: np.ndarray, eps: float = 1e-5) -> np.ndarray:
        """Finite-difference Jacobian — used for validation only."""
        n_dof = 3 * self.n_joints
        n_p   = len(beta)
        J     = np.zeros((n_dof, n_p))
        f0    = self.evaluate(beta)
        for j in range(n_p):
            b1 = beta.copy(); b1[j] += eps
            J[:, j] = (self.evaluate(b1) - f0) / eps
        return J

    # ──────────────────────────────────────────────────────────────────────────
    # Offline Training
    # ──────────────────────────────────────────────────────────────────────────

    @classmethod
    def train(cls,
              rig_fn:      Callable[[np.ndarray], List[np.ndarray]],
              n_params:    int,
              n_joints:    int,
              test_lambdas: Optional[List[float]] = None,
              sigma:        float = 1e-3) -> 'LearnedRigApproximation':
        """
        Offline classification + sorting.

        rig_fn(beta) must return a list of n_joints local 4×4 transforms.

        Steps:
          1. Evaluate F(0) to get the zero-pose.
          2. For each parameter i, sample F(δ_i λ) for λ in test_lambdas.
          3. Classify each parameter as RotationOp, TranslationOp, or None.
          4. Sort operators pairwise to determine composition order.

        Returns a LearnedRigApproximation with classified operators.
        """
        if test_lambdas is None:
            test_lambdas = [0.1, 0.3, 0.5, 0.7, 1.0]

        # ── Step 1: zero pose ────────────────────────────────────────────────
        beta0  = np.zeros(n_params)
        pose0  = rig_fn(beta0)
        pose0f = _pose_to_vec(pose0)

        # Precompute inverse of each joint at zero pose
        inv0   = [np.linalg.inv(M) for M in pose0]

        # ── Step 2 & 3: classify each parameter ─────────────────────────────
        ops = []
        for i in range(n_params):
            op = _classify_parameter(rig_fn, i, n_params, n_joints,
                                     pose0, inv0, test_lambdas, sigma)
            ops.append(op)
            if isinstance(op, RotationOp):
                name = f"rotation(joint={op.joint_idx}, axis={op.axis.round(2)}, rate={op.rate:.3f})"
            elif isinstance(op, TranslationOp):
                name = f"translation(joint={op.joint_idx})"
            elif isinstance(op, ForearmTwistOp):
                name = f"forearm_twist(joints={op.joint_indices}, rate={op.rate:.3f})"
            elif isinstance(op, CompoundOp):
                parts = [type(s).__name__ for s in op.sub_ops]
                name = f"compound({'+'.join(parts)})"
            else:
                name = "discarded"
            print(f"  param {i}: classified as {name}")

        # ── Step 4: sort (simplified — full pairwise sort is O(n log n)) ────
        ops = _sort_operators(rig_fn, ops, n_params, n_joints, test_lambdas)

        return cls(ops, n_joints, pose0f)


# ══════════════════════════════════════════════════════════════════════════════
# Classification helpers
# ══════════════════════════════════════════════════════════════════════════════

def _classify_parameter(rig_fn, param_idx, n_params, n_joints,
                        pose0, inv0, test_lambdas, sigma):
    """
    Sample F(δ_i λ) for multiple λ.  For each joint, compute the relative
    effect M_rel(λ) = F_j(δ_i λ) · F_j(0)⁻¹ and try to fit a rotation
    or translation.

    Returns a RotationOp, TranslationOp, ForearmTwistOp, or None.
    """
    # Collect effects per joint per lambda
    effects = {}   # {joint_idx: [(lam, M_rel), ...]}
    for lam in test_lambdas:
        beta = np.zeros(n_params)
        beta[param_idx] = lam
        pose = rig_fn(beta)
        for j, (Mj, M0j_inv) in enumerate(zip(pose, inv0)):
            rel = Mj @ M0j_inv
            effects.setdefault(j, []).append((lam, rel))

    # ── Find joints that are actually affected ────────────────────────────────
    affected = {}   # {joint_idx: (op_type, op_params)}
    for j, pairs in effects.items():
        op = _fit_joint_effect(j, pairs, sigma)
        if op is not None:
            affected[j] = op

    if not affected:
        return None   # parameter discarded

    # ── Single joint: standard RotationOp / TranslationOp ───────────────────
    if len(affected) == 1:
        j, op = next(iter(affected.items()))
        return op

    # ── Multiple joints: check for ForearmTwistOp / CompoundOp pattern ─────
    # All affected joints must show rotation about a common axis.
    rot_ops = {j: op for j, op in affected.items() if isinstance(op, RotationOp)}
    if len(rot_ops) < len(affected):
        # Some joints have non-rotation effects — too complex to classify
        return None

    if len(rot_ops) < 2:
        return None

    # Check all axes are parallel
    axes = np.array([op.axis for op in rot_ops.values()])
    ref  = axes[0]
    if not all(np.allclose(np.abs(a @ ref), 1.0, atol=0.05) for a in axes[1:]):
        return None   # inconsistent axes

    # Group joints by their individual rate (5% relative tolerance)
    rates    = np.array([op.rate for op in rot_ops.values()])
    joint_list = list(rot_ops.keys())

    rate_groups = {}   # {representative_rate: [(joint_idx, RotationOp), ...]}
    for j, op in rot_ops.items():
        placed = False
        for key in list(rate_groups.keys()):
            if abs(op.rate - key) < 0.05 * max(op.rate, key, 1e-8):
                rate_groups[key].append((j, op))
                placed = True
                break
        if not placed:
            rate_groups[op.rate] = [(j, op)]

    if len(rate_groups) == 1:
        # ── All same rate → equal incremental ForearmTwistOp ──────────────
        # N joints each rotating locally by rate*param/N ≡ ind_rate*param.
        # Represent as ForearmTwistOp with cumulative fracs [1/N, 2/N, ..., 1].
        N          = len(rot_ops)
        ind_rate   = float(np.mean(np.abs(rates)))
        full_rate  = ind_rate * N
        joint_ids  = sorted(joint_list)
        fracs      = [(k + 1) / N for k in range(N)]   # cumulative [1/N … 1.0]
        return ForearmTwistOp(joint_ids, fracs, ref, full_rate)

    else:
        # ── Mixed rates → CompoundOp ───────────────────────────────────────
        # Build one sub-op per rate group:
        #   groups with N>1 joints at equal rate → ForearmTwistOp
        #   groups with  1 joint at its rate     → RotationOp
        sub_ops = []
        for rate_key, group in sorted(rate_groups.items()):
            if len(group) > 1:
                N         = len(group)
                full_rate = rate_key * N
                jids      = sorted([j for j, _ in group])
                fracs     = [(k + 1) / N for k in range(N)]
                sub_ops.append(ForearmTwistOp(jids, fracs, ref, full_rate))
            else:
                j, op = group[0]
                sub_ops.append(op)   # already a correctly fitted RotationOp
        return CompoundOp(sub_ops)

    # Multiple joints with different axes — parameter has complex dependency
    return None


def _fit_joint_effect(joint_idx, pairs, sigma):
    """
    Try to fit (λ, M_rel(λ)) pairs to a RotationOp or TranslationOp.
    Returns an Op or None.
    """
    lams = np.array([p[0] for p in pairs])
    rels = [p[1] for p in pairs]

    # ── Try Rotation ─────────────────────────────────────────────────────────
    rot_vecs = []
    is_rot   = True
    for lam, M in zip(lams, rels):
        R = M[:3, :3]
        if not _is_rotation(R):
            is_rot = False; break
        # Also check translation part is zero
        if np.linalg.norm(M[:3, 3]) > sigma * abs(lam) + 1e-6:
            is_rot = False; break
        rot_vecs.append(Rotation.from_matrix(R).as_rotvec())

    if is_rot and rot_vecs:
        angles = np.array([np.linalg.norm(rv) for rv in rot_vecs])
        if np.max(angles) > 1e-6:
            # Check proportionality: angle / lambda should be ~constant
            mask = lams > 1e-4
            if mask.any():
                ratios = angles[mask] / lams[mask]
                if np.std(ratios) < 0.05 * np.mean(ratios):
                    # Check axis consistency
                    norm_vecs = [rv / np.linalg.norm(rv) for rv in rot_vecs
                                 if np.linalg.norm(rv) > 1e-6]
                    if norm_vecs:
                        ref = norm_vecs[0]
                        if all(np.allclose(np.abs(v @ ref), 1.0, atol=0.05)
                               for v in norm_vecs[1:]):
                            axis = ref if rot_vecs[-1] @ ref > 0 else -ref
                            return RotationOp(joint_idx, axis, float(np.mean(ratios)))

    # ── Try Translation ──────────────────────────────────────────────────────
    is_trans = True
    trans    = []
    for lam, M in zip(lams, rels):
        if not np.allclose(M[:3, :3], np.eye(3), atol=1e-4):
            is_trans = False; break
        trans.append(M[:3, 3])

    if is_trans and trans:
        dirs = np.array([t / lam for t, lam in zip(trans, lams) if abs(lam) > 1e-6])
        if len(dirs) > 0:
            std = np.std(dirs, axis=0)
            if np.all(std < 0.05 * np.abs(np.mean(dirs, axis=0)) + 1e-6):
                return TranslationOp(joint_idx, np.mean(dirs, axis=0))

    return None


def _is_rotation(R: np.ndarray) -> bool:
    return (np.allclose(R @ R.T, np.eye(3), atol=1e-4) and
            np.isclose(np.linalg.det(R), 1.0, atol=1e-4))


# ══════════════════════════════════════════════════════════════════════════════
# Sorting helpers (Gustafson 2020 §4)
# ══════════════════════════════════════════════════════════════════════════════

def _sort_operators(rig_fn, ops, n_params, n_joints, test_lambdas):
    """
    Pairwise sort: determine if X precedes Y by checking
      (Y₀ ∘ X_α)(Y₀ ∘ X₀)⁻¹  ≈  (Yβ ∘ X_α)(Yβ ∘ X₀)⁻¹     (eq. 6)
    If true, X precedes Y in composition.

    Full implementation uses topological sort; here we use a simplified
    insertion sort for clarity.
    """
    valid_idx  = [i for i, op in enumerate(ops) if op is not None]
    sorted_idx = []

    for i in valid_idx:
        inserted = False
        for pos, j in enumerate(sorted_idx):
            if _x_precedes_y(rig_fn, i, j, n_params, test_lambdas, n_joints):
                sorted_idx.insert(pos, i)
                inserted = True
                break
        if not inserted:
            sorted_idx.append(i)

    # Rebuild ops list in new order (pad None for discarded params)
    reordered_ops = [None] * n_params
    for new_pos, orig_idx in enumerate(sorted_idx):
        reordered_ops[new_pos] = ops[orig_idx]
    return reordered_ops


def _x_precedes_y(rig_fn, xi, yi, n_params, test_lambdas, n_joints):
    """
    Test eq. 6: does parameter xi precede yi?
    Uses the first alpha and beta from test_lambdas.
    """
    alpha = test_lambdas[0]
    beta  = test_lambdas[-1]
    atol  = 1e-3

    def eval_pose(x_val, y_val):
        params = np.zeros(n_params)
        params[xi] = x_val
        params[yi] = y_val
        pose = rig_fn(params)
        return np.array([M[:3, :3] for M in pose])  # (n_joints, 3, 3)

    X0_Y0 = eval_pose(0,     0    )
    Xa_Y0 = eval_pose(alpha, 0    )
    X0_Yb = eval_pose(0,     beta )
    Xa_Yb = eval_pose(alpha, beta )

    # LHS: (Y₀ ∘ X_α)(Y₀ ∘ X₀)⁻¹  → Xa_Y0 @ inv(X0_Y0)
    lhs = np.array([Xa_Y0[j] @ np.linalg.inv(X0_Y0[j]) for j in range(n_joints)])
    # RHS: (Yβ ∘ X_α)(Yβ ∘ X₀)⁻¹  → Xa_Yb @ inv(X0_Yb)
    rhs = np.array([Xa_Yb[j] @ np.linalg.inv(X0_Yb[j]) for j in range(n_joints)])

    return np.allclose(lhs, rhs, atol=atol)


# ══════════════════════════════════════════════════════════════════════════════
# Rotation vector Jacobian helper
# ══════════════════════════════════════════════════════════════════════════════

def _dmat_to_drotvec(R44: np.ndarray, dR44: np.ndarray) -> np.ndarray:
    """
    Given current rotation matrix R (4×4) and its differential dR (4×4),
    return d(rotvec) via the log-map derivative formula:

        d(rotvec) = J_r(θ)⁻¹ · vee(Rᵀ · dR)

    where J_r is the right Jacobian of SO(3), θ = ||rotvec||,
    and vee extracts the rotation vector from a skew matrix.

    For small θ this reduces to d(rotvec) ≈ vee(Rᵀ · dR).
    """
    R  = R44[:3, :3]
    dR = dR44[:3, :3]
    rv = Rotation.from_matrix(R).as_rotvec()
    th = np.linalg.norm(rv)

    # Rᵀ · dR is skew-symmetric; extract axial vector
    skew_mat = R.T @ dR
    vee = np.array([skew_mat[2, 1], skew_mat[0, 2], skew_mat[1, 0]])

    if th < 1e-8:
        return vee   # identity limit

    # Right Jacobian inverse of SO(3):
    # J_r⁻¹ = I + 0.5·[θ]_× + (1 - sin(θ)/θ·(1-cos(θ)) / (θ²·(1-cos(θ))/θ) )·[θ]_×²
    # Simplified: J_r⁻¹ ≈ I + 0.5·[rv]_× + (1/θ² - sin(θ)/(2θ(1-cos(θ))))·[rv]_×²
    a = 1.0 / (th * th) - np.sin(th) / (2.0 * th * (1.0 - np.cos(th)))
    Jr_inv = np.eye(3) + 0.5 * _skew(rv / th) * th + a * (_skew(rv / th) @ _skew(rv / th)) * th**2
    return Jr_inv @ vee


# ══════════════════════════════════════════════════════════════════════════════
# Gauss-Newton / Levenberg-Marquardt Inverter
# ══════════════════════════════════════════════════════════════════════════════

class RigInverter:
    """
    Real-time rig inverter: given a target skeleton pose, find rig parameters.

    Uses Gauss-Newton with Levenberg-Marquardt fallback, both operating on
    the analytic approximation F̂(β).  Runs in ~2 ms for production rigs
    (Gustafson 2020).

    Jacobian columns are computed analytically and can be parallelised.
    """

    def __init__(self, model: LearnedRigApproximation,
                 max_gn_iters:  int   = 30,
                 max_lm_iters:  int   = 30,
                 convergence:   float = 1e-6,
                 lm_lambda_init: float = 1e-3):
        self.model          = model
        self.max_gn_iters   = max_gn_iters
        self.max_lm_iters   = max_lm_iters
        self.convergence    = convergence
        self.lm_lambda_init = lm_lambda_init

    def invert(self,
               target_pose:  List[np.ndarray],
               beta_init:    Optional[np.ndarray] = None,
               verbose:      bool = False) -> Tuple[np.ndarray, dict]:
        """
        Invert target_pose (list of n_joints local 4×4 matrices) → rig params.

        Returns (beta, info) where info contains convergence details.
        """
        target_vec = _pose_to_vec(target_pose)
        n_p = len(self.model.ops)
        beta = beta_init.copy() if beta_init is not None else np.zeros(n_p)

        # ── Gauss-Newton ────────────────────────────────────────────────────
        info = {"method": "GN", "iters": 0, "residual": np.inf, "converged": False}
        beta, info = self._gauss_newton(target_vec, beta, info, verbose)

        # ── LM fallback ─────────────────────────────────────────────────────
        if not info["converged"]:
            info["method"] = "LM"
            beta, info = self._levenberg_marquardt(target_vec, beta, info, verbose)

        return beta, info

    # ── Gauss-Newton ─────────────────────────────────────────────────────────

    def _gauss_newton(self, target, beta, info, verbose):
        for it in range(self.max_gn_iters):
            r = self.model.evaluate(beta) - target                # residual
            J = self.model.jacobian(beta)                         # analytic J
            # Solve normal equations: Jᵀ J Δβ = -Jᵀ r
            JtJ = J.T @ J
            Jtr = J.T @ r
            try:
                delta = np.linalg.solve(JtJ, -Jtr)
            except np.linalg.LinAlgError:
                break
            beta = beta + delta
            res  = float(np.sqrt(r @ r))
            if verbose:
                print(f"  GN iter {it:2d}  |r|={res:.4e}  |Δβ|={np.linalg.norm(delta):.4e}")
            info["iters"]    = it + 1
            info["residual"] = res
            if np.linalg.norm(delta) < self.convergence:
                info["converged"] = True
                break
        return beta, info

    # ── Levenberg-Marquardt ───────────────────────────────────────────────────

    def _levenberg_marquardt(self, target, beta, info, verbose):
        lam = self.lm_lambda_init
        r0  = self.model.evaluate(beta) - target
        f0  = float(r0 @ r0)

        for it in range(self.max_lm_iters):
            J   = self.model.jacobian(beta)
            JtJ = J.T @ J
            Jtr = J.T @ r0
            try:
                delta = np.linalg.solve(JtJ + lam * np.diag(np.diag(JtJ)), -Jtr)
            except np.linalg.LinAlgError:
                break

            beta_new = beta + delta
            r1 = self.model.evaluate(beta_new) - target
            f1 = float(r1 @ r1)

            if f1 < f0:
                beta = beta_new
                r0   = r1
                f0   = f1
                lam  = max(lam / 10.0, 1e-10)
            else:
                lam = min(lam * 10.0, 1e10)

            res = float(np.sqrt(f0))
            if verbose:
                print(f"  LM iter {it:2d}  |r|={res:.4e}  λ={lam:.2e}")
            info["iters"]    += 1
            info["residual"]  = res
            if np.linalg.norm(delta) < self.convergence:
                info["converged"] = True
                break

        return beta, info


# ══════════════════════════════════════════════════════════════════════════════
# Concrete Example: Arm + Forearm Partial Twist Rig
# ══════════════════════════════════════════════════════════════════════════════

class ArmRig:
    """
    Synthetic arm rig: shoulder (3-DOF) + elbow (1-DOF) +
    forearm partial twist (3 procedural joints) + hand (3-DOF).

    Joints
    ──────
      0  shoulder   : 3-DOF rotation (rx, ry, rz)
      1  elbow      : 1-DOF rotation (Rx only, i.e. elbow_bend)
      2  forearm_1  : procedural — local Rx = hand_rx / 3  (1/3 of extracted twist)
      3  forearm_2  : procedural — local Rx = hand_rx / 3  (cumulative 2/3)
      4  forearm_3  : procedural — local Rx = hand_rx / 3  (cumulative 3/3)
      5  hand       : 3-DOF rotation (rx, ry, rz)

    Rig Parameters (7)
    ──────────────
      0  shoulder_rx  [-π, π]
      1  shoulder_ry  [-π, π]
      2  shoulder_rz  [-π, π]
      3  elbow_bend   [ 0, π]
      4  hand_rx      [-π, π]   ← ALSO drives forearm partial twist
      5  hand_ry      [-π, π]
      6  hand_rz      [-π, π]

    hand_rx is a CompoundOp:
      - ForearmTwistOp(joints=[2,3,4], fracs=[1/3,2/3,1.0], axis=X, rate=1.0)
        drives forearm_1/2/3 with incremental local Rx = hand_rx/3 each.
      - RotationOp(joint=5, axis=X, rate=1.0)
        drives the hand's Rx component.
    hand_ry and hand_rz are plain RotationOps on joint 5.

    Both shoulder and hand use ZYX Euler order: R = Rx @ Ry @ Rz.
    """

    num_params  = 7
    num_joints  = 6
    param_names = ["shoulder_rx", "shoulder_ry", "shoulder_rz",
                   "elbow_bend",
                   "hand_rx", "hand_ry", "hand_rz"]
    joint_names = ["shoulder", "elbow", "forearm_1", "forearm_2", "forearm_3", "hand"]

    def evaluate(self, beta: np.ndarray) -> List[np.ndarray]:
        """
        F(β) → list of 6 local 4×4 rotation matrices.

        The forearm joints are procedural: each receives hand_rx/3,
        approximating a swing-twist extraction of the hand Rx component.
        """
        sx, sy, sz, eb, hx, hy, hz = beta

        R_sh   = _rot_x(sx) @ _rot_y(sy) @ _rot_z(sz)   # shoulder ZYX Euler
        R_el   = _rot_x(eb)                               # elbow pure Rx
        inc    = hx / 3.0                                 # incremental forearm twist
        R_f1   = _rot_x(inc)                              # forearm_1: world twist = hx/3
        R_f2   = _rot_x(inc)                              # forearm_2: world twist = 2hx/3
        R_f3   = _rot_x(inc)                              # forearm_3: world twist = hx
        R_hand = _rot_x(hx) @ _rot_y(hy) @ _rot_z(hz)   # hand ZYX Euler

        return [R_sh, R_el, R_f1, R_f2, R_f3, R_hand]

    def ground_truth_jacobian(self, beta: np.ndarray) -> np.ndarray:
        """
        Analytic Jacobian of this rig for validation.
        J is (18 × 7): 3 rotvec DOFs × 6 joints, 7 rig params.

        Structure:
          rows  0: 3  — shoulder   (params 0,1,2)
          rows  3: 6  — elbow      (param  3)
          rows  6: 9  — forearm_1  (param  4,  rate 1/3)
          rows  9:12  — forearm_2  (param  4,  rate 1/3)
          rows 12:15  — forearm_3  (param  4,  rate 1/3)
          rows 15:18  — hand       (params 4,5,6)
        """
        sx, sy, sz, eb, hx, hy, hz = beta
        J = np.zeros((18, 7))

        # ── Shoulder (ZYX Euler: R = Rx @ Ry @ Rz) ─────────────────────────
        Rx_sh = _rot_x(sx)[:3, :3]
        Ry_sh = _rot_y(sy)[:3, :3]
        Rz_sh = _rot_z(sz)[:3, :3]
        R_sh  = Rx_sh @ Ry_sh @ Rz_sh
        dRx_s = Rotation.from_rotvec(sx * np.array([1.,0.,0.])).as_matrix() \
                @ _skew(np.array([1.,0.,0.]))
        dRy_s = Rotation.from_rotvec(sy * np.array([0.,1.,0.])).as_matrix() \
                @ _skew(np.array([0.,1.,0.]))
        dRz_s = Rotation.from_rotvec(sz * np.array([0.,0.,1.])).as_matrix() \
                @ _skew(np.array([0.,0.,1.]))
        J[ 0: 3, 0] = _dmat33_to_drotvec(R_sh, dRx_s @ Ry_sh @ Rz_sh)
        J[ 0: 3, 1] = _dmat33_to_drotvec(R_sh, Rx_sh @ dRy_s @ Rz_sh)
        J[ 0: 3, 2] = _dmat33_to_drotvec(R_sh, Rx_sh @ Ry_sh @ dRz_s)

        # ── Elbow (pure Rx hinge) ────────────────────────────────────────────
        R_el = _rot_x(eb)[:3, :3]
        dEl  = R_el @ _skew(np.array([1.,0.,0.]))
        J[ 3: 6, 3] = _dmat33_to_drotvec(R_el, dEl)

        # ── Forearm joints (each: Rx(hx/3), d/d(hx) = (1/3)*R_f @ [X]×) ───
        R_f  = _rot_x(hx / 3.0)[:3, :3]
        dF   = R_f @ _skew(np.array([1.,0.,0.])) * (1.0 / 3.0)
        J[ 6: 9, 4] = _dmat33_to_drotvec(R_f, dF)   # forearm_1
        J[ 9:12, 4] = _dmat33_to_drotvec(R_f, dF)   # forearm_2
        J[12:15, 4] = _dmat33_to_drotvec(R_f, dF)   # forearm_3

        # ── Hand (ZYX Euler: R = Rx @ Ry @ Rz) ─────────────────────────────
        Rx_h   = _rot_x(hx)[:3, :3]
        Ry_h   = _rot_y(hy)[:3, :3]
        Rz_h   = _rot_z(hz)[:3, :3]
        R_hand = Rx_h @ Ry_h @ Rz_h
        dhRx   = Rotation.from_rotvec(hx * np.array([1.,0.,0.])).as_matrix() \
                 @ _skew(np.array([1.,0.,0.]))
        dhRy   = Rotation.from_rotvec(hy * np.array([0.,1.,0.])).as_matrix() \
                 @ _skew(np.array([0.,1.,0.]))
        dhRz   = Rotation.from_rotvec(hz * np.array([0.,0.,1.])).as_matrix() \
                 @ _skew(np.array([0.,0.,1.]))
        J[15:18, 4] = _dmat33_to_drotvec(R_hand, dhRx @ Ry_h @ Rz_h)
        J[15:18, 5] = _dmat33_to_drotvec(R_hand, Rx_h @ dhRy @ Rz_h)
        J[15:18, 6] = _dmat33_to_drotvec(R_hand, Rx_h @ Ry_h @ dhRz)

        return J


def _rot_x(a): c,s=np.cos(a),np.sin(a); M=np.eye(4); M[1,1]=c; M[1,2]=-s; M[2,1]=s; M[2,2]=c; return M
def _rot_y(a): c,s=np.cos(a),np.sin(a); M=np.eye(4); M[0,0]=c; M[0,2]=s; M[2,0]=-s; M[2,2]=c; return M
def _rot_z(a): c,s=np.cos(a),np.sin(a); M=np.eye(4); M[0,0]=c; M[0,1]=-s; M[1,0]=s; M[1,1]=c; return M


def _dmat33_to_drotvec(R: np.ndarray, dR: np.ndarray) -> np.ndarray:
    """d(rotvec) from 3×3 R and 3×3 dR (thin wrapper)."""
    R44 = np.eye(4); R44[:3,:3] = R
    dR44 = np.zeros((4,4)); dR44[:3,:3] = dR
    return _dmat_to_drotvec(R44, dR44)


# ══════════════════════════════════════════════════════════════════════════════
# Main: demonstration + validation
# ══════════════════════════════════════════════════════════════════════════════

def demo_arm_rig():
    print("=" * 60)
    print("Analytic Inverse Rig Mapping — Arm + Forearm + Hand Demo")
    print("=" * 60)
    print("Params: shoulder_rx/ry/rz, elbow_bend, hand_rx/ry/rz  (7 params)")
    print("Joints: shoulder, elbow, forearm_1, forearm_2, forearm_3, hand  (6 joints)")
    print("hand_rx drives BOTH forearm partial twist AND hand Rx (CompoundOp)")

    rig = ArmRig()

    # ── 1. Training (offline classification + sorting) ───────────────────────
    print("\n[1] Training (classification + sorting)...")
    model = LearnedRigApproximation.train(
        rig_fn    = rig.evaluate,
        n_params  = rig.num_params,
        n_joints  = rig.num_joints,
    )

    # ── 2. Validate Jacobian ─────────────────────────────────────────────────
    print("\n[2] Jacobian validation (analytic vs. FD vs. ground truth)...")
    print("    Expected: J is (18×7); hand_rx col has 1/3 in forearm rows + 1.0 in hand row")
    beta_test = np.array([0.3, -0.2, 0.1, 0.7, 0.2, -0.3, 0.4])
    J_analytic = model.jacobian(beta_test)
    J_fd       = model.jacobian_fd(beta_test)
    J_gt       = rig.ground_truth_jacobian(beta_test)
    print(f"  J_analytic vs J_fd   max_err = {np.max(np.abs(J_analytic - J_fd)):.4e}")
    print(f"  J_analytic vs J_gt   max_err = {np.max(np.abs(J_analytic - J_gt)):.4e}")

    # ── 3. Inversion ─────────────────────────────────────────────────────────
    print("\n[3] Inversion test cases:")
    inverter = RigInverter(model, max_gn_iters=30, max_lm_iters=30)

    test_cases = [
        ("rest pose",
         np.zeros(7)),
        ("shoulder only",
         np.array([0.4,  0.2, -0.1,  0.0,  0.0,  0.0,  0.0])),
        ("elbow bend 90°",
         np.array([0.0,  0.0,  0.0,  np.pi/2, 0.0, 0.0, 0.0])),
        ("hand_rx only (twist)",
         np.array([0.0,  0.0,  0.0,  0.0, 1.2,  0.0,  0.0])),
        ("hand_rx/ry/rz",
         np.array([0.0,  0.0,  0.0,  0.0, 0.4, -0.2,  0.5])),
        ("shoulder + elbow",
         np.array([0.3,  0.1, -0.2,  0.8,  0.0,  0.0,  0.0])),
        ("elbow + hand (full)",
         np.array([0.0,  0.0,  0.0,  0.6,  0.4, -0.1,  0.3])),
        ("full combined",
         np.array([0.3, -0.2,  0.1,  0.7,  0.2, -0.3,  0.4])),
    ]

    for name, beta_true in test_cases:
        target = rig.evaluate(beta_true)
        beta_solved, info = inverter.invert(target, verbose=False)
        err_beta = np.max(np.abs(beta_solved - beta_true))
        err_pose = info["residual"]
        status   = "✓" if err_beta < 1e-4 else "⚠"
        print(f"  {status} {name:<25s}  |Δβ|∞={err_beta:.2e}  "
              f"|r|={err_pose:.2e}  iters={info['iters']}  [{info['method']}]")

    print("\nDone.")


if __name__ == "__main__":
    demo_arm_rig()
