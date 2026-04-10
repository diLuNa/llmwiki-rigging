"""
rigid_body_rest.py
Geometric resting analysis of convex rigid bodies.

Source: "Putting Rigid Bodies to Rest"
  Baktash, Sharp, Zhou, Jacobson, Crane — ACM ToG / SIGGRAPH 2025
  DOI: 10.1145/3731203

Theory:
  Given a convex body, the probability of landing on face i when dropped
  from a random orientation (negligible momentum) equals:
      p_i = area(Morse-Smale basin_i on Gauss sphere) / 4π

  For convex polyhedra, the Morse-Smale basins are well-approximated by
  the Spherical Voronoi cells of the face normals on S².

  The support function h(n) = max_{x ∈ K} n·x evaluates the extent of
  the body in direction n. The potential energy for a given contact normal
  n (floor normal pointing into the body) is V(n) = h(-n).

  Quasi-static drop trajectory: gradient descent of V(n) on S², tracking
  transitions between vertex/edge/face contact configurations.

API:
  - support_function(vertices, directions)       → h values per direction
  - convex_hull_gauss_map(vertices)              → normals, face centroids
  - check_face_stability(hull, com)              → stable mask, margins
  - compute_spherical_voronoi_areas(normals)     → cell areas on S²
  - resting_probabilities(vertices, com)         → p_i per face
  - drop_trajectory(vertices, com, n0, steps)    → trajectory on S²
  - inverse_design_target_probs(hull, com, p_target, iters) → deformed hull

Dependencies: NumPy, SciPy (ConvexHull, SphericalVoronoi)
"""

import numpy as np
from scipy.spatial import ConvexHull, SphericalVoronoi
from scipy.optimize import minimize


# ──────────────────────────────────────────────────────────────────────────────
# Support Function
# ──────────────────────────────────────────────────────────────────────────────

def support_function(vertices: np.ndarray, directions: np.ndarray) -> np.ndarray:
    """
    Evaluate the support function h(n) = max_{x ∈ hull} n·x for each direction.

    Parameters
    ----------
    vertices   : (N, 3) float — convex body vertices
    directions : (M, 3) float — unit query directions (will be normalized)

    Returns
    -------
    h : (M,) float — support function values
    supporting_indices : (M,) int — index of supporting vertex per direction
    """
    D = directions / (np.linalg.norm(directions, axis=1, keepdims=True) + 1e-12)
    dots = D @ vertices.T          # (M, N)
    supporting_indices = np.argmax(dots, axis=1)
    h = dots[np.arange(len(D)), supporting_indices]
    return h, supporting_indices


def potential_energy(vertices: np.ndarray, contact_normals: np.ndarray) -> np.ndarray:
    """
    V(n) = h(-n) — COM height when body contacts floor with normal n pointing up.

    Parameters
    ----------
    vertices        : (N, 3) float
    contact_normals : (M, 3) float — unit vectors pointing from floor into body

    Returns
    -------
    V : (M,) float
    """
    h, _ = support_function(vertices, -contact_normals)
    return h


# ──────────────────────────────────────────────────────────────────────────────
# Gauss Map (Convex Hull)
# ──────────────────────────────────────────────────────────────────────────────

def convex_hull_gauss_map(vertices: np.ndarray):
    """
    Compute the convex hull and its Gauss map.

    Returns
    -------
    hull        : scipy.spatial.ConvexHull
    face_normals: (F, 3) float — outward unit normals per face (Gauss-map points)
    face_areas  : (F,) float  — 3D face areas
    com_hull    : (3,) float  — centroid of convex hull (volume-weighted COM)
    """
    hull = ConvexHull(vertices)

    # Outward face normals (already unit in scipy ConvexHull)
    face_normals = hull.equations[:, :3]           # (F, 3), outward unit normals
    # Ensure they point outward from interior
    centroid = np.mean(vertices[hull.vertices], axis=0)

    face_normals_out = []
    face_areas = []
    for i, simplex in enumerate(hull.simplices):
        v0, v1, v2 = vertices[simplex]
        n = np.cross(v1 - v0, v2 - v0)
        area = np.linalg.norm(n) * 0.5
        n_unit = n / (np.linalg.norm(n) + 1e-12)
        # Flip if pointing inward
        fc = (v0 + v1 + v2) / 3.0
        if np.dot(n_unit, fc - centroid) < 0:
            n_unit = -n_unit
        face_normals_out.append(n_unit)
        face_areas.append(area)

    face_normals = np.array(face_normals_out)
    face_areas   = np.array(face_areas)

    # Volume-weighted COM (divergence theorem on convex hull)
    # COM = (1 / (4 * Volume)) * Σ_face (n_i · c_i) * (c_i_x + c_i_y + c_i_z ...) * area_i
    # Simplified: use average of face centroids weighted by area (approximate for demo)
    face_centroids = np.array([
        np.mean(vertices[s], axis=0) for s in hull.simplices
    ])
    com_hull = np.sum(face_centroids * face_areas[:, None], axis=0) / face_areas.sum()

    return hull, face_normals, face_areas, com_hull


