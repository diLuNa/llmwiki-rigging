---
title: "Latent Generative Modelling"
tags: [neural, diffusion, blendshapes, digital-human]
---

## Definition
Two-stage generative modelling in which a compact *latent representation* is learned first (via an autoencoder), then a generative model (diffusion or autoregressive) operates in that latent space rather than on raw pixels/waveforms.

Stage 1 — train autoencoder (encoder + decoder) to learn a spatially-structured latent grid.
Stage 2 — freeze encoder; train generative model on latent codes extracted from training data.

At sample time: generate latent → decode back to input space with the frozen decoder.

## Key Design Axes

### Capacity: Tensor Size Reduction (TSR)
$\text{TSR} = \frac{w_{in} \cdot h_{in} \cdot c_{in}}{w_{out} \cdot h_{out} \cdot c_{out}}$

Higher TSR → smaller, faster generative model but poorer reconstruction. Tuned empirically. Modern image models: 8×–32× spatial downsampling, 4–32 channels (TSR ≈ 4–64×). Video models push 32×–64× spatial+temporal.

### Curation: Which Information Is Kept
The trio of reconstruction losses shapes what latents encode:
- **Regression (L1/L2)**: emphasises low-frequency structure; alone causes blurry reconstructions and erases texture
- **Perceptual (LPIPS)**: encourages feature-level matching; preserves mid-frequency detail
- **Adversarial (GAN)**: encourages realistic high-frequency texture; enables aggressive downsampling without blurring

Removing adversarial → texture erased rather than abstracted. Removing regression → unstable, bad local minima.

### Shape: How Information Is Presented
- **KL regularisation** (VAE-style): in practice scaled down by several orders of magnitude; main effect is outlier suppression, not Gaussianisation. The "V in VAE is vestigial" for modern autoencoders.
- **Equivariance regularisation** (EQ-VAE, AF-VAE): transformations of input produce corresponding transformations in latent → smoother latent spectrum → better modelability
- **Generative prior co-training** (LARP, CRT): lightweight latent model backpropagates into encoder to make latents easier to model
- **Self-supervised supervision** (VA-VAE, MAETok): align latents with DINOv2 or MAE features for semantic regularity

### Topology: Grid vs. Sequence
Most current models inherit the 2D grid of the input ("advanced pixels"). Alternatives gaining traction:
- 1D sequence latents (TiTok, FlowMo) — exploits powerful LLM sequence models
- Variable-length 1D with coarse-to-fine structure (FlexTok, One-D-Piece, Semanticist) — adapts token count to image complexity
- Bag-of-tokens (TokenSet) — abandons grid entirely

## Why Two Stages?
1. **Perceptual signals are highly redundant**: most bits don't affect perception; latents filter them out more precisely than diffusion loss alone
2. **Computational efficiency**: iterative sampling (diffusion/AR) is expensive; doing it in a compact latent space is dramatically faster than in pixel space
3. **Texture/structure separation**: perception works differently at different scales; autoencoders can abstract texture while preserving structure, which a generative model cannot easily do jointly

## Rate-Distortion-Modelability Trade-off
Extension of classical rate-distortion: *modelability* (V-information; how computationally easy it is for a generative model to extract information from latents) is a third axis. Too much compression → unstructured noise that's hard to model. Too little → large representation requires more powerful generative model. Balance tuned empirically.

## Relevance to Character Rigging

| Use case | Latent modelling role |
|----------|-----------------------|
| Neural 3DMMs (ImFace, CoMA) | Autoencoder latent = face shape/expression code; enables interpolation and random generation |
| DiffusionRig | Latent diffusion conditioned on rig parameters for appearance editing |
| Neural blend shapes | Latent codes encode pose-dependent corrective residuals |
| GAN face textures (GANtlitz, EG3D) | VQGAN-style latent enables high-res texture generation |
| Blendshape weight generation | VAE on weight vectors provides a smooth latent for optimization |

## Key External Reference
Dieleman, Sander. "Generative modelling in latent space." sander.ai, 2025-04-15.
(Source: `raw/assets/Generative modelling in latent space.md`)

## Connections
- [[papers/ding-2023-diffusionrig]] — rig-conditioned latent diffusion for facial appearance
- [[papers/zheng-2022-imface]] — implicit neural latent representation for 3D morphable face model
- [[papers/ranjan-2018-coma]] — convolutional mesh autoencoder; latent = shape code
- [[papers/bagautdinov-2018-facial-cvae]] — compositional VAE for face geometry
- [[papers/gruber-2024-gantlitz]] — VQGAN-based multi-modal face texture generation
- [[concepts/neural-blend-shapes]] — neural blend shapes operate in a learned latent space

## Notes
- The "tyranny of the grid" describes the tension between efficient grid-based processing and the non-uniform distribution of perceptual information in images.
- Diffusion decoders (DALL-E 3 consistency decoder, ε-VAE, DiTo) improve quality but increase latency — relevant when real-time decoding matters for production rigs.
- End-to-end (single-stage) approaches are gaining ground (simple diffusion, PixelFlow) but are not yet cost-effective at production resolution.
