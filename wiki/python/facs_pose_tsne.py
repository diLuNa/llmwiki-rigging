"""
FACS-guided t-SNE / UMAP clustering of face expression poses.

Input
-----
expression_params : (N, 382)  PCA expression coefficients
pca_basis         : (382, V*3) decoder matrix  (optional, for Option B)
mean_face         : (V*3,)     mean face vertices (optional, for Option B)
region_masks      : dict[str -> np.ndarray of int]  vertex index sets per FACS region

Output
------
embedding         : (N, 2)    2-D coordinates for scatter plot
features          : (N, R*3)  per-region mean displacement vectors (Option B only)
"""

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.cm as cm

try:
    import umap
    _REDUCER = "umap"
except ImportError:
    from sklearn.manifold import TSNE
    _REDUCER = "tsne"
    print("umap-learn not found — falling back to sklearn TSNE (slower).")
    print("Install with:  pip install umap-learn")


# ---------------------------------------------------------------------------
# FACS region definitions
# ---------------------------------------------------------------------------
# Map each region name to the vertex indices that cover it.
# Replace these with your actual mesh's vertex indices.
# If you have FLAME topology, see FLAME_REGION_MASKS below.

FACS_REGION_NAMES = [
    "inner_brow_L",    # AU1 L  — medial frontalis
    "inner_brow_R",    # AU1 R
    "outer_brow_L",    # AU2 L  — lateral frontalis
    "outer_brow_R",    # AU2 R
    "brow_lower_L",    # AU4 L  — corrugator + depressor supercilii
    "brow_lower_R",    # AU4 R
    "upper_eyelid_L",  # AU5/7 L — levator palpebrae / palpebral orbicularis
    "upper_eyelid_R",  # AU5/7 R
    "cheek_L",         # AU6 L  — orbital orbicularis
    "cheek_R",         # AU6 R
    "nose",            # AU9    — LLSAN / nose bridge
    "upper_lip_L",     # AU10/12 L
    "upper_lip_R",     # AU10/12 R
    "lip_corner_L",    # AU12/15 L
    "lip_corner_R",    # AU12/15 R
    "lower_lip",       # AU16/17 — depressor labii / mentalis
    "orbicularis",     # AU22/23/24 — central mouth ring
    "jaw",             # AU26/27 — masseter / pterygoids
]

# Approximate FLAME vertex index ranges (5023-vertex topology).
# Adjust for your own mesh. These are rough centroid-based estimates;
# replace with your own segmentation mask per character.
FLAME_REGION_MASKS = {
    "inner_brow_L":   np.arange(1400, 1480),
    "inner_brow_R":   np.arange(1480, 1560),
    "outer_brow_L":   np.arange(1320, 1400),
    "outer_brow_R":   np.arange(1560, 1640),
    "brow_lower_L":   np.arange(2140, 2200),
    "brow_lower_R":   np.arange(2200, 2260),
    "upper_eyelid_L": np.arange(3620, 3720),
    "upper_eyelid_R": np.arange(3720, 3820),
    "cheek_L":        np.arange(1900, 2060),
    "cheek_R":        np.arange(2060, 2140),
    "nose":           np.arange(2600, 2760),
    "upper_lip_L":    np.arange(3100, 3200),
    "upper_lip_R":    np.arange(3200, 3300),
    "lip_corner_L":   np.arange(3000, 3060),
    "lip_corner_R":   np.arange(3060, 3100),
    "lower_lip":      np.arange(3300, 3440),
    "orbicularis":    np.arange(3440, 3560),
    "jaw":            np.arange(400,  620),
}


# ---------------------------------------------------------------------------
# Option A — direct on PCA parameters
# ---------------------------------------------------------------------------

def embed_from_pca_params(
    expression_params: np.ndarray,
    n_pre_pca: int = 50,
    umap_neighbors: int = 15,
    umap_min_dist: float = 0.05,
    tsne_perplexity: float = 50,
) -> np.ndarray:
    """
    t-SNE / UMAP directly on 382-dim expression PCA parameters.

    Pre-reduces to n_pre_pca dimensions first (t-SNE does not scale well
    beyond ~100 dims or 100k points without this step).

    Returns embedding (N, 2).
    """
    print(f"[A] Pre-PCA: {expression_params.shape[1]}D → {n_pre_pca}D ...")
    pre = PCA(n_components=n_pre_pca, random_state=0)
    X = pre.fit_transform(expression_params)
    print(f"    Explained variance: {pre.explained_variance_ratio_.sum():.3f}")
    return _reduce_2d(X, umap_neighbors, umap_min_dist, tsne_perplexity)


