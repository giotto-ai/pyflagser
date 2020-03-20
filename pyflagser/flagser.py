"""Implementation of the python API for the flagser C++ library."""

import numpy as np
import scipy.sparse as sp
from flagser_pybind import compute_homology, implemented_filtrations


def flagser(flag_matrix, min_dimension=0, max_dimension=np.inf, directed=True,
            filtration="max", coeff=2, approximation=-1):
    """Compute persistent homology of a directed/undirected
    weighted/unweighted flag complexes.

    Important: the input graphs cannot contain self-loops, i.e. edges
    that start and end in the same vertex, therefore diagonal elements
    of the flag matrix store vertex weights.

    Parameters
    ----------
    flag_matrix : ndarray or scipy.sparse matrix, required
        Matrix representation of a directed/undirected weighted/unweighted
        graph. Diagonal elements are vertex weights.

    min_dimension : int, optional, default: ``0``
        Minimum homology dimension.

    max_dimension : int or np.inf, optional, default: ``np.inf``
        Maximum homology dimension.

    directed : bool, optional, default: ``True``
        If true, computes the directed flag complex. Otherwise, it computes
        the undirected flag complex.

    filtration : string, optional, default: ``'max'``
        Algorithm determining the filtration. Warning: if an edge filtration is
        specified, it is assumed that the resulting filtration is consistent,
        meaning that the filtration value of every simplex of dimension at
        least two should evaluate to a value that is at least the maximal value
        of the filtration values of its containing edges. For performance
        reasons, this is not checked automatically.  Possible values are:
        ['dimension', 'zero', 'max', 'max3', 'max_plus_one', 'product', 'sum',
        'pmean', 'pmoment', 'remove_edges', 'vertex_degree']

    coeff : int, optional, default: ``2``
        Compute homology with coefficients in the prime field
        :math:`\\mathbb{F}_p = \\{ 0, \\ldots, p - 1 \\}` where
        :math:`p` equals `coeff`.

    approximation : int, optional, default: ``-1``
        Skip all cells creating columns in the reduction matrix with more than
        this number of entries. Use this for hard problems; a good value is
        often ``100,000``. Increase for higher precision, decrease for faster
        computation. A negative value computes highest possible precision.

    Returns
    -------
    out : dict of list
        A dictionary holding the results of the flagser computation. Each
        value is a list of length `max_dimension` - `min_dimension` + 1. The
        key-value pairs in `out` are as follows:

        - ``'dgms'``: list of ndarray of shape ``(n_pairs, 2)``
          A list of persistence diagrams, one for each dimension greater
          than or equal than `min_dimension` and less than `max_dimension`.
          Each diagram is an ndarray of size (n_pairs, 2) with the first
          column representing the birth time and the second column
          representing the death time of each pair.
        - ``'cell_count'``: list of int
          Cell count per dimension greater than or equal than
          `min_dimension` and less than `max_dimension`.
        - ``'betti'``: list of int
          Betti number per dimension greater than or equal than
          `min_dimension` and less than `max_dimension`.
        - ``'euler'``: list of int
          Euler characteristic per dimension greater than or equal than
          `min_dimension` and less than `max_dimension`.

    Notes
    -----
    For more details, please refer to the `flagser documentation \
    <https://github.com/luetge/flagser/blob/master/docs/\
    documentation_flagser.pdf>`_.

    """
    vertices = np.asarray(flag_matrix.diagonal()).copy()

    if not approximation:
        approximation = -1

    edges = sp.coo_matrix(flag_matrix, copy=True)
    edges.setdiag(np.nan)

    mask_out_of_diag = np.logical_not(np.isnan(edges.data))

    if edges.dtype == bool:
        edges = np.vstack([edges.row[mask_out_of_diag],
                           edges.col[mask_out_of_diag]]).T[:, :2]
    else:
        edges = np.vstack([edges.row[mask_out_of_diag],
                           edges.col[mask_out_of_diag],
                           edges.data[mask_out_of_diag]]).T

    if max_dimension == np.inf:
        _max_dimension = -1
    else:
        _max_dimension = max_dimension

    if filtration not in implemented_filtrations:
        print('Unrecognized {} filtration, using max'.format(filtration))
        print('Available algorithms : {}'.format(implemented_filtrations))
        filtration = "max"

    homology = compute_homology(vertices, edges, min_dimension, _max_dimension,
                                directed, coeff, approximation, filtration)
    # Creating dictionary of return values
    out = dict()
    out['dgms'] = [np.asarray(homology[0].get_persistence_diagram()[i])
                   for i in range(len(homology[0].get_persistence_diagram()))]
    out['cell_count'] = homology[0].get_cell_count()
    out['betti'] = homology[0].get_betti_numbers()
    out['euler'] = homology[0].get_euler_characteristic()

    return out