# ──────────────────────────────────────────────────────────────────────────────
# Face Stability
# ──────────────────────────────────────────────────────────────────────────────

def point_in_triangle_2d(p: np.ndarray, a: np.ndarray, b: np.ndarray,
                          c: np.ndarray) -> tuple:
    """
    Check if 2D point p is inside triangle (a,b,c).
    Returns (inside: bool, min_signed_dist: float margin to nearest edge).
    """
    def sign(p1, p2, p3):
        return (p1[0]-p3[0])*(p2[1]-p3[1]) - (p2[0]-p3[0])*(p1[1]-p3[1])

    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    inside  = not (has_neg and has_pos)

    # Margin = minimum signed distance to any edge (positive = inside)
    def edge_sd(p, a, b):
        e = b - a
        n = np.array([-e[1], e[0]])
        n = n / (np.linalg.norm(n) + 1e-12)
        return np.dot(p - a, n)

    margin = min(edge_sd(p, a, b), edge_sd(p, b, c), edge_sd(p, c, a))
    return inside, margin


def check_face_stability(hull: ConvexHull, vertices: np.ndarray,
                          com: np.ndarray) -> tuple:
    """
    For each hull face (triangle), check if COM projects inside the face.
    Stable resting ⟺ COM projection inside face (no tendency to roll off).

    Parameters
    ----------
    hull     : scipy.spatial.ConvexHull
    vertices : (N, 3) float — original vertices
    com      : (3,) float  — center of mass

    Returns
    -------
    stable  : (F,) bool  — True if face is a stable resting configuration
    margins : (F,) float — signed distance of COM projection to nearest face edge
    """
    stable  = []
    margins = []

    for simplex in hull.simplices:
        v0, v1, v2 = vertices[simplex]

        # Face normal (outward)
        e1 = v1 - v0
        e2 = v2 - v0
        n  = np.cross(e1, e2)
        n  = n / (np.linalg.norm(n) + 1e-12)
        # Ensure outward
        fc = (v0 + v1 + v2) / 3.0
        centroid = np.mean(vertices[hull.vertices], axis=0)
        if np.dot(n, fc - centroid) < 0:
            n = -n; v1, v2 = v2, v1; e1, e2 = v2-v0, v1-v0

        # Project COM onto face plane
        proj = com - np.dot(com - v0, n) * n

        # 2D basis in face plane
        b1 = e1 / (np.linalg.norm(e1) + 1e-12)
        b2 = np.cross(n, b1)

        # 2D coordinates
        def to2d(p): return np.array([np.dot(p - v0, b1), np.dot(p - v0, b2)])

        p2  = to2d(proj)
        a2  = to2d(v0)
        b2_ = to2d(v1)
        c2  = to2d(v2)

        inside, margin = point_in_triangle_2d(p2, a2, b2_, c2)
        stable.append(inside)
        margins.append(margin)

    return np.array(stable), np.array(margins)


# ──────────────────────────────────────────────────────────────────────────────
# Spherical Voronoi Cell Areas (proxy for Morse-Smale basin areas)
# ──────────────────────────────────────────────────────────────────────────────

