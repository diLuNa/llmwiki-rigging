---
question: "What is the Gauss-Newton algorithm and when is it used in character rigging?"
date: 2026-04-13
---

## Definition

The **Gauss-Newton algorithm** is an iterative numerical method for solving **non-linear least squares problems**. It's a specialized variant of Newton's method that uses the Jacobian matrix (not the full Hessian) to approximate the curvature of the error surface.

### The Problem It Solves

Given a function $\mathbf{f}(\mathbf{x})$ and target values $\mathbf{y}$, minimize the squared error:

$$\min_{\mathbf{x}} \mathcal{L}(\mathbf{x}) = \min_{\mathbf{x}} \left\| \mathbf{f}(\mathbf{x}) - \mathbf{y} \right\|^2 = \min_{\mathbf{x}} \sum_{i=1}^{m} (f_i(\mathbf{x}) - y_i)^2$$

This is **non-linear least squares** — the function $\mathbf{f}$ is nonlinear, and we're minimizing the sum of squared residuals.

### The Algorithm

Starting from an initial guess $\mathbf{x}_0$, iterate:

$$\mathbf{x}_{k+1} = \mathbf{x}_k - (J_k^T J_k)^{-1} J_k^T \mathbf{r}_k$$

where:
- $J_k$ = Jacobian matrix of $\mathbf{f}$ at $\mathbf{x}_k$ (size: $m \times n$, where $m$ = outputs, $n$ = inputs)
- $\mathbf{r}_k = \mathbf{f}(\mathbf{x}_k) - \mathbf{y}$ = residual (error) vector at iteration $k$
- $(J_k^T J_k)^{-1} J_k^T$ = pseudo-inverse of $J_k$ (applies only if $J_k^T J_k$ is invertible)

**In vector form:**
$$J_k^T J_k \, \Delta \mathbf{x}_k = -J_k^T \mathbf{r}_k$$

Solve this linear system for $\Delta \mathbf{x}_k$, then update $\mathbf{x}_{k+1} = \mathbf{x}_k + \Delta \mathbf{x}_k$.

### Why It Works

Gauss-Newton approximates the Hessian (second derivative) of the loss function using only first derivatives:

**True Hessian:**
$$H = J^T J + \sum_{i=1}^{m} (f_i - y_i) H_i$$

**Gauss-Newton approximation:**
$$H \approx J^T J$$

The second term (involving the true Hessians $H_i$ weighted by residuals) is dropped. This works well when:
- Residuals are small at optimum (the dropped term is negligible)
- The Jacobian dominates the curvature

When residuals are large or the problem is poorly conditioned, Gauss-Newton can fail or converge slowly.

## Rigging Applications

### 1. Inverse Kinematics (IK) Solving

**Problem:** Given target end-effector position $\mathbf{p}^*$, find joint angles $\boldsymbol{\theta}$ that minimize:

$$\min_{\boldsymbol{\theta}} \| \mathbf{f}(\boldsymbol{\theta}) - \mathbf{p}^* \|^2$$

where $\mathbf{f}(\boldsymbol{\theta})$ is the forward kinematics function.

**Gauss-Newton solves this by:**
1. Computing the Jacobian of forward kinematics (how end-effector moves with each joint)
2. Forming the normal equations: $(J^T J) \Delta \boldsymbol{\theta} = -J^T (f(\boldsymbol{\theta}) - p^*)$
3. Solving for joint angle updates iteratively

This is the **industry standard for real-time IK** in game engines and production rigs.

### 2. Blendshape Weight Solving

**Problem:** Fit blend shapes to target geometry — find weights $\mathbf{w}$ such that:

$$\min_{\mathbf{w}} \left\| \sum_{i=1}^{K} w_i \mathbf{B}_i - \mathbf{v}^* \right\|^2$$

where $\mathbf{B}_i$ are blend shape meshes and $\mathbf{v}^*$ is target vertex positions.

**Gauss-Newton approach:**
- Jacobian: each column is a blend shape $\mathbf{B}_i$ (size: $3N \times K$ for $N$ vertices, $K$ shapes)
- Residual: current mesh minus target
- Solve normal equations: $(B^T B) \mathbf{w} = B^T \mathbf{v}^*$

This is **quadratic programming** (QP) when weights are constrained to $[0,1]$ and sum to 1 (see [[papers/jtdp-2003-blendshape-fitting]]).

### 3. Performance-Driven Animation

**Problem:** Fit blendshape weights to 3D markers from performance capture:

$$\min_{\mathbf{w}} \left\| \text{project}(\text{LBS}(\mathbf{w})) - \mathbf{m}^* \|^2$$

where markers $\mathbf{m}^*$ are tracked positions.

Gauss-Newton is used in [[papers/faceit-diaz-barros]] (FACEIT) and [[papers/jtdp-2003-blendshape-fitting]] to solve for weights from marker data.

### 4. Skinning Weight Extraction

In [[papers/le-2012-ssdr]], Gauss-Newton solves for LBS weights given bone transforms and target deformations:

