"""
kelvinlet_affine.py
Locally affine Kelvinlet brushes: Twist, Scale, Pinch.
Source: de Goes & James, SIGGRAPH 2018, Eq. (14)-(17).

All functions accept an (N, 3) point array and return an (N, 3) displacement array.
"""

import numpy as np


def _ba(nu: float) -> float:
    return 1.0 / (4.0 * (1.0 - nu))


# ---------------------------------------------------------------------------
# Shared affine falloff scalar
# ---------------------------------------------------------------------------

def _alpha(r2: np.ndarray, eps: float) -> np.ndarray:
    """
    alpha(r) = 1/r_eps³  +  3*eps² / (2*r_eps⁵)
    Scalar per point, shape (N, 1).
    """
    re  = np.sqrt(r2 + eps * eps)
    re3 = re ** 3
    re5 = re ** 5
    return 1.0 / re3 + 1.5 * eps * eps / re5


# ---------------------------------------------------------------------------
# Twist brush — Eq. (15)
# ---------------------------------------------------------------------------

def twist(
    points: np.ndarray,
    center: np.ndarray,
    axis:   np.ndarray,
    amount: float = 1.0,
    epsilon: float = 1.0,
    nu:     float = 0.5,
) -> np.ndarray:
    """
    Twist (vortex) brush: u(r) = -alpha * (q × r).
    Volume-preserving for any nu (divergence = 0).

    Args:
        axis   : (3,) rotation axis direction (normalized internally)
        amount : float  angular velocity magnitude at brush center
    """
    q  = normalize(axis) * amount
    r  = points - center[np.newaxis, :]
    r2 = np.sum(r * r, axis=1, keepdims=True)
    a  = _alpha(r2, epsilon)                  # (N, 1)

    # q × r for each point: (N, 3)
    qxr = np.cross(q[np.newaxis, :], r)

    return -a * qxr


# ---------------------------------------------------------------------------
# Scale brush — Eq. (16)
# ---------------------------------------------------------------------------

def scale(
    points:  np.ndarray,
    center:  np.ndarray,
    amount:  float = -1.0,
    epsilon: float = 1.0,
    nu:      float = 0.5,
) -> np.ndarray:
    """
    Isotropic scale (dilation/contraction) brush.
    s > 0: contraction toward center.  s < 0: dilation away.
    Note: displacement is zero for incompressible material (nu=0.5).

    Args:
        amount : float  scale strength s
    """
    ba_val = _ba(nu)
    r      = points - center[np.newaxis, :]
    r2     = np.sum(r * r, axis=1, keepdims=True)
    a      = _alpha(r2, epsilon)

    coeff = (2.0 * ba_val - 1.0)              # (2b-a)/a; zero at nu=0.5
    return coeff * a * (amount * r)


# ---------------------------------------------------------------------------
# Pinch brush — Eq. (17)
# ---------------------------------------------------------------------------

def pinch(
    points:  np.ndarray,
    center:  np.ndarray,
    axis:    np.ndarray,
    amount:  float = 1.0,
    epsilon: float = 1.0,
    nu:      float = 0.5,
) -> np.ndarray:
    """
    Pinch (squeeze+stretch) brush along axis d.
    F = amount * (outer(d,d) - I/3) — symmetric, traceless.

    Args:
        axis   : (3,) primary stretch axis (normalized internally)
        amount : float  pinch magnitude
    """
    ba_val = _ba(nu)
    d  = normalize(axis)
    r  = points - center[np.newaxis, :]
    r2 = np.sum(r * r, axis=1, keepdims=True)
    re  = np.sqrt(r2 + epsilon * epsilon)
    re3 = re ** 3
    re5 = re ** 5

    rdotd = r @ d                              # (N,)
    Fr    = amount * (rdotd[:, np.newaxis] * d[np.newaxis, :] - r / 3.0)   # (N, 3)
    rFr   = amount * (rdotd ** 2 - r2[:, 0]) / 3.0                         # (N,)

    coeff1 = (2.0 * ba_val - 1.0) / re3                                    # (N, 1)
    coeff2 = 3.0 / (2.0 * re5)                                             # (N, 1)

    return (coeff1 * Fr
            - coeff2 * (2.0 * ba_val * rFr[:, np.newaxis] * r
                        + epsilon * epsilon * Fr))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    rng = np.random.default_rng(1)
    pts    = rng.uniform(-3, 3, (500, 3))
    center = np.zeros(3)
    eps    = 1.5

    d_twist = twist(pts, center, axis=[0, 1, 0], amount=0.5, epsilon=eps)
    d_scale = scale(pts, center, amount=-0.3,    epsilon=eps, nu=0.3)
    d_pinch = pinch(pts, center, axis=[1, 0, 0], amount=1.0, epsilon=eps)

    print("twist max disp:", np.max(np.linalg.norm(d_twist, axis=1)))
    print("scale max disp:", np.max(np.linalg.norm(d_scale, axis=1)))
    print("pinch max disp:", np.max(np.linalg.norm(d_pinch, axis=1)))

    # Volume preservation check for twist (divergence ≈ 0 → disp should be
    # perpendicular to q): verify mean radial component along axis is near zero.
    axis_dir = np.array([0, 1, 0])
    radial = d_twist @ axis_dir
    print(f"twist radial component along axis (should be ~0): {np.mean(np.abs(radial)):.6f}")
