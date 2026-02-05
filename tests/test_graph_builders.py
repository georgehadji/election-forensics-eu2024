import numpy as np
import pytest

from methods.spatial.graph_builders import normalize_rows, knn_graph, randomized_graph


def test_normalize_rows():
    W = np.array([[1, 1], [0, 0]], dtype=float)
    Wn = normalize_rows(W)

    assert np.allclose(Wn[0], [0.5, 0.5])
    assert np.allclose(Wn[1], [0.0, 0.0])


def test_knn_graph_basic():
    coords = np.array([[0, 0], [1, 0], [0, 1]], dtype=float)
    W = knn_graph(coords, k=1)

    assert W.shape == (3, 3)
    assert np.allclose(W.sum(axis=1), 1.0)


def test_knn_invalid_k():
    coords = np.array([[0, 0], [1, 0]])
    with pytest.raises(ValueError):
        knn_graph(coords, k=0)


def test_randomized_graph_preserves_shape():
    W = np.array([[0, 1], [1, 0]], dtype=float)
    Wr = randomized_graph(W, seed=42)

    assert Wr.shape == W.shape
    assert np.allclose(Wr.sum(axis=1), 1.0)