def compute_spherical_voronoi_areas(face_normals: np.ndarray) -> np.ndarray:
    """
    Compute the Spherical Voronoi cell area on S² for each face normal.
    This approximates the Morse-Smale basin area → resting probability.

    p_i ≈ cell_area_i / (4π)

    Parameters
    ----------
    face_normals : (F, 3) float — unit outward normals (Gauss-map points on S²)

    Returns
    -------
    areas : (F,) float — spherical Voronoi cell areas
    """
    # SphericalVoronoi requires points on unit sphere
    normals = face_normals / (np.linalg.norm(face_normals, axis=1, keepdims=True) + 1e-12)

    # Remove duplicate normals (parallel faces) — keep unique within tolerance
    _, unique_idx = np.unique(normals.round(6), axis=0, return_index=True)
    unique_normals = normals[np.sort(unique_idx)]

    if len(unique_normals) < 4:
        # Degenerate: return uniform distribution
        return np.full(len(face_normals), 4 * np.pi / len(face_normals))

    sv = SphericalVoronoi(unique_normals, radius=1.0, center=np.zeros(3))
    sv.sort_vertices_of_regions()
    cell_areas_unique = np.array([sv.calculate_areas()[i] for i in range(len(unique_normals))])

    # Map back to original normals (duplicate normals share the same area)
    areas = np.zeros(len(face_normals))
    unique_normals_set = {tuple(unique_normals[i].round(6)): cell_areas_unique[i]
                          for i in range(len(unique_normals))}
    for i, n in enumerate(normals):
        key = tuple(n.round(6))
        areas[i] = unique_normals_set.get(key, 0.0)

    return areas


# ──────────────────────────────────────────────────────────────────────────────
# Full Resting Probability Pipeline
# ──────────────────────────────────────────────────────────────────────────────

