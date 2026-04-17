---
title: "ACES Color Management in DCC"
tags: [pipeline, houdini, rendering, digital-human, appearance]
source: raw/assets/An Idiot's Guide to ACES.md
external: https://www.toadstorm.com/blog/?p=694
---

## What Is ACES?

**ACES** (Academy Color Encoding System) is a color management standard that normalizes all input sources (film, CG, video) into a single working color space, making color consistent across every tool in the pipeline.

For CG artists the key component is **ACEScg**: the ACES color space designed for rendering and compositing. Its primaries (**AP1**) define a wider gamut than sRGB/Rec.709, enabling more accurate representation of highly saturated and HDR colors. ACEScg is linearly encoded (no gamma curve), so it works naturally with floating-point renders.

| Color space | Primaries | Encoding | Notes |
|-------------|-----------|----------|-------|
| sRGB / Rec.709 | sRGB | gamma 2.2 | Default for display devices |
| Linear sRGB | sRGB | linear (no gamma) | Typical "linear workflow" — still sRGB primaries |
| ACEScg | AP1 | linear | Wide gamut; CG working space |
| ACES2065-1 | AP0 | linear | Archival/interchange; not for daily work |

What most pipelines call "linear workflow" is linear *encoding* but still sRGB *primaries* — the gamut limitation remains. ACEScg removes that limitation.

---

## The ACES Pipeline

```
INPUT TEXTURES       → apply IDT (Input Device Transform) → ACEScg working space
CG RENDER            → rendered in ACEScg natively
COMPOSITE            → all operations in ACEScg (linear)
VIEWER               → Viewer LUT: ACEScg → Output (sRGB / Rec.709 / DCI-P3)
DELIVERY             → ODT (Output Device Transform) baked into final image
```

### Reference Rendering Transform (RRT)

The ACES **Output** color space (e.g. `Output – Rec. 709`) includes an **RRT** — a film-emulation S-curve applied between ACEScg and the display space. The RRT:
- Rolls off highlights naturally (avoids sRGB oversaturation blowout)
- Deepens shadows
- **Modifies brand/exact colors** — a specified sRGB value will not survive the RRT unchanged

When exact color reproduction is required (compositing screens, brand matching), you must either bypass the RRT or pre-invert it (see Gotchas).

---

## Input Texture Conversion (IDT)

Only convert **color** textures. **Data** textures must never be color-corrected.

| Texture type | Convert? | IDT to use |
|--------------|----------|-----------|
| Diffuse / albedo | **Yes** | `Utility – sRGB – Texture` (LDR JPG/PNG) or `Utility – Linear – sRGB` (float EXR) |
| Specular / roughness | **No** | pass through raw |
| Normal map | **No** | pass through raw |
| Displacement / height | **No** | pass through raw |
| Emission mask | context-dependent | treat as data unless it encodes a display color |

Rule of thumb: if the file is not floating-point → `Utility – sRGB – Texture`. If it is floating-point → `Utility – Linear – sRGB`.

---

## OCIO Setup

