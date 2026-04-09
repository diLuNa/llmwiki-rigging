---
title: "MetaHuman Creator: Face Rig Architecture (RigLogic + DNA)"
authors: [Epic Games; 3Lateral]
venue: GDC 2021 / Unreal Engine Technical Documentation
year: 2021
tags: [blendshapes, rig-generation, digital-human, facial-capture, real-time]
source: knowledge
---

## Summary
MetaHuman Creator is Epic Games' cloud-based digital human creation tool, built on a production facial rig system developed by 3Lateral (Epic's R&D division). The rig uses a proprietary binary format called **DNA** and a linear evaluation engine called **RigLogic** that evaluates identically in Maya, Unreal Engine, and other DCCs from the same file. Each MetaHuman has ~200 expression controls driving 258–669 blendshapes + 397–713 joints via dense matrix algebra, with 8 LOD levels for real-time scalability.

## Problem
Building photorealistic digital humans for real-time use requires: (1) a compact facial rig expressible in every DCC; (2) a rig that evaluates correctly without per-platform re-rigging; (3) LOD-scalable computation from cinematic to game performance budgets; and (4) a data format separating rig behavior from geometry so each can evolve independently.

## Method

### DNA File Format

Four-layer hierarchical binary format. Layers are **independently loadable**:

| Layer | Contents |
|-------|----------|
| **Descriptor** | Character metadata: name, age, facial archetype, gender, coordinate system, compatibility parameters |
| **Definition** | Static rig structure: control names, joint hierarchy, blendshape names, mesh definitions, LOD mappings, bind poses |
| **Behavior** | Dynamic evaluation data: control→joint mappings, RigLogic coefficient matrices, blendshape weight equations, animated map values |
| **Geometry** | Mesh data: vertex positions/normals/UVs, skin weights (12 influences/vertex), blendshape target deltas |

The Behavior and Geometry layers are **independent by design**: runtime evaluation loads only the Behavior layer; geometry modification does not touch rig behavior. Binary format achieves 10–15× compression vs JSON.

API: `BinaryStreamReader` with selectable layer depth and `maxLOD` parameter for partial loading.

### RigLogic Evaluation Algorithm

**Core equation:** $\mathbf{y} = K \mathbf{x}$

Where $\mathbf{x} \in [0,1]^{200}$ are control input values, $\mathbf{y}$ are output joint transforms and blendshape weights, and $K$ is the rig parameter matrix.

**Evaluation pipeline:**
1. **GUI controls → raw values:** animator face board controls mapped to normalized mathematical parameters
2. **Raw values → joint transforms:** matrix multiplication in joint group blocks
3. **Raw values → blendshape weights:** weighted linear combinations per blendshape
4. **Blendshape weights → shader multipliers:** animated texture/material modification channels

**Matrix storage optimization:** Rather than sparse CRS (compressed row storage), RigLogic uses **dense block-partitioned submatrices** organized by joint groups. Each group is anatomically meaningful (eyes, mouth, cheeks, brow, jaw). Dense layout enables SIMD vectorization and cache locality → **~6× performance improvement** over sparse representation with <2% memory overhead.

**LOD switching:** Data ordered by LOD level. Switching LOD = referencing a strict joint subset. Zero data reload. 8 head LODs, 4 body LODs.

### Blendshape Architecture

- **Total blendshapes:** 258–669 (character-dependent; production assets tend toward upper range)
- **ARKit subset:** 52 blendshapes for mobile AR tracking compatibility
- **Corrective shapes:** 1,000+ corrective shapes for complex pose combinations
- **Interpolation:** Pose Space Deformation (PSD) with Radial Basis Functions (RBF) for corrective activation
- **FACS grounding:** ideally one top-level control per FACS AU; ~200 expression controls total

### Joint Architecture

- **Total joints:** 397–713 (LOD and character dependent)
- **Head joints alone:** ~586 in highest-detail configuration
- **Skin influences:** 12 per vertex
- **Joint groups:** anatomically organized dense blocks (enables efficient blocked matrix computation)

