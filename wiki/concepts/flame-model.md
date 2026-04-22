---
title: "FLAME Face Model"
tags: [blendshapes, correctives, pose-space, lbs, digital-human, rig-generation, math]
---

## Definition
FLAME (Faces Learned with an Articulated Model and Expressions) is a statistical parametric 3D face model representing identity shape, head/jaw articulation, and facial expressions in a single unified function. It applies the SMPL body model architecture to the head, adding expression blendshapes that SMPL lacks. The model consists of **N = 5023 vertices** and **K = 4 rig joints** (neck, jaw, left eyeball, right eyeball), with a global head rotation.

$$M(\beta, \theta, \psi) = W\!\bigl(T_P(\beta, \theta, \psi),\; J(\beta),\; \theta,\; \mathcal{W}\bigr)$$

where the posed template is:

$$T_P(\beta, \theta, \psi) = \bar{T} + B_S(\beta;\mathcal{S}) + B_P(\theta;\mathcal{P}) + B_E(\psi;\mathcal{E})$$

**Parameters:**
| Symbol | Dim | Meaning |
|--------|-----|---------|
| $\beta$ | 300 | Shape (identity) coefficients |
| $\theta$ | 15 | Pose — 5 rotation vectors $\in \mathbb{R}^3$ (global + neck + jaw + 2 eyes) |
| $\psi$ | 100 | Expression coefficients |

**Learned components:**
| Symbol | Dim | Meaning |
|--------|-----|---------|
| $\bar{T}$ | $3N$ | Mean template (zero-pose, neutral) |
| $\mathcal{S}$ | $3N \times 300$ | Orthonormal shape basis (PCA over 3800 subjects) |
| $\mathcal{P}$ | $3N \times 9K$ | Pose corrective basis (linear in rotation matrix elements) |
| $\mathcal{E}$ | $3N \times 100$ | Orthonormal expression basis (PCA from 4D sequences) |
| $\mathcal{J}$ | $K \times N$ | Sparse joint regressor (joints float with shape) |
| $\mathcal{W}$ | $N \times K$ | LBS blend weights |

## Formulation Detail

**Shape blendshapes** — linear PCA over identity:
$$B_S(\beta;\mathcal{S}) = \sum_{n=1}^{|\beta|} \beta_n \mathbf{S}_n$$

**Pose blendshapes** — linear in rotation matrix elements; identical to SMPL $B_P$:
$$B_P(\theta;\mathcal{P}) = \sum_{n=1}^{9K} \bigl(R_n(\theta) - R_n(\theta^*)\bigr)\mathbf{P}_n$$

where $\theta^*$ is the rest pose. Non-linear in $\theta$ (via the rotation map), linear in the matrix elements. Trained from head-pose data of 10 subjects (~8000 registered frames).

**Expression blendshapes** — linear PCA over expression residuals:
$$B_E(\psi;\mathcal{E}) = \sum_{n=1}^{|\psi|} \psi_n \mathbf{E}_n$$

Expression residuals computed by removing pose influence, then applying PCA across 69,000 D3DFACS + self-captured frames. The resulting basis $\mathcal{E}$ is orthonormal and expression-specific.

**Joint regression** — joints float with subject shape (important: avoid using fixed joint positions):
$$J(\beta) = \mathcal{J}(\bar{T} + B_S(\beta))$$

**LBS** — standard linear blend skinning applied after all correctives:
$$v_{\text{final}} = \text{LBS}\bigl(T_P, J(\beta), \theta, \mathcal{W}\bigr)$$

## Fitting Pipeline
Three-stage registration per scan:

1. **Model-only fit** — optimize $(\beta, \theta, \psi)$ with scan-to-mesh + 49-landmark + prior terms. Fast (~25s/frame). Initializes expression.
2. **Coupled fit** — jointly optimize $(\beta, \theta, \psi)$ and the template $T$ with a coupling term $E_C = \sum_e \lambda_e \|T_e - M(\beta,\theta,\psi)_e\|$ (edge differences) + Laplacian regularization $E_R$. (~50s/frame)
3. **Texture-based** — adds photometric term $E_T$ from Ratio-of-Gaussians filtered textures. (~80s/frame)

**Alternating bootstrap:** model training alternates with registration — 4 iterations. Expression space trained before pose correctives to avoid expression overfitting.

## Training Data Summary
| Component | Data | Subjects |
|-----------|------|----------|
| Shape ($\mathcal{S}$) | CAESAR body database | 3800 |
| Pose correctives ($\mathcal{P}$) | Self-captured head/jaw sequences | 10 |
| Expressions ($\mathcal{E}$) | D3DFACS + self-captured 4D (69k frames, 21k used) | 12+ |

## Downstream Ecosystem

