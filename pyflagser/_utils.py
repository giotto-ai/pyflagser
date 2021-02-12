"""Utility functions for adjacency matrices."""

import warnings

import numpy as np


def _extract_unweighted_graph(adjacency_matrix):
    input_shape = adjacency_matrix.shape
    # Warn if dense and not square
    if isinstance(adjacency_matrix, np.ndarray) and \
            (input_shape[0] != input_shape[1]):
        warnings.warn("Dense `adjacency_matrix` should be square.")

    # Extract vertices and give them weight one
    n_vertices = max(input_shape)
    vertices = np.ones(n_vertices, dtype=float)

    # Extract edge indices
    if isinstance(adjacency_matrix, np.ndarray):
        # Off-diagonal mask
        mask = np.logical_not(np.eye(input_shape[0], M=input_shape[1],
                                     dtype=bool))

        # Data mask
        mask = np.logical_and(adjacency_matrix, mask)

        edges = np.argwhere(mask)
    else:
        edges = np.argwhere(adjacency_matrix)

        # Remove diagonal elements a posteriori
        edges = edges[edges[:, 0] != edges[:, 1]]

    # Assign weight one
    edges = np.insert(edges, 2, 1, axis=1)

    return vertices, edges


def _extract_weighted_graph(adjacency_matrix, max_edge_weight):
    input_shape = adjacency_matrix.shape
    # Warn if dense and not square
    if isinstance(adjacency_matrix, np.ndarray) and \
            (input_shape[0] != input_shape[1]):
        warnings.warn("Dense `adjacency_matrix` should be square.")

    # Extract vertex weights
    n_vertices = max(input_shape)
    vertices = np.zeros(n_vertices, dtype=adjacency_matrix.dtype)
    vertices[:min(input_shape)] = adjacency_matrix.diagonal()

    # Extract edge indices and weights
    if isinstance(adjacency_matrix, np.ndarray):
        row, column = np.indices(adjacency_matrix.shape)
        row, column = row.flat, column.flat
        data = adjacency_matrix.flat

        # Off-diagonal mask
        mask = np.logical_not(np.eye(input_shape[0], M=input_shape[1],
                                     dtype=bool).flat)
    else:
        # Convert to COO format to extract row, column, and data arrays
        fmt = adjacency_matrix.getformat()
        adjacency_matrix = adjacency_matrix.tocoo()
        row, column = adjacency_matrix.row, adjacency_matrix.col
        data = adjacency_matrix.data
        adjacency_matrix = adjacency_matrix.asformat(fmt)

        # Off-diagonal mask
        mask = row != column

    # Mask infinite or thresholded weights
    if np.issubdtype(adjacency_matrix.dtype, np.floating):
        if (max_edge_weight is None) or np.isposinf(max_edge_weight):
            mask = np.logical_and(mask, np.isfinite(data))
        else:
            mask = np.logical_and(mask, data <= max_edge_weight)
    elif max_edge_weight is not None:
        mask = np.logical_and(mask, data <= max_edge_weight)

    edges = np.c_[row[mask], column[mask], data[mask]]

    return vertices, edges
