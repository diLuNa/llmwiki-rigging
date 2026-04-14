---
title: "Refined Inverse Rigging: A Balanced Approach to High-fidelity Blendshape Animation"
source: "https://arxiv.org/html/2401.16496v1"
author:
published:
created: 2026-04-14
description:
tags:
  - "clippings"
---
[Stevo Racković](https://orcid.org/0000-0002-5656-9189)  
Department of Mathematics  
Instituto Superior Técnico  
Lisbon, Portugal  
stevo.rackovic@tecnico.ulisboa.pt  
& [Cláudia Soares](https://orcid.org/0000-0003-3071-6627)  
Department of Computer Sceince  
NOVA School of Science and Technology  
Caparica, Portugal  
& [Dušan Jakovetić](https://orcid.org/0000-0003-3497-5589)  
Department of Mathematics and Informatics  
Faculty of Sciences  
Novi Sad, Serbia  

(January 2024)

###### Abstract

In this paper, we present an advanced approach to solving the inverse rig problem in blendshape animation, using high-quality corrective blendshapes. Our algorithm introduces novel enhancements in three key areas: ensuring high data fidelity in reconstructed meshes, achieving greater sparsity in weight distributions, and facilitating smoother frame-to-frame transitions. While the incorporation of corrective terms is a known practice, our method differentiates itself by employing a unique combination of $l_{1}$ norm regularization for sparsity and a temporal smoothness constraint through roughness penalty, focusing on the sum of second differences in consecutive frame weights.

A significant innovation in our approach is the temporal decoupling of blendshapes, which permits simultaneous optimization across entire animation sequences. This feature sets our work apart from existing methods and contributes to a more efficient and effective solution. Our algorithm exhibits a marked improvement in maintaining data fidelity and ensuring smooth frame transitions when compared to prior approaches that either lack smoothness regularization or rely solely on linear blendshape models. In addition to superior mesh resemblance and smoothness, our method offers practical benefits, including reduced computational complexity and execution time, achieved through a novel parallelization strategy using clustering methods.

Our results not only advance the state of the art in terms of fidelity, sparsity, and smoothness in inverse rigging but also introduce significant efficiency improvements. The source code will be made available upon acceptance of the paper.

![Refer to caption](https://arxiv.org/html/2401.16496v1/extracted/5376102/Figures/WeightsEvolutionFaces.png)

Figure 1: Demonstrating the Efficacy of Temporally Coherent Blendshape Animation. First row: Our Quartic Smooth method captures the intricate dynamics of facial expressions by leveraging a sophisticated blendshape rig, ensuring both high-fidelity mesh reconstruction and smooth temporal transitions in animation weights. Second row: The Linear Smooth method, as proposed by 1, prioritizes temporal smoothness but simplifies the blendshape model to a linear function, resulting in a trade-off with mesh accuracy. Third row: Quartic approach from 2 achieves a high degree of mesh fidelity by utilizing a complex blendshape model but does not account for the smoothness of frame-to-frame transitions, leading to potential discontinuities. Displayed are selected weight trajectories over 100 animation frames, with two consecutive frames magnified to showcase the mesh results. The second column employs red shading to illustrate mesh error, and the third column uses yellow to highlight discrepancies between successive frames, underscoring the balance between accuracy and smoothness in animation sequences.

## 1 Introduction

Blendshape animation, a predominant method in animating human faces, manipulates a 3D facial mesh $\textbf{b}_{0}\in\mathbb{R}^{3n}$ through interpolation among a predefined set of blendshapes $\textbf{b}_{1},\ldots,\textbf{b}_{m}\in\mathbb{R}^{3n}$, where $n$ denotes the number of mesh vertices [^3]. Representing diverse facial configurations, these blendshapes, when linearly combined with weights $\textbf{w}=[w_{1},\ldots,w_{m}]$, enable the creation of a wide range of expressions as

$$
f_{L}(\textbf{w};\textbf{B})=\textbf{b}_{0}+\textbf{B}\textbf{w},
$$

with $\textbf{B}\in\mathbb{R}^{3n\times m}$ forming a matrix of blendshape vectors. Here, the subscript L denotes the linear nature of this blendshape function. Modern advancements incorporate non-linear corrective terms into these models, enhancing realism and flexibility [^4]. For instance, a quartic blendshape function, denoted here as $f_{Q}$, integrates up to three levels of corrective terms:

$$
f_{Q}(\textbf{w})=\textbf{Bw}+\sum_{\{i,j\}\in\mathcal{P}}w_{i}w_{j}\textbf{b}%
^{\{ij\}}+\sum_{\{i,j,k\}\in\mathcal{T}}w_{i}w_{j}w_{k}\textbf{b}^{\{ijk\}}+%
\sum_{\{i,j,k,l\}\in\mathcal{Q}}w_{i}w_{j}w_{k}w_{l}\textbf{b}^{\{ijkl\}}.
$$

Such a detailed correction level is employed in industry-standard solutions like Metahumans <sup>1</sup>.

This paper addresses the inverse rig problem: given a target mesh $\widehat{\textbf{b}}\in\mathbb{R}^{3n}$, the goal is to find a set of weights w that accurately approximates the target. Model-based solutions to this problem leverage the structure of rig functions, utilizing optimization techniques rather than relying purely on data [^5] [^6]. The state-of-the-art (SOTA) model-based approach, as proposed in [^4], solves the problem by minimizing the data fidelity of the model while regularizing for sparsity, while constraining the weight values to a feasible set considering that the weights only make sense on an interval $[0,1]$, i.e.,

$$
\operatorname*{minimize}_{\textbf{0}\leq\textbf{w}\leq\textbf{1}}\frac{1}{2}\|%
f_{Q}(\textbf{w})-\widehat{\textbf{b}}\|_{2}^{2}+\alpha\textbf{1}^{T}\textbf{w},
$$

employing a coordinate descent method. Prior methods [^7] [^8] [^9], while effective, are confined to linear blendshape models and thus are less capable of replicating complex facial dynamics. However, a critical aspect in animation is the smoothness of frame-to-frame transitions, often overlooked in isolated frame fitting. This temporal dimension has been explored, for instance, by [^1], who introduced a smoothness regularization to the optimization objective:

$$
\operatorname*{minimize}_{\textbf{0}\leq\textbf{w}\leq\textbf{1}}\|f_{L}(%
\textbf{w})-\widehat{\textbf{b}}\|_{2}^{2}+\alpha\|\textbf{w}\|_{2}^{2}+\beta%
\|\textbf{w}-\textbf{v}\|_{2}^{2},
$$

where $\textbf{v}\in\mathbb{R}^{m}$ represents the weight vector from the previous frame, introducing a temporal continuity constraint. While effective, these methods primarily address linear blendshape models, limiting their capability to capture the more nuanced facial expressions enabled by non-linear models.

In this work, we bridge this gap by proposing a novel objective that harmoniously integrates both the advanced corrective terms of non-linear blendshape functions and the imperative of temporal smoothness. Our formulation extends beyond the scope of (3) by concurrently optimizing across all frames. This holistic approach not only ensures the fidelity of each individual frame to the target mesh but also guarantees the smoothness of transitions throughout the animation sequence, by formulating the problem

$$
\operatorname*{minimize}_{\textbf{0}\leq\textbf{w}\leq\textbf{1}}\sum_{t=1}^{T%
}\left(\frac{1}{n}\|f_{Q}(\textbf{w}^{(t)})-\widehat{\textbf{b}}^{(t)}\|_{2}^{%
2}+\frac{\alpha}{m}\|\textbf{w}^{(t)}\|_{1}\right)+\beta\sum_{t=2}^{T-1}\|%
\textbf{w}^{(t+1)}-2\textbf{w}^{(t)}+\textbf{w}^{(t-1)}\|_{2}^{2},
$$

where $T$ is the number of frames in the sequence, and $\beta$ is a regularization parameter that balances data fidelity and smoothness constraints. Notably, our method is adaptable to various levels of corrective terms within the blendshape function, ranging from linear ($f_{L}$) to higher-order non-linear functions (such as $f_{Q}$).

The generalizability and flexibility of our approach enable it to address a wider array of animation challenges, including those with complex facial dynamics.

This approach, through its comprehensive optimization across the entire animation sequence and its adaptability to various blendshape complexities, presents a significant step forward in achieving more precise facial reconstructions and ensuring smoother motion transitions in blendshape animation.

## 2 Related Work

Facial expressions play a crucial role in human perception and communication, a significance that extends into the realm of 3D animation. This section reviews the evolution and current state of facial animation techniques, particularly focusing on blendshape models, and situates our work within this landscape.

### 2.1 Anatomically-Based versus Blendshape Models

Anatomically-based face models, as discussed in works like [^10] and [^11], offer high-fidelity deformation and realistic perception. Despite their detailed representation, these models pose challenges in animation control and interpretability. In contrast, blendshape models, a standard in practical face animation due to their simplicity and ease of manipulation, have been extensively explored [^12] [^13] [^14]. While traditionally sculpted manually, there have been developments towards automation [^15] [^16] [^17] [^18] [^19] [^20]. Our work assumes the existence of such a blendshape basis, focusing instead on the inverse rigging process.

### 2.2 Inverse Rig Problem and Approaches

The inverse rig problem, central to our work, involves generating animations by adjusting blendshape weights over time. Two main approaches exist: model-based and data-based. Model-based methods [^5] [^16] [^4] utilize optimization techniques, leveraging the rig structure, as opposed to data-based methods that rely on regression models trained on extensive animated data [^21] [^22] [^23] [^24]. Our approach falls into the former category, focusing on a blendshape-based model-based solution. Previous works in this area typically address least squares problems with additional regularization for stability [^5] [^9] [^25], sparsity [^16] [^26] [^6], or temporal smoothness [^27] [^28].

### 2.3 Direct Manipulation and Face Segmentation

Related areas include direct manipulation, demanding real-time solutions for adjusting expressions [^8] [^1] [^9] [^25], and face segmentation for animation, where the focus varies from creating large mesh segments for inverse rig [^29] [^27] [^30] [^31] [^32] [^24] [^33] to adding secondary motion effects with smaller segments [^34] [^26] [^35] [^36]. While not our primary focus, the concept of face clustering for distributed rig inversion is also explored in our work.

### 2.4 Our Contribution

In this paper, we contribute to the field of blendshape animation by introducing an integrated problem formulation for high-quality rig inversion, combining 1.) complex corrective blendshape terms that enhance the fidelity of mesh reconstructions, drawing on the methodologies established in [^6] [^2]. We implement 2.) sparsity regularization to achieve a lower cardinality in the weight vectors, which aids in simplifying post-animation adjustments, as discussed in prior works [^7] [^4]. Additionally, 3.) acknowledging the critical role of temporal continuity in animation, we employ a roughness penalty regularization strategy aimed at ensuring smoother transitions between frames.

## 3 Refined Inverse Rigging Methodology for Blendshape Animation

In this section, we detail our approach for solving the inverse rig problem, prioritizing high accuracy in mesh reconstruction and ensuring smooth transitions between blendshape weights across frames. Unlike [^4], which focuses on single-frame analysis, our method evaluates the entire animation sequence, necessitating a matrix-based representation for weights and other elements in the objective function.

### 3.1 Data Fidelity and Regularization Framework

Consider an animation comprising $T$ frames, denoted as $t=1,\ldots,T$. We represent the weight vectors for each frame as $\textbf{w}^{(t)}$ and assemble these into a weight matrix $\textbf{W}=[\textbf{w}^{(1)},\ldots,\textbf{w}^{(T)}]\in\mathbb{R}^{m\times T}$. The rig function for the entire sequence is then expressed as:

$$
\begin{split}f(\textbf{W})=&\textbf{BW}+\sum_{t=1}^{T}\sum_{\{i,j\}\in\mathcal%
{P}}w_{i}^{(t)}w_{j}^{(t)}\text{diag}(\textbf{b}^{\{ij\}})\textbf{E}^{(t)}+%
\sum_{\{i,j,k\}\in\mathcal{T}}w_{i}^{(t)}w_{j}^{(t)}w_{k}^{(t)}\text{diag}(%
\textbf{b}^{\{ijk\}})\textbf{E}^{(t)}\\
&+\sum_{\{i,j,k,l\}\in\mathcal{Q}}w_{i}^{(t)}w_{j}^{(t)}w_{k}^{(t)}w_{l}^{(t)}%
\text{diag}(\textbf{b}^{\{ijkl\}})\textbf{E}^{(t)},\end{split}
$$

where $\textbf{E}^{(t)}$ is a matrix of zeros with the $t^{th}$ column consisting of ones. Similarly, we define the target meshes matrix  
$\hat{\textbf{B}}=[\hat{\textbf{b}}^{(1)},\ldots,\hat{\textbf{b}}^{(T)}]\in%
\mathbb{R}^{n\times T}$, with $\hat{\textbf{b}}^{(t)}$ being the target mesh for frame $t$. We propose the objective that consists of three terms:

$$
\operatorname*{minimize}_{0\leq\textbf{W}\leq 1}E_{\text{df}}+\alpha E_{\text{%
sr}}+\beta E_{\text{tsr}},
$$

where $E_{\text{df}}$ stands for a data fidelity term, i.e., a difference between the estimated mesh and the target mesh in vertex space, $E_{\text{sr}}$ stands for the sparsity regularization forcing the cardinality of the weights to be low, and $E_{\text{tsr}}$ is temporal smoothness regularizer, forcing the weights in the consecutive frames to have similar values; $\alpha,\beta\geq 0$ are corresponding regularization weights, dictating the importance of each term. Let us observe each of these terms individually.

#### Data Fidelity

The data fidelity term, along with the sparsity regularization term, aligns with the formulation in (2) but is now adapted to a matrix context to handle the entire animation sequence. Specifically, the data fidelity term is defined as:

$$
E_{\text{df}}=\frac{1}{n}\|f(\textbf{W})-\hat{\textbf{B}}\|_{F}^{2},
$$

where $\|\cdot\|_{F}$ denotes the Frobenius norm, measuring the discrepancy between the estimated mesh sequence $f(\textbf{W})$ and the target mesh sequence $\hat{\textbf{B}}$.

We employ a coordinate descent approach to minimize this term, focusing on a single blendshape controller, denoted as $e$, across the temporal dimension. In this context, we reformulate (7) into a quadratic expression:

$$
E_{\text{df}}=\frac{1}{n}\textbf{W}_{e}^{T}\Phi\textbf{W}_{e}+\frac{2}{n}%
\textbf{W}_{e}^{T}\Theta,
$$

where $\textbf{W}_{e}$ represents the weights corresponding to controller $e$ over all frames. The matrices $\Phi$ and $\Theta$ are constructed as follows:

Matrix $\Phi=\text{diag}([\phi^{(1)T}\phi^{(1)},\ldots,\phi^{(T)T}\phi^{(T)}])$ encapsulates all the terms interacting with the quadratic terms of the objective. Each $\phi^{(t)}$ represents the contribution of the quadratic term of the blendshape controller $e$ at frame $t$, computed as:

$$
\phi^{(t)}_{i}=B_{ie}+\sum_{j\in\mathcal{P}(e)}w_{j}^{(t)}\textbf{b}^{\{je\}}_%
{i}+\sum_{\{j,k\}\in\mathcal{T}(e)}w_{j}^{(t)}w_{k}^{(t)}\textbf{b}^{\{jke\}}_%
{i}+\sum_{\{j,k,l\}\in\mathcal{Q}(e)}w_{j}^{(t)}w_{k}^{(t)}w_{l}^{(t)}\textbf{%
b}^{\{jkle\}}_{i},
$$

which considers not only the direct influence of controller $e$ but also its interaction with other controllers in the corrective terms.

Matrix $\Theta=[\phi^{(1)T}\psi^{(1)},\ldots,\phi^{(T)T}\psi^{(T)}]^{T}$ represents the linear interaction terms, where each $\psi^{(t)}$ is given by:

$$
\begin{split}\psi_{i}^{(t)}&=\sum_{j\neq e}w_{j}^{(t)}B_{ij}+\sum_{\{j,k\}\in%
\mathcal{P}}w_{j}^{(t)}w_{k}^{(t)}\textbf{b}^{\{jk\}}_{i}+\sum_{\{j,k,l\}\in%
\mathcal{T}}w_{j}^{(t)}w_{k}^{(t)}w_{l}^{(t)}\textbf{b}^{\{jkl\}}_{i}\\
&+\sum_{\{j,k,l,h\}\in\mathcal{Q}}w_{j}^{(t)}w_{k}^{(t)}w_{l}^{(t)}w_{h}^{(t)}%
\textbf{b}^{\{jklh\}}_{i}-\hat{\textbf{b}}^{(t)}_{i}.\end{split}
$$

This accounts for the contributions of all other blendshape controllers, as well as the deviation from the target mesh $\hat{\textbf{b}}^{(t)}$ at frame $t$.

Through this formulation, the data fidelity term effectively quantifies and minimizes the difference between the animated mesh sequence and the target sequence, thereby ensuring high accuracy in replicating desired facial expressions over time.

#### Sparsity Regularization

In our approach, the sparsity regularization term is critical for ensuring that the animation remains computationally efficient and interpretable. It is defined as the normalized sum of all blendshape weights across the entire animation sequence. Mathematically, this is represented as:

$$
E_{\text{sr}}=\frac{1}{m}\sum_{i=1}^{m}\sum_{t=1}^{T}w_{i}^{(t)}=\frac{1}{m}%
\textbf{1}^{T}\textbf{W}\textbf{1},
$$

where 1 denotes a vector of ones of appropriate dimension. This formulation encourages the model to use as few active blendshapes as possible at each frame, leading to a sparser and more interpretable set of blendshape weights. Importantly, due to the non-negativity constraints on the weights, $E_{\text{sr}}$ is guaranteed to be a non-negative term.

The integration of sparsity regularization into the optimization process serves multiple purposes: it not only enhances computational efficiency by reducing the number of active blendshapes but also simplifies the task of manual adjustments or further processing by animators. By penalizing the sum of the weights, the model naturally gravitates towards solutions where fewer blendshapes are used to achieve the desired facial expressions, thereby promoting a more streamlined and manageable animation process.

#### Temporal Smoothness Regularization

A key aspect of realistic animation is the smoothness of transitions between frames. To achieve this, we incorporate a roughness penalty function into our regularization framework. This function penalizes the squared differences between adjacent weight values across frames, effectively encouraging temporal continuity in the animation. The temporal smoothness regularization term is formulated as follows:

$$
E_{\text{tsr}}=\sum_{t=1}^{T-2}\sum_{i=1}^{m}|w_{i}^{(t)}-2w_{i}^{(t+1)}+w_{i}%
^{(t+2)}|^{2}=\sum_{i}\textbf{W}_{i}^{T}\textbf{F}\textbf{W}_{i},
$$

where $\textbf{W}_{i}$ denotes the weight vector for the $i^{th}$ blendshape across all frames. The matrix F is a pentadiagonal matrix defined as:

$$
\textbf{F}=\begin{bmatrix}1&-2&1&\color[rgb]{.5,.5,.5}\definecolor[named]{%
pgfstrokecolor}{rgb}{.5,.5,.5}\pgfsys@color@gray@stroke{.5}%
\pgfsys@color@gray@fill{.5}0&\cdots&\color[rgb]{.5,.5,.5}\definecolor[named]{%
pgfstrokecolor}{rgb}{.5,.5,.5}\pgfsys@color@gray@stroke{.5}%
\pgfsys@color@gray@fill{.5}0\\
-2&5&-4&1&\cdots&\color[rgb]{.5,.5,.5}\definecolor[named]{pgfstrokecolor}{rgb}%
{.5,.5,.5}\pgfsys@color@gray@stroke{.5}\pgfsys@color@gray@fill{.5}0\\
1&-4&6&-4&\ddots&\vdots\\
\color[rgb]{.5,.5,.5}\definecolor[named]{pgfstrokecolor}{rgb}{.5,.5,.5}%
\pgfsys@color@gray@stroke{.5}\pgfsys@color@gray@fill{.5}0&1&-4&6&\ddots&1\\
\vdots&\ddots&\ddots&\ddots&\ddots&-2\\
\color[rgb]{.5,.5,.5}\definecolor[named]{pgfstrokecolor}{rgb}{.5,.5,.5}%
\pgfsys@color@gray@stroke{.5}\pgfsys@color@gray@fill{.5}0&\cdots&\color[rgb]{%
.5,.5,.5}\definecolor[named]{pgfstrokecolor}{rgb}{.5,.5,.5}%
\pgfsys@color@gray@stroke{.5}\pgfsys@color@gray@fill{.5}0&1&-2&1\end{bmatrix},
$$

with the pattern designed to penalize the roughness or abrupt changes in the weight vectors between consecutive frames.

This regularization term thus plays a crucial role in ensuring the naturalness and fluidity of the generated animation. By minimizing $E_{\text{tsr}}$, our model actively works to smooth out the transitions, leading to more lifelike and appealing animations that closely mimic natural human expressions over time.

#### Final formulation.

To synthesize the various aspects of our method into a coherent optimization framework, we formulate a comprehensive objective function that balances the need for data fidelity, sparsity, and temporal smoothness. This objective, to be minimized with respect to each blendshape controller $e$, encapsulates the essence of our approach:

$$
\operatorname*{minimize}_{\textbf{0}\leq\textbf{W}_{e}\leq\textbf{1}}\textbf{W%
}_{e}^{T}\left(\frac{1}{n}\Phi+\beta\textbf{F}\right)\textbf{W}_{e}+2\textbf{W%
}_{e}^{T}\left(\frac{1}{n}\Theta+\frac{\alpha}{2m}\textbf{1}\right).
$$

In this equation, $\Phi$ and $\Theta$ are matrices derived from the data fidelity term, encoding the relationship between the blendshape weights and the target meshes. The matrix F, arising from the temporal smoothness regularization term, ensures that changes in the blendshape weights are gradual over the sequence of frames. Lastly, the term involving 1, originating from the sparsity regularization, promotes solutions with fewer active blendshapes, thereby aiding in interpretability and computational efficiency.

This carefully constructed objective function is central to our method, guiding the optimization process towards solutions that are not only accurate in reproducing the target facial expressions but also efficient and smooth over time. By balancing these critical aspects, our approach advances the state-of-the-art in blendshape animation, particularly in scenarios requiring high fidelity and natural motion dynamics.

### 3.2 Clustering Approach for Computational Efficiency

![Refer to caption](https://arxiv.org/html/2401.16496v1/x4.png)

Figure 2: Top row: The trade-off between Reconstruction Error ( E R subscript 𝐸 𝑅 E\_{R} italic\_E start\_POSTSUBSCRIPT italic\_R end\_POSTSUBSCRIPT ) and Density D 𝐷 E\_{D} italic\_E start\_POSTSUBSCRIPT italic\_D end\_POSTSUBSCRIPT ) (left), and Inter-Density I ⁢ 𝐼 E\_{ID} italic\_E start\_POSTSUBSCRIPT italic\_I italic\_D end\_POSTSUBSCRIPT ) (right), across different clustering approaches, with annotations indicating the chosen number of clusters ( K 𝐾 italic\_K ). Bottom row: Visualization of clusters obtained using S J 𝑆 𝐽 RSJD italic\_R italic\_S italic\_J italic\_D with = 29 K=29 italic\_K = 29 (left) and A 𝐴 RSJD\_{A} italic\_R italic\_S italic\_J italic\_D start\_POSTSUBSCRIPT italic\_A end\_POSTSUBSCRIPT 13 K=13 italic\_K = 13 (right). In addition to the mesh clusters, a bipartite graph representation is shown, using the same color coding, where the left partition denotes mesh vertices, and the right partition signifies the blendshape indices assigned to each cluster.

