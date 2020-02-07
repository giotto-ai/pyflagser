"""Testing for the python bindings of the C++ flagser library."""

import numpy as np
import scipy.sparse as sp
import pytest
import os
from numpy.testing import assert_almost_equal

from pyflagser import loadflag, saveflag

flag_files = []

dirname = os.path.join(os.path.dirname(__file__), "../../flagser/test")
for file in os.listdir(dirname):
    if file.endswith(".flag"):
        flag_files.append(os.path.join(dirname, file))


@pytest.mark.parametrize("flag_file",
                         [(flag_file) for flag_file in flag_files])
def test_flagio(flag_file):
    flag_matrix = loadflag(flag_file)
    _, fname_temp = os.path.split(flag_file)
    saveflag(fname_temp, flag_matrix)
    flag_matrix_temp = loadflag(fname_temp)
    os.remove(fname_temp)

    assert_almost_equal(flag_matrix.diagonal(),
                        flag_matrix_temp.diagonal())
    assert_almost_equal(np.sort(np.hstack([sp.find(flag_matrix)])),
                        np.sort(np.hstack([sp.find(flag_matrix_temp)])))
