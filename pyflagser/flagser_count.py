"""Implementation of the python API for the cell count of the flagser C++
library."""

import numpy as np

from ._utils import _extract_unweighted_graph, _extract_weighted_graph
from flagser_pybind import implemented_filtrations
from flagser_count_pybind import compute_cell_count


def flagser_count_unweighted(adjacency_matrix, min_dimension=0,
                             max_dimension=np.inf, directed=True):
    """Compute the cell count per dimension of a directed/undirected unweighted
    flag complex.

    From an adjacency_matrix construct all cells forming its associated flag
    complex and count their number per dimension.

    Parameters
    ----------
    adjacency_matrix : 2d ndarray or scipy.sparse matrix of shape \
        (n_vertices, n_vertices), required
        Adjacency matrix of a directed/undirected unweighted graph. It is
        understood as a boolean matrix. Off-diagonal, ``0`` or ``False`` values
        denote abstent edges while non-``0`` or ``True`` values denote edges
        which are present. Diagonal values are ignored.

    min_dimension : int, optional, default: ``0``
        Minimum cell dimension to count.

    max_dimension : int or np.inf, optional, default: ``np.inf``
        Maximum cell dimension to count.

    directed : bool, optional, default: ``True``
        If ``True``, computes homology for the directed flad complex determined
        by `adjacency_matrix`. If ``False``, computes homology for the
        undirected flag complex obtained by considering all edges as
        undirected, and it is therefore sufficient (but not necessary)
        to pass an upper-triangular matrix.

    Returns
    -------
    out : list of int
        Cell count (number of simplices) per dimension greater than or equal
        than `min_dimension` and less than `max_dimension`.

    Notes
    -----
    The input graphs cannot contain self-loops, i.e. edges that start and end
    in the same vertex, therefore diagonal elements of the input adjacency
    matrix will be ignored.

    References
    ----------
    .. [1] D. Luetgehetmann, "Documentation of the C++ flagser library";
           `GitHub: luetge/flagser <https://github.com/luetge/flagser/blob/\
           master/docs/documentation_flagser.pdf>`_.

    """
    # Handle default parameters
    if max_dimension == np.inf:
        _max_dimension = -1
    else:
        _max_dimension = max_dimension

    # All edge filtrations are equivalent in the static case
    _filtration = 'max'

    # Extract vertices and edges
    vertices, edges = _extract_unweighted_graph(adjacency_matrix)

    # Call flagser_count binding
    cell_count = compute_cell_count(vertices, edges, min_dimension,
                                    _max_dimension,  directed, _filtration)

    return cell_count[min_dimension:]


def flagser_count_weighted(adjacency_matrix, max_edge_length=None,
                           min_dimension=0, max_dimension=np.inf,
                           directed=True, filtration="max"):
    """Compute the cell count per dimension of a directed/undirected
    weighted/unweighted flag complexes.

    Parameters
    ----------
    adjacency_matrix : 2d ndarray or scipy.sparse matrix of shape \
        (n_vertices, n_vertices), required
        Matrix representation of a directed/undirected weighted graph. Diagonal
        elements are vertex weights. The way zero values are handled depends on
        the format of the matrix. If the matrix is a dense ``numpy.ndarray``,
        zero values denote zero-weighted edges. If the matrix is a sparse
        ``scipy.sparse`` matrix, explicitly stored off-diagonal zeros and all
        diagonal zeros denote zero-weighted edges. Off-diagonal values that
        have not been explicitely stored are treated by ``scipy.sparse`` as
        zeros but will be understood as infinitely-valued edges, i.e., edges
        absent from the filtration.

    max_edge_weight : int or float or ``None``, optional, default: ``None``
        Maximum edge weight to be considered in the filtration. All edge
        weights greater than that value will be considered as
        infinitely-valued, i.e., absent from the filtration. If ``None``, all
        finite edge weights are considered.

    min_dimension : int, optional, default: ``0``
        Minimum cell dimension to count.

    max_dimension : int or np.inf, optional, default: ``np.inf``
        Maximum cell dimension to count.

    directed : bool, optional, default: ``True``
        If ``True``, computes persistent homology for the directed filtered
        flag complex determined by `adjacency_matrix`. If False, computes
        persistent homology for the undirected filtered flag complex obtained
        by considering all weighted edges as undirected, and it is therefore
        sufficient (but not necessary) to pass an upper-triangular matrix. When
        ``False``, if two directed edges corresponding to the same undirected
        edge are assigned different weights, only the one on the upper
        triangular part of the adjacency matrix is considered.

    filtration : string, optional, default: ``'max'``
        Algorithm determining the filtration. Warning: if an edge filtration is
        specified, it is assumed that the resulting filtration is consistent,
        meaning that the filtration value of every simplex of dimension at
        least two should evaluate to a value that is at least the maximal value
        of the filtration values of its containing edges. For performance
        reasons, this is not checked automatically.  Possible values are:
        ['dimension', 'zero', 'max', 'max3', 'max_plus_one', 'product', 'sum',
        'pmean', 'pmoment', 'remove_edges', 'vertex_degree']

    Returns
    -------
    out : list of int
        Cell count (number of simplices) per dimension greater than or equal
        than `min_dimension` and less than `max_dimension`.

    Notes
    -----
    The input graphs cannot contain self-loops, i.e. edges that start and end
    in the same vertex, therefore diagonal elements of the input adjacency
    matrix store vertex weights.

    References
    ----------
    .. [1] D. Luetgehetmann, "Documentation of the C++ flagser library";
           `GitHub: luetge/flagser <https://github.com/luetge/flagser/blob/\
           master/docs/documentation_flagser.pdf>`_.

    """
    # Handle default parameters
    if max_dimension == np.inf:
        _max_dimension = -1
    else:
        _max_dimension = max_dimension

    if filtration not in implemented_filtrations:
        raise ValueError("Filtration not recognized. Available filtrations "
                         "are ", implemented_filtrations)

    # Extract vertices and edges weights
    vertices, edges = _extract_weighted_graph(adjacency_matrix,
                                              max_edge_length)

    # Call flagser_count binding
    cell_count = compute_cell_count(vertices, edges, min_dimension,
                                  _max_dimension, directed, filtration)

    return cell_count[min_dimension:]
