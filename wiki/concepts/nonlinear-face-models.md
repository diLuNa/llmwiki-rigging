---
title: "Nonlinear 3D Face Models"
tags: [neural, digital-human, blendshapes, rig-generation, appearance, facial-capture]
---

## Definition
A nonlinear 3D face model is any parametric face representation where the mapping from latent code (identity, expression, pose) to 3D geometry is **not** a linear combination of basis shapes. Classical linear 3DMMs (Basel Face Model, FLAME shape basis) use PCA — a single matrix multiply. Nonlinear models replace this with neural networks (MLP, CNN, GCN, implicit network, diffusion, NeRF/3DGS) or physically-motivated nonlinear operators, capturing fine detail and complex shape variation that linear bases cannot represent with a compact number of components.

The canonical linear baseline is FLAME:
```math
M(\beta, \theta, \psi) = W(T + B_S(\beta) + B_P(\theta) + B_E(\psi),\ J(\beta),\ \theta,\ \mathcal{W})
```
where $B_S, B_E$ are PCA bases (linear). Nonlinear models replace one or more of these with learned nonlinear decoders.

## Variants / Taxonomy

### Mesh-Based Autoencoders (Graph Conv)

Learn compact nonlinear latent spaces directly on mesh topology using spectral or spatial graph convolutions.

- [[papers/ranjan-2018-coma]] **(CoMA, ECCV 2018)** — Chebyshev spectral conv + hierarchical mesh pooling; nonlinear face shape space from expression sequences; architectural precursor to FLAME-based neural models
- [[papers/bagautdinov-2018-facial-cvae]] **(Compositional VAE, CVPR 2018)** — hierarchical VAE; region-wise latent decomposition (global identity + local parts); optimized for tracking
- [[papers/zhou-2017-mesh-vae]] **(Mesh VAE + RIMD, 2017)** — RIMD features (rotation-invariant mesh differences) as input to VAE; latent encodes only deformation, not rigid motion

### CNN Encoder-Decoder (Image-Supervised)

Replace PCA basis with a convolutional encoder-decoder trained from 2D images without requiring 3D supervision.

- [[papers/tran-2018-nonlinear-3dmm]] **(Nonlinear 3DMM, CVPR 2018)** — CNN image encoder → nonlinear shape and texture decoder; retains identity/expression factorization; in-the-wild training

### FLAME Extensions & Monocular Reconstruction

Keep FLAME's control structure; improve reconstruction accuracy or add neural residual geometry on top. Forms a coherent MPI-IS lineage: FLAME → DECA → EMOCA → MICA → SMIRK.

- [[papers/feng-2021-deca]] **(DECA, SIGGRAPH 2021)** — FLAME base + per-identity neural displacement $D(\beta, \psi)$; details animate consistently; in-the-wild differentiable rendering
- [[papers/danecek-2022-emoca]] **(EMOCA, CVPR 2022)** — adds perceptual emotion consistency loss to DECA; emotion-faithful expression reconstruction; valence/arousal regression
- [[papers/zielonka-2022-mica]] **(MICA, ECCV 2022)** — metrical FLAME identity prior from ArcFace; 15–24% lower shape error; widely used as frozen identity backbone
- [[papers/retsinas-2024-smirk]] **(SMIRK, CVPR 2024)** — analysis-by-neural-synthesis: neural renderer generates expression-augmented training pairs; current SOTA for in-the-wild expression reconstruction

### Neural Parametric Head Models (Implicit SDF)

Replace the entire FLAME shape+expression basis with local implicit neural fields, enabling full-head capture (hair, teeth, ears).

- [[papers/giebenhain-2023-nphm]] **(NPHM, CVPR 2023)** — ensemble of local SDF fields centered on facial anchors; separate identity SDF + expression deformation field; trained on 5,200+ complete head scans
- [[papers/sevastopolsky-2024-headcraft]] **(HeadCraft, 3DV 2025)** — StyleGAN2 UV displacement maps on top of NPHM; combines coarse NPHM animation with scan-quality geometric detail

