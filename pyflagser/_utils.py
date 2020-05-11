"""Utility functions for flag matrices"""

import numpy as np


def _extract_static_weights(flag_matrix):
    # Extract vertices weights
    vertices = np.zeros(flag_matrix.diagonal().shape, dtype=np.bool)

    # Extract edges indices and weights
    if isinstance(flag_matrix, np.ndarray):
        row, column = np.indices(flag_matrix.shape)
        row, column = row.flat, column.flat

        # Off-diagonal mask
        mask = np.logical_not(np.eye(vertices.shape[0], dtype=bool).flat)

        # Data mask
        mask = np.logical_and(mask, flag_matrix.flat != 0)

    else:
        # Convert to COO format to extract row and column arrays
        fmt = flag_matrix.getformat()
        flag_matrix = flag_matrix.tocoo()
        row, column = flag_matrix.row, flag_matrix.col
        data = np.asarray(flag_matrix.data, dtype=np.bool)
        flag_matrix = flag_matrix.asformat(fmt)

        # Off-diagonal mask
        mask = np.ones(row.shape[0], dtype=np.bool)
        mask[np.arange(row.shape[0])[row == column]] = False

        # Data mask
        mask = np.logical_and(mask, data)

    edges = np.vstack([row[mask], column[mask]]).T[:, :2]
    return vertices, edges


def _extract_persistence_weights(flag_matrix, max_edge_length):
    # Extract vertices weights
    vertices = np.asarray(flag_matrix.diagonal())

    # Extract edges indices and weights
    if isinstance(flag_matrix, np.ndarray):
        row, column = np.indices(flag_matrix.shape)
        row, column = row.flat, column.flat
        data = flag_matrix.flat

        # Off-diagonal mask
        mask = np.logical_not(np.eye(vertices.shape[0], dtype=bool).flat)
    else:
        # Convert to COO format to extract row column, and data arrays
        fmt = flag_matrix.getformat()
        flag_matrix = flag_matrix.tocoo()
        row, column = flag_matrix.row, flag_matrix.col
        data = flag_matrix.data
        flag_matrix = flag_matrix.asformat(fmt)

        # Off-diagonal mask
        mask = np.ones(row.shape[0], dtype=np.bool)
        mask[np.arange(row.shape[0])[row == column]] = False

    # Infinite weights mask
    if max_edge_length is not None:
        mask = np.logical_and(mask, data <= max_edge_length)

    edges = np.vstack([row[mask], column[mask], data[mask]]).T

    return vertices, edges
