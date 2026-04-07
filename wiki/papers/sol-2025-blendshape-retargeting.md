---
title: "A New Blendshape-Based Retargeting for 3D Facial Expression"
authors: [Sol, A.; Seo, Y. H.; (Omotion R&D)]
venue: International Journal (2025)
year: 2025
tags: [blendshapes, correctives, digital-human, rig-generation, neural, facial-capture]
source: raw/papers/A new blendshape-based retargeting for 3D facial expression.pdf
---

## Summary
Proposes a neural pipeline for retargeting facial expressions across 3D characters with different blendshape rigs. Uses a mask-based approach to handle occlusion and facial asymmetry, a VAE-based latent space for expression encoding, and a fully-connected decoder that produces target blendshape weights from source expression features. Enables high-quality cross-identity facial expression transfer without requiring corresponding shapes between source and target rigs.

## Problem
Facial expression retargeting between different 3D characters is difficult because blendshape rigs are character-specific: the same expression is represented by different blendshape combinations on different characters. Direct weight copying produces incorrect expressions; full rig-aware correspondences are expensive to establish manually.

## Method
**Overall pipeline:**
1. **Expression encoding**: Extract geometric features from the source 3D face mesh (vertex positions, normals, or mesh deformation). A mask mechanism handles occluded or asymmetric facial regions.

2. **3D geometry model**: The source face is parameterized via a 3D morphable model or blendshape basis, aligning to a canonical space. Baseline shapes are used as a reference for computing expression deltas.

3. **VAE latent space**: Expression features are encoded into a compact latent code $z$ via a variational autoencoder. The KL regularization ensures a smooth, interpolable latent space:
$$\mathcal{L} = \mathcal{L}_{\text{recon}} + \lambda_{\text{KL}} D_{KL}(q(z|x) \| \mathcal{N}(0,I))$$

4. **Blendshape decoder**: A fully-connected network decodes $z$ into target blendshape weights, which are applied to the target character's blendshape rig. The decoder is trained with paired supervision on expression+blendshape weight datasets.

5. **Displacement and rotation**: The method handles both mesh displacement components and rotational deformation (jaw articulation, cheek puff), not just pure displacement targets.

**Mask-based robustness**: A spatial mask allows the network to down-weight unreliable facial regions (lower face occlusion, asymmetric expressions), improving retargeting accuracy on challenging inputs.

## Key Results
- Accurate retargeting across diverse face identities (human and non-human characters).
- Mask-based approach handles facial asymmetry and partial occlusion better than unmasked baselines.
- The VAE latent space enables smooth expression interpolation between key poses.
- Evaluated on blendshape reconstruction error and perceptual studies.

## Limitations
- Limited technical detail is publicly available; exact architecture and dataset not fully disclosed.
- Requires a blendshape rig on the target character — does not generate a rig from scratch.
- Training data needs paired (source expression, target blendshape weight) supervision.

## Connections
- [[papers/li-2021-neural-blend-shapes]] — neural approach to generating blendshape-compatible deformations; related automatic rig learning
- [[papers/li-2017-flame]] — FLAME's expression space is a natural source representation for retargeting
- [[papers/loper-2015-smpl]] — related statistical parametric face space
- [[papers/bermano-2013-facial-performance]] — facial performance processing in a shape space, related problem domain
- [[concepts/blendshapes]] — the retargeting target is a blendshape weight vector
- [[concepts/digital-human-appearance]] — facial expression retargeting is a key component of digital human production pipelines

## Implementation Notes
The core retargeting operation at runtime:
```python
# Given source 3D face mesh (N vertices), target rig with K blendshapes:
z = encoder(source_features, mask)          # VAE encode
w_target = decoder(z)                       # predicted blendshape weights, shape (K,)
v_out = v_neutral + sum(w_target[k] * delta[k] for k in range(K))
```
The mask can be computed from face landmark visibility or a semantic segmentation of the input face.
