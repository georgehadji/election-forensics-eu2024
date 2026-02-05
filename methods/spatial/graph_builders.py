from typing import Iterable
import numpy as np


def normalize_rows(W: np.ndarray) -> np.ndarray:
    """
    Row-normalize a weight matrix.
    Rows with zero sum remain zero.
    """
    row_sums = W.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        Wn = np.divide(W, row_sums, where=row_sums != 0)
    return Wn


def knn_graph(coords: np.ndarray, k: int) -> np.ndarray:
    """
    Build a k-nearest-neighbors weight matrix from coordinates.

    coords: array of shape (N, 2)
    k: number of neighbors
    """
    if k <= 0:
        raise ValueError("k must be positive")

    N = coords.shape[0]
    W = np.zeros((N, N), dtype=float)

    for i in range(N):
        dists = np.linalg.norm(coords - coords[i], axis=1)
        idx = np.argsort(dists)[1 : k + 1]
        W[i, idx] = 1.0

    return normalize_rows(W)


def randomized_graph(W: np.ndarray, seed: int = 0) -> np.ndarray:
    """
    Degree-preserving randomization of an adjacency matrix.
    """
    rng = np.random.default_rng(seed)
    N = W.shape[0]

    degrees = (W > 0).sum(axis=1)
    Wr = np.zeros_like(W)

    for i in range(N):
        if degrees[i] == 0:
            continue
        idx = rng.choice(N, size=degrees[i], replace=False)
        Wr[i, idx] = 1.0

    return normalize_rows(Wr)
