"""Implementation of the python API for the flagser C++ library."""

import scipy.sparse as sp
import numpy as np
from flagser_pybind import compute_homology


def flagser(flag_matrix, max_dimension=2, directed=True, coeff=2):
    """Compute persistent homology for directed flag complexes from
    the flag matrix of a directed/undirected weighted/unweighted
    graph.

    Important: the input graphs cannot contain self-loops. i.e. edges
    that start and end in the same vertex, therefore diagonal elements
    of the flag matrix store vertices weight.

    Parameters
    ----------
    flag_matrix : ndarray or scipy.sparse matrix
        Matrix representation of a directed/undirected
        weighted/unweighted graph. Diagonal elements contain vertices
        weight.
    max_dimension : int, optional (default: 2)
        Maximum dimension.
    directed : bool, optional (default:``True``)
        If true, computes the directed flag complex. Otherwise it
        computes the undirected flag complex.
    coeff : int, optional (default: 2)
        Compute homology with coefficients in the prime field
        :math:`\\mathbb{F}_p = \\{ 0, \\ldots, p - 1 \\}` where
        :math:`p` equals `coeff`.

    Returns
    -------
    out: dict of list of ``max_dimension`` elements
        A dictionnary holding all of the results of the flagser
    computation as follows:
    {
     'dgms': list of ``max_dimension`` ndarrays of shape (n_pairs, 2)
        A list of persistence diagrams, one for each dimension less
        than maxdim. Each diagram is an ndarray of size (n_pairs, 2)
        with the first column representing the birth time and the
        second column representing the death time of each pair.
     'cell_count': list of ``max_dimension`` ints
        Cell count per dimension
     'betti': list of ``max_dimension`` ints
        Betti number per dimension.
     'euler': int
        Euler characteristic.
    }
    """
    vertices = np.asarray(flag_matrix.diagonal()).copy()
    edges = flag_matrix.tolil()
    edges.setdiag(0)

    if edges.dtype == bool:
        edges = np.hstack([sp.find(edges)]).T[:, :2]
    else:
        edges = np.hstack([sp.find(edges)]).T

    homology = compute_homology(vertices, edges, max_dimension,
                                directed, coeff)
    # Creating dictionary of returns values
    ret = {}
    ret['dgms'] = homology[0].get_persistence_diagram()
    ret['cell_count'] = homology[0].get_cell_count()
    ret['betti'] = homology[0].get_betti_numbers()
    ret['euler'] = homology[0].get_euler_characteristic()

    return ret
