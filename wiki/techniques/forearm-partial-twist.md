---
title: "Forearm Partial Twist — Swing-Twist Decomposition"
tags: [vex, python, houdini, skinning, lbs, rig-generation, kine-fx]
---

## Overview

The **forearm partial twist** (also called *forearm roll* or *twist bone*) is a standard character rigging technique that prevents the **candy-wrapper artifact**: when the wrist/hand rotates around the forearm axis (pronation/supination), a single-joint LBS wrist collapses into a pinched spiral. The fix is to insert one or two intermediate joints between the elbow and wrist, each receiving a *fraction* of the total wrist twist, so the deformation rolls gradually along the forearm.

This technique is ubiquitous in game and film rigs (Maya HumanIK, Unreal MetaHuman, KineFX) and applies cleanly on top of any joint-based skinning system (LBS, DQS, CoR).

---

## The Candy-Wrapper Problem

In standard LBS with a single wrist joint:

```
UpperArm → Elbow → Wrist (twist_fraction=1.0) → Hand
```

Vertices skinned to the elbow AND the wrist simultaneously interpolate between two extreme rotations. When the wrist pronates 90°, the intermediate vertices receive a blend that spirals — the classic candy-wrapper twist.

**Root cause:** LBS interpolates rotation matrices linearly, not along geodesics. The rotation blend is not isometric.  
**DQS** [[papers/kavan-2007-dqs]] partially mitigates this (dual-quaternion slerp preserves volume better), but it does **not** eliminate the twist artifact for large forearm rolls — it reduces bulging but the angular distribution problem remains.  
**CoR skinning** [[papers/le-2016-cor-skinning]] also does not solve it — CoR targets volume preservation, not twist distribution.

The correct fix requires *distributing* the twist rotation across multiple joints.

---

## Algorithm: Swing-Twist Decomposition

### Theory

Any rotation quaternion $Q$ can be uniquely decomposed with respect to a reference axis $\hat{A}$ as:

$$Q = Q_{\text{swing}} \times Q_{\text{twist}}$$

where:
- $Q_{\text{twist}}$ = rotation **around** $\hat{A}$ (the forearm bone axis)
- $Q_{\text{swing}}$ = rotation **perpendicular** to $\hat{A}$ (bending)

To extract $Q_{\text{twist}}$ from $Q = (x, y, z, w)$:

1. Project the imaginary part $\vec{v} = (x, y, z)$ onto $\hat{A}$:  
   $\vec{p} = (\vec{v} \cdot \hat{A})\,\hat{A}$
2. Reconstruct: $Q_{\text{twist}} = \text{normalize}(p_x,\, p_y,\, p_z,\, w)$
3. Fallback to identity if $\|Q_{\text{twist}}\| < \epsilon$ (no twist present)

The intermediate forearm joint receives:

$$Q_{\text{partial}} = \text{slerp}(\mathbf{I},\; Q_{\text{twist}},\; t)$$

where $t \in [0,1]$ is the joint's position along the forearm (0 = elbow, 1 = wrist).

### Setup

```
UpperArm → Elbow → ForearmTwist1 (t=0.33) → ForearmTwist2 (t=0.66) → Wrist → Hand
```

- **ForearmTwist1** at 1/3 of the forearm: receives 33% of the wrist twist
- **ForearmTwist2** at 2/3 of the forearm: receives 66% of the wrist twist
- **Wrist** at $t=1.0$: receives the full twist (driven by FK/IK solver)

The position of each intermediate joint is linearly interpolated: $\mathbf{p} = \text{lerp}(\mathbf{p}_{\text{elbow}},\, \mathbf{p}_{\text{wrist}},\, t)$.

---

## Houdini VEX Implementation

Source: [[vex/forearm-partial-twist.vex]]

**Setup: Geometry Wrangle SOP on a 1-point geometry.**  
Plug elbow skeleton SOP into input 1, hand/wrist into input 2.

```vex
// 1. Read transforms
matrix4 elbow_xf = detail(0, "elbow_xform");
matrix4 hand_xf  = detail(0, "hand_xform");
float   t        = detail(0, "twist_fraction", 0.5);
vector  A        = normalize(detail(0, "twist_axis", {1,0,0}));

// 2. Relative rotation: elbow → hand in elbow local space
matrix4 rel_xf  = invert(elbow_xf) * hand_xf;
matrix3 rel_rot = /* orthonormalize */ matrix3(rel_xf);
vector4 q_rel   = quaternion(rel_rot);

// 3. Swing-Twist decomposition
vector imag     = set(q_rel.x, q_rel.y, q_rel.z);
float  proj_len = dot(imag, A);
vector proj     = proj_len * A;
vector4 twist_q = normalize(set(proj.x, proj.y, proj.z, q_rel.w));

// 4. Partial twist via slerp
vector4 partial_twist = slerp({0,0,0,1}, twist_q, t);
if (dot(partial_twist, {0,0,0,1}) < 0)
    partial_twist = -partial_twist;   // stay in short-path hemisphere

// 5. Assemble output transform
matrix3 final_rot = matrix3(elbow_xf) * qconvert(partial_twist);
vector  joint_pos = lerp(set(elbow_xf.wx,elbow_xf.wy,elbow_xf.wz),
                         set(hand_xf.wx, hand_xf.wy, hand_xf.wz), t);
// → assemble into matrix4 → setdetailattrib "forearm_xform"
```