### Control Hierarchy

Five semantic layers from animator to hardware:
1. **Face Board controls** (animator-facing FACS sliders)
2. **Raw values** (normalized mathematical parameters)
3. **Joint transforms** (rotations/translations in hierarchy)
4. **Blendshape weights** (0–1 activation per shape)
5. **Shader/animated-map multipliers** (material channels)

### Runtime: Maya vs Unreal Engine

Same DNA file evaluates in both environments via the **RigLogicModule** UE plugin:

- **Maya:** RigLogic plugin drives rig deformations directly from DNA; same Behavior layer
- **Unreal Engine:** `UDNAAsset` holds DNA data; DNA imported as bitstream, split into runtime (Behavior) chunks for evaluation and design-time chunks for authoring; integrates with Control Rig + Sequencer

Cross-platform guarantee: no re-rigging when moving between Maya and UE. Sculpted expressions remain accurate.

## Key Results
- Production-deployed on MetaHuman Creator (2021–present)
- Used in: Senua's Saga: Hellblade II, multiple AAA game titles
- MetaHumans 3.0+: 40% performance improvement over prior versions
- GDC 2021: "Rigging the MetaHumans" (Riham Toulan, Senior Technical Animator)
- Open-sourced DNA Calibration library: [EpicGames/MetaHuman-DNA-Calibration](https://github.com/EpicGames/MetaHuman-DNA-Calibration) (Nov 2022)

## Limitations
- **Closed ecosystem:** customizing beyond the DNA system requires using the calibration library or third-party bridges (Blender, Houdini)
- **Corrective explosion:** 1,000+ corrective shapes needed for full fidelity — non-trivial to author or modify
- **Maya round-trip issues:** exported MetaHuman rigs in Maya can have broken facial controls after save/reload; non-ASCII filenames cause errors
- **Blendshape extension:** adding custom blendshapes to base MetaHuman difficult to propagate across all LOD variants
- **Compute load at LOD 0:** 12 influences × ~586 joints × 258–669 blendshapes is heavy for mobile targets even with SIMD

## Connections
- [[concepts/blendshapes]] — FACS blendshapes + PSD correctives form the deformation basis
- [[concepts/pose-space-deformation]] — RBF correctives for complex pose combinations
- [[concepts/facial-blendshape-rigs]] — MetaHuman is the production reference FACS rig for real-time digital humans
- [[concepts/linear-blend-skinning]] — 12-influence LBS underlies the skeletal deformation
- [[concepts/muscles]] — MetaHuman does NOT use muscle simulation at runtime; blendshapes encode muscle-like behavior baked into shapes
- [[papers/lewis-2014-blendshape-star]] — FACS blendshape rig framework MetaHuman is built on
- [[papers/choi-2022-animatomy]] — Animatomy (Weta) is the direct muscle-simulation-based alternative to MetaHuman's blendshape approach
- [[papers/cong-2016-art-directed-blendshapes]] — ILM's approach: simulation → blendshapes; MetaHuman's correctives are authored vs simulated

## Implementation Notes
**DNA Calibration Python API (key patterns):**
```python
from dna import BinaryStreamReader, DataLayer_All

# Load only Behavior layer (runtime-efficient)
stream = FileStream("ada.dna", FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
reader = BinaryStreamReader(stream, DataLayer.Behavior)
reader.read()

# Access raw RigLogic control mappings
n_controls = reader.getGUIControlCount()  # ~200
n_joints = reader.getJointCount()         # 397-713
n_blendshapes = reader.getBlendShapeTargetCount(meshIndex=0)  # 258-669
```

**RigLogic matrix layout insight:** Joint groups are the key to performance. Each group is a dense $(m \times n)$ block where $m$ = joints in group, $n$ = controls affecting that group. SIMD processes each block independently → good parallelism, low cache miss rate. Sparse CRS would scatter memory accesses across the full $(\text{all joints} \times \text{all controls})$ matrix.
