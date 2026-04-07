---
title: "Sculpt Transfer — VEX Implementation"
tags: [vex, houdini, sculpt-transfer, hda, correctives]
---

## Overview
VEX implementation of the sculpt transfer algorithm from [[papers/degoes-2020-sculpt]]. Moves a corrective delta sculpted at one pose to another pose.

## Algorithm (VEX)
1. Input: rest mesh, posed mesh A (where delta was sculpted), posed mesh B (target), delta mesh.
2. Apply delta to rest mesh → modified rest.
3. Deform modified rest into pose B using rig transforms.
4. Subtract unmodified pose B from deformed result → transferred delta.

## Notes
- The Jacobian-aware transfer requires per-vertex transform gradients. In VEX, approximated per-point using neighbor differencing.
- Implemented as HDA with rest, pose A, pose B, and delta inputs.

## Related
- [[concepts/laplacian-smoothing]] — bandage smoothing applied post-transfer
- [[papers/degoes-2020-sculpt]]