**Parameter reference:**

| Attribute | Type | Default | Meaning |
|-----------|------|---------|---------|
| `elbow_xform` | matrix4 (detail) | — | Elbow world-space transform |
| `hand_xform` | matrix4 (detail) | — | Hand/wrist world-space transform |
| `twist_fraction` | float (detail) | 0.5 | 0=elbow, 1=wrist |
| `twist_axis` | vector (detail) | `{1,0,0}` | Bone roll axis in elbow local space |
| `use_inputs` | int (detail) | 0 | 1 = read from SOP inputs 1 & 2 |

**Outputs:** `forearm_xform` (matrix4), `forearm_r` (euler), `forearm_t` (position).

---

## Python Implementation

Source: [[python/forearm_partial_twist.py]]

NumPy module; usable in a Houdini Python SOP or standalone.

```python
import numpy as np
from forearm_partial_twist import swing_twist_decompose, partial_twist_xform

# Decompose wrist rotation
q_twist = swing_twist_decompose(q_rel, twist_axis=np.array([1,0,0]))

# Partial twist for ForearmTwist1 (t = 0.33)
out_xf = partial_twist_xform(elbow_xf, hand_xf, q_twist, t=0.33)
```

---

## KineFX Integration (Houdini)

In a **KineFX** rig, forearm twist joints are typically driven via a **Channel Wrangle** or **Rig Pose** node reading from the skeleton's `xform` point attributes:

```
Skeleton SOP (full chain)
  → [Split] → elbow joint point, wrist joint point
  → forearm-partial-twist.vex (1-pt geometry) × 2 runs
  → Channel Wrangle: set twist joint transform from "forearm_xform"
```

Alternatively, use a **Control Wrangle** that reads `point(0,"xform",elbow_ptnum)` directly from the skeleton, skipping the detail attribute plumbing.

**Twist axis from skeleton (auto-derive):**
```vex
// Derive twist axis from bone direction instead of hardcoding
vector hand_pos  = set(hand_xf.wx, hand_xf.wy, hand_xf.wz);
vector elbow_pos = set(elbow_xf.wx, elbow_xf.wy, elbow_xf.wz);
vector bone_world = normalize(hand_pos - elbow_pos);
// Transform into elbow local space
vector A = normalize(bone_world * invert(matrix3(elbow_xf)));
```

---

## Gotchas & Edge Cases

### 1. Quaternion hemisphere flip (> 180° rotation)
`slerp` takes the short path (< 180°). For wrist rolls beyond 180°, the extracted `twist_q` may flip sign. The dot-product hemisphere check in the VEX snippet handles this for the slerp range. For continuous full-rotation animation (e.g., a screwdriver motion), track an integer turn counter and unwrap the angle:

```vex
// Unwrap: detect sign flip across frames
float prev_dot = detail(0, "prev_twist_dot", 1.0);
if (dot(twist_q, prev_q) < 0) twist_q = -twist_q;
setdetailattrib(0, "prev_twist_dot", dot(twist_q, {0,0,0,1}));
```

### 2. Twist axis must match bone direction
If `twist_axis` points perpendicular to the bone, decomposition extracts swing instead of twist. Verify:

```vex
vector bone_dir_world = {1,0,0} * matrix3(elbow_xf);
// Should point from elbow toward wrist. If not, flip or choose a different axis.
```

### 3. Scale in transforms
The VEX snippet orthonormalizes the rotation before decomposition (strips scale). If the skeleton has non-uniform scale, verify `elbow_xf` and `hand_xf` represent rigid-body transforms or pre-strip scale.

### 4. Number of twist joints
- **1 twist joint** at $t=0.5$: adequate for most game rigs, visible seam at fast rolls
- **2 twist joints** at $t=0.33, 0.66$: film-quality; standard for photoreal characters
- **3+ twist joints**: rarely necessary; use only if cloth or skin simulation requires very smooth surface normals along the forearm

---

## Comparison with Alternative Approaches

| Approach | Twist artifact | Volume preservation | Cost | Notes |
|----------|---------------|---------------------|------|-------|
| Plain LBS (no twist joints) | Severe candy-wrapper | Poor | Free | Unacceptable for close-ups |
| **Partial twist joints (this technique)** | None | Good | +1–2 joints | Industry standard |
| DQS [[papers/kavan-2007-dqs]] | Reduced (not eliminated) | Good (bulge-free) | Same as LBS | Doesn't fix the angular distribution |
| CoR skinning [[papers/le-2016-cor-skinning]] | Not addressed | Excellent | Pre-computation | Targets collapsing, not twist |
| Pose-space correctives (PSD) | Correctable | Good | Corrective shapes | Overkill for twist; use for extreme poses |

---

## Related

- [[vex/forearm-partial-twist.vex]] — Houdini Geometry Wrangle implementation
- [[python/forearm_partial_twist.py]] — NumPy Python module
- [[papers/kavan-2007-dqs]] — dual-quaternion skinning (partial mitigation of twist artifact)
- [[papers/le-2016-cor-skinning]] — centers of rotation (volume preservation, not twist distribution)
- [[concepts/linear-blend-skinning]] — the root cause of the candy-wrapper artifact
- [[techniques/bandage-smoothing-vex]] — another skinning artifact correction technique
