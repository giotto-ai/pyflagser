"""Testing for the python bindings of the C++ flagser library."""

import os

import numpy as np
import pytest
import scipy.sparse as sp
from fetch_flag_files import fetch_flag_files
from numpy.testing import assert_almost_equal

from pyflagser import loadflag, saveflag


def test_super(webdl):
    flag_files = fetch_flag_files(webdl)

    @pytest.mark.parametrize('flag_file', flag_files)
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
