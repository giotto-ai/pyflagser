"""Testing for the python bindings of the C++ flagser library."""

import os

import numpy as np
import scipy.sparse as sp
from numpy.testing import assert_almost_equal

from pyflagser import loadflag, saveflag


def test_flagio(flag_file):
    flag_matrix = loadflag(flag_file)
    fname_temp = os.path.split(flag_file)[1]
    saveflag(fname_temp, flag_matrix)
    flag_matrix_temp = loadflag(fname_temp)
    os.remove(fname_temp)

    assert_almost_equal(flag_matrix.diagonal(),
                        flag_matrix_temp.diagonal())
    assert_almost_equal(np.sort(np.hstack([sp.find(flag_matrix)])),
                        np.sort(np.hstack([sp.find(flag_matrix_temp)])))
