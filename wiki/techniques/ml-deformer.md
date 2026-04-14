---
title: "ML Deformer — Neural Deformation Approximation in Production"
tags: [neural, skinning, real-time, houdini, correctives, facial-capture]
papers: [bailey-2020-fast-deep-facial, song-2020-differential-subspace, arcelin-2024-ml-deformer-crowds, radzihovsky-2020-facebaker, li-2021-neural-blend-shapes]
---

## What Is ML Deformer

**ML Deformer** is a family of neural network–based techniques that approximate complex character rigs (especially facial) by training a network to predict residual deformations on top of Linear Blend Skinning. Core innovation: decompose rig deformation into **linear** (LBS, cheap) and **non-linear** (learned by NN, replaces complex rigs) components.

**Houdini Integration** (SideFX, Houdini 20+): Official procedural nodes (`ML Train Deformer` + `ML Deform`) for training and inference using ONNX format models.

---

## The Problem Solved

| Traditional Rig | ML Deformer |
|-----------------|------------|
| 50–200 deformers per character | 1 neural network |
| 50–200ms per-frame evaluation | 2–5ms per-frame evaluation |
| Difficult to optimize for real-time | Built for real-time (game engines, VR, crowds) |
| Custom for each character | Generalizable (retrain for new character) |
| Brittle correctives (sculpted by hand) | Learned from example poses |

**Use case**: Interactive characters, crowd simulation, VR/game export, where original rigging is too expensive.

---

## Three Main Architectural Approaches

### Approach 1: CNN Residual on LBS
**Paper**: [[papers/bailey-2020-fast-deep-facial]] (Bailey et al., SIGGRAPH 2020)

**Formula**:
```
v_final = v_LBS + CNN(pose_params)
```

- CNN predicts per-vertex 3D displacement residuals
- Simple to understand and implement
- Fixed architecture per topology (requires retraining for new meshes)
- Can extrapolate poorly to unseen poses

**Typical network**: Encoder-decoder with 3–4 conv layers; outputs N×3 residuals.