def resting_probabilities(vertices: np.ndarray, com: np.ndarray = None) -> dict:
    """
    Compute resting probability for each face of the convex hull.

    Parameters
    ----------
    vertices : (N, 3) float — mesh vertices (will be convex-hulled)
    com      : (3,) float  — center of mass; if None, uses hull centroid

    Returns
    -------
    dict with keys:
      'hull'         — scipy ConvexHull
      'face_normals' — (F, 3) outward unit normals
      'stable'       — (F,) bool, stable faces
      'margins'      — (F,) float, COM margin per face
      'voronoi_area' — (F,) float, spherical Voronoi cell area
      'prob'         — (F,) float, resting probability (sums to ~1 over stable faces)
      'com'          — (3,) float, center of mass used
    """
    hull, face_normals, face_areas, com_hull = convex_hull_gauss_map(vertices)
    if com is None:
        com = com_hull

    stable, margins = check_face_stability(hull, vertices, com)
    vor_areas       = compute_spherical_voronoi_areas(face_normals)

    # Raw probability from Voronoi cell area / 4π
    FOUR_PI = 4.0 * np.pi
    prob_raw = vor_areas / FOUR_PI

    # Zero out unstable faces
    prob_raw[~stable] = 0.0

    # Normalize (so stable face probabilities sum to 1)
    total = prob_raw.sum()
    prob  = prob_raw / (total + 1e-12)

    return {
        'hull':         hull,
        'face_normals': face_normals,
        'stable':       stable,
        'margins':      margins,
        'voronoi_area': vor_areas,
        'prob':         prob,
        'com':          com,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Quasi-Static Drop Trajectory
# ──────────────────────────────────────────────────────────────────────────────

def drop_trajectory(vertices: np.ndarray, com: np.ndarray,
                    n0: np.ndarray, steps: int = 200,
                    step_size: float = 0.02) -> np.ndarray:
    """
    Simulate quasi-static rolling from initial contact normal n0.
    Performs gradient descent of V(n) = h(-n) on S².

    Parameters
    ----------
    vertices  : (N, 3) float — convex hull vertices
    com       : (3,) float  — center of mass
    n0        : (3,) float  — initial contact normal (pointing up from floor)
    steps     : int         — maximum gradient descent steps
    step_size : float       — step size on S²

    Returns
    -------
    trajectory : (T, 3) float — sequence of contact normals on S²
                                (T ≤ steps+1, terminates at stable face)
    """
    hull = ConvexHull(vertices)
    face_normals_raw = np.array([
        np.cross(vertices[s[1]] - vertices[s[0]], vertices[s[2]] - vertices[s[0]])
        for s in hull.simplices
    ])
    face_normals = face_normals_raw / (
        np.linalg.norm(face_normals_raw, axis=1, keepdims=True) + 1e-12
    )
    centroid = np.mean(vertices[hull.vertices], axis=0)
    # Ensure outward normals
    for i, (s, n) in enumerate(zip(hull.simplices, face_normals)):
        fc = np.mean(vertices[s], axis=0)
        if np.dot(n, fc - centroid) < 0:
            face_normals[i] = -n

    n_curr = n0 / (np.linalg.norm(n0) + 1e-12)
    traj = [n_curr.copy()]

    for _ in range(steps):
        V_curr = potential_energy(vertices, n_curr[None])[0]

        # Euclidean gradient of V on R³, then project onto tangent plane of S²
        eps = 1e-4
        grad = np.zeros(3)
        for j in range(3):
            dv = np.zeros(3); dv[j] = eps
            V_p = potential_energy(vertices, (n_curr + dv)[None])[0]
            V_m = potential_energy(vertices, (n_curr - dv)[None])[0]
            grad[j] = (V_p - V_m) / (2 * eps)

        # Project gradient onto tangent plane of S² at n_curr
        grad_tan = grad - np.dot(grad, n_curr) * n_curr

        grad_norm = np.linalg.norm(grad_tan)
        if grad_norm < 1e-6:
            break   # at critical point

        # Descend: move opposite to gradient, re-project onto S²
        n_next = n_curr - step_size * grad_tan / grad_norm
        n_next = n_next / (np.linalg.norm(n_next) + 1e-12)

        # Check for convergence (snap to nearest face normal if very close)
        dots = face_normals @ n_next
        i_near = np.argmax(dots)
        if dots[i_near] > 0.999:
            n_next = face_normals[i_near]
            traj.append(n_next.copy())
            break   # reached a face — settled

        traj.append(n_next.copy())
        n_curr = n_next

    return np.array(traj)


# ──────────────────────────────────────────────────────────────────────────────
# Inverse Design: Shape with Target Resting Probabilities
# ──────────────────────────────────────────────────────────────────────────────

def inverse_design_target_probs(vertices: np.ndarray, com: np.ndarray,
                                  target_face_idx: list,
                                  target_probs: list,
                                  iters: int = 100,
                                  lr: float = 0.01) -> np.ndarray:
    """
    Deform the convex hull so that specified faces achieve target resting probs.
    Simplified gradient descent on vertex positions (convex shape preserved via
    re-convex-hulling at each step).

    Parameters
    ----------
    vertices        : (N, 3) float — initial vertices
    com             : (3,) float  — fixed center of mass
    target_face_idx : list of int — face indices to target
    target_probs    : list of float — desired probabilities for those faces
    iters           : int         — optimization steps
    lr              : float       — learning rate (vertex perturbation scale)

    Returns
    -------
    vertices_opt : (N, 3) float — optimized vertex positions
    loss_history : list of float
    """
    verts = vertices.copy().astype(float)
    loss_history = []

    for it in range(iters):
        result = resting_probabilities(verts, com)
        prob   = result['prob']

        # Loss: sum of squared differences for target faces
        loss = 0.0
        for fi, pi in zip(target_face_idx, target_probs):
            if fi < len(prob):
                loss += (prob[fi] - pi) ** 2
        loss_history.append(loss)

        if loss < 1e-8:
            break

        # Numerical gradient w.r.t. each vertex coordinate
        grad = np.zeros_like(verts)
        eps  = 1e-3
        for vi in range(len(verts)):
            for d in range(3):
                verts[vi, d] += eps
                r_p = resting_probabilities(verts, com)
                loss_p = sum((r_p['prob'][fi] - pi)**2
                             for fi, pi in zip(target_face_idx, target_probs)
                             if fi < len(r_p['prob']))
                verts[vi, d] -= 2 * eps
                r_m = resting_probabilities(verts, com)
                loss_m = sum((r_m['prob'][fi] - pi)**2
                             for fi, pi in zip(target_face_idx, target_probs)
                             if fi < len(r_m['prob']))
                verts[vi, d] += eps
                grad[vi, d] = (loss_p - loss_m) / (2 * eps)

        verts -= lr * grad

    return verts, loss_history


# ──────────────────────────────────────────────────────────────────────────────
# Houdini Python SOP Helper
# ──────────────────────────────────────────────────────────────────────────────

def run_in_houdini_python_sop(node):
    """
    Compute resting probabilities for the input mesh and write results
    back as primitive attributes.

    Input 0: mesh geometry (any topology; will be convex-hulled)
    Adds:
      prim attr  "stable"      int   — 1 if face is a stable resting config
      prim attr  "rest_prob"   float — resting probability for this face
      prim attr  "margin"      float — COM margin (positive = well inside)
      detail attr "voronoi_area" float[] — spherical Voronoi cell areas
      detail attr "com"        vector — center of mass used
    """
    import hou  # type: ignore

    geo = node.geometry()
    pts = np.array([p.position() for p in geo.points()])

    # COM: from detail attribute, else centroid
    com_raw = geo.attribValue("com") if geo.findGlobalAttrib("com") else None
    com = np.array(com_raw) if com_raw else pts.mean(axis=0)

    result = resting_probabilities(pts, com)

    # Write primitive attributes
    stable_attr  = geo.addAttrib(hou.attribType.Prim, "stable",  0)
    prob_attr    = geo.addAttrib(hou.attribType.Prim, "rest_prob", 0.0)
    margin_attr  = geo.addAttrib(hou.attribType.Prim, "margin",   0.0)

    prims = list(geo.prims())
    for i, prim in enumerate(prims):
        if i < len(result['stable']):
            prim.setAttribValue(stable_attr,  int(result['stable'][i]))
            prim.setAttribValue(prob_attr,    float(result['prob'][i]))
            prim.setAttribValue(margin_attr,  float(result['margins'][i]))

    # Write detail attributes
    vor_area_list = result['voronoi_area'].tolist()
    geo.addAttrib(hou.attribType.Global, "voronoi_area", [0.0] * len(vor_area_list))
    geo.setGlobalAttribValue("voronoi_area", vor_area_list)

    com_list = result['com'].tolist()
    geo.addAttrib(hou.attribType.Global, "com", hou.Vector3(0, 0, 0))
    geo.setGlobalAttribValue("com", hou.Vector3(*com_list))


# ──────────────────────────────────────────────────────────────────────────────
# Standalone Demo
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    """
    Demo: analyze resting probabilities of a standard cube and a tetrahedron.
    """
    print("=" * 60)
    print("DEMO: Resting probabilities of a unit cube")
    print("=" * 60)

    # Unit cube vertices
    cube = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
    ], dtype=float)
    com_cube = np.array([0.5, 0.5, 0.5])

    result = resting_probabilities(cube, com_cube)
    print(f"Faces analyzed: {len(result['prob'])}")
    print(f"Stable faces:   {result['stable'].sum()}")
    print(f"Probabilities (stable faces):")
    for i, (s, p) in enumerate(zip(result['stable'], result['prob'])):
        if s:
            print(f"  Face {i:3d}: {p:.4f}  (margin={result['margins'][i]:.4f})")
    print(f"Sum of probs: {result['prob'].sum():.4f}  (expect ~1.0)")

    print()
    print("=" * 60)
    print("DEMO: Drop trajectory from n0 = [0, 0, 1] (initial flat orientation)")
    print("=" * 60)

    n0   = np.array([0.0, 0.0, 1.0])
    traj = drop_trajectory(cube, com_cube, n0, steps=100)
    print(f"Trajectory length: {len(traj)} steps")
    print(f"Start:  {traj[0].round(4)}")
    print(f"End:    {traj[-1].round(4)}")

    print()
    print("=" * 60)
    print("DEMO: Regular tetrahedron — all 4 faces should be equally likely (~0.25)")
    print("=" * 60)

    # Regular tetrahedron
    s = np.sqrt(2.0 / 3.0)
    tet = np.array([
        [0,  0,  1],
        [2*s, 0, -1/3],
        [-s,  np.sqrt(1 - s*s - (1/3)**2) if (1-s*s-(1/3)**2) > 0 else s, -1/3],
        [-s, -np.sqrt(1 - s*s - (1/3)**2) if (1-s*s-(1/3)**2) > 0 else s, -1/3],
    ], dtype=float)
    # Simpler: unit tetrahedron from ConvexHull
    tet_simple = np.array([
        [1,  1,  1],
        [1, -1, -1],
        [-1,  1, -1],
        [-1, -1,  1],
    ], dtype=float)
    com_tet = tet_simple.mean(axis=0)   # = [0,0,0]

    result_tet = resting_probabilities(tet_simple, com_tet)
    print(f"Faces analyzed: {len(result_tet['prob'])}")
    stable_probs = result_tet['prob'][result_tet['stable']]
    print(f"Stable face probabilities: {stable_probs.round(4)}")
    print(f"Expected: ~{1/len(stable_probs):.4f} each  "
          f"(variance: {np.var(stable_probs):.6f})")
