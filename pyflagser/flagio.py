"""Implementation of input/output functions for .flag files"""

import numpy as np
import scipy.sparse as sp


def loadflag(fname, fmt='csr', dtype=None):
    """Load a ``.flag`` file, and return a matrix representation.

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

    Returns
    -------
    flag_matrix : matrix of format `fmt`
        Matrix representation of a directed/undirected weighted/unweighted
        graph. Diagonal elements are vertex weights.

    """
    with open(fname, 'r') as f:
        next(f)
        line = f.readline().strip()
        vertices = list(map(float, line.split(' ')))
        flag_matrix = sp.csr_matrix((len(vertices), len(vertices)),
                                    dtype=dtype)
        flag_matrix.setdiag(vertices)

        for line in f.readlines()[1:]:
            edge = line.strip().split(' ')
            flag_matrix[int(float(edge[0])), int(float(edge[1]))] = \
                float(edge[2])

    return flag_matrix.asformat(fmt)


def saveflag(fname, flag_matrix):
    """Save the matrix representation of a filtered flag complex into a
    ``.flag`` file.

    Parameters
    ----------
    fname : file, str, or pathlib.Path, required
        Filename of extension ``.flag``.

    flag_matrix : 2d ndarray or scipy sparse matrix, required
        Matrix representation of a directed/undirected weighted/unweighted
        graph. Diagonal elements are vertex weights.

    """
    with open(fname, 'w') as f:
        np.savetxt(f, flag_matrix.diagonal().reshape((1, -1)), delimiter=' ',
                   comments='', header='dim 0', fmt='%.18e')

        if flag_matrix.dtype == bool:
            np.savetxt(f, np.hstack([sp.find(flag_matrix)]).T[:, :2],
                       comments='', header='dim 1', fmt='%i %i')
        else:
            np.savetxt(f, np.hstack([sp.find(flag_matrix)]).T,
                       comments='', header='dim 1', fmt='%i %i %.18e')