### Implicit Neural Representations (Pure SDF)

Represent face geometry as a continuous signed distance field rather than a fixed mesh. Resolution-independent; can capture arbitrary-scale geometric detail.

- [[papers/zheng-2022-imface]] **(ImFace, CVPR 2022)** — SDF with separate identity deformation field $\phi_\text{id}$ and expression deformation field $\phi_\text{exp}$; disentangled by design; no fixed vertex count
- [[papers/zheng-2023-imface-pp]] **(ImFace++, TPAMI 2024)** — RDF (Radial Deformation Field) space; two-stage coarse/fine architecture; adds expression transfer and face editing

### NeRF-Based Morphable Face Models

Map shape, expression, and appearance codes plus 3D coordinate/view direction jointly through a neural radiance field.

- [[papers/zhuang-2022-mofanerf]] **(MoFaNeRF, ECCV 2022)** — first morphable NeRF face model; single MLP jointly encodes shape, expression, appearance; supports fitting, generation, rigging, editing, novel-view synthesis
- [[papers/yu-2023-nofa]] **(NOFA, SIGGRAPH 2023)** — one-shot NeRF avatar via EG3D GAN inversion; single source image; expression driven by FLAME tracker

### 3D Gaussian Splatting Avatars

Real-time-renderable avatars with rig-compatible expression control via 3D Gaussian representations.

- [[papers/qian-2024-gaussian-avatars]] **(GaussianAvatars, CVPR 2024)** — 3DGS splats bound to FLAME triangle local frames; rig-driven real-time rendering; per-Gaussian offset optimization for fine detail
- [[papers/ma-2024-gaussian-blendshapes]] **(3D Gaussian Blendshapes, SIGGRAPH 2024)** — explicit Gaussian $\Delta$ bases; $G(\alpha) = G_0 + \sum \alpha_i G_i$; direct 3DGS analogue of mesh blendshapes; ~370 fps
- [[papers/giebenhain-2024-npga]] **(NPGA, SIGGRAPH Asia 2024)** — NPHM-conditioned Gaussians (richer expression than FLAME); backward-to-forward deformation distillation; +2.6 dB PSNR over prior methods

### Diffusion-Based Shape Models

Generative models over face geometry enabling diverse, localized, or temporally coherent shape generation.

- [[papers/potamias-2024-shapefusion]] **(ShapeFusion, ECCV 2024)** — masked DDPM over FLAME-topology meshes; arbitrary localized edits; any region, not just predefined FACS zones
- [[papers/zou-2024-4d-expression-diffusion]] **(4D Expression Diffusion, ACM TOMM 2024)** — DDPM over 3D landmark trajectories; generates temporally coherent expression sequences; multi-modal conditioning (label, text, partial sequence)

### Neural Blend Shapes (Nonlinear Correctives)

Learn pose-dependent corrective shapes as neural functions of pose rather than RBF interpolation.

- [[papers/li-2021-neural-blend-shapes]] **(SIGGRAPH 2021)** — jointly learns LBS weights + pose-dependent corrective basis from unrigged mesh data; nonlinear PSD via MLP; real-time compatible

### Cross-Identity Retargeting

Encode expression from a source rig into a latent space and decode into a different target rig's blendshape weights.

- [[papers/sol-2025-blendshape-retargeting]] **(2025)** — VAE latent expression encoding + FC decoder; mask-based occlusion handling; cross-identity FACS weight retargeting without corresponding shapes
- [[papers/qiu-2024-freeavatar]] **(FreeAvatar, SIGGRAPH Asia 2024)** — topology-agnostic expression foundation model; contrastive expression similarity training; multi-avatar animator with dynamic identity injection

## Neural Facial Auto-Rigging

End-to-end systems that generate FACS-compatible blendshape rigs for arbitrary meshes without manual shape authoring. See also [[concepts/auto-rigging]].