ACES is distributed as an [OpenColorIO](https://github.com/colour-science/OpenColorIO-Configs) config. Download and set the environment variable:

```bash
export OCIO=/path/to/aces_1.0.3/config.ocio
```

Add to `~/.bash_profile` (or `~/.zshrc`) to make it permanent. Most DCCs detect this variable automatically.

---

## Per-DCC Setup

### Houdini

1. Set the `OCIO` env var before launching Houdini.
2. The **Render View** will show ACES display LUTs in its color dropdown (bottom of the pane).
3. In shaders, use **OCIO Color Transform VOP** to convert input textures to ACEScg.
4. In **COPs** (File COP): uncheck "Linearize Non-Linear Images" (it tries to apply its own gamma), set "File Raster Depth" to 16- or 32-bit float, then pipe through an OCIO Transform VOP.
5. Pre-baking textures to ACEScg on disk (using COPs or `ocioconvert`) is often safer than relying on in-shader transform support, especially with Redshift.

**File COP caveat:** Houdini's File COP auto-linearizes on load. Either disable "Linearize Non-Linear Images" and apply OCIO manually, or change the OCIO Transform input space to `Utility – Linear – sRGB` to account for the already-applied linearization.

### Maya

1. Preferences → Settings → Color Management → Enable Color Management + Use OCIO Configuration.
2. Set Rendering Space = `ACEScg`.
3. Set View Transform = `Output – sRGB` (or Rec. 709, depending on monitor).
4. Per-texture: set color space on each File node manually — automated rules cannot distinguish color vs data textures.
5. Redshift does not respect Maya's color management; configure Redshift's own color management under Render Settings → Color Management or in the Redshift Render View gear icon.

### Fusion

1. Set `OCIO` env var; Fusion exposes "OCIO ColorSpace ViewLUT" in viewer LUT list.
2. Click LUT → OCIO ColorSpace ViewLUT → Edit: source = `ACES – ACEScg`, output = `Output – Rec.709` (or sRGB).
3. For non-ACEScg footage: use **OCIOColorspace** node before compositing (input space = `Utility – sRGB – Texture`).
4. Output write: use OCIOColorspace to convert to delivery space before the Saver node. Disable viewer LUT to preview actual output colors.

### Nuke

1. Project Settings → Color → Working Space = `ACEScg`, Monitor = `sRGB` or `Rec. 709`.
2. Default rules: 8-bit files → `Utility – sRGB – Texture`, float → `ACEScg`.
3. Non-ACEScg float inputs: use **OCIOFileTransform** to convert from `Utility – Linear – sRGB` to ACEScg.
4. Before delivery: OCIOFileTransform to target delivery space (Rec.709, Rec.2020, ACES2065-1).

---

## Gotchas

### Self-Illuminated Materials (screen comps, brand colors)

If a self-illuminated material must match a reference image exactly after ACES output, normal IDT conversion is not enough — the RRT S-curve will modify its appearance.

**3D fix:** convert the texture using the **Output** space as the IDT (e.g. `Output – sRGB`). This pre-inverts the RRT so that after ACES rendering the color looks identical to the original. Side effect: what appears as "white" in ACEScg will have values ~16.0 in scene-linear — this is expected and will affect GI/reflections.

**Composite fix:** exit ACEScg temporarily near the end of the comp: OCIOColorspace from ACEScg → sRGB, switch viewer LUT off, composite the sRGB reference elements, then optionally convert back if HDR delivery is needed.

### Data Textures
Never apply a color IDT to normal, roughness, displacement, or mask maps. These encode numeric data; color-correcting them produces physically wrong values.

### Floating-Point Writing
Write ACEScg images as 16-bit or 32-bit float EXR. Writing to 8-bit from an ACEScg render is lossy and clips HDR content.

### RRT and Brand Colors
ACES RRT is not a no-op. If a client specifies an exact sRGB value for a logo color, that value will shift after passing through the RRT. Either: (a) treat the logo as a self-illuminated element (use Output IDT trick above), or (b) exit ACEScg in comp and handle the logo in sRGB.

---

## Connections

- [[concepts/digital-human-appearance]] — skin reflectance capture and generative textures need correct ACEScg input for PBR lighting
- [[papers/weyrich-2006-skin-reflectance]] — spectral skin reflectance data; color space accuracy matters for BSSRDF parameters
- [[techniques/parallel-transport]] — unrelated technique page from same blog source (toadstorm.com)

---

## External References

- [An Idiot's Guide to ACES — toadstorm.com (2020)](https://www.toadstorm.com/blog/?p=694) — practical production guide for CG artists; source of this page
- [ACES Primer (acescentral.com)](https://acescentral.com/uploads/default/original/1X/6ad8b74b085ac8945c1e638cbbd8fdf687b7f60e.pdf) — official technical reference
- [Chris Brejon's ACES Guide](https://chrisbrejon.com/cg-cinematography/chapter-1-5-academy-color-encoding-system-aces/) — in-depth practical cinematography context
- [OpenColorIO Configs (GitHub)](https://github.com/colour-science/OpenColorIO-Configs) — OCIO config download including aces_1.0.3