$$\min_{\mathbf{W}} \left\| \text{LBS}(\mathbf{W}, \mathbf{T}) - \mathbf{V}^* \right\|^2$$

subject to non-negativity ($w \geq 0$) and sum-to-one constraints ($\sum w = 1$).

### 5. Non-Linear Blend Shape Solving (Bailey 2020)

In neural deformation approximation ([[papers/bailey-2020-fast-deep-facial]]), Gauss-Newton (or variants) trains the neural network to minimize:

$$\min_{\theta} \left\| \text{CNN}(\mathbf{p}, \theta) - \Delta \mathbf{v}^* \right\|^2$$

where $\mathbf{p}$ are pose parameters and $\Delta \mathbf{v}^*$ are target residual displacements.

## Comparison to Other Optimization Methods

| Method | Convergence | Robustness | Speed per Iteration | Use Case |
|--------|-------------|-----------|-------------------|----------|
| **Gauss-Newton** | Quadratic (near solution) | Moderate (fails on large residuals) | Fast (linear solve) | IK, small residuals, real-time |
| **Levenberg-Marquardt** | Quadratic to linear (adaptive) | Excellent (interpolates GN and gradient) | Moderate | Robust blendshape fitting |
| **Gradient Descent** | Linear | Poor (slow) | Very fast (one gradient step) | Simple, not for rigging |
| **Newton's Method** | Quadratic | Poor (requires Hessian) | Slow (Hessian computation) | General; overkill for least squares |
| **Trust Region** | Quadratic | Excellent | Moderate | Robust optimization; general |

**For character rigging:** Gauss-Newton is preferred because:
- Residuals are typically small (rig should be accurate)
- Only Jacobian needed (Hessian expensive)
- Fast per-iteration (linear solve is cheap)
- Reliable when problem is well-posed

**When it fails:**
- Large residuals → approximation breaks down
- Singular Jacobian → no solution or degenerate IK
- Poorly conditioned problem → slow convergence or oscillation

### Robust Variants for Production

**Levenberg-Marquardt (LM)** is a damped variant that adds a regularization term:

$$(J^T J + \lambda I) \Delta \mathbf{x} = -J^T \mathbf{r}$$

where $\lambda$ (damping factor) is adapted per iteration:
- Large $\lambda$ → more like gradient descent (slower, more stable)
- Small $\lambda$ → more like Gauss-Newton (faster near solution)

**This is the production standard** for robust IK and blendshape solving. See [[papers/jtdp-2003-blendshape-fitting]] and [[papers/faceit-diaz-barros]] for examples.

## Practical Example: Simple IK

Given a 2-link arm, forward kinematics:
```
x = L1*cos(θ1) + L2*cos(θ1 + θ2)
y = L1*sin(θ1) + L2*sin(θ1 + θ2)
```

Jacobian:
```
J = [[-L1*sin(θ1) - L2*sin(θ1+θ2), -L2*sin(θ1+θ2)],
     [ L1*cos(θ1) + L2*cos(θ1+θ2),  L2*cos(θ1+θ2)]]
```

Given target $(x^*, y^*)$, Gauss-Newton solves:
```
(J^T J) Δθ = -J^T (f(θ) - [x*, y*])
θ_new = θ_old + Δθ
```

Repeat until convergence (typically 3–10 iterations for IK).

## Mathematical Connection to Jacobian

Gauss-Newton is **fundamentally a Jacobian-based method**. It approximates the problem curvature using only first derivatives:

- **Gradient**: $\nabla \mathcal{L} = J^T \mathbf{r}$ (points downhill)
- **Hessian approximation**: $H \approx J^T J$ (Gauss-Newton)
- **Update**: $\Delta \mathbf{x} = -(J^T J)^{-1} J^T \mathbf{r}$ (Newton step with approx. Hessian)

This is why understanding the [[queries/jacobian-matrix]] is critical for understanding Gauss-Newton.

## Related Wiki Pages

- [[queries/jacobian-matrix]] — foundational; Gauss-Newton uses Jacobian at its core
- [[papers/jtdp-2003-blendshape-fitting]] — Gauss-Newton for marker-based blendshape weight solving
- [[papers/faceit-diaz-barros]] — FACEIT uses LM (damped Gauss-Newton) for 2D landmark fitting
- [[papers/le-2012-ssdr]] — SSDR uses QP (constrained least squares) for weight extraction
- [[papers/bailey-2020-fast-deep-facial]] — neural deformers trained via gradient descent (related but distinct)
- [[concepts/pose-space-deformation]] — PSD relies on Gauss-Newton for weight optimization in practice

---

**Summary:** Gauss-Newton is the go-to algorithm for non-linear least squares problems in character rigging. It uses the Jacobian to iteratively solve for IK angles, blendshape weights, and skinning parameters. When residuals are small and the problem is well-posed, it converges fast and reliably. The Levenberg-Marquardt variant adds damping for robustness and is the production standard.
