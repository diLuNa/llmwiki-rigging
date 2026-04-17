---
title: "MIRRORED-Anims: Motion Inversion for Rig-space Retargeting to Obtain a Reliable Enlarged Dataset of Character Animations"
authors: [Unknown; see project page mirrored-anims.github.io]
venue: ACM SIGGRAPH Conference on Motion, Interaction, and Games (MIG) 2025
year: 2025
tags: [rig-generation, motion-retargeting, inverse-rig, skinning, lbs]
source: raw/assets/MIRRORED-Anims_ Motion Inversion for Rig-space Retargeting to Obtain a Reliable Enlarged Dataset of Character Animations _ Proceedings of the 2025 18th ACM SIGGRAPH Conference on Motion, Interaction, and Games.md
---

## Summary
MIRRORED-Anims is an open-source, rig-based motion retargeting system that transfers motion between skinned humanoid characters of different morphologies. It automatically builds a template control rig for any input character, performs analytic rig inversion to extract controller values from a source animation, then retargets in rig-space. It outperforms all learning-based methods on Mixamo test data (MSE 0.008 vs next best 0.284) and generates the omaxiM dataset (2446 motions × 40 characters) as an open-source alternative to the restricted Mixamo dataset.

## Problem
Learning-based retargeting methods (SAN, R²ET, SMTNet) train exclusively on the Mixamo dataset, which is small (≈12 characters), restricted by Adobe's license, and contains significant ground-penetration artifacts. There is no way to generate large, diverse, high-quality paired training data without a reliable, explainable, open-source retargeting baseline.

## Method

### Automatic Control Rig Construction
A template Blender control rig (provided by a professional rigger) is automatically fitted to any humanoid skeleton:
- **Heel bone placement**: SVD on foot-skinned vertices in ground-plane projection → oriented bounding box → heel bone position
- **Foot roll mechanism**: dual-hinge system using Copy Rotation + Limit Rotation constraints (handles dorsiflexion, pronation/supination)
- **Hip controller**: placed under pelvis at thigh height to prevent leg-stretch during forward lean
- **Arm/leg IK**: standard Blender IK with auto-placed pole targets for elbow/knee orientation
- **Spine**: single controller whose rotation is split equally among all spine bones (scales to N spines)
- **Fingers**: single controller per finger; rotation drives proximal phalanx, scale drives curl of remaining phalanges

### Analytic Rig Inversion
Because all characters share the same rig template, the inversion can be solved analytically:
1. Place hip controller so rig pelvis matches source pelvis
2. Rotate spine/neck controllers to match last spine/head world rotation
3. Solve foot rotation via case-disjunction on heel and toe rotations
4. Solve finger scale/rotation from first and last phalanx rotations
5. Place IK effectors (hand/foot) at matching world positions; determine pole target angles from elbow/knee positions

Average joint position error: 6.06 × 10⁻³ m (mean), 6.77 × 10⁻² m (worst joint). Some error is irreducible due to over-constrained fingers and distributed spine.

### Rig-Space Retargeting
**Driving controller weighting**: assigns a soft weight to each extremity controller (hands, feet, hips) based on three factors combined multiplicatively:

```math
w_c^f = \frac{1}{1+\alpha h_c^f} \cdot \frac{1}{1+\gamma v_c^f} \cdot \frac{1}{1+\beta \|h_c^f - p_{\text{COM}}^f\|}
```

where $h_c^f$ = height, $v_c^f$ = speed, and $p_{\text{COM}}^f$ = projected center-of-mass. The softmax of this weight vector identifies which controller is "driving" each frame.

For each frame, compute target controller positions by scaling source-relative offsets by the ratio of limb lengths source/target, propagating from driving foot → hip → other foot → spine → hands → poles.

### Collision Refinement (Section 7)
Torso approximated as a set of truncated cones fitted to spine bone slices via least-squares circle fitting. Each cone is LBS-skinned to spine bones. For any IK effector close to the torso:
1. Convert effector to T-pose position using inverse LBS with softmax-weighted proximity to cone circles
2. Identify which cone slice it falls in; express position in cone-surface local frame
3. Transfer to corresponding cone slice on target; invert LBS to get final world position
4. Interpolate between raw retargeted position and collision-resolved position based on proximity

## Key Results
| Method | MSE ↓ | MSE_lc ↓ | Pen.% ↓ |
|--------|--------|----------|---------|
| Ours | **0.008** | **0.002** | **3.04** |
| SMTNet | 0.284 | 0.229 | 3.50 |
| NKN | 0.326 | 0.231 | 8.71 |
| SAN | 0.435 | 0.255 | 9.74 |
| R²ET | 0.499 | 0.496 | 7.62 |

Training R²ET on omaxiM (their dataset) instead of Mixamo: MSE drops 0.447 → 0.360, Pen.% drops 9.32 → 8.24. Demonstrates dataset quality impact.

Real-time retargeting to/from SMPL is supported.

## Limitations
- Rig inversion is only analytic because all characters share the same fixed template rig. Any deviation from the template structure requires re-deriving the inversion rules.
- Inversion error is non-zero for over-constrained joints (fingers, spine); maximum joint error can reach 15 cm for extreme poses.
- Retargeting is purely kinematic — no dynamics, no secondary motion, no physical plausibility beyond contact preservation.
- Torso collision approximation (cones) is coarse; does not handle arm self-collisions or thigh-torso contacts.
- Only humanoid bipedal characters; no quadrupeds or multi-limb rigs.

## Connections
- [[concepts/rig-inversion]] — this paper implements a novel analytic rig inversion as part of a retargeting pipeline
- [[papers/holden-2015-inverse-rig]] — pioneered data-driven inverse rig mapping; MIRRORED-Anims cites it as prior work
- [[papers/marquis-bolduc-2022-differentiable-rig]] — alternative: differentiable rig function approximation; MIRRORED-Anims uses analytic rules instead
- [[papers/gustafson-2020-inverse-rig]] — analytic Jacobian learning; MIRRORED-Anims similarly avoids learned inversion
- [[papers/aberman-2020-skeleton-aware-retargeting]] — SAN; a learning-based baseline outperformed by MIRRORED-Anims

## Implementation Notes
- Built in Blender (open source). Control rig template available on project page.
- Rig inversion algorithm described conceptually in Section 5; full pseudo-code in Supplementary Material.
- The omaxiM dataset can be used as a drop-in replacement for Mixamo to train learning-based methods.
- The method requires a standard humanoid T-pose skeleton. Non-humanoid or non-T-posed rigs are not handled automatically.
- LBS inversion for collision refinement uses softmax-weighted proximity to cone circles as proxy skinning weights — not exact skinning-weight inversion.

## Quotes
> "Because it relies solely on transparent, explainable rig operations, MIRRORED-Anims can be used to generate ground-truth motions for any humanoid character, providing a reliable baseline for the future training of learning-based methods."