Given the localized nature of facial features, a significant number of vertices in the human face may have limited influence on the majority of blendshape weights. Our approach incorporates a face clustering strategy to exploit this characteristic for enhanced computational efficiency. This strategy allows for a parallelized and potentially more regularized solution to the inverse rigging problem [^7] [^33] [^2].

We adopt the clustering methodologies proposed in [^33] (denoted as $RSJD$) and [^2] (denoted as $RSJD_{A}$). These methods are particularly suitable as they generate clusters in a model-based manner. However, our approach remains flexible enough to be applicable with other clustering techniques, provided they meaningfully separate mesh segments and blendshape controllers.

The core idea is to treat each cluster as an independent model, thereby decomposing the overall inverse rigging problem (12) into a series of smaller subproblems. Each subproblem focuses on a specific subset of vertices and blendshapes relevant to its cluster. This subdivision not only facilitates parallel processing but also potentially introduces additional regularization opportunities, leading to a more efficient solution overall.

Following the recommendations in [^2], we generate several instantiations of each clustering approach. The optimal configuration is selected based on a balance between Reconstruction Error and Density in the resulting clustering graphs, as illustrated in Figure 2 (top). Optimal cluster numbers, such as $K=29$ for $RSJD$ and $K=13$ for $RSJD_{A}$, are determined to minimize the model size while retaining essential information. The corresponding mesh clusters and their bipartite graph representations are detailed in Figure 2 (bottom), showcasing the effective distribution of vertices and blendshape indices across the identified clusters.

