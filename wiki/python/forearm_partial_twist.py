"""
forearm_partial_twist.py
Forearm partial twist joints via Swing-Twist quaternion decomposition.

Solves the candy-wrapper artifact in LBS forearm rigs by distributing
pronation/supination (twist around the bone axis) across intermediate
forearm joints. Each joint receives slerp(identity, twist_q, t) where
t is its fractional position along the elbow→wrist segment.

Typical chain:
    UpperArm → Elbow → ForearmTwist1(t=0.33) → ForearmTwist2(t=0.66) → Wrist → Hand

Usage:
    import numpy as np
    from forearm_partial_twist import swing_twist_decompose, partial_twist_xform

    # --- offline: compute once per frame ---
    q_rel   = relative_quaternion(elbow_xf, hand_xf)   # see helpers below
    q_twist = swing_twist_decompose(q_rel, twist_axis=np.array([1.,0.,0.]))

    # --- per joint ---
    xf1 = partial_twist_xform(elbow_xf, hand_xf, q_twist, t=0.33)
    xf2 = partial_twist_xform(elbow_xf, hand_xf, q_twist, t=0.66)

Dependencies: NumPy only.
"""

import numpy as np


# ──────────────────────────────────────────────────────────────────────────────
# Quaternion utilities  (x,y,z,w convention matching Houdini vector4)
# ──────────────────────────────────────────────────────────────────────────────

def qnormalize(q: np.ndarray) -> np.ndarray:
    """Normalize quaternion (x,y,z,w). Returns identity if near-zero."""
    n = np.linalg.norm(q)
    return q / n if n > 1e-8 else np.array([0., 0., 0., 1.])


def qconjugate(q: np.ndarray) -> np.ndarray:
    """Conjugate of quaternion (x,y,z,w) = (-x,-y,-z,w)."""
    return np.array([-q[0], -q[1], -q[2], q[3]])


def qmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Hamilton product of two quaternions (x,y,z,w)."""
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return np.array([
        aw*bx + ax*bw + ay*bz - az*by,
        aw*by - ax*bz + ay*bw + az*bx,
        aw*bz + ax*by - ay*bx + az*bw,
        aw*bw - ax*bx - ay*by - az*bz,
    ])


def qslerp(q0: np.ndarray, q1: np.ndarray, t: float) -> np.ndarray:
    """
    Spherical linear interpolation between q0 and q1.
    Always takes the short path (flips q1 if dot < 0).
    """
    dot = np.dot(q0, q1)
    if dot < 0.0:
        q1 = -q1
        dot = -dot
    dot = np.clip(dot, -1.0, 1.0)
    if dot > 0.9995:                      # nearly identical — linear fallback
        return qnormalize(q0 + t * (q1 - q0))
    theta0 = np.arccos(dot)
    theta  = theta0 * t
    sin0   = np.sin(theta0)
    return (np.sin(theta0 - theta) / sin0) * q0 + (np.sin(theta) / sin0) * q1


def mat3_to_quat(R: np.ndarray) -> np.ndarray:
    """Convert 3×3 rotation matrix to quaternion (x,y,z,w). Shepperd method."""
    trace = R[0,0] + R[1,1] + R[2,2]
    if trace > 0:
        s = 0.5 / np.sqrt(trace + 1.0)
        w = 0.25 / s
        x = (R[2,1] - R[1,2]) * s
        y = (R[0,2] - R[2,0]) * s
        z = (R[1,0] - R[0,1]) * s
    elif R[0,0] > R[1,1] and R[0,0] > R[2,2]:
        s = 2.0 * np.sqrt(1.0 + R[0,0] - R[1,1] - R[2,2])
        w = (R[2,1] - R[1,2]) / s
        x = 0.25 * s
        y = (R[0,1] + R[1,0]) / s
        z = (R[0,2] + R[2,0]) / s
    elif R[1,1] > R[2,2]:
        s = 2.0 * np.sqrt(1.0 + R[1,1] - R[0,0] - R[2,2])
        w = (R[0,2] - R[2,0]) / s
        x = (R[0,1] + R[1,0]) / s
        y = 0.25 * s
        z = (R[1,2] + R[2,1]) / s
    else:
        s = 2.0 * np.sqrt(1.0 + R[2,2] - R[0,0] - R[1,1])
        w = (R[1,0] - R[0,1]) / s
        x = (R[0,2] + R[2,0]) / s
        y = (R[1,2] + R[2,1]) / s
        z = 0.25 * s
    return qnormalize(np.array([x, y, z, w]))


def quat_to_mat3(q: np.ndarray) -> np.ndarray:
    """Convert quaternion (x,y,z,w) to 3×3 rotation matrix."""
    x, y, z, w = q
    return np.array([
        [1-2*(y*y+z*z),   2*(x*y-z*w),   2*(x*z+y*w)],
        [  2*(x*y+z*w), 1-2*(x*x+z*z),   2*(y*z-x*w)],
        [  2*(x*z-y*w),   2*(y*z+x*w), 1-2*(x*x+y*y)],
    ])


def orthonormalize(R: np.ndarray) -> np.ndarray:
    """Remove scale from a 3×3 matrix by Gram-Schmidt orthonormalization."""
    x = R[:, 0] / np.linalg.norm(R[:, 0])
    y = R[:, 1] - np.dot(R[:, 1], x) * x
    y = y / np.linalg.norm(y)
    z = np.cross(x, y)
    return np.column_stack([x, y, z])


# ──────────────────────────────────────────────────────────────────────────────
# Core API
# ──────────────────────────────────────────────────────────────────────────────

def relative_quaternion(elbow_xf: np.ndarray, hand_xf: np.ndarray) -> np.ndarray:
    """
    Compute the relative rotation quaternion from elbow to hand in elbow local space.

    Parameters
    ----------
    elbow_xf : (4,4) float
        Elbow joint world-space transform (column-major, row 3 = translation).
    hand_xf : (4,4) float
        Hand/wrist joint world-space transform.

    Returns
    -------
    q_rel : (4,) float  (x,y,z,w)
        Relative rotation quaternion.
    """
    rel_xf  = np.linalg.inv(elbow_xf) @ hand_xf
    rel_rot = orthonormalize(rel_xf[:3, :3])
    return mat3_to_quat(rel_rot)


def swing_twist_decompose(
    q: np.ndarray,
    twist_axis: np.ndarray = np.array([1., 0., 0.]),
) -> np.ndarray:
    """
    Decompose quaternion q into swing × twist, and return the twist component.

    The twist quaternion captures rotation *around* twist_axis only.
    The swing quaternion (rotation perpendicular to twist_axis) is discarded.

    Parameters
    ----------
    q : (4,) float  (x,y,z,w)
        Input rotation quaternion (relative elbow→hand).
    twist_axis : (3,) float
        Bone roll axis in **elbow local space**. Defaults to +X (along bone).
        Must be unit length.

    Returns
    -------
    q_twist : (4,) float  (x,y,z,w)
        Twist component of q around twist_axis. Returns identity if no twist.
    """
    A    = twist_axis / (np.linalg.norm(twist_axis) + 1e-12)
    imag = q[:3]                          # imaginary part (axis × sin θ/2)
    proj = np.dot(imag, A) * A            # projection onto twist axis
    q_twist = np.array([proj[0], proj[1], proj[2], q[3]])
    return qnormalize(q_twist)


def partial_twist_xform(
    elbow_xf: np.ndarray,
    hand_xf: np.ndarray,
    q_twist: np.ndarray,
    t: float,
) -> np.ndarray:
    """
    Build the world-space 4×4 transform for a forearm twist joint at fraction t.

    Parameters
    ----------
    elbow_xf : (4,4) float
        Elbow joint world transform.
    hand_xf : (4,4) float
        Hand/wrist joint world transform.
    q_twist : (4,) float  (x,y,z,w)
        Twist quaternion from swing_twist_decompose().
    t : float
        Position along forearm [0=elbow, 1=wrist]. Typical: 0.33 or 0.66.

    Returns
    -------
    out_xf : (4,4) float
        World-space transform for the intermediate forearm joint.
    """
    identity_q    = np.array([0., 0., 0., 1.])
    partial_q     = qslerp(identity_q, q_twist, t)

    # Elbow base rotation (strip scale)
    elbow_rot = orthonormalize(elbow_xf[:3, :3])

    # Apply partial twist on top of elbow rotation
    twist_rot3 = quat_to_mat3(partial_q)
    final_rot  = elbow_rot @ twist_rot3

    # Interpolated position along forearm
    elbow_pos = elbow_xf[3, :3]          # row-vector convention (Houdini-style)
    hand_pos  = hand_xf[3, :3]
    joint_pos = (1.0 - t) * elbow_pos + t * hand_pos

    out_xf = np.eye(4)
    out_xf[:3, :3] = final_rot
    out_xf[3, :3]  = joint_pos
    return out_xf


def build_forearm_chain(
    elbow_xf: np.ndarray,
    hand_xf: np.ndarray,
    twist_axis: np.ndarray = np.array([1., 0., 0.]),
    fractions: tuple = (0.33, 0.66),
) -> list:
    """
    Build the full set of forearm twist joint transforms in one call.

    Parameters
    ----------
    elbow_xf, hand_xf : (4,4) float
        Elbow and hand world transforms.
    twist_axis : (3,) float
        Bone roll axis in elbow local space.
    fractions : tuple of float
        Twist fractions for each intermediate joint. Default: (0.33, 0.66).

    Returns
    -------
    list of (4,4) float
        One transform per fraction, in the same order.
    """
    q_rel   = relative_quaternion(elbow_xf, hand_xf)
    q_twist = swing_twist_decompose(q_rel, twist_axis)
    return [partial_twist_xform(elbow_xf, hand_xf, q_twist, t) for t in fractions]


# ──────────────────────────────────────────────────────────────────────────────
# Houdini Python SOP helper (hou module optional)
# ──────────────────────────────────────────────────────────────────────────────

def run_in_houdini_python_sop(node):
    """
    Example driver for a Python SOP node in Houdini.
    Reads elbow/hand xforms from skeleton geometry (input 0),
    writes forearm twist transforms back as point attributes.

    Assumes skeleton geometry has:
      - Point 'elbow_pt' (int channel) → elbow joint point index
      - Point 'wrist_pt' (int channel) → wrist/hand joint point index
      - Point attribute 'xform' (matrix4) on each skeleton point

    Outputs: new points with 'xform' attr set to the forearm twist transforms.
    """
    import hou  # type: ignore
    geo       = node.geometry()
    skel      = node.inputs()[0].geometry()
    elbow_idx = node.parm("elbow_pt").eval()
    wrist_idx = node.parm("wrist_pt").eval()
    fractions = [node.parm("t1").eval(), node.parm("t2").eval()]

    # Read elbow / wrist world transforms
    def get_xf(geo, ptnum):
        xf_raw = geo.point(ptnum).attribValue("xform")
        return np.array(xf_raw).reshape(4, 4)

    elbow_xf = get_xf(skel, elbow_idx)
    hand_xf  = get_xf(skel, wrist_idx)

    xforms = build_forearm_chain(
        elbow_xf, hand_xf,
        twist_axis=np.array([1., 0., 0.]),
        fractions=fractions,
    )

    xf_attrib = geo.findPointAttrib("xform")
    if xf_attrib is None:
        xf_attrib = geo.addAttrib(hou.attribType.Point, "xform", [0.]*16)

    for i, xf in enumerate(xforms):
        pt = geo.createPoint()
        pt.setAttribValue(xf_attrib, xf.flatten().tolist())
        pt.setPosition(hou.Vector3(*xf[3, :3]))


# ──────────────────────────────────────────────────────────────────────────────
# Standalone test / demo
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    """
    Demo: forearm rotating 90° around the X-axis (pronation).

    Expected output:
      ForearmTwist1 (t=0.33) receives ~30° of twist
      ForearmTwist2 (t=0.66) receives ~60° of twist
    """
    # Elbow at origin, hand at (10,0,0), both with identity rotation
    elbow_xf = np.eye(4)
    hand_xf  = np.eye(4)
    hand_xf[3, 0] = 10.0   # hand is 10 units along X

    # Rotate hand 90° around X axis (forearm pronation)
    angle = np.pi / 2
    c, s  = np.cos(angle), np.sin(angle)
    hand_xf[:3, :3] = np.array([
        [1,  0,  0],
        [0,  c, -s],
        [0,  s,  c],
    ])

    xforms = build_forearm_chain(
        elbow_xf, hand_xf,
        twist_axis=np.array([1., 0., 0.]),
        fractions=(0.33, 0.66),
    )

    for i, (t, xf) in enumerate(zip((0.33, 0.66), xforms)):
        # Extract rotation angle around X from the rotation matrix
        # R_yx = sin(angle), R_yy = cos(angle) for pure X-axis rotation
        angle_deg = np.degrees(np.arctan2(xf[1, 2], xf[1, 1]))
        print(f"ForearmTwist{i+1} (t={t:.2f}): "
              f"pos={xf[3,:3]}, twist_angle={angle_deg:.1f}°")
        # Expected ~30° and ~60°

    # Decomposition check: reconstruct full twist at t=1.0
    q_rel   = relative_quaternion(elbow_xf, hand_xf)
    q_twist = swing_twist_decompose(q_rel, np.array([1.,0.,0.]))
    angle_full = 2.0 * np.degrees(np.arccos(np.clip(q_twist[3], -1., 1.)))
    print(f"Full twist at wrist: {angle_full:.1f}°  (expect 90.0°)")
