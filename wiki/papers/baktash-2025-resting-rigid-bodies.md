---
title: "Putting Rigid Bodies to Rest"
authors: [Baktash, Hossein; Sharp, Nicholas; Zhou, Qingnan; Jacobson, Alec; Crane, Keenan]
venue: ACM Transactions on Graphics (SIGGRAPH 2025)
year: 2025
tags: [simulation, math, volumes, houdini, vex, python]
source: raw/papers/baktash-2025-resting-rigid-bodies.pdf
doi: 10.1145/3731203
---

## Summary
Given a convex rigid body, where will it come to rest when dropped on a flat surface? This paper answers the question purely geometrically — no simulation, no sampling — by computing all stable resting orientations and their exact probabilities from the **Morse-Smale complex of the support function over the Gauss sphere**. The method runs orders of magnitude faster than rigid body simulation and enables *inverse design*: sculpting a shape so that it lands on desired faces with desired probabilities (e.g., a fair die in a non-cubic shape, or a loaded die with prescribed biases).

## Problem
Predicting where a rigid body comes to rest requires either (a) forward simulation with many random drops (slow, stochastic) or (b) exhaustive orientation search. Neither scales for interactive design feedback or inverse optimization. A direct geometric characterization of the resting probability distribution was missing.

## Method

### Support Function and Gauss Map

For a convex body $K$, the **support function** $h : S^2 \to \mathbb{R}$ maps each unit direction $\mathbf{n}$ to the farthest extent of $K$ in that direction:

$$h(\mathbf{n}) = \max_{\mathbf{x} \in K} \; \mathbf{n} \cdot \mathbf{x}$$

The **Gauss map** $\mathcal{G}$ maps each surface point to its outward unit normal on $S^2$. For a convex polyhedron:
- Each **face** (planar region) maps to a single **point** on $S^2$ (its normal)
- Each **edge** maps to a **great circle arc** (the range of normals at that edge)
- Each **vertex** maps to a **spherical polygon** (the cone of normals that "see" the vertex)

This partitions $S^2$ into the **Gauss map image** of the polyhedron.

### Resting Equilibria

When the body rests on a flat floor under gravity $\mathbf{g} = -\hat{\mathbf{y}}$, the contact configuration is determined by the **contact normal** $\mathbf{n} \in S^2$ (pointing up from the floor into the body):

- **Face contact** (stable): $\mathbf{n}$ is the face normal. Stable if the center of mass (COM) projects *inside* the face polygon.
- **Edge contact** (unstable saddle): $\mathbf{n}$ lies along the arc between two adjacent face normals. COM is on the edge line.
- **Vertex contact** (unstable maximum): $\mathbf{n}$ lies in the spherical polygon of a vertex. COM is directly over the vertex.

Stable resting faces correspond to **local minima of the potential energy** $V(\mathbf{n}) = h(-\mathbf{n})$ on $S^2$ (the height of the COM when the body contacts in direction $\mathbf{n}$).

### Morse-Smale Complex

The **Morse-Smale complex** of $h(-\mathbf{n})$ on $S^2$ decomposes the sphere into cells:
- **Minima** = stable face contacts
- **Maxima** = unstable vertex contacts
- **Saddles** = unstable edge contacts
- **Ascending/descending 1-manifolds** = ridge/valley lines between critical points
- **2-cells** = regions whose gradient flow descends to the same minimum

Each 2-cell is the **basin of attraction** of a stable face. A body dropped from a random orientation with random small perturbation (negligible momentum) will land on face $i$ with probability:

$$p_i = \frac{\text{area of cell}_i}{4\pi}$$

### Quasi-Static Drop Trajectory

For a given initial orientation $\mathbf{n}_0$, the quasi-static drop follows the **gradient flow** of $V(\mathbf{n}) = h(-\mathbf{n})$ on $S^2$, tracking contact changes:
1. Start: body in contact at $\mathbf{n}_0$ (vertex, edge, or face)
2. Roll: follow the downhill gradient along the current contact configuration
3. Transition: when the contact type changes (vertex→edge, edge→face), update the contact manifold
4. Terminate: when a stable face is reached (COM inside face, no downhill direction)

The trajectory is piecewise smooth and purely geometric — it recovers the physical rolling path for negligible kinetic energy.

### Inverse Design

Given target resting probabilities $\{p_i^*\}$ for a set of faces, find a shape deformation that achieves them by optimizing the Gauss-map cell areas. The optimization adjusts vertex positions of the convex hull (hence the Gauss-map partition) to match the target distribution. Used to design:
- **Fair dice** in arbitrary shapes (tetrahedra, elongated forms) — equalize all cell areas
- **Loaded dice** — bias cell areas to prescribed probabilities
- **Orientable props** — maximize probability of landing on a designated face

## Key Results
- Exact resting probabilities match Monte Carlo simulation with >5,000 random drops
- Quasi-static trajectory matches physics engine output for low-energy drops
- Inverse design converges in seconds for moderate vertex counts
- Demonstrated on custom-printed dice with measured physical validation

## Limitations
- **Convex bodies only**: the Gauss map and support function apply to convex hulls; non-convex bodies are handled by computing the convex hull of their geometry (loses concavities)
- **Negligible momentum assumption**: the quasi-static model fails for high-energy drops (bouncing, spinning)
- **Flat surface only**: no inclined planes or non-flat terrain
- **No friction modeling**: friction affects the trajectory at edges but not the final stable face (if COM inside face)

## Connections
- [[concepts/neo-hookean-simulation]] — adjacent: both deal with physical behavior of deformable/rigid bodies
- [[authors/crane-keenan]] — senior author; Gauss map and Morse theory are recurring tools in his work
- [[authors/jacobson-alec]] — co-author; geometry processing expertise
- [[authors/sharp-nicholas]] — co-author; geometry processing and discrete differential geometry
- [[vex/rigid-body-rest-analysis.vex]] — Houdini implementation: support function, Gauss map partition, resting probability per face
- [[python/rigid_body_rest.py]] — Python implementation: full pipeline with scipy ConvexHull, spherical Voronoi, inverse design

## Implementation Notes
- The Gauss map of a convex polyhedron is computed from the **convex hull**: face normals = Gauss-map points; dual of the convex hull on $S^2$ = spherical Voronoi of the face normals
- **Resting probability** per face ≈ area of spherical Voronoi cell of face normal / 4π (exact for the Morse-Smale cell when COM is always inside)
- In practice: `scipy.spatial.SphericalVoronoi` gives the cell areas directly
- **Stability check**: COM projection inside a face = 2D point-in-polygon test in the face's local coordinate frame
- The **support function** in VEX: `h(n) = max over all points: dot(n, P)`; for a mesh this is just `max(dot(n, P[i]) for all i)`
- GitHub implementation uses C++/Eigen/Qhull; the Python snippet in this wiki provides a NumPy/SciPy equivalent

## Quotes
> "We show how to extract rolling equilibria from the Morse-Smale complex of the support function over the Gauss map."

> "Our method is orders of magnitude faster than state-of-the-art rigid body simulation, and enables inverse design of shapes with target resting behaviors."
