"""
kelvinlet_sharp.py
Sharp Kelvinlets: Laplacian, Bi-Laplacian, Cusped Laplacian, Cusped Bi-Laplacian.
Source: de Goes & James, ACM ToG 2019 (Sharp Kelvinlets), Eq. (15)-(18).

Provides independent control over:
  - locality   : Kelvinlet < Laplacian < Bi-Laplacian  (increasing localization)
  - spikiness  : smooth < cusped  (non-smooth profile at brush tip)

All functions accept (N, 3) point arrays and return (N, 3) displacement arrays.
"""

import numpy as np


def _ba(nu: float) -> float:
    return 1.0 / (4.0 * (1.0 - nu))


# ---------------------------------------------------------------------------
# Smooth Laplacian Kelvinlet — Eq. (15)
# ---------------------------------------------------------------------------

def laplacian(
    points:  np.ndarray,
    center:  np.ndarray,
    force:   np.ndarray,
    epsilon: float = 1.0,
    nu:      float = 0.5,
) -> np.ndarray:
    """
    Laplacian Kelvinlet: faster O(1/r³) far-field decay than the grab brush.
    Smooth C∞ profile.

    Args:
        force : (3,) force vector at brush center
    """
    ba_val = _ba(nu)
    r  = points - center[np.newaxis, :]
    r2 = np.sum(r * r, axis=1, keepdims=True)
    re = np.sqrt(r2 + epsilon * epsilon)
    re7 = re ** 7

    A = (15.0 * epsilon**4 - 2.0 * ba_val * re**2 * (5.0 * epsilon**2 + 2.0 * r2)) / (2.0 * re7)
    B = 3.0 * ba_val * (7.0 * epsilon**2 + 2.0 * r2) / re7

    rdotf = r @ force
    return A * force[np.newaxis, :] + B * rdotf[:, np.newaxis] * r


# ---------------------------------------------------------------------------
# Smooth Bi-Laplacian Kelvinlet — Eq. (16)
# ---------------------------------------------------------------------------

def bilaplacian(
    points:  np.ndarray,
    center:  np.ndarray,
    force:   np.ndarray,
    epsilon: float = 1.0,
    nu:      float = 0.5,
) -> np.ndarray:
    """
    Bi-Laplacian Kelvinlet: very fast O(1/r⁹) far-field decay.
    Most localized smooth brush.
    """
    ba_val  = _ba(nu)
    eps4    = epsilon ** 4
    r  = points - center[np.newaxis, :]
    r2 = np.sum(r * r, axis=1, keepdims=True)
    re = np.sqrt(r2 + epsilon * epsilon)
    re11 = re ** 11

    A = 105.0 * eps4 * (3.0 * (epsilon**2 - 2.0 * r2) - 2.0 * ba_val * re**2) / (2.0 * re11)
    B = 945.0 * ba_val * eps4 / re11

    rdotf = r @ force
    return A * force[np.newaxis, :] + B * rdotf[:, np.newaxis] * r


# ---------------------------------------------------------------------------
# Cusped Laplacian Kelvinlet — Eq. (17)
# ---------------------------------------------------------------------------

def cusped_laplacian(
    points:  np.ndarray,
    center:  np.ndarray,
    force:   np.ndarray,
    epsilon: float = 1.0,
    nu:      float = 0.5,
) -> np.ndarray:
    """
    Cusped Laplacian Kelvinlet: O(1/r³) decay with non-smooth (spiky) profile at tip.
    """
    ba_val = _ba(nu)
    eps2   = epsilon ** 2
    eps4   = eps2 * eps2

    r  = points - center[np.newaxis, :]
    r2 = np.sum(r * r, axis=1, keepdims=True)
    rm = np.sqrt(r2)                                    # |r|, (N,1)
    re = np.sqrt(r2 + eps2)
    re5 = re ** 5

    # Near-zero guard
    safe_rm  = np.where(rm > 1e-7, rm,  1e-7)
    safe_re5 = np.where(re5 > 0,   re5, 1e-20)

    # A coefficient (Eq. 17)
    r5   = safe_rm ** 5
    re5_ = re ** 5
    term1 = (15.0 - 10.0 * ba_val) * eps4 * eps2
    term2 = (90.0 - 88.0 * ba_val) * eps4 * r2
    term3 = 120.0 * eps2 * r2 ** 2 * (1.0 - ba_val)
    term4 = 48.0 * (1.0 - ba_val) * safe_rm * (r5 - re5_)
    A = 2.0 / (eps4 * safe_re5) * (term1 + term2 + term3 + term4)

    # B coefficient (Eq. 17)
    bt1 = 2.0 * eps2 * r2 * (4.0 * re - 5.0 * safe_rm)
    bt2 = 4.0 * r2 ** 2 * (re - safe_rm)
    bt3 = eps4 * (4.0 * re - 7.0 * safe_rm)
    B = -12.0 * ba_val / (eps4 * safe_rm * safe_re5) * (bt1 + bt2 + bt3)

    # Tip: A → (15 - 10*ba)/eps², B → 0
    tip_mask = (rm < 1e-7)
    A = np.where(tip_mask, (15.0 - 10.0 * ba_val) / eps2, A)
    B = np.where(tip_mask, 0.0, B)

    rdotf = r @ force
    return A * force[np.newaxis, :] + B * rdotf[:, np.newaxis] * r


