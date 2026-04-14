---
title: "Rig Inversion by Training a Differentiable Rig Function"
authors: [Marquis Bolduc, Mathieu; Phan, Hau Nghiep]
venue: SIGGRAPH Asia 2022 Technical Communications
year: 2022
tags: [rig-generation, neural, pose-space]
source: raw/papers/2301.09567v1.pdf
---

## Summary
Trains a differentiable MLP approximation of the rig function, then uses it as a frozen decoder to train an inverse rig model with a **mesh-space loss** rather than a parameter-space loss. The mesh loss sidesteps all three fundamental difficulties of rig inversion — non-surjectivity, non-injectivity, and parameter importance weighting — simultaneously. Achieves ~3–4× lower vertex error than Holden 2015 on a production facial rig.

## Problem
Three properties of production rig functions make inversion hard:

1. **Non-surjectivity**: captured meshes fall outside the rig's output manifold; a parameter-space training set can never cover them.
2. **Non-injectivity**: multiple rig parameter vectors may produce the same mesh. Training with a parameter-space loss causes gradient averaging over conflicting ground truths, producing blurry solutions.
3. **Parameter weighting**: perceptually important parameters affect many mesh vertices; less important ones affect few. A parameter-space regression loss treats them equally.

Prior work (Holden 2015/2017) trains to match parameter vectors directly, which amplifies all three problems on large, complex rigs (137+ parameters).

## Method

### Stage 1: Learn a differentiable rig approximation $\hat{L}_d$

Sample 100 000 random sparse rig parameter vectors; evaluate each through Maya to get the output blendshape weight vector (628 weights → 8447-vertex mesh). Train a decoder-shaped MLP:

```
Input:  rig params r ∈ ℝ¹³⁷   (sparse, uniform random)
Hidden: 2 × 1024, Leaky ReLU
Output: 628 blendshape weights, Sigmoid (forces output ∈ [0,1])
Loss:   MSE on vertex positions (after multiplying weights by blendshape matrix)
```

This is a well-posed regression (L is a function, not just an approximation), so training converges reliably. Achieved 0.78 mm mean vertex error vs. 0.22 mm for a programmatic PyTorch re-implementation of the same rig.

### Stage 2: Train the inverse rig model using $\hat{L}_d$

Compose the frozen $\hat{L}_d$ after the inverse model to form an autoencoder:

```
mesh x  →  [inverse model ˆL⁻¹]  →  r̂  →  [frozen ˆL_d]  →  x̂
                                        Loss: MSE(x, x̂)
```

Training data: randomly combined blendshapes (ignoring rig logic) — these are out-of-manifold but plausible meshes. The rig approximation $\hat{L}_d$ "denoises" them to the nearest in-manifold mesh, resolving non-surjectivity automatically.

Inverse model architecture:
```
Input:  mesh (or blendshape weights) x
Hidden: 4 × [2048, 1024, 512, 256], Leaky ReLU
Output: rig params r̂ ∈ ℝ¹³⁷, tanh (constrains output to rig domain)
```

ReLU activations encourage sparsity in the recovered parameters, which artists prefer. The mesh loss automatically down-weights parameters that have little visible effect.

## Key Results

**EA facial rig (137 params, 628 weights, 8447 vertices):**

| Method | Mean error (random poses) | Mean error (captured data) |
|--------|--------------------------|---------------------------|
| Proposed (programmatic $\hat{L}_d$) | **2.5 mm** | **4.8 mm** |
| Proposed (trained $\hat{L}_d$) | **3.0 mm** | **4.9 mm** |
| Holden et al. 2015 | 9.2 mm | 10.0 mm |

**Temporal coherency** (roughness = squared 2nd-order differences):

| Method | Roughness |
|--------|-----------|
| Proposed (programmatic $\hat{L}_d$) | **3.8 × 10⁻³** |
| Proposed (trained $\hat{L}_d$) | **3.4 × 10⁻³** |
| Direct optimization (programmatic) | 2.3 × 10⁻² |

An encoder-shaped inverse model produces naturally smooth parameter trajectories without explicit regularization, because the network implicitly learns a Lipschitz mapping.

## Limitations
- Requires no artist-posed training sequences, but does require ~100 000 random rig evaluations (offline, via Maya scripting) for $\hat{L}_d$.
- Accuracy ceiling set by $\hat{L}_d$ quality; the approximation introduces 0.78 mm mean error before inversion even begins.
- Not applicable to rigs where the rig function cannot be called automatically (interactive-only rigs).
- No temporal model — sequential coherence comes from the encoder topology, not an explicit motion prior. Cannot enforce global trajectory constraints.
- MLP architecture does not exploit mesh structure; authors note mesh-convolutional architectures as future work.

## Connections
- [[papers/holden-2015-inverse-rig]] — prior method; parameter-space loss compared against
- [[papers/holden-2017-inverse-rig-tvcg]] — extended journal version of Holden 2015 (GPR + NN)
- [[papers/gustafson-2020-inverse-rig]] — complementary analytic Jacobian approach; better for rigs whose operators can be classified as linear-in-angle; this work better for large black-box rigs
- [[papers/an-2024-refined-inverse-rigging]] — related blendshape inverse rigging
- [[papers/song-2020-differential-subspace]] — cited as prior art on rig function approximation
- [[concepts/rig-inversion]]
- [[authors/marquis-bolduc-mathieu]]

## Implementation Notes
- Training data generation for $\hat{L}_d$ is embarrassingly parallel — spin up N Maya instances, each evaluating a shard of random parameter vectors.
- Sparsity in random training inputs is important: select both the number of active parameters and their values from a uniform distribution. Dense random inputs explore unrealistic combinations.
- Tanh output for the inverse model is critical — feeding out-of-domain values to $\hat{L}_d$ produces unpredictable behavior.
- The mesh loss indirectly handles the parameter importance weighting problem: meshes are typically denser in perceptually critical regions (face center, lips, eyes), so errors in parameters that drive those regions receive higher gradient signal.
- The method works on non-blendshape rigs too (the authors show a full-body skeleton rig qualitatively in Fig. 4) — any rig whose output can be evaluated and compared in a vertex-distance metric is compatible.

## Quotes
> "We propose to train the deep learning model inverting the rig function by replacing the loss on the output rig parameter vector r by a loss on the mesh L(L̂⁻¹(x)) resulting from the rig parameter vector L⁻¹ when evaluated by the rig function L." (§3.2)

> "Using an encoder-shaped inverse rig model outputs rig parameters that are an order of magnitude smoother, without need for noise augmentation." (§4.3)
