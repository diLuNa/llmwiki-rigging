---
question: "What is the most detailed technical description of the MetaHuman rig and how it works internally?"
date: 2026-04-09
---

## MetaHuman Rig: Internal Architecture

MetaHuman's facial rig consists of three interlocking systems: the **DNA file format**, the **RigLogic evaluation engine**, and the **blendshape + joint deformation stack**.

### DNA File Format

A four-layer binary format (10–15× compressed vs JSON):

| Layer | Contents | Loadable standalone? |
|-------|----------|---------------------|
| Descriptor | Metadata, character archetype | Yes |
| Definition | Joint names, blendshape names, LOD mappings | Yes |
| Behavior | RigLogic coefficient matrices, control→output mappings | **Yes** — runtime only needs this |
| Geometry | Vertices, UVs, skin weights, blendshape deltas | Yes |

**Key design:** Behavior and Geometry layers are independent. Runtime loads Behavior only; geometry edits don't touch behavior.

Open source: [EpicGames/MetaHuman-DNA-Calibration](https://github.com/EpicGames/MetaHuman-DNA-Calibration)

### RigLogic: The Evaluation Algorithm

**Core:** $\mathbf{y} = K\mathbf{x}$ — a linear mapping from ~200 control inputs to joint transforms + blendshape weights.

**Pipeline:**
1. Face Board sliders (animator) → normalized raw values $\mathbf{x} \in [0,1]^{200}$
2. $\mathbf{x}$ → joint rotations/translations (via dense joint-group block matrices)
3. $\mathbf{x}$ → blendshape weights (via weighted linear combinations)
4. $\mathbf{x}$ → shader/animated-map multipliers (material channels)

**Performance trick:** Joints are organized into anatomically-meaningful **joint groups** (eyes, mouth, jaw, cheeks, brow). Each group forms a **dense block submatrix** rather than a row in a sparse CRS matrix. Dense blocks enable SIMD vectorization → ~6× faster than sparse CRS, with <2% memory overhead.

**LOD:** 8 head LODs, 4 body LODs. Switching LOD = referencing a strict joint subset. Zero data reload.

### Deformation Stack

| Component | Count | Notes |
|-----------|-------|-------|
| Expression controls | ~200 | Ideally one per FACS AU |
| Total joints | 397–713 | Character/LOD dependent; ~586 for head |
| Skin influences per vertex | 12 | LBS with 12 influences |
| Primary blendshapes | 258–669 | Character dependent |
| Corrective shapes | 1,000+ | PSD/RBF activated by pose conditions |
| ARKit subset | 52 | Mobile AR compatibility |

**Correctives:** Pose Space Deformation with Radial Basis Functions. Correctives activate automatically when specific pose combinations occur, preventing artifacts (eye bulging, lip stretch, jaw volume loss).

### Cross-Platform Architecture

Same DNA file evaluates in Maya, Unreal Engine, Blender (via third-party tools). In UE, `RigLogicModule` plugin and `UDNAAsset` load DNA as a bitstream, separating runtime (Behavior) and authoring chunks. Evaluation is identical to Maya — no re-rigging required.

### What MetaHuman Does NOT Do

- **No muscle simulation at runtime**: blendshapes encode muscle-like behavior baked offline (cf. [[papers/cong-2016-art-directed-blendshapes]])  
- **Not nonlinear**: RigLogic is strictly linear ($\mathbf{y} = K\mathbf{x}$); correctives add piecewise nonlinearity via RBF activation
- **No physics at runtime**: no secondary dynamics (jiggle, etc.) unless added separately via UE physics systems

### Comparison: MetaHuman vs ILM/Weta Approaches

| | MetaHuman | ILM (Cong) | Animatomy (Weta) |
|---|---|---|---|
| Runtime representation | Blendshapes | Blendshapes (from sim) | Blendshape curves |
| Muscle simulation | None (offline bake) | Offline (FEM) | None (fiber curves) |
| Controls | ~200 FACS sliders | ~51 FACS AUs | Muscle fiber strains |
| Speed | Real-time (~6× SIMD opt) | Offline only | Real-time |
| Portability | DNA format, any DCC | Proprietary | Weta-internal |

### Key References
- [[papers/epic-2021-metahuman-rig]] — full technical wiki page
- [[papers/lewis-2014-blendshape-star]] — FACS blendshape rig foundation
- [[concepts/facial-blendshape-rigs]] — production rig context
- [[concepts/pose-space-deformation]] — RBF correctives
