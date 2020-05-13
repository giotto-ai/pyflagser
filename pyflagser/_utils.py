"""Utility functions for flag matrices"""

import numpy as np


def _extract_unweighted_graph(adjacency_matrix):
    # Extract vertices and give them weight one
    vertices = np.ones(adjacency_matrix.shape[0], dtype=np.float)

    # Extract edges indices
    if isinstance(adjacency_matrix, np.ndarray):
        # Off-diagonal mask
        mask = np.logical_not(np.eye(adjacency_matrix.shape[0], dtype=bool))

        # Data mask
        mask = np.logical_and(adjacency_matrix, mask)

        edges = np.argwhere(mask)
    else:
        # Convert to COO format to extract row and column arrays
        # fmt = adjacency_matrix.getformat()
        # adjacency_matrix = adjacency_matrix.tocoo()
        # row, column = adjacency_matrix.row, adjacency_matrix.col
        # data = np.asarray(adjacency_matrix.data, dtype=np.bool)
        # adjacency_matrix = adjacency_matrix.asformat(fmt)

        # # Off-diagonal mask
        # mask = np.ones(row.shape[0], dtype=np.bool)
        # mask[np.arange(row.shape[0])[row == column]] = False

        # # Data mask
        # mask = np.logical_and(mask, data)

        # edges = np.vstack([row[mask], column[mask]]).T[:, :2]

        # Data mask
        mask = np.stack(np.nonzero(adjacency_matrix)).T

        # Removes diagonal elements a posteriori
        edges = mask[mask[:, 0] != mask[:, 1]]

    # Assign weight one
    edges = np.hstack([edges, np.ones(edges[:, [0]].shape, dtype=np.int)])

    return vertices, edges


def _extract_weighted_graph(adjacency_matrix, max_edge_length):
    # Extract vertices weights
    vertices = np.asarray(adjacency_matrix.diagonal())

    # Extract edges indices and weights
    if isinstance(adjacency_matrix, np.ndarray):
        row, column = np.indices(adjacency_matrix.shape)
        row, column = row.flat, column.flat
        data = adjacency_matrix.flat

        # Off-diagonal mask
        mask = np.logical_not(np.eye(vertices.shape[0], dtype=bool).flat)
    else:
        # Convert to COO format to extract row column, and data arrays
        fmt = adjacency_matrix.getformat()
        adjacency_matrix = adjacency_matrix.tocoo()
        row, column = adjacency_matrix.row, adjacency_matrix.col
        data = adjacency_matrix.data
        adjacency_matrix = adjacency_matrix.asformat(fmt)

        # Off-diagonal mask
        mask = np.ones(row.shape[0], dtype=np.bool)
        mask[np.arange(row.shape[0])[row == column]] = False

    # Infinite weights mask
    if max_edge_length is not None:
        mask = np.logical_and(mask, data <= max_edge_length)

    edges = np.vstack([row[mask], column[mask], data[mask]]).T

    return vertices, edges
