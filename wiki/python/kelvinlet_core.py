"""
kelvinlet_core.py
Regularized Kelvinlet grab brush — single-scale, bi-scale, tri-scale.
Source: de Goes & James, SIGGRAPH 2018, Eq. (6)-(11).

All functions accept an (N, 3) point array and return an (N, 3) displacement array.
Vectorized with NumPy; no loops over points.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Material helpers
# ---------------------------------------------------------------------------

def _ba(nu: float) -> float:
    """b/a ratio from Poisson ratio: ba = 1 / (4*(1-nu))."""
    return 1.0 / (4.0 * (1.0 - nu))


def _c(nu: float) -> float:
    """Normalization constant c = 2 / (3 - 2*ba)."""
    return 2.0 / (3.0 - 2.0 * _ba(nu))


# ---------------------------------------------------------------------------
# Core: regularized Kelvinlet matrix applied to a vector
# ---------------------------------------------------------------------------

def _K_eps(r: np.ndarray, v: np.ndarray, eps: float, ba: float) -> np.ndarray:
    """
    Evaluate K_eps(r) * v for each row of r.

    Args:
        r   : (N, 3) offset vectors from brush center
        v   : (3,)   force/displacement vector
        eps : float  regularization scale (brush radius)
        ba  : float  b/a ratio = 1/(4*(1-nu))

    Returns:
        (N, 3) displacement contribution (without c*eps normalization)
    """
    r2  = np.sum(r * r, axis=1, keepdims=True)          # (N,1)
    re  = np.sqrt(r2 + eps * eps)                        # (N,1)  r_epsilon
    re3 = re ** 3

    A = (1.0 - ba) / re + 0.5 * eps * eps / re3         # (N,1)
    B = ba / re3                                         # (N,1)
    rdotv = r @ v                                        # (N,)  dot(r, v)

    return A * v[np.newaxis, :] + B * rdotv[:, np.newaxis] * r


# ---------------------------------------------------------------------------
# Grab brush — single-scale
# ---------------------------------------------------------------------------

def grab(
    points:  np.ndarray,
    center:  np.ndarray,
    disp:    np.ndarray,
    epsilon: float = 1.0,
    nu:      float = 0.5,
) -> np.ndarray:
    """
    Regularized Kelvinlet grab brush (Eq. 6-7).

    Args:
        points  : (N, 3) mesh vertices
        center  : (3,)   brush center x0
        disp    : (3,)   desired displacement at brush center
        epsilon : float  brush radius (regularization scale)
        nu      : float  Poisson ratio; 0.5 = incompressible

    Returns:
        (N, 3) displacement to add to points
    """
    ba_val = _ba(nu)
    c_val  = _c(nu)
    r = points - center[np.newaxis, :]                   # (N, 3)
    return c_val * epsilon * _K_eps(r, disp, epsilon, ba_val)


# ---------------------------------------------------------------------------
# Grab brush — bi-scale (O(1/r³) decay)
# ---------------------------------------------------------------------------

def grab_biscale(
    points:  np.ndarray,
    center:  np.ndarray,
    disp:    np.ndarray,
    epsilon: float = 1.0,
    nu:      float = 0.5,
    ratio:   float = 1.1,
) -> np.ndarray:
    """
    Bi-scale Kelvinlet grab brush (Eq. 8-9). Faster falloff than single-scale.

    Args:
        ratio : float  eps2 / eps1 (default 1.1; must be > 1)
    """
    ba_val = _ba(nu)
    c_val  = _c(nu)
    eps1   = epsilon
    eps2   = ratio * epsilon

    r    = points - center[np.newaxis, :]
    norm = 1.0 / (1.0 / eps1 - 1.0 / eps2)
    Kd   = _K_eps(r, disp, eps1, ba_val) - _K_eps(r, disp, eps2, ba_val)
    return c_val * norm * Kd


# ---------------------------------------------------------------------------
# Grab brush — tri-scale (O(1/r⁵) decay)
# ---------------------------------------------------------------------------

def grab_triscale(
    points:  np.ndarray,
    center:  np.ndarray,
    disp:    np.ndarray,
    epsilon: float = 1.0,
    nu:      float = 0.5,
    ratio2:  float = 1.1,
    ratio3:  float = 1.21,
) -> np.ndarray:
    """
    Tri-scale Kelvinlet grab brush (Eq. 10-11). Fastest falloff, most localized.

    Args:
        ratio2 : float  eps2 / eps1 (default 1.1)
        ratio3 : float  eps3 / eps1 (default 1.21)
    """
    ba_val = _ba(nu)
    c_val  = _c(nu)
    eps1   = epsilon
    eps2   = ratio2 * epsilon
    eps3   = ratio3 * epsilon

    e1sq, e2sq, e3sq = eps1**2, eps2**2, eps3**2

    # Weights cancelling O(1/r) and O(1/r³) terms
    w1 =  1.0
    w2 = -(e3sq - e1sq) / (e3sq - e2sq)
    w3 =  (e2sq - e1sq) / (e3sq - e2sq)

    sum_w_over_e = w1 / eps1 + w2 / eps2 + w3 / eps3

    r    = points - center[np.newaxis, :]
    Ksum = (w1 * _K_eps(r, disp, eps1, ba_val)
          + w2 * _K_eps(r, disp, eps2, ba_val)
          + w3 * _K_eps(r, disp, eps3, ba_val))
    return c_val / sum_w_over_e * Ksum


# ---------------------------------------------------------------------------
# Convenience: apply displacement to a copy of points
# ---------------------------------------------------------------------------

def apply_grab(points, center, disp, epsilon=1.0, nu=0.5, mode="tri"):
    """
    Deform points with a grab brush.

    Args:
        mode : "single" | "bi" | "tri"

    Returns:
        (N, 3) deformed points
    """
    fns = {"single": grab, "bi": grab_biscale, "tri": grab_triscale}
    d = fns[mode](points, np.asarray(center), np.asarray(disp), epsilon, nu)
    return points + d


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    rng = np.random.default_rng(0)
    pts = rng.uniform(-5, 5, (1000, 3))

    center  = np.array([0.0, 0.0, 0.0])
    disp    = np.array([0.0, 1.0, 0.0])
    epsilon = 2.0
    nu      = 0.45

    pts_single = apply_grab(pts, center, disp, epsilon, nu, "single")
    pts_bi     = apply_grab(pts, center, disp, epsilon, nu, "bi")
    pts_tri    = apply_grab(pts, center, disp, epsilon, nu, "tri")

    # Displacement at brush center should equal disp (up to scaling convention)
    for label, deformed in [("single", pts_single), ("bi", pts_bi), ("tri", pts_tri)]:
        tip_disp = apply_grab(center[np.newaxis], center, disp, epsilon, nu, label)[0] - center
        print(f"{label:8s} | tip displacement = {tip_disp}")