| System | What it adds | Wiki |
|--------|-------------|------|
| SMPL-X | Full body + face: integrates FLAME as the head component | — |
| DECA | Per-identity neural displacement map $D(\beta,\psi)$ on top of FLAME geometry | [[papers/feng-2021-deca]] |
| EMOCA | Perceptual emotion loss on top of DECA training | [[papers/danecek-2022-emoca]] |
| MICA | ArcFace-based metrical identity prior (better $\beta$) | [[papers/zielonka-2022-mica]] |
| SMIRK | Analysis-by-neural-synthesis FLAME fitting; SOTA expression reconstruction | [[papers/retsinas-2024-smirk]] |
| DiffusionRig | Rig-conditioned diffusion over FLAME-based renders | [[papers/ding-2023-diffusionrig]] |
| INSTA | Instant-NGP hash-grid anchored to FLAME mesh | [[papers/zielonka-2023-insta]] |
| GaussianAvatars | 3DGS splats bound to FLAME triangle local frames | [[papers/qian-2024-gaussian-avatars]] |
| NPGA | NPHM-conditioned Gaussians; richer than FLAME expression | [[papers/giebenhain-2024-npga]] |
| Animatomy | Borrows FLAME $B_P(\theta)$ corrective formulation for production rig | [[papers/choi-2022-animatomy]] |
| Face Anything | FLAME coordinate system used as canonical correspondence space for 4D recon | [[papers/kocasari-2026-face-anything]] |
| NPHM | Replaces FLAME mesh with local SDF ensemble; retains conceptual split identity/expression | [[papers/giebenhain-2023-nphm]] |

## Variants / Taxonomy

**Texture models** — FLAME-based texture space (separate, not in base model):
- RingNet (CVPR 2019) — texture-free FLAME fitting from images
- DECA UV displacement map — per-identity wrinkle detail in UV space

**FLAME-compatible datasets:**
- D3DFACS — 4D expression sequences (public, registered to FLAME topology)
- NoW Challenge — neutral face scan evaluation benchmark
- VOCA (SIGGRAPH Asia 2019) — speech-driven 3D face animation using FLAME

**License:** Academic use only, requires registration at `flame.is.tue.mpg.de`. MPI-IS model release includes male + female models, blendweights, landmark embeddings, and Python code.

## Implementation Notes

```python
import numpy as np

def rodrigues(r):
    """Axis-angle to rotation matrix (per-joint)."""
    theta = np.linalg.norm(r)
    if theta < 1e-8:
        return np.eye(3)
    r /= theta
    K = np.array([[0, -r[2], r[1]], [r[2], 0, -r[0]], [-r[1], r[0], 0]])
    return np.eye(3) + np.sin(theta)*K + (1-np.cos(theta))*(K @ K)

def flame_forward(T_bar, S, P, E, J_reg, W, beta, theta, psi):
    """
    T_bar: (3N,) mean template
    S: (3N, |beta|) shape basis
    P: (3N, 9K) pose corrective basis
    E: (3N, |psi|) expression basis
    J_reg: (K, N) joint regressor
    W: (N, K) LBS weights
    """
    N = T_bar.shape[0] // 3
    K = J_reg.shape[0]

    # Shape
    v_shaped = T_bar + S @ beta                          # (3N,)

    # Joints (float with shape)
    V = v_shaped.reshape(N, 3)
    J = J_reg @ V                                        # (K, 3)

    # Pose correctives
    R_flat = []
    R_mats = []
    theta_vecs = theta.reshape(-1, 3)                    # (K+1, 3): global + K joints
    R_rest = np.eye(3).flatten()                         # rest pose rotation
    for i in range(1, K + 1):                            # skip global rotation
        R = rodrigues(theta_vecs[i])
        R_flat.append(R.flatten() - R_rest)
    dR = np.concatenate(R_flat)                          # (9K,)
    v_posed = v_shaped + P @ dR                          # (3N,)

    # Expression
    v_expr = v_posed + E @ psi                           # (3N,)

    # LBS (simplified — full implementation needs global transform tree)
    # See full FLAME PyTorch code at flame.is.tue.mpg.de
    return v_expr.reshape(N, 3)
```

**Key gotchas:**
- The 5 rotation vectors in $\theta$ are ordered: `[global, neck, jaw, left_eye, right_eye]`
- Expression coefficients $\psi$ are zero-mean; $\psi = 0$ gives neutral expression
- Pose correctives use 9K elements (9 per rotation matrix, K joints — **not** the global rotation)
- The joint regressor $\mathcal{J}$ operates on the **shaped** (not mean) template to correctly float joint locations with identity
- Male and female models have separate $\{\bar{T}, \mathcal{S}, \mathcal{W}, \mathcal{J}\}$ — always use matched pair
- Expression space is NOT FACS-aligned by default; a learned mapping matrix $\Phi$ (expression $\rightarrow$ AU) must be trained separately if FACS control is needed

## Connections
- [[papers/li-2017-flame]] — original paper
- [[papers/loper-2015-smpl]] — FLAME extends SMPL architecture to face
- [[concepts/linear-blend-skinning]] — LBS used for articulation
- [[concepts/pose-space-deformation]] — $B_P(\theta)$ are pose-space correctives
- [[concepts/blendshapes]] — $B_E(\psi)$ is a linear blendshape basis
- [[concepts/nonlinear-face-models]] — FLAME as the linear baseline many nonlinear models extend
- [[papers/choi-2022-animatomy]] — production rig using FLAME's $B_P$ formulation
