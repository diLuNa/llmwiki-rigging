---
title: "FACS-Guided t-SNE / UMAP Clustering of Expression Poses"
date: 2026-04-22
tags: [blendshapes, facs, neural, python, digital-human, pose-space]
context: "Face PCA model with 253 identity + 382 expression parameters, 100k animated poses"
---

## Problem

Given 100k animated expression poses (each described by 382 PCA expression parameters), cluster them so that poses with similar FACS-region activation land close together in 2D. The goal is a t-SNE / UMAP map where each point is a pose and spatial proximity reflects perceptual/anatomical similarity.

## Core Insight

PCA expression parameters are orthogonal in *variance space*, not in *perceptual/anatomical space*. A single PCA component may span multiple face regions. To get FACS-meaningful clustering you need features that respect anatomical region boundaries.

**Two approaches:**

| | Option A | Option B |
|---|---|---|
| **Input** | 382 PCA params | Decoded mesh vertices |
| **Features** | PCA params directly | Per-FACS-region mean displacement |
| **Cluster meaning** | PCA geometry | Regional face activation |
| **Requires decoder?** | No | Yes (`pca_basis`, `mean_face`) |
| **Quality** | Baseline | FACS-meaningful |

---

## Option A — Direct t-SNE on PCA Parameters

```python
# Pre-reduce with PCA (t-SNE doesn't scale to 382D / 100k points directly)
pre = PCA(n_components=50, random_state=0)
X = pre.fit_transform(expression_params)   # (100k, 50)

# UMAP (preferred) or t-SNE
reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.05)
embedding = reducer.fit_transform(X)       # (100k, 2)
```

Fast, no decoder needed. Clusters by PCA geometry — useful as a sanity check but not inherently FACS-aligned.

---

## Option B — FACS Region Displacement Features

### Pipeline

```
expression_params (N, 382)
    ↓  @ pca_basis (382, V×3)  + mean_face
vertex positions (N, V, 3)
    ↓  subtract mean → delta (N, V, 3)
    ↓  mean per FACS region → (N, 3) per region
region features (N, R×3)   ← R ≈ 18 regions
    ↓  StandardScaler + optional pre-PCA
UMAP / t-SNE → embedding (N, 2)
```

### FACS Region Definitions

18 regions covering major AU groups. Each region = a set of vertex indices:

| Region | AU(s) | Muscle |
|---|---|---|
| inner_brow L/R | AU1 | frontalis, medial |
| outer_brow L/R | AU2 | frontalis, lateral |
| brow_lower L/R | AU4 | corrugator + depressor supercilii |
| upper_eyelid L/R | AU5/7 | levator palpebrae / palpebral orbicularis |
| cheek L/R | AU6 | orbital orbicularis |
| nose | AU9 | LLSAN |
| upper_lip L/R | AU10/12 | levator labii / zygomaticus major |
| lip_corner L/R | AU12/15 | zygomaticus major / depressor anguli oris |
| lower_lip | AU16/17 | depressor labii / mentalis |
| orbicularis | AU22–24 | orbicularis oris |
| jaw | AU26/27 | masseter / pterygoids |

### Dominant-Region Labelling

For each pose, identify the region with largest displacement magnitude → use as a colour label on the map:

```python
magnitudes = np.stack([
    np.linalg.norm(features[:, i*3:(i+1)*3], axis=1)
    for i in range(n_regions)
], axis=1)  # (N, R)
dominant_region = magnitudes.argmax(axis=1)  # (N,)
```

### Per-Region Overlay Plots

Plot one subplot per FACS region, each coloured by displacement magnitude. This lets you verify that each region activates in a spatially coherent part of the embedding — if AU12 (lip corner) poses cluster together and light up on the lip_corner subplot, the features are working correctly.

---

## Implementation

Full Python implementation: `[[python/facs_pose_tsne.py]]`

Functions:
- `embed_from_pca_params()` — Option A
- `decode_to_vertices()` — PCA decode to mesh, batched
- `region_displacement_features()` — per-region mean delta
- `embed_from_mesh_regions()` — full Option B pipeline
- `dominant_region_labels()` — AU-region colouring
- `plot_map()` — scatter embedding
- `plot_map_by_region()` — per-region activation grid

---

## Practical Notes

**Scale:** For 100k points, UMAP is strongly preferred over t-SNE (`pip install umap-learn`). UMAP runs in minutes; sklearn's TSNE can take hours at this scale.

**Pre-PCA:** Always pre-reduce to ~50 dims before UMAP/t-SNE. Both work poorly in high dimensions; pre-PCA speeds things up without losing meaningful structure (check explained variance ≥ 0.95).

**Batched decoding:** Decoding 100k × 382 → mesh at once requires ~100k × V × 3 × 4 bytes ≈ 6 GB for V=5023. Use the provided `batch_size=2000` decode loop to stay within memory.

**Region mask quality:** The FLAME index ranges in the script are approximations. For best results, define your masks from the mesh segmentation of your specific character topology. One approach: pick a few "seed" vertices per region by hand and grow the mask by vertex adjacency within a geodesic radius.

**Interpreting the map:** Regions of the map with many nearby points = common expression configurations. Isolated clusters = rare or extreme poses. A radial structure around a central neutral-pose cluster is typical — the angular direction encodes expression type, the radial distance encodes intensity.

---

## Connections

- [[concepts/facs]] — AU definitions and region anatomy
- [[concepts/pose-space-deformation]] — pose-space structure this map reveals
- [[concepts/flame-model]] — FLAME 382-component expression space
- [[concepts/blendshapes]] — blendshapes are the inverse of this: each AU is a point in this map