### 3.3 Optimization Strategy

The optimization strategy used in solving the proposed objective is coordinate descent, a well established optimization technique that is guaranteed to produce monotonically non-increasing costs [^37] [^38]. With coordinate descent, a single component of the problem is visited at a time, and the objective is minimized in it, while keeping the other values fixed, as we do in (12), observing only a single controller $e$ as a variable. This decoupling in components allows us to simplify otherwise non-convex problem (4), into a constrained quadratic program, for which fast solutions and implementations are readily available [^39] [^40]. Coordinate descent is particularly suitable for for the application in inverse rigging, since estimating one blendshape weight at a time will help avoid the simultaneous activation of blendshapes with canceling effects, i.e., moving the corner of the mouth up and down at the same time [^7].

An important aspect of coordinate descent is the order of component updates. Even though the convergence guaranties hold with an arbitrary update order [^38], in practice a poor choice can lead to slower convergence and a bad local minima. This problem was also studied in blendshape animation literature [^7] [^4] [^41]. We follow the stance of [^7], ordering the blendshapes by their overall magnitude of deformation in the mesh, in line with artist intuition of initially setting the more drastic weights before focusing on fine details.

## 4 Quantitative Analysis of Animation Techniques

This section presents the comprehensive evaluation of our proposed blendshape animation methodology. We first describe the data and benchmark models used in our study, followed by a detailed analysis of the results. The performance of our method is compared against established benchmarks to demonstrate its efficacy in achieving high-fidelity, smooth animations. The impact of different parameters on the results is also examined to provide insights into the behavior of our approach under various conditions.

