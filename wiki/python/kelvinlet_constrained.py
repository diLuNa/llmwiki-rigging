"""
kelvinlet_constrained.py
Multi-point constrained Kelvinlet deformation.
Source: de Goes & James, SIGGRAPH 2018, Eq. (18) / §5.

Place n Kelvinlets at control points and solve for forces {f_i} such that
prescribed displacements {u_i} are matched exactly.  Useful for:
  - Pinning anchor points to zero displacement while grabbing one control point.
  - Multi-point sculpt strokes.

Two phases:
  Phase 1 (solve):   build 3n×3n linear system and solve for forces (numpy).
  Phase 2 (deform):  evaluate superposed deformation on the full point cloud.
"""

import numpy as np
from kelvinlet_core import _K_eps, _ba, _c


# ---------------------------------------------------------------------------
# Phase 1 — solve for forces
# ---------------------------------------------------------------------------

def solve_forces(
    centers:    np.ndarray,
    disps:      np.ndarray,
    epsilons:   np.ndarray | float = 1.0,
    nu:         float = 0.5,
) -> np.ndarray:
    """
    Solve for Kelvinlet force vectors that reproduce prescribed displacements.

    Args:
        centers  : (n, 3)  control point positions
        disps    : (n, 3)  desired displacement at each control point
        epsilons : (n,) or float  per-control-point brush radius
        nu       : float  Poisson ratio

    Returns:
        forces   : (n, 3)  solved force vectors
    """
    centers  = np.asarray(centers,  dtype=float)
    disps    = np.asarray(disps,    dtype=float)
    n        = len(centers)
    ba_val   = _ba(nu)

    if np.isscalar(epsilons):
        epsilons = np.full(n, float(epsilons))
    else:
        epsilons = np.asarray(epsilons, dtype=float)

    # Build 3n × 3n block-matrix K
    # Block K[i,j] = K_eps_i(center_j - center_i)  evaluated with eps_i
    K_mat = np.zeros((3 * n, 3 * n))
    for i in range(n):
        for j in range(n):
            rij  = centers[j] - centers[i]          # (3,)
            re   = np.sqrt(np.dot(rij, rij) + epsilons[i] ** 2)
            re3  = re ** 3
            A    = (1.0 - ba_val) / re + 0.5 * epsilons[i] ** 2 / re3
            B    = ba_val / re3
            Kij  = A * np.eye(3) + B * np.outer(rij, rij)
            K_mat[3*i:3*i+3, 3*j:3*j+3] = Kij

    u_vec  = disps.flatten()                         # (3n,)
    f_vec  = np.linalg.solve(K_mat, u_vec)
    return f_vec.reshape(n, 3)


# ---------------------------------------------------------------------------
# Phase 2 — evaluate deformation on point cloud
# ---------------------------------------------------------------------------

def deform(
    points:    np.ndarray,
    centers:   np.ndarray,
    forces:    np.ndarray,
    epsilons:  np.ndarray | float = 1.0,
    nu:        float = 0.5,
) -> np.ndarray:
    """
    Evaluate superposed constrained Kelvinlet displacement on a point cloud.

    Args:
        points   : (N, 3)  mesh vertices
        centers  : (n, 3)  Kelvinlet control positions
        forces   : (n, 3)  solved force vectors (from solve_forces)
        epsilons : (n,) or float  per-Kelvinlet brush radii
        nu       : float  Poisson ratio

    Returns:
        disps : (N, 3)  total displacement per vertex
    """
    points   = np.asarray(points,  dtype=float)
    centers  = np.asarray(centers, dtype=float)
    forces   = np.asarray(forces,  dtype=float)
    n        = len(centers)
    ba_val   = _ba(nu)

    if np.isscalar(epsilons):
        epsilons = np.full(n, float(epsilons))
    else:
        epsilons = np.asarray(epsilons, dtype=float)

    total = np.zeros_like(points)
    for i in range(n):
        r    = points - centers[i]                   # (N, 3)
        r2   = np.sum(r * r, axis=1, keepdims=True)
        re   = np.sqrt(r2 + epsilons[i] ** 2)
        re3  = re ** 3
        A    = (1.0 - ba_val) / re + 0.5 * epsilons[i] ** 2 / re3  # (N,1)
        B    = ba_val / re3                                          # (N,1)
        rdotf = r @ forces[i]                                        # (N,)
        total += A * forces[i][np.newaxis, :] + B * rdotf[:, np.newaxis] * r

    return total


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------

def apply_constrained(
    points:   np.ndarray,
    centers:  np.ndarray,
    disps:    np.ndarray,
    epsilons: float | np.ndarray = 1.0,
    nu:       float = 0.5,
) -> np.ndarray:
    """
    Solve for forces then deform all points.  Returns deformed point cloud.
    """
    forces = solve_forces(centers, disps, epsilons, nu)
    d      = deform(points, centers, forces, epsilons, nu)
    return points + d


# ---------------------------------------------------------------------------
# Example: grab one point, pin two anchors to zero
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    rng  = np.random.default_rng(2)
    pts  = rng.uniform(-4, 4, (800, 3))
    eps  = 1.0
    nu   = 0.4

    # Control points: one grab, two pins
    centers  = np.array([[0.0, 0.0, 0.0],
                         [2.0, 0.0, 0.0],
                         [-2.0, 0.0, 0.0]])
    disps    = np.array([[0.0, 1.5, 0.0],   # grab: move up
                         [0.0, 0.0, 0.0],   # pin: zero disp
                         [0.0, 0.0, 0.0]])  # pin: zero disp

    forces = solve_forces(centers, disps, epsilons=eps, nu=nu)
    print("Solved forces:\n", forces)

    # Verify displacement at control points matches prescribed
    d_ctrl = deform(centers, centers, forces, epsilons=eps, nu=nu)
    for i, (got, want) in enumerate(zip(d_ctrl, disps)):
        err = np.linalg.norm(got - want)
        print(f"ctrl {i}: prescribed={want}, got={got}, err={err:.2e}")

    pts_deformed = pts + deform(pts, centers, forces, epsilons=eps, nu=nu)
    print("Max vertex displacement:", np.max(np.linalg.norm(pts_deformed - pts, axis=1)))