# ---------------------------------------------------------------------------
# Cusped Bi-Laplacian Kelvinlet — Eq. (18)
# ---------------------------------------------------------------------------

def cusped_bilaplacian(
    points:  np.ndarray,
    center:  np.ndarray,
    force:   np.ndarray,
    epsilon: float = 1.0,
    nu:      float = 0.5,
    cutoff:  float = 5.0,
) -> np.ndarray:
    """
    Cusped Bi-Laplacian Kelvinlet: O(1/r⁹) decay with cusped profile.
    Effectively zero beyond R = |r|/epsilon >= cutoff (default 5.0).
    """
    ba_val = _ba(nu)

    r  = points - center[np.newaxis, :]
    r2 = np.sum(r * r, axis=1, keepdims=True)
    rm = np.sqrt(r2)                          # (N,1)
    R  = rm / epsilon                         # normalized radius (N,1)
    R1 = np.sqrt(R**2 + 1.0)                  # r_eps / epsilon = sqrt(R²+1)

    safe_rm = np.where(rm > 1e-7, rm, 1e-7)
    safe_R  = np.where(R  > 1e-7, R,  1e-7)

    eps5 = epsilon ** 5
    eps7 = epsilon ** 7

    R2   = R ** 2
    R1_9 = R1 ** 9
    R1_10 = R1_9 * R1

    # A coefficient (Eq. 18)
    polyA = ((((512.0*R2 + 2304.0)*R2 + 4032.0)*R2 + 3360.0)*R2 + 1260.0)*R2 + 105.0
    a_term = -512.0 * R * R1_10 + polyA * R1
    polyB_A = 35.0 + R2*(280.0 + R2*(560.0 + R2*(448.0 + 128.0*R2)))
    b_term_A = 128.0 * R * R1_10 - R1**3 * polyB_A
    A = 9.0 / (eps5 * R1_10) * (a_term + 2.0 * ba_val * b_term_A)

    # B coefficient (Eq. 18)
    polyB = R2*(R2*(R2*(128.0*R2 + 576.0) + 1008.0) + 840.0) + 315.0
    b_term = 128.0 * R1_9 - safe_R * polyB     # NOTE: paper uses R, not safe_R at r=0
    B = 18.0 * ba_val / (eps7 * safe_R * R1_9) * b_term

    # Zero out beyond cutoff
    mask  = (R >= cutoff)
    A = np.where(mask, 0.0, A)
    B = np.where(mask, 0.0, B)

    rdotf = r @ force
    return A * force[np.newaxis, :] + B * rdotf[:, np.newaxis] * r


# ---------------------------------------------------------------------------
# Blended sharp brush — mix cusped and smooth
# ---------------------------------------------------------------------------

def sharp_blend(
    points:     np.ndarray,
    center:     np.ndarray,
    force:      np.ndarray,
    epsilon:    float = 1.0,
    nu:         float = 0.5,
    family:     str   = "laplacian",    # "laplacian" | "bilaplacian"
    smooth_w:   float = 0.0,            # 0 = fully cusped, 1 = fully smooth
) -> np.ndarray:
    """
    Linear blend between cusped and smooth variants.

    Args:
        family   : "laplacian" or "bilaplacian"
        smooth_w : 0 → pure cusped, 1 → pure smooth
    """
    if family == "laplacian":
        d_cusp   = cusped_laplacian(points, center, force, epsilon, nu)
        d_smooth = laplacian(       points, center, force, epsilon, nu)
    else:
        d_cusp   = cusped_bilaplacian(points, center, force, epsilon, nu)
        d_smooth = bilaplacian(       points, center, force, epsilon, nu)

    return (1.0 - smooth_w) * d_cusp + smooth_w * d_smooth


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    rng    = np.random.default_rng(3)
    pts    = rng.uniform(-3, 3, (600, 3))
    center = np.zeros(3)
    force  = np.array([0.0, 1.0, 0.0])
    eps    = 1.0
    nu     = 0.4

    for name, fn in [
        ("laplacian",         lambda: laplacian(pts, center, force, eps, nu)),
        ("bilaplacian",       lambda: bilaplacian(pts, center, force, eps, nu)),
        ("cusped_laplacian",  lambda: cusped_laplacian(pts, center, force, eps, nu)),
        ("cusped_bilaplacian",lambda: cusped_bilaplacian(pts, center, force, eps, nu)),
        ("blend(0.5)",        lambda: sharp_blend(pts, center, force, eps, nu, smooth_w=0.5)),
    ]:
        d = fn()
        print(f"{name:25s} | max={np.max(np.linalg.norm(d,axis=1)):.4f}  "
              f"  tip_y={sharp_blend(center[np.newaxis], center, force, eps, nu)[0,1]:.4f}"
              if "blend" in name else
              f"{name:25s} | max={np.max(np.linalg.norm(d,axis=1)):.4f}")