![Refer to caption](https://arxiv.org/html/2401.16496v1/x5.png)

Figure 3: Parametric Analysis of Animation Metrics During Training, comparing our method ( Quartic Smooth ) with benchmarks. Top row: This graph illustrates the interplay between blendshape cardinality and maximum mesh error under various animation approaches. The color coding denotes different levels of the sparsity regularizer, α 𝛼 \\alpha italic\_α, while individual points represent a spectrum of the smoothness parameter, β 𝛽 \\beta italic\_β, converging at = 0 \\beta=0 italic\_β = 0 indicated by the solid gray line. The horizontal dotted line marks the cardinality of the actual animation data used as the ground truth, whereas the vertical dotted line indicates the mesh error that would result if no blendshapes were activated (all weights at ). Bottom row: Here, we chart the roughness penalty corresponding to the varying values of along the x-axis. The color scheme is consistent with the top graph, linked to the values. The horizontal dotted line represents the benchmark roughness penalty derived from the ground-truth animation data.

![Refer to caption](https://arxiv.org/html/2401.16496v1/x6.png)

Figure 4: Comparative Analysis of Training Metrics Across Different Parameterizations and Methodologies. In this Figure we show how applying clustering on top of our approach affects the overall results.

### 4.1 Dataset Characteristics and Comparative Benchmarks

We selected the Metahuman character Jesse to evaluate our algorithm. This choice is motivated by the high-quality and realistic nature of Metahuman blendshape models, coupled with their accessibility as publicly available resources. The Jesse model is equipped with $m=80$ base blendshapes and over $400$ corrective terms, encompassing the first, second, and third levels of correction. These elements make it an ideal candidate for demonstrating the nuanced capabilities of our method in handling complex facial animations.

Originally, the meshes contain $24000$ vertices. To focus on the facial region, which is our primary interest, we have excluded vertices on the neck and an inactive area at the back of the skull. This results in a subsampled mesh comprising $n=10000$ vertices. The model is animated to generate a reference motion, which comprises $80$ frames for the training set and $100$ frames for the test set. This division allows for a robust assessment of our method’s performance both in learning and generalization.

In our results section, we refer to our proposed method as Quartic Smooth. This designation emphasizes its unique aspects: the inclusion of corrective terms using a quartic blendshape function for enhanced realism, and the integration of smoothness regularization, setting it apart from previous model-based solutions. These characteristics are pivotal in achieving more lifelike and dynamically consistent facial animations.

Our benchmarks include two prior works for comparative analysis. The first is the method described in [^1], named Linear Smooth, which incorporates smoothness regularization but does not include corrective terms. This method optimizes the objective defined in (3). The second benchmark is the Quartic algorithm from [^2], which considers corrective terms for better mesh reconstruction but treats each frame independently, overlooking temporal continuity. Quartic solves the objective in (2). Notably, while both benchmarks include weight regularization, they differ in approach: Quartic uses an $l_{1}$ norm, promoting sparsity, whereas Linear Smooth employs a squared $l_{2}$ norm, penalizing large activations without directly reducing the number of active components.

Additionally, we explore an extension of our proposed algorithm that incorporates the face clustering technique detailed in Section 3.2. We examine two instances of clustering: Clustered $RSJD$ 29 and Clustered $RSJD_{A}$ 13, named after the clustering methods and the chosen number of clusters ($K$). These cases help to assess the impact of facial clustering on the performance and efficiency of our approach.

### 4.2 Analytical Performance Evaluation

All the considered methods have a weight regularization hyperparameter $\alpha$ that should be selected before comparing the results in more details. Additionally, our proposed method, Quartic Smooth, as well as the benchmark Linear Smooth, have the smoothness regularization hyperparameter $\beta$. To select the appropriate values, each method is cross-validated with a wide choice of values, as presented in Fig. 3 and 4. In general these results draw an expected trade-of curve between cardinality and mesh error, with the exception of the Linear Smooth — in this case a favorable decrease of the cardinality is never achieved, since $l_{2}$ norm in the objective tends to keep small positive values rather than setting them to zero. Optimal values for the parameters are selected so that all three presented metrics are minimized, and the final selection that is used for further tests is listed in Tab. 1.

|  | Quartic Smooth | Linear Smooth | Quartic | Clustered $RSJD$ 29 | Clustered $RSJD_{A}$ 13 |
| --- | --- | --- | --- | --- | --- |
| $\alpha$ | $0.0078$ | $0.01$ | $0.9$ | $1$ | $0.8$ |
| $\beta$ | $1$ | $00$ | / | $10$ | $1$ |

Table 1: Final parameter values for each method.

![Refer to caption](https://arxiv.org/html/2401.16496v1/x7.png)

Figure 5: Results over the test set with the selected hyperparameter values corresponding to Table 1. The execution time for the clustered approach is presented in solid and shaded — solid color indicates the execution time of the slowest cluster, as that is the cost when solving the problem in parallel, while shaded bar shows the time of solving the clusters sequentially.

|  | Max Mesh Error | Mean Mesh Error | Cardinality | $l_{1}$ Norm | Roughness Penalty | Execution Time |
| --- | --- | --- | --- | --- | --- | --- |
| Quartic Smooth | $.101$ | $.019$ | $56.3$ | $9.431$ | $7.2e^{-5}$ | $2.16$ |
| Linear Smooth | $.257$ | $.051$ | $68.6$ | $9.649$ | $4.2e^{-4}$ | $0.02$ |
| Quartic | $.086$ | $.016$ | $49.7$ | $9.818$ | $1.1e^{-3}$ | $14.4$ |
| $RSJD$ | $.387$ | $.093$ | $58.2$ | $8.695$ | $2.8e^{-4}$ | $0.15$ |
| $RSJD_{A}$ | $.433$ | $.115$ | $54.0$ | $5.500$ | $1.5e^{-4}$ | $0.44$ |

Table 2: Average metrics values for test results (see also Figure 5).

By examining Tab. 2, we can compare the performance of the various methods (Quartic Smooth, Linear Smooth, Quartic, RSJD, and $RSJD_{A}$) across several key metrics: Max Mesh Error, Mean Mesh Error, Cardinality, $l_{1}$ Norm, Roughness Penalty, and Execution Time.

#### Max Mesh Error and Mean Mesh Error:

Quartic exhibits the lowest Max and Mean Mesh Errors ($.086$ and $.016$, respectively), indicating its superior ability to closely match the target mesh in the worst-case and on average. This suggests high accuracy in mesh reconstruction. Quartic Smooth also performs well, with slightly higher errors, but still significantly better than Linear Smooth, RSJD, and $RSJD_{A}$.

#### Cardinality:

The Cardinality, which indicates the number of active blendshapes, is lowest for Quartic (49.7), suggesting it is the most efficient in terms of blendshape usage. Quartic Smooth has a moderately higher cardinality (56.3) compared to Quartic, but lower than Linear Smooth and RSJD.

#### l1subscript𝑙1l\_{1}italic\_l start\_POSTSUBSCRIPT 1 end\_POSTSUBSCRIPT Norm:

The $l_{1}$ Norm, reflecting the sum of absolute weights, is highest for Quartic (9.818) and lowest for $RSJD_{A}$ (5.500). Higher values indicate more weight is being used overall, which can suggest more intense or complex facial expressions.

#### Roughness Penalty:

Quartic Smooth has the lowest Roughness Penalty ($7.2e^{-5}$), highlighting its effectiveness in ensuring smooth frame-to-frame transitions. Quartic, despite its accuracy, has a higher roughness penalty ($1.1e^{-3}$), implying less smoothness in transitions compared to Quartic Smooth.

#### Execution Time:

Linear Smooth is the fastest ($.02$ seconds), which is expected given its less complex nature (lacking corrective terms). Quartic is the slowest (14.4 seconds), possibly due to the computational overhead of handling corrective terms. Quartic Smooth strikes a balance between complexity and speed (2.16 seconds), offering a more efficient solution than Quartic while maintaining high accuracy and smoothness. This advantage over Quartic is due to the parallelizable structure given by the clustering.

Quartic Smooth demonstrates a well-balanced performance across accuracy, efficiency, and smoothness, making it a robust choice for high-quality and realistic blendshape animation. Quartic excels in mesh error metrics but at the cost of higher roughness and longer execution time, while Linear Smooth offers the fastest execution with compromises in accuracy and smoothness. The clustered approaches (RSJD and $RSJD_{A}$) offer varying trade-offs, with $RSJD_{A}$ showing lower execution times and roughness penalties but at the cost of higher mesh errors.

Figure 3 shows graphs evaluating three approaches: Quartic Smooth, Linear Smooth, and Quartic. Each graph shows the trade-off between cardinality and maximum mesh error on the top row and the roughness penalty across different smoothness parameter $\beta$ values on the bottom row.

#### Quartic Smooth:

The top graph suggests that as the sparsity regularizer $\alpha$ increases, both the cardinality and the maximum mesh error generally increase. This indicates that higher sparsity (achieved by a larger $\alpha$) comes at the cost of accuracy (higher mesh error). In the bottom graph, the roughness penalty seems relatively stable across various values of $\beta$, suggesting that the smoothness regularization is not significantly impacting the roughness penalty in this approach.

#### Linear Smooth:

The top graph shows that the maximum mesh error and cardinality do not significantly change with different values of $\alpha$, indicating a potential plateau in the trade-off, where increasing sparsity does not impact the mesh error substantially. The bottom graph shows variations in the roughness penalty across different values of $\beta$, but the changes are not dramatic, implying that the model’s smoothness is not highly sensitive to this parameter within the tested range.

#### Quartic:

The top graph indicates that increasing $\alpha$ leads to a decrease in the maximum mesh error but at the expense of a rapid increase in cardinality, suggesting a strong influence of the sparsity regularizer on model complexity. There’s no bottom graph for roughness as the Quartic model does not seem to include the smoothness parameter $\beta$.

The Quartic Smooth approach seems to strike a balance between maintaining mesh accuracy and controlling the model complexity (cardinality), especially when compared to the Linear Smooth and Quartic approaches. The roughness penalties across all methods are relatively low, indicating smooth transitions, with Quartic Smooth showing a slight advantage. However, one must consider the trade-offs between accuracy, sparsity, and temporal smoothness when selecting the appropriate parameters for each method.

Figure 4 shows a comparative analysis of three different blendshape animation approaches: Quartic Smooth, Clustered RSJD 29, and Clustered RSJD\_A 13. The analysis is based on the evolution of specific metrics over the training set while varying two parameters: the sparsity regularizer ($\alpha$) and the smoothness parameter ($\beta$).

The Quartic Smooth approach in our experiments offers a favorable balance between animation accuracy and sparsity, with smooth temporal transitions as indicated by the low roughness penalties. The clustered approaches may provide computational benefits, but potentially at the cost of increased max mesh error, especially for higher sparsity levels. The choice between these methods may depend on the specific requirements of an animation project, such as the necessity for real-time performance (favoring clustered methods) versus the need for high-fidelity animations (favoring Quartic Smooth).

![Refer to caption](https://arxiv.org/html/2401.16496v1/extracted/5376102/Figures/ErrorScatters.png)

Figure 6: Resulting meshes for selected frames (rows), and for each method (columns). Stronger red tones indicate higher mesh error.

## 5 Conclusion

We have introduced Quartic Smooth, an advanced model-based approach for blendshape animation that adeptly balances accuracy, sparsity, and temporal smoothness. Our method demonstrates a marked improvement in mesh fidelity over traditional linear models and offers a flexible framework for both high-quality and real-time applications. Our findings illustrate Quartic Smooth’s superior performance in creating realistic facial animations with reduced computational overhead, particularly when compared to existing linear and non-linear approaches. The introduction of face clustering techniques further augments computational efficiency, opening possibilities for real-time animation processing. Future work will explore the optimization of these techniques and the integration of machine learning to refine parameter selection. With its contribution to the realistic and efficient inverse rigging of facial animations, Quartic Smooth is poised to influence future developments in character animation within the computer graphics community.

[^1]: Jaewoo Seo, Geoffrey Irving, J. P. Lewis, and Junyong Noh. Compression and direct manipulation of complex blendshape models. *ACM Trans. Graph.*, 30(6):1–10, dec 2011.

[^2]: Stevo Racković, Cláudia Soares, and Dušan Jakovetić. Distributed solution of the blendshape rig inversion problem. In *SIGGRAPH Asia 2023 Technical Communications*, SA ’23, New York, NY, USA, 2023. Association for Computing Machinery. ISBN 9798400703140. doi:[10.1145/3610543.3626166](https://doi.org/10.1145/3610543.3626166). URL [https://doi.org/10.1145/3610543.3626166](https://doi.org/10.1145/3610543.3626166).

[^3]: John P. Lewis, Ken Anjyo, Taehyun Rhee, Mengjie Zhang, Frederic H. Pighin, and Zhigang Deng. Practice and theory of blendshape facial models. *Eurographics (State of the Art Reports)*, 1(8):2, 2014.

[^4]: Stevo Racković, Cláudia Soares, Dušan Jakovetić, and Zoranka Desnica. High-fidelity interpretable inverse rig: An accurate and sparse solution optimizing the quartic blendshape model. *arXiv preprint arXiv:2302.04820*, 2023a.

[^5]: Cumhur Ozan Çetinaslan. *Position Manipulation Techniques for Facial Animation*. PhD thesis, Faculdade de Ciencias da Universidade do Porto, 2016.

[^6]: Stevo Racković, Cláudia Soares, Dušan Jakovetić, and Zoranka Desnica. A majorization–minimization-based method for nonconvex inverse rig problems in facial animation: algorithm derivation. *Optimization Letters*, pages 1–15, 2023b.

[^7]: Yeongho Seol, Jaewoo Seo, Paul Hyunjin Kim, J. P. Lewis, and Junyong Noh. Artist friendly facial animation retargeting. In *SIGGRAPH Asia 2011*, 2011.

[^8]: J.P. Lewis and Ken-ichi Anjyo. Direct manipulation blendshapes. *IEEE Computer Graphics and Applications*, 30(04):42–50, 2010.

[^9]: Ozan Cetinaslan and Veronica Orvalho. Sketching manipulators for localized blendshape editing. *Graphical Models*, 108:101059, 2020a.

[^10]: Eftychios Sifakis, Igor Neverov, and Ronald Fedkiw. Automatic determination of facial muscle activations from sparse motion capture marker data. In *ACM SIGGRAPH 2005 Papers*, page 417–425. Association for Computing Machinery, 2005.

[^11]: Alexandru-Eugen Ichim, Petr Kadleček, Ladislav Kavan, and Mark Pauly. Phace: Physics-based face modeling and animation. *ACM Transactions on Graphics (TOG)*, 36(4):1–14, 2017.

[^12]: Frédéric H. Pighin, Jamie Hecker, Dani Lischinski, Richard Szeliski, and D. Salesin. Synthesizing realistic facial expressions from photographs. *Proceedings of the 25th annual conference on Computer graphics and interactive techniques*, 1998.

[^13]: Byoungwon Choe and Hyeong-Seok Ko. Analysis and synthesis of facial expressions with hand-generated muscle actuation basis. In *ACM SIGGRAPH 2006*. 2006.

[^14]: Byoungwon Choe, Hanook Lee, and Hyeong-Seok Ko. Performance-driven muscle-based facial animation. *The Journal of Visualization and Computer Animation*, 12(2):67–79, 2001.

[^15]: Zhigang Deng, Pei-Ying Chiang, Pamela Fox, and Ulrich Neumann. Animating blendshape faces by cross-mapping motion capture data. In *Proceedings of the 2006 Symposium on Interactive 3D Graphics and Games*, page 43–48. Association for Computing Machinery, 2006.

[^16]: Sofien Bouaziz, Yangang Wang, and Mark Pauly. Online modeling for realtime facial animation. *ACM Trans. Graph.*, 32(4), 2013.

[^17]: Lucio Moser, Chinyu Chien, Mark Williams, Jose Serra, Darren Hendler, and Doug Roble. Semi-supervised video-driven facial animation transfer for production. *ACM Transactions on Graphics (TOG)*, 40(6):1–18, 2021.

[^18]: Hao Li, Thibaut Weise, and Mark Pauly. Example-based facial rigging. *ACM Trans. Graph.*, 29(4):1–6, 2010.

[^19]: Hao Li, Jihun Yu, Yuting Ye, and Chris Bregler. Realtime facial animation with on-the-fly correctives. *ACM Trans. Graph.*, 32(4):42–1, 2013.

[^20]: Roger Blanco i Ribera, Eduard Zell, J. P. Lewis, Junyong Noh, and Mario Botsch. Facial retargeting with automatic range of motion alignment. *ACM Trans. Graph.*, 36(4), 2017.

[^21]: Jaewon Song, Byungkuk Choi, Yeongho Seol, and Jun yong Noh. Characteristic facial retargeting. *Computer Animation and Virtual Worlds*, 22, 2011.

[^22]: Yeongho Seol and J. P. Lewis. Tuning facial animation in a mocap pipeline. In *ACM SIGGRAPH 2014 Talks*, SIGGRAPH ’14. Association for Computing Machinery, 2014.

[^23]: Daniel Holden, Jun Saito, and Taku Komura. Learning an inverse rig mapping for character animation. In *Proceedings of the 14th ACM SIGGRAPH/Eurographics Symposium on Computer Animation*, pages 165–173, 2015.

[^24]: Stephen W. Bailey, Dalton Omens, Paul Dilorenzo, and James F. O’Brien. Fast and deep facial deformations. *ACM Trans. Graph.*, 39(4), 2020.

[^25]: Ozan Cetinaslan and Veronica Orvalho. Stabilized blendshape editing using localized jacobian transpose descent. *Graphical Models*, 112:101091, 2020b.

[^26]: Thomas Neumann, Kiran Varanasi, Stephan Wenger, Markus Wacker, Marcus Magnor, and Christian Theobalt. Sparse localized deformation components. *ACM Trans. Graph.*, 32(6):1–10, 2013.

[^27]: J. Rafael Tena, Fernando De la Torre, and Iain Matthews. Interactive region-based linear 3D face models. In *ACM SIGGRAPH 2011 Papers*, 2011.

[^28]: Yeongho Seol, J.P. Lewis, Jaewoo Seo, Byungkuk Choi, Ken Anjyo, and Junyong Noh. Spacetime expression cloning for blendshapes. *ACM Trans. Graph.*, 31(2), 2012.

[^29]: Pushkar Joshi, Wen C Tien, Mathieu Desbrun, and Frédéric Pighin. Learning controls for blend shape based realistic facial animation. In *ACM SIGGRAPH 2006*. 2006.

[^30]: Hirose Kei and Higuchi Tomoyuki. Creating facial animation of characters via mocap data. *Journal of Applied Statistics*, 39(12):2583–2597, 2012.

[^31]: Clément Reverdy, Sylvie Gibet, and Caroline Larboulette. Optimal marker set for motion capture of dynamical facial expressions. In *Proceedings of the 8th ACM SIGGRAPH Conference on Motion in Games*, page 31–36. Association for Computing Machinery, 2015.

[^32]: Fratarcangeli Marco, Bradley Derek, A. Gruber, Zoss Gaspard, and Beeler Thabo. Fast nonlinear least squares optimization of large-scale semi-sparse problems. *Computer Graphics Forum*, 39, 2020.

[^33]: Stevo Racković, Cláudia Soares, Dušan Jakovetić, Zoranka Desnica, and Relja Ljubobratović. Clustering of the blendshape facial model. In *2021 29th European Signal Processing Conference (EUSIPCO)*, pages 1556–1560. IEEE, 2021.

[^34]: Gaspard Zoss, Eftychios Sifakis, Markus Gross, Thabo Beeler, and Derek Bradley. Data-driven extraction and composition of secondary dynamics in facial performance capture. *ACM Transactions on Graphics (TOG)*, 39(4):107–1, 2020.

[^35]: Chenglei Wu, Derek Bradley, Markus Gross, and Thabo Beeler. An anatomically-constrained local deformation model for monocular face capture. *ACM Trans. Graph.*, 35(4):1–12, 2016.

[^36]: Marco Romeo and S. Schvartzman. Data-driven facial simulation. In *Computer Graphics Forum*, volume 39, pages 513–526. Wiley Online Library, 2020.

[^37]: Zhi-Quan Luo and Paul Tseng. On the convergence of the coordinate descent method for convex differentiable minimization. *Journal of Optimization Theory and Applications*, 72(1):7–35, 1992.

[^38]: Stephen J Wright. Coordinate descent algorithms. *Mathematical programming*, 151(1):3–34, 2015.

[^39]: Jorge J Moré and Gerardo Toraldo. Algorithms for bound constrained quadratic programming problems. *Numerische Mathematik*, 55(4):377–400, 1989.

[^40]: Pauli Virtanen, Ralf Gommers, Travis E Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, Pearu Peterson, Warren Weckesser, Jonathan Bright, et al. Scipy 1.0: fundamental algorithms for scientific computing in python. *Nature methods*, 17(3):261–272, 2020.

[^41]: David AB Hyde, Michael Bao, and Ronald Fedkiw. On obtaining sparse semantic solutions for inverse problems, control, and neural network training. *Journal of Computational Physics*, 443:110498, 2021.