# ---------------------------------------------------------------------------
# Option B — decode to mesh → FACS region features → embed
# ---------------------------------------------------------------------------

def decode_to_vertices(
    expression_params: np.ndarray,
    pca_basis: np.ndarray,
    mean_face: np.ndarray,
    batch_size: int = 2000,
) -> np.ndarray:
    """
    Decode (N, 382) expression params to (N, V, 3) vertex positions.

    pca_basis : (382, V*3)   — row i is the i-th PCA component
    mean_face : (V*3,)       — flattened mean face vertices
    """
    N = len(expression_params)
    V = mean_face.shape[0] // 3
    out = np.empty((N, V, 3), dtype=np.float32)

    for start in range(0, N, batch_size):
        end = min(start + batch_size, N)
        batch = expression_params[start:end].astype(np.float32)  # (B, 382)
        verts = batch @ pca_basis.astype(np.float32) + mean_face  # (B, V*3)
        out[start:end] = verts.reshape(-1, V, 3)
        if start % (batch_size * 10) == 0:
            print(f"    decoded {end:>7,} / {N:,}")

    return out  # absolute positions (N, V, 3)


def region_displacement_features(
    positions: np.ndarray,
    region_masks: dict,
    mean_verts: np.ndarray,
) -> tuple[np.ndarray, list[str]]:
    """
    For each pose and each FACS region, compute the mean displacement
    vector relative to the mean face.

    positions  : (N, V, 3)
    mean_verts : (V, 3)

    Returns
    -------
    features     : (N, R*3)   — per-region 3-D mean displacement; magnitude
                                encodes activation strength, direction encodes type
    region_names : list[str]
    """
    delta = positions - mean_verts[None]  # (N, V, 3)
    region_names = list(region_masks.keys())
    cols = []
    for name in region_names:
        idx = region_masks[name]
        cols.append(delta[:, idx, :].mean(axis=1))  # (N, 3)
    features = np.concatenate(cols, axis=1)          # (N, R*3)
    return features, region_names


def embed_from_mesh_regions(
    expression_params: np.ndarray,
    pca_basis: np.ndarray,
    mean_face: np.ndarray,
    region_masks: dict | None = None,
    n_pre_pca: int = 0,
    umap_neighbors: int = 15,
    umap_min_dist: float = 0.05,
    tsne_perplexity: float = 50,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """
    Full Option-B pipeline.

    Returns
    -------
    embedding    : (N, 2)
    features     : (N, R*3)  raw region displacement features
    region_names : list[str]
    """
    if region_masks is None:
        region_masks = FLAME_REGION_MASKS

    V = mean_face.shape[0] // 3
    mean_verts = mean_face.reshape(V, 3)

    print("[B] Decoding poses to mesh ...")
    positions = decode_to_vertices(expression_params, pca_basis, mean_face)

    print("[B] Computing FACS region features ...")
    features, region_names = region_displacement_features(
        positions, region_masks, mean_verts
    )
    print(f"    Feature shape: {features.shape}  ({len(region_names)} regions × 3)")

    # Standardise so all regions have equal initial weight
    scaler = StandardScaler()
    X = scaler.fit_transform(features)

    # Optional pre-PCA when number of features > n_pre_pca
    if n_pre_pca and X.shape[1] > n_pre_pca:
        pre = PCA(n_components=n_pre_pca, random_state=0)
        X = pre.fit_transform(X)
        print(f"    Pre-PCA → {n_pre_pca}D, var={pre.explained_variance_ratio_.sum():.3f}")

    embedding = _reduce_2d(X, umap_neighbors, umap_min_dist, tsne_perplexity)
    return embedding, features, region_names


# ---------------------------------------------------------------------------
# Dominant-region labelling
# ---------------------------------------------------------------------------

def dominant_region_labels(
    features: np.ndarray,
    region_names: list[str],
) -> tuple[np.ndarray, np.ndarray]:
    """
    Label each pose by the FACS region with the largest displacement magnitude.

    Returns
    -------
    labels     : (N,) int   index into region_names
    magnitudes : (N, R)     per-region displacement magnitude
    """
    R = len(region_names)
    magnitudes = np.stack(
        [np.linalg.norm(features[:, i*3:(i+1)*3], axis=1) for i in range(R)],
        axis=1,
    )  # (N, R)
    labels = magnitudes.argmax(axis=1)
    return labels, magnitudes


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------

def plot_map(
    embedding: np.ndarray,
    c=None,
    cmap="tab20",
    label: str = "",
    title: str = "Expression Pose Map",
    alpha: float = 0.25,
    s: float = 1.0,
    save: str | None = None,
):
    fig, ax = plt.subplots(figsize=(11, 9))
    sc = ax.scatter(
        embedding[:, 0], embedding[:, 1],
        c=c, cmap=cmap, alpha=alpha, s=s,
        linewidths=0, rasterized=True,
    )
    if c is not None:
        plt.colorbar(sc, ax=ax, label=label, shrink=0.75, pad=0.01)
    ax.set_title(title, fontsize=13)
    ax.axis("equal")
    ax.set_xlabel("dim 0")
    ax.set_ylabel("dim 1")
    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=150, bbox_inches="tight")
    plt.show()
    return fig, ax


