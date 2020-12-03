"""Implementation of the python API for the cell count of the flagser C++
library."""

from ._utils import _extract_unweighted_graph, _extract_weighted_graph
from .modules.flagser_count_pybind import compute_cell_count


def flagser_count_unweighted(adjacency_matrix, directed=True):
    """Compute the cell count per dimension of a directed/undirected unweighted
    flag complex.

    From an adjacency matrix construct all cells forming its associated flag
    complex and compute their number per dimension.

    Parameters
    ----------
    adjacency_matrix : 2d ndarray or scipy.sparse matrix, required
        Adjacency matrix of a directed/undirected unweighted graph. It is
        understood as a boolean matrix. Off-diagonal, ``0`` or ``False`` values
        denote absent edges while non-``0`` or ``True`` values denote edges
        which are present. Diagonal values are ignored.

    directed : bool, optional, default: ``True``
        If ``True``, computes homology for the directed flag complex determined
        by `adjacency_matrix`. If ``False``, computes homology for the
        undirected flag complex obtained by considering all edges as
        undirected, and it is therefore sufficient (but not necessary)
        to pass an upper-triangular matrix.

    Returns
    -------
    out : list of int
        Cell counts (number of simplices), per dimension greater than or equal
        to `min_dimension` and less than `max_dimension`.

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
    # Extract vertices and edges
    vertices, edges = _extract_unweighted_graph(adjacency_matrix)

    # Call flagser_count binding
    cell_count = compute_cell_count(vertices, edges, directed)

    return cell_count


def flagser_count_weighted(adjacency_matrix, max_edge_weight=None,
                           directed=True):
    """Compute the cell count per dimension of a directed/undirected
    filtered flag complex.

    From an adjacency matrix construct a filtered flag complex as a sequence of
    its cells associated to their filtration values and compute the number of
    cells per dimension at the end of the filtration.

    Parameters
    ----------
    adjacency_matrix : 2d ndarray or scipy.sparse matrix, required
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

    directed : bool, optional, default: ``True``
        If ``True``, computes persistent homology for the directed filtered
        flag complex determined by `adjacency_matrix`. If ``False``, computes
        persistent homology for the undirected filtered flag complex obtained
        by considering all weighted edges as undirected, and if two directed
        edges corresponding to the same undirected edge are explicitly assigned
        different weights and neither exceeds `max_edge_weight`, only the one
        in the upper triangular part of the adjacency matrix is considered.
        Therefore:

        - if `max_edge_weight` is ``numpy.inf``, it is sufficient to pass a
          (dense or sparse) upper-triangular matrix;
        - if `max_edge_weight` is finite, it is recommended to pass either a
          symmetric dense matrix, or a sparse upper-triangular matrix.

    Returns
    -------
    out : list of int
        Cell counts (number of simplices) at filtration value
        `max_edge_weight`, per dimension.

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
    # Extract vertices and edges weights
    vertices, edges = _extract_weighted_graph(adjacency_matrix,
                                              max_edge_weight)

    # Call flagser_count binding
    cell_count = compute_cell_count(vertices, edges, directed)

    return cell_count
