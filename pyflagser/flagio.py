"""Implementation of input/output functions for .flag files"""

import numpy as np
import scipy.sparse as sp


def loadflag(fname, fmt=None, dtype=None):
    """
    Load a flag matrix from a ``.flag`` file.

    Parameters
    ----------
    fname : file, str, or pathlib.Path
        Filename of extension``.flag``.
    fmt : {"dense", "dia", "csr", "csc", "lil", ...}, optional
        Matrix format of the result.  By default (fmt=None) an
        appropriate sparse matrix format is returned.  This choice is
        subject to change.
    dtype : data-type, optional (default: ``np.float``)
        Data-type of the resulting array.

    Returns
    -------
    flag_matrix : matrix of format `format`
        Adjacency matrix for the flag complex contained in ``fname``.
    """
    with open(fname, 'r') as f:
        next(f)
        line = f.readline().strip()
        vertices = list(map(float, line.split(' ')))
        flag_matrix = sp.lil_matrix((len(vertices), len(vertices)),
                                    dtype=dtype)
        flag_matrix.setdiag(vertices)

        for line in f.readlines()[1:]:
            edge = line.strip().split(' ')
            flag_matrix[int(float(edge[0])), int(float(edge[1]))] = \
                float(edge[2])

    return flag_matrix.asformat(fmt)


def saveflag(fname, flag_matrix):
    """
    Construct a sparse matrix from diagonals.

    Parameters
    ----------
    flag_matrix : numpy 2d array or scipy sparse matrix
        Adjacency matrix for the flag complex contained in ``fname``.
    fname : file, str, or pathlib.Path
        Filename of extension``.flag``.
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
