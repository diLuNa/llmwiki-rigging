---
title: "Dem Bones — Skinning Decomposition in Production"
tags: [skinning, lbs, rig-generation, weights, houdini, auto-rigging]
papers: [le-2012-ssdr, le-2014-skeletal-rigging]
---

## What Is Dem Bones

**Dem Bones** is the EA SEED open-source C++ library and CLI tool that implements **Smooth Skinning Decomposition with Rigid Bones (SSDR)** and its skeletal rigging extension. It converts any animated mesh sequence (geometry cache, FBX, Alembic) into a skinned LBS model — automatically computing joint positions, bone transforms, and sparse skinning weights.

EA has used it in production since 2015. Released under BSD 3-Clause in 2019.

- GitHub: [github.com/electronicarts/dem-bones](https://github.com/electronicarts/dem-bones)
- EA announcement: [ea.com/seed/news/open-source-dem-bones](https://www.ea.com/seed/news/open-source-dem-bones)

### What It Solves

| Input | Output |
|-------|--------|
| Animated mesh sequence (consistent topology) | Bone transforms (per-frame rigid matrices) |
| Optional: existing skin weights | Sparse, non-negative skinning weights |
| Optional: skeleton with joint positions | Joint positions (in joint-position mode) |

Converts offline work (simulation, motion capture, complex Python rigs) into a game-engine–compatible LBS model at the press of a button.

---

## Three Operating Modes

### Mode 1 — Full Decomposition (auto joints + weights)
*Input: mesh sequence only*
Runs the full SSDR pipeline from [[papers/le-2012-ssdr]]:
1. K-means cluster per-vertex best-fit transforms → initial bone set
2. Alternate: weight update (NNLS + sparsity) ↔ transform update (SVD Procrustes)
3. Optionally run skeletal rigging extension from [[papers/le-2014-skeletal-rigging]]: solve joint positions + prune redundant bones

### Mode 2 — Weight Solving (skeleton given)
*Input: mesh sequence + skeleton pose sequence*
Given joint transforms from an existing rig, solve only for the skinning weights $W$. Useful for baking a complex rig down to a simpler skeleton (fewer bones, different topology).

### Mode 3 — Transform Solving (weights given)
*Input: mesh sequence + skinning weights*
Given fixed per-vertex weights, solve for per-frame bone transforms. Useful as a retargeting utility or when weights are painted by hand and transforms need to be inferred from motion.

---

## Houdini Integration — Dem Bones Skinning Converter SOP

SideFX Labs ships a **Dem Bones Skinning Converter SOP** wrapping the EA library.

Documentation: [sidefx.com/docs/houdini/nodes/sop/dembones_skinningconverter](https://www.sidefx.com/docs/houdini/nodes/sop/dembones_skinningconverter.html)

### Setup

```
geo_cache (geo sequence) ─┐
                          ├─ Dem Bones Skinning Converter SOP
optional skeleton ────────┘
         │
         ▼ FBX export (bones + weights)
         ▼ or: prim/point attrs @captureweight, @capturepath for KineFX
```

### Key SOP Parameters

| Parameter | Typical Value | Meaning |
|-----------|--------------|---------|
| Max Number of Bones | 20–60 | Upper bound on extracted bone count; pruning may reduce it |
| Bind Pose Frame | 0 or rest frame index | Frame used as rest pose for weight solving |
| Global Iterations | 30 | Outer SSDR alternation iterations |
| Transform Iterations | 5 | Inner SVD iterations per global step |
| Splitting Iterations | 5 | Bone splitting / initialization refinement steps |
| Weights Iterations | 1–5 | NNLS inner iterations per weight update |
| Smoothness | 0.01–0.1 | Spatial weight smoothness $\lambda$ (0 = raw SSDR) |
| Min Non-Zero Weights | 1–4 | Sparsity constraint $p$ per vertex |
| Error Tolerance | 1e-4 | Early stopping threshold |

**Gotcha:** The SOP requires clean geometry (consistent topology, no self-intersections, no NaN positions). Set Min Non-Zero Weights to 1 if the solver gets stuck.

### Typical Houdini Pipeline

```
1. INPUT
   Animated mesh sequence (Alembic or geo sequence)
   → Ensure consistent point count across frames

2. DEM BONES SKINNING CONVERTER SOP
   → Set frame range, bind pose, target bone count
   → Run "Save to Disk" (bakes FBX output)
   → SOP also writes capture attrs in-place:
       @captureweight  (float[], one per bone)
       @capturepath    (string[], bone names)

3. KINEFX INTEGRATION
   Bone Capture Biharmonic (or Capture Attribute Unpack)
   → Animate with the extracted skeleton
   → Use Capture Layer Paint SOP to touch up weights

4. EXPORT
   → ROP FBX Output with skeleton + blended skin
   → Or use as LBS deformer directly in Houdini via
     Bone Deform SOP + extracted transforms
```

---

## Algorithm Summary (for VEX / Python reference)

The SSDR alternating optimization:

```
initialize:
  B = k-means on per-vertex best-fit transforms (SVD per vertex, F frames)

repeat until convergence:
  # Weight update (per vertex, independent)
  for each vertex i:
    W[i] = argmin ||V[i] - sum_k w_ik * B[k] @ V0[i]||²
    subject to: w >= 0, sum(w) = 1, ||w||_0 <= p
    (solved via NNLS + greedy sparsity drop)

  # Transform update (per bone, per frame)
  for each bone k, frame f:
    weighted_verts = {(W[i,k] * V0[i], W[i,k] * V[i,f]) for all i}
    R[k,f], T[k,f] = SVD_Procrustes(weighted_verts)
```

For the **skeletal rigging extension** (joint positions):
```
# Joint update (per bone)
for each bone k:
  j[k] = argmin sum_f ||T[k,f] - (I - R[k,f]) @ j[k]||²
  (closed-form linear solve)
```

---

## Comparison: SSDR vs Dem Bones vs Other Baking Methods

| Method | Input | Joint Positions | Weight Quality | Notes |
|--------|-------|-----------------|---------------|-------|
| SSDR (Le 2012) | Mesh sequence | ✗ (transforms only) | Good | Original paper |
| Le 2014 (skeletal) | Mesh sequence | ✓ (auto) | Good + smooth | Extension via joint constraints |
| Dem Bones (EA) | Mesh/FBX/Alembic | ✓ | Good + smooth | Production implementation of both |
| Houdini Dem Bones SOP | Any geo sequence | ✓ | Good | UI wrapper, exports FBX |
| Maya Bake Deformer | Maya rig | ✓ (from rig) | OK | Weight-solving mode only |
| Neural (RigNet) | Static mesh | ✓ | Varies | No animation sequence needed |

---

## Use Cases in Character Rigging

1. **Simulation baking** — FEM soft-body or cloth sim → LBS for real-time
2. **Rig approximation** — heavy Python/VEX rig → light LBS for game engine export
3. **Scan rig extraction** — performance capture mesh sequence → animatable skeleton
4. **Blend shape to LBS** — facial blend shapes → small bone set for mobile/VR
5. **Weight transfer** — new skeleton topology, paint-free: let SSDR solve the weights

---

## External References

- EA Dem Bones GitHub: [github.com/electronicarts/dem-bones](https://github.com/electronicarts/dem-bones)
- EA SEED announcement: [ea.com/seed/news/open-source-dem-bones](https://www.ea.com/seed/news/open-source-dem-bones)
- Houdini SOP docs: [sidefx.com/docs/houdini/nodes/sop/dembones_skinningconverter](https://www.sidefx.com/docs/houdini/nodes/sop/dembones_skinningconverter.html)
- SideFX Labs showcase: [sidefxlabs.artstation.com/projects/AqOz4L](https://sidefxlabs.artstation.com/projects/AqOz4L)
- Maya implementation: [robertjoosten.github.io/projects/dem_bones](https://robertjoosten.github.io/projects/dem_bones/)
- Primary paper: [[papers/le-2012-ssdr]]
- Skeletal rigging extension: [[papers/le-2014-skeletal-rigging]]