def plot_map_by_region(
    embedding: np.ndarray,
    features: np.ndarray,
    region_names: list[str],
    n_cols: int = 4,
    save: str | None = None,
):
    """
    Grid of subplots — one per FACS region, coloured by displacement magnitude.
    Lets you verify that each region activates in a spatially coherent part
    of the embedding.
    """
    R = len(region_names)
    n_cols = min(n_cols, R)
    n_rows = (R + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 3.5, n_rows * 3.2))
    axes = np.array(axes).flatten()

    for i, name in enumerate(region_names):
        mag = np.linalg.norm(features[:, i*3:(i+1)*3], axis=1)
        lo, hi = np.percentile(mag, [2, 98])
        sc = axes[i].scatter(
            embedding[:, 0], embedding[:, 1],
            c=mag, cmap="plasma", alpha=0.2, s=0.4,
            linewidths=0, rasterized=True, vmin=lo, vmax=hi,
        )
        axes[i].set_title(name, fontsize=7)
        axes[i].axis("off")
        plt.colorbar(sc, ax=axes[i], shrink=0.8, pad=0.02)

    for j in range(i + 1, len(axes)):
        axes[j].axis("off")

    plt.suptitle("Per-FACS-region activation on embedding", fontsize=12)
    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=150, bbox_inches="tight")
    plt.show()
    return fig


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _reduce_2d(X, umap_neighbors, umap_min_dist, tsne_perplexity):
    print(f"[embed] {X.shape} → 2D via {_REDUCER.upper()} ...")
    if _REDUCER == "umap":
        reducer = umap.UMAP(
            n_components=2,
            n_neighbors=umap_neighbors,
            min_dist=umap_min_dist,
            metric="euclidean",
            random_state=0,
            verbose=True,
        )
    else:
        reducer = TSNE(
            n_components=2,
            perplexity=tsne_perplexity,
            n_iter=1000,
            init="pca",
            random_state=0,
            verbose=1,
        )
    return reducer.fit_transform(X).astype(np.float32)


# ---------------------------------------------------------------------------
# Demo / entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # ── Synthetic data (replace with your actual arrays) ───────────────────
    rng = np.random.default_rng(0)
    N, D_expr = 20_000, 382

    # Simulate 24 FACS-like prototype poses driving the distribution
    N_proto = 24
    prototypes = rng.standard_normal((N_proto, D_expr)).astype(np.float32) * 4
    cluster_ids = rng.integers(0, N_proto, N)
    expression_params = (
        rng.standard_normal((N, D_expr)).astype(np.float32) * 0.5
        + prototypes[cluster_ids]
    )

    # ── Option A (no decoder needed) ───────────────────────────────────────
    emb_A = embed_from_pca_params(expression_params, n_pre_pca=50)

    plot_map(
        emb_A,
        c=cluster_ids.astype(float),
        cmap="tab20",
        label="Prototype cluster",
        title="Option A — t-SNE on raw PCA params",
        save="pose_map_A.png",
    )
    np.save("embedding_A.npy", emb_A)

    # ── Option B (with decoder) ─────────────────────────────────────────────
    # Fake decoder for demo: random basis and mean face (5023 FLAME vertices)
    V = 5023
    pca_basis = rng.standard_normal((D_expr, V * 3)).astype(np.float32) * 0.001
    mean_face = rng.standard_normal(V * 3).astype(np.float32)

    emb_B, feats, rnames = embed_from_mesh_regions(
        expression_params,
        pca_basis,
        mean_face,
        region_masks=FLAME_REGION_MASKS,
    )

    dom_labels, dom_mags = dominant_region_labels(feats, rnames)
    plot_map(
        emb_B,
        c=dom_labels.astype(float),
        cmap="tab20",
        label="Dominant FACS region",
        title="Option B — FACS region features",
        save="pose_map_B.png",
    )
    plot_map_by_region(emb_B, feats, rnames, save="pose_map_B_regions.png")
    np.save("embedding_B.npy", emb_B)

    print("Done. Embeddings saved to embedding_A.npy / embedding_B.npy")
