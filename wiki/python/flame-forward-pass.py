"""
FLAME forward pass — numpy reference implementation.
See wiki/concepts/flame-model.md for full derivation.

FLAME model files (requires MPI-IS license):
  https://flame.is.tue.mpg.de/

Loading official FLAME pkl:
  import pickle
  with open('generic_model.pkl', 'rb') as f:
      flame = pickle.load(f, encoding='latin1')
  T_bar = flame['v_template'].flatten()           # (3*5023,)
  S     = flame['shapedirs']                      # (5023, 3, 300) -> reshape (15069, 300)
  P     = flame['posedirs']                       # (5023, 3, 9K) -> reshape (15069, 9K)
  E     = flame['shapedirs'][..., 300:]           # expression dirs appended in some releases
  J_reg = flame['J_regressor'].toarray()          # (K, 5023)
  W     = flame['weights']                        # (5023, K)
  kintree = flame['kintree_table']                # (2, K) parent table
"""

import numpy as np


def rodrigues(r: np.ndarray) -> np.ndarray:
    """Axis-angle vector (3,) -> rotation matrix (3,3)."""
    theta = np.linalg.norm(r)
    if theta < 1e-8:
        return np.eye(3)
    r_hat = r / theta
    K = np.array([
        [0,       -r_hat[2],  r_hat[1]],
        [r_hat[2], 0,        -r_hat[0]],
        [-r_hat[1], r_hat[0], 0       ]
    ])
    return np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)


def lbs(v: np.ndarray, J: np.ndarray, theta: np.ndarray,
        W: np.ndarray, parents: np.ndarray) -> np.ndarray:
    """
    Linear blend skinning.
    v: (N, 3) vertices in rest pose (after correctives)
    J: (K, 3) joint positions
    theta: (K+1, 3) axis-angle rotations [global, joint_0, ..., joint_K]
    W: (N, K+1) blend weights (including global joint)
    parents: (K+1,) parent index per joint (-1 for root)
    Returns: (N, 3) deformed vertices
    """
    n_joints = theta.shape[0]
    # Build local rotation matrices
    R_local = np.stack([rodrigues(theta[i]) for i in range(n_joints)])  # (K+1, 3, 3)

    # Global transforms: T_j = T_parent * T_local_j
    T = np.zeros((n_joints, 4, 4))
    for i in range(n_joints):
        T_local = np.eye(4)
        T_local[:3, :3] = R_local[i]
        T_local[:3, 3] = J[i] if i == 0 else J[i] - J[parents[i]]
        if parents[i] < 0:
            T[i] = T_local
        else:
            T[i] = T[parents[i]] @ T_local

    # Skinning transform relative to rest pose joint
    G = np.zeros_like(T)
    for i in range(n_joints):
        rest = np.eye(4)
        rest[:3, 3] = J[i]
        G[i] = T[i] @ np.linalg.inv(rest)

    # Weighted sum of transforms
    v_h = np.concatenate([v, np.ones((v.shape[0], 1))], axis=1)  # (N, 4)
    v_out = np.zeros((v.shape[0], 4))
    for i in range(n_joints):
        v_out += W[:, i:i+1] * (G[i] @ v_h.T).T

    return v_out[:, :3]


def flame_forward(
    T_bar: np.ndarray,   # (15069,) mean template
    S:     np.ndarray,   # (15069, 300) shape basis
    P:     np.ndarray,   # (15069, 9K) pose corrective basis (K=4 face joints, not global)
    E:     np.ndarray,   # (15069, 100) expression basis
    J_reg: np.ndarray,   # (K+1, 5023) joint regressor
    W:     np.ndarray,   # (5023, K+1) LBS weights
    parents: np.ndarray, # (K+1,) parent table
    beta:  np.ndarray,   # (300,) shape coefficients
    theta: np.ndarray,   # (15,) = 5 * 3 axis-angle rotations
    psi:   np.ndarray,   # (100,) expression coefficients
) -> np.ndarray:
    """
    Full FLAME forward pass.  Returns (5023, 3) vertex positions.

    theta order: [global(3), neck(3), jaw(3), left_eye(3), right_eye(3)]
    The global rotation is applied through LBS; only joints 1..K drive pose correctives.
    """
    N = T_bar.shape[0] // 3
    K_pose = P.shape[1] // 9  # number of joints with pose correctives (4)

    # 1. Shape
    v_shaped = T_bar + S @ beta                         # (3N,)

    # 2. Joint positions (float with shape)
    V = v_shaped.reshape(N, 3)
    J = J_reg @ V                                       # (K+1, 3)

    # 3. Pose correctives (joints 1..K, not global)
    theta_vecs = theta.reshape(-1, 3)                   # (5, 3)
    R_rest = np.eye(3).flatten()                        # rest = identity
    dR = np.concatenate([
        (rodrigues(theta_vecs[i + 1]).flatten() - R_rest)
        for i in range(K_pose)
    ])                                                  # (9K,)
    v_posed = v_shaped + P @ dR                         # (3N,)

    # 4. Expression
    v_expr = v_posed + E @ psi                          # (3N,)

    # 5. LBS
    v_final = lbs(v_expr.reshape(N, 3), J, theta_vecs, W, parents)

    return v_final                                      # (5023, 3)


# ---------------------------------------------------------------------------
# Example usage (random parameters, no model file needed)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    N, K1, B, X = 5023, 5, 300, 100  # K1 = 5 (global + 4 joints)
    K_pose = K1 - 1                   # 4 joints drive pose correctives

    rng = np.random.default_rng(0)
    T_bar  = rng.standard_normal(3 * N)
    S      = rng.standard_normal((3 * N, B)) * 0.01
    P      = rng.standard_normal((3 * N, 9 * K_pose)) * 0.001
    E      = rng.standard_normal((3 * N, X)) * 0.01
    J_reg  = np.zeros((K1, N)); J_reg[rng.integers(0,K1,K1), rng.integers(0,N,K1)] = 1.0
    W      = np.abs(rng.standard_normal((N, K1))); W /= W.sum(1, keepdims=True)
    parents = np.array([-1, 0, 1, 1, 1])  # root, neck<-root, jaw<-neck, eyes<-neck

    beta  = np.zeros(B)
    theta = np.zeros(3 * K1)
    theta[6] = 0.3                         # open jaw slightly
    psi   = np.zeros(X)
    psi[0] = 1.0                           # first expression component

    verts = flame_forward(T_bar, S, P, E, J_reg, W, parents, beta, theta, psi)
    print(f"Output vertices: {verts.shape}")   # (5023, 3)
    print(f"Centroid: {verts.mean(0)}")