| Paper | Venue | Key idea |
|-------|-------|----------|
| [[papers/ming-2024-mesh-blendshapes]] | ECCV 2024 | Production-importable FACS rigs from consumer video via neural inverse rendering |
| [[papers/qin-2023-nfr]] | SIGGRAPH 2023 | Neural Jacobian Fields (NJF) + deformation autoencoder; FACS-regularized latent $z_\text{FACS}$ + residual $z_\text{ext}$; arbitrary topology |
| [[papers/hou-2024-neutral-facial-rigging]] | Electronics 2024 | RigGenNet (param → joints) + RigRecogNet (GAN inverse); local constraints on eyes/lips |
| [[papers/ma-2025-riganyface]] | NeurIPS 2025 | DiffusionNet + 2D optical flow supervision on unlabeled meshes; disconnected parts; non-humanoid faces |
| [[papers/canrig-2026-neural-face-rigging]] | EG 2026 | Cross-attention for spatially variable local/global control influence; per-control attention masks |

## Key Concepts

**Why go nonlinear?** Linear PCA blendshape spaces cannot represent:
- Extreme expressions not captured in training data (extrapolation is linear, so it diverges)
- Fine-scale wrinkles and pores that require many PCA components
- Sharp non-Gaussian shape distributions (faces cluster in expression modes, not a single Gaussian)

**Disentanglement** — the core challenge in all nonlinear face models: separating identity $\beta$ from expression $\psi$ in a nonlinear space requires explicit architectural choices (separate decoders, contrastive training, FACS regularization). Linear models get it for free from the PCA factorization.

**Representation evolution:**
| Era | Representation | Rendering | Expression control |
|-----|---------------|-----------|-------------------|
| Pre-2018 | Mesh PCA (FLAME, Basel) | Rasterizer | Linear weights |
| 2018–2021 | GCN / VAE on mesh | Diff. rasterizer | Latent code |
| 2021–2022 | SDF / NeRF | Volume render | Latent code |
| 2023–2024 | 3DGS bound to FLAME/NPHM | Gaussian splat | Rig params |
| 2024– | Diffusion over mesh/latent | — | Masked / conditioned |

**FLAME as hub:** FLAME sits at the center of this cluster. DECA, EMOCA, MICA, SMIRK, DiffusionRig, GaussianAvatars, NPGA, and Animatomy all extend or reference it. Its pose-corrective formulation $B_P(\theta) = \sum_k (R_k - R_k^*) P_k$ is the linear bridge between articulation and nonlinear correction.

**Production compatibility:** Neural models rarely replace blendshape rigs directly in animation. More commonly:
1. They generate or initialize rig shapes (auto-rigging: NFR, RigAnyFace, ming-2024)
2. They provide a richer shape prior for performance capture (MICA, EMOCA, SMIRK)
3. They drive blendshape weights via retargeting (sol-2025, FreeAvatar)
4. They synthesize appearance from rig parameters (DiffusionRig, GaussianAvatars)
5. They provide real-time rendering with expression control (3DGS cluster)

## Connections
- [[concepts/facial-blendshape-rigs]] — the linear production system these nonlinear models extend or interface with
- [[concepts/auto-rigging]] — neural auto-rigging pipeline; these models often provide the shape prior or output format
- [[concepts/rig-inversion]] — tracking/fitting: mapping from images or scans into the nonlinear latent space
- [[concepts/digital-human-appearance]] — DiffusionRig and DECA both model photorealistic appearance on top of face geometry; GaussianAvatars and NPGA handle rendering
- [[concepts/mesh-graph-nets]] — CoMA shares the spectral GCN architecture with MeshGraphNets
- [[concepts/pose-space-deformation]] — nonlinear neural blend shapes are the automated, data-driven version of PSD
- [[concepts/speech-driven-animation]] — 4D expression diffusion is applicable to audio-conditioned expression sequence generation
- [[concepts/implicit-surfaces]] — NPHM, ImFace, MoFaNeRF use SDF/implicit representations
