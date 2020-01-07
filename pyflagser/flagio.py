"""Implementation of input/output functions for .flag files"""

import numpy as np
import scipy.sparse as sp

def loadflag(fname, format=None, dtype=None):
    """
    Load a flag matrix from a ``.flag`` file.

    Parameters
    ----------
    fname : file, str, or pathlib.Path
        Filename of extension``.flag``.
    format : {"dense", "dia", "csr", "csc", "lil", ...}, optional
        Matrix format of the result.  By default (format=None) an
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
        for line in f.readlines():
            line = line.strip()
            print(line)


    with open(fname, 'r') as f:
        next(f)
        line = f.readline().strip()
        vertices = list(map(float, line.split(' ')))
        flag_matrix = sp.lil_matrix((len(vertices), len(vertices)),
                                    dtype=dtype)
        flag_matrix.setdiag(vertices)

        for line in f.readlines()[3:]:
            edge = line.strip().split(' ')
            flag_matrix[int(float(edge[0])), int(float(edge[1]))] = float(edge[2])

        # edges = []
        # for line in f.readlines()[3:]:
        #     line = line.strip()
        #     edges.append(list(map(float, line.split(' '))))

    # edges = np.asarray(edges)
    # if flag_matrix.shape[1] == 3:
    #     flag_matrix[flag_matrix[:, 2] == 0, 2] = np.inf
    #     flag_matrix = sp.coo_matrix((flag_matrix[:, 2].astype(np.float),
    #                                  (flag_matrix[:, 0].astype(np.int),
    #                                   flag_matrix[:, 1].astype(np.int))),
    #                                 shape=(vertices.shape[0],
    #                                        vertices.shape[0]),
    #                                 dtype=dtype)
    # else:
    #     flag_matrix = sp.lil_matrix((np.ones(len(flag_matrix), dtype=dtype),
    #                                  (flag_matrix[:, 0].astype(np.int),
    #                                   flag_matrix[:, 1].astype(np.int))),
    #                                 shape=(vertices.shape[0],
    #                                        vertices.shape[0]),
    #                                 dtype=dtype)
    # flag_matrix.setdiag(vertices)
    return flag_matrix

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
                   comments='', header='dim 0')

        if flag_matrix.dtype == bool:
            np.savetxt(f, np.hstack([sp.find(flag_matrix)]).T[:, :2],
                       comments='', header='dim 1')
        else:
            np.savetxt(f, np.hstack([sp.find(flag_matrix)]).T,
                       comments='', header='dim 1')
