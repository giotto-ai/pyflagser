"""Testing for the python bindings of the C++ flagser library."""

import numpy as np
import scipy.sparse as sp
import os
import pytest
from numpy.testing import assert_almost_equal

from pyflagser import loadflag, saveflag, flagser

flag_files = []

dirname = os.path.join(os.path.dirname(__file__), "../flagser/test")
for file in os.listdir(dirname):
    if file.endswith(".flag"):
        flag_files.append(os.path.join(dirname, file))

betti = {'e.flag': [5, 0],
         'double-d3-allzero.flag':[4, 0],
         'd.flag': [5, 0],
         'double-d3.flag': [1, 0, 5],
         'c.flag': [8, 0],
         'd7.flag': [1, 0, 0, 0, 0, 0, 1854],
         'b.flag': [4, 0],
         'd4.flag': [1, 0, 0, 9],
         'a.flag': [5, 0],
         'medium-test-data.flag': [14237, 39477, 378, 0],
         'd5.flag': [1, 0, 0, 0, 44],
         'd2.flag': [1, 1],
         'f.flag': [3, 0],
         'd4-allzero.flag': [4, 0],
         'd3.flag': [1, 0, 2],
         'd3-allzero.flag': [3, 0],
         'd10.flag': [1, 0, 0, 0, 0, 0, 0, 0, 0, 1334961]}

def test_flagio():
    for flag_file in flag_files:
        flag_matrix = loadflag(flag_file)
        _, fname_temp = os.path.split(flag_file)
        saveflag(fname_temp, flag_matrix)
        flag_matrix_temp = loadflag(fname_temp)
        os.remove(fname_temp)

        assert_almost_equal(flag_matrix.diagonal(),
                            flag_matrix_temp.diagonal())
        assert_almost_equal(np.sort(np.hstack([sp.find(flag_matrix)])),
                            np.sort(np.hstack([sp.find(flag_matrix_temp)])))

def test_flagser():
    for flag_file in flag_files:
        print(flag_file)
        flag_matrix = loadflag(flag_file)

        ret = flagser(flag_matrix)
        assert_almost_equal(ret['betti'],
                            betti[os.path.split(flag_file)[1]])