**GitHub**: [stephen-w-bailey/fast-n-deep-faces](https://github.com/stephen-w-bailey/fast-n-deep-faces)

---

### Approach 2: Differential Subspace Reconstruction
**Paper**: [[papers/song-2020-differential-subspace]] (Song et al., SIGGRAPH 2020)

**Formula**:
```
δ_modified = δ_LBS + NN(pose_params)   # learned differential offsets
v_final = reconstruct(δ_modified)      # harmonic solve from differential coords
```

- Network predicts differential coordinate (Laplacian) offsets
- Harmonic reconstruction ensures mesh quality (smooth surfaces)
- Mesh-aware: respects connectivity
- Better error distribution than CNN (fewer localized artifacts)

**Advantages**: Smoother approximations, sparser training data, production-validated (Blue Sky Studios)

---

### Approach 3: Joint Learning (Skeleton + Weights + Correctives)
**Paper**: [[papers/li-2021-neural-blend-shapes]] (Li et al., SIGGRAPH 2021)

**Formula**:
```
rig, weights, correctives = NN_encoder(deformed_meshes)
v_final = LBS(weights) + NN_correctives(pose_params)
```

- **No ground-truth rig required** — learns from deformed geometry alone
- Indirect supervision via indirect FACS segmentation
- End-to-end optimization
- MeshCNN architecture exploits connectivity

**Advantages**: Most generalizable (no pre-existing rig needed); outputs interpretable controls (blendshape names, skeleton)

**GitHub**: [PeizhuoLi/neural-blend-shapes](https://github.com/PeizhuoLi/neural-blend-shapes)

---

## Houdini Implementation — ML Deformer SOP

SideFX officially integrated ML Deformer in Houdini 20 (2023).

**Official Docs**: [sidefx.com/docs/houdini/ml/mldeformer.html](https://www.sidefx.com/docs/houdini/ml/mldeformer.html)

### Setup Pipeline

```
Original rig (any) ──┐
                     ├─ Bake poses + deformations ──→ Training dataset
Example poses    ─────┘

Training dataset ──→ ML Train Deformer SOP ──→ ONNX model

ONNX model + skeleton ──→ ML Deform SOP ──→ Approximated deformations
```

### Key SOP Parameters

#### ML Train Deformer

| Parameter | Typical Value | Meaning |
|-----------|--------------|---------|
| Training Data Path | `path/to/poses.bgeo.sc` | Point sequence (one point per pose) with @P and deformed geometry |
| Model Output Path | `path/model.onnx` | Where to save trained ONNX model |
| Pose Parameters | Blend shapes / joint angles | Input feature vector (can apply PCA for compression) |
| Network Layers | 3–4 | Hidden layer count |
| Learning Rate | 1e-4 | Initial learning rate |
| Epochs | 100–500 | Training iterations |
| Batch Size | 32 | Training batch size |
| Validation Split | 0.2 | Fraction of data for validation |
| Loss Function | MSE | Mean Squared Error on reconstructed geometry |
| Output Format | ONNX | Open Neural Network Exchange (portable across platforms) |

#### ML Deform SOP

| Parameter | Type | Meaning |
|-----------|------|---------|
| Model Path | file | Path to trained ONNX model |
| Input Pose Vector | float[] | Current pose parameters (blend shape weights, joint angles) |
| Output Deformation | geometry | Deformed mesh (input mesh + predicted residuals) |

### Typical Houdini Workflow

```
1. CAPTURE TRAINING DATA
   Rig in original state ──→ Channel Wrangle SOP (export pose params)
   Deformed geometry ──→ Store geometry for each pose

2. PREPARE TRAINING SET
   Assemble: sequence of points with @P (pose vector) and deformed geo reference
   PCA SOP: optional dimensionality reduction of pose params

3. TRAIN MODEL
   ML Train Deformer SOP ──→ outputs .onnx file
   (Runs in Houdini Python; uses PyTorch or TensorFlow backend)

4. DEPLOY MODEL
   ML Deform SOP: load .onnx + input pose params ──→ deformed output
   Use directly in animation or export to game engine

5. ITERATE
   If accuracy insufficient: add more training poses, retrain model
```

---

## Comparison Table: Four Production Approaches

| Approach | Paper | Input | Architecture | Training Data | Speed | Quality | Generalization |
|----------|-------|-------|--------------|---------------|-------|---------|-----------------|
| **CNN Residual** | Bailey 2020 | Pose params | CNN encoder-decoder | 100–500 poses | ⭐⭐⭐ (fastest) | ⭐⭐ | Poor (extrapolates badly) |
| **Differential** | Song 2020 | Pose params | NN + harmonic recon | 80–300 poses | ⭐⭐ | ⭐⭐⭐ (smoothest) | Moderate |
| **Joint Learning** | Li 2021 | Deformed meshes only | MeshCNN | No rig needed | ⭐ (slowest) | ⭐⭐⭐ | Best (topology-agnostic) |
| **FaceBaker** | Radzihovsky 2020 | Pose params | Hierarchical | Varies | ⭐⭐⭐ | ⭐⭐⭐ | Very good (Pixar-validated) |

---

## Use Cases

1. **Game Export** — Complex Houdini/Maya rig → LBS + neural corrections → game engine
2. **Real-time VR** — High-fidelity facial rig → fast approximation for VR headset
3. **Crowd Simulation** — Hundreds/thousands of characters → neural deformers at scale
4. **Animation Retargeting** — Transfer rig between characters via learned model
5. **Simulation Baking** — FEM simulation / muscles → approximate with fast network
6. **Performance Capture** — Real-time re-rigging of captured performance data

---

## Training Best Practices

1. **Data Collection**
   - Include edge cases: extreme poses, asym-metrical expressions, out-of-training poses
   - Aim for 200–500 diverse poses minimum
   - Include both "normal" and "exaggerated" versions

2. **Input Dimensionality**
   - If 100+ blend shapes: apply PCA to 20–50 dims
   - If 20+ joints: similarly reduce via PCA
   - Reduces overfitting, faster training

3. **Network Architecture**
   - 3–4 hidden layers often optimal (more = diminishing returns)
   - 256–512 units per layer typical
   - ReLU activations standard
   - Batch normalization optional but helpful

4. **Regularization**
   - L2 weight decay (1e-5 to 1e-4)
   - Dropout (0.1–0.3) if overfitting occurs
   - Smoothness loss on output (penalize per-vertex differences)

5. **Training Schedule**
   - Start with high learning rate (1e-3), decay to 1e-5
   - Batch size 32–64 typical
   - Early stopping if validation loss plateaus (patience = 20–50 epochs)
   - 100–500 epochs depending on data size and complexity

6. **Validation & Testing**
   - Hold out ~20% of poses for validation (monitor during training)
   - Test on completely unseen poses (>20% of data)
   - Measure: per-vertex L2 error, max error, temporal smoothness (frame-to-frame)

---

## External References

**Papers & Research:**
- Bailey et al. 2020: [doi.org/10.1145/3386569.3392397](https://doi.org/10.1145/3386569.3392397) | [GitHub](https://github.com/stephen-w-bailey/fast-n-deep-faces)
- Song et al. 2020: [doi.org/10.1145/3386569.3392491](https://doi.org/10.1145/3386569.3392491) (Blue Sky Studios)
- Li et al. 2021: [doi.org/10.1145/3450626.3459852](https://doi.org/10.1145/3450626.3459852) | [GitHub](https://github.com/PeizhuoLi/neural-blend-shapes)
- Radzihovsky et al. 2020: [doi.org/10.1145/3388767.3407340](https://doi.org/10.1145/3388767.3407340) (Pixar FaceBaker)
- Arcelin et al. 2024: [arxiv.org/abs/2406.09783](https://arxiv.org/abs/2406.09783) | [DIGIPRO](https://doi.org/10.1145/3665320.3670994) (Golaem production study)

**Houdini Documentation:**
- [sidefx.com/docs/houdini/ml/mldeformer.html](https://www.sidefx.com/docs/houdini/ml/mldeformer.html)
- [sidefx.com/docs/houdini/nodes/sop/ml_deform.html](https://www.sidefx.com/docs/houdini/nodes/sop/ml_deform.html)
- [sidefx.com/docs/houdini/ml/ml_traindeformer.html](https://www.sidefx.com/docs/houdini/ml/ml_traindeformer.html)
- Content Library: [sidefx.com/contentlibrary/ml-deformer/](https://www.sidefx.com/contentlibrary/ml-deformer/)

**Open Source:**
- [github.com/dgovil/MLDeform](https://github.com/dgovil/MLDeform) — ML deformation system
- [github.com/vincentbonnetcg-zz/awesome-ml-character](https://github.com/vincentbonnetcg-zz/awesome-ml-character) — curated ML character research
