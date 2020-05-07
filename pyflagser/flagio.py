"""Implementation of input/output functions for .flag files"""

import warnings
import numpy as np
import scipy.sparse as sp

from ._utils import _extract_static_weights, _extract_persistence_weights


def load_static_flag(fname, fmt='csr', dtype=np.bool):
    """Load a ``.flag`` file, and return a connectivity or an adjacency matrix.

    Parameters
    ----------
    fname : file, str, or pathlib.Path, required
        Filename of extension ``.flag`` containing the information of a flag
        matrix.

    fmt : {'dense', 'dia', 'csr', 'csc', 'lil', ...}, optional, default: 'csr'
        Matrix format of the result. By default, a CSR sparse matrix is
        returned. Keep in mind that some matrix formats do not track zero
        values.

    dtype : data-type, optional, default: ``np.bool``
        Data-type of the resulting array.

    Returns
    -------
    flag_matrix : matrix of format `fmt`
        Connectivity matrix of a directed/undirected weighted/unweighted graph.
        Diagonal elements are vertex weights.

    """
    with open(fname, 'r') as f:
        next(f)
        line = f.readline().strip()
        vertices = list(map(dtype, line.split(' ')))
        flag_matrix = sp.csr_matrix((len(vertices), len(vertices)),
                                    dtype=dtype)
        # Silence sparse warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', sp.SparseEfficiencyWarning)
            flag_matrix.setdiag(vertices)

            for line in f.readlines()[1:]:
                edge = line.strip().split(' ')
                flag_matrix[int(float(edge[0])), int(float(edge[1]))] = 1

    return flag_matrix.asformat(fmt)


def load_persistence_flag(fname, fmt='csr', dtype=np.float,
                          infinity_value=None):
    """Load a ``.flag`` file, and return a connectivity or an adjacency matrix.

    Parameters
    ----------
    fname : file, str, or pathlib.Path, required
        Filename of extension ``.flag`` containing the information of a flag
        matrix.

    fmt : {'dense', 'dia', 'csr', 'csc', 'lil', ...}, optional, default: 'csr'
        Matrix format of the result. By default, a CSR sparse matrix is
        returned. Keep in mind that some matrix formats do not track zero
        values.

    dtype : data-type, optional, default: ``np.float``
        Data-type of the resulting array.

    infinity_value: int or float or None, optional, default: ``None``
        Value to use to denote an absence of edge. It is only useful when `fmt`
        is `'dense'`. If ``None``, it is set to the maximum value allowed by
        `dtype`.

    Returns
    -------
    flag_matrix : matrix of format `fmt`
        Matrix representation of a directed/undirected weighted/unweighted
        graph. Diagonal elements are vertex weights.

    """
    # Warn if dtype is bool
    if np.issubdtype(dtype, np.bool_):
        warnings.warn("dtype is a bool type, you may want to use "
                      " the load_static_flag function instead.")

    # Handle default parameter
    if infinity_value is None:
        if fmt != 'dense':
            _infinity_value = None
        else:
            # Get the maximum value depending on flag_matrix.dtype
            if np.issubdtype(dtype, np.integer):
                _infinity_value = np.iinfo(dtype).max
            elif np.issubdtype(dtype, np.float_):
                _infinity_value = np.inf
            else:
                _infinity_value = 0
    else:
        if fmt != 'dense':
            warnings.warn("infinty_value has been specified with a fmt that "
                          "is not 'dense' and will be ignored.")
            _infinity_value = None
        else:
            _infinity_value = infinity_value

    with open(fname, 'r') as f:
        next(f)
        line = f.readline().strip()
        vertices = np.array(line.split(' '), dtype=dtype)

        if fmt == 'dense':
            flag_matrix = np.asarray(
                _infinity_value
                * np.ones((len(vertices), len(vertices))), dtype=dtype)
            flag_matrix[np.eye(flag_matrix.shape, dtype=np.bool)] = vertices
        else:
            flag_matrix = sp.csr_matrix((len(vertices), len(vertices)),
                                        dtype=dtype)

        # Silence sparse warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', sp.SparseEfficiencyWarning)
            flag_matrix.setdiag(vertices)

            for line in f.readlines()[1:]:
                edge = line.strip().split(' ')
                print(edge)
                flag_matrix[int(float(edge[0])), int(float(edge[1]))] = \
                    float(edge[2])

    return flag_matrix.asformat(fmt)


def save_static_flag(fname, flag_matrix):
    """Save a directed/undirected graph connectivity matrix into a ``.flag``
    file.

    Parameters
    ----------
    fname : file, str, or pathlib.Path, required
        Filename of extension ``.flag``.

    flag_matrix : 2d ndarray or scipy sparse matrix, required
        Matrix representation of a directed/undirected unweighted graph. It is
        understood as a boolean matrix. Diagonal elements are vertex weights
        with non-``0`` or ``True`` values corresponding to ``True`` values and
        ``0`` or ``False`` values corresponding to ``False`` values.
        Off-diagonal, ``0`` or ``False`` values denote edge absence while
        non-``0`` or ``True`` values denote edges presence.

    """
    # Extract vertices and edges weights
    vertices, edges = _extract_static_weights(flag_matrix)

    with open(fname, 'w') as f:
        np.savetxt(f, vertices, delimiter=' ', comments='', header='dim 0',
                   fmt='%.18e')
        np.savetxt(f, edges, comments='', header='dim 1', fmt='%i %i')


def save_persistence_flag(fname, flag_matrix, max_edge_length=None):
    """Save a directed/undirected weighted/unweighted graph adjacency matrix
    into a ``.flag`` file.

    Parameters
    ----------
    fname : file, str, or pathlib.Path, required
        Filename of extension ``.flag``.

    flag_matrix : 2d ndarray or scipy sparse matrix, required
        Matrix representation of a directed/undirected weighted/unweighted
        graph. Diagonal elements are vertex weights. The way zero values are
        handled depends on the format of the matrix. If the matrix is a dense
        ``np.ndarray``, zero values denote zero-weighted edges. If the matrix
        is a sparse ``scipy.sparse`` matrix, explicitely stored off-diagonal
        zeros  and all diagonal zeros denote zero-weighted edges. Off-diagonal
        values that have not been explicitely stored are treated by
        ``scipy.sparse`` as zeros but will be understood as infinitely-valued
        edges, i.e., edges absent from the filtration.

    max_edge_length : int or float or ``None``, optional, default: ``None``
        Maximum edge length to be considered in the filtration. All edge
        weights greater than that value will be considered as
        infinitely-valued, i.e., absent from the filtration.

    """
    # Handle default parameter
    if max_edge_length is None:
        # Get the maximum value depending on flag_matrix.dtype
        if np.issubdtype(flag_matrix.dtype, np.integer):
            _max_edge_length = np.iinfo(flag_matrix.dtype).max
        elif np.issubdtype(flag_matrix.dtype, np.float_):
            _max_edge_length = np.inf
        else:
            _max_edge_length = None
    else:
        _max_edge_length = max_edge_length

    # Extract vertices and edges weights
    vertices, edges = _extract_persistence_weights(flag_matrix,
                                                   _max_edge_length)

    with open(fname, 'w') as f:
        np.savetxt(f, vertices.reshape((1, -1)), delimiter=' ', comments='',
                   header='dim 0', fmt='%.18e')
        np.savetxt(f, edges, comments='', header='dim 1', fmt='%i %i %.18e')
