"""Testing for the python bindings of the C++ flagser library."""

import os

from numpy.testing import assert_almost_equal

from pyflagser import loadflag, flagser

betti = {
    'a.flag': [1, 2, 0],
    'b.flag': [1, 0, 0],
    'c.flag': [1, 5],
    'd.flag': [1, 0, 1],
    'e.flag': [1, 0, 0, 0],
    'f.flag': [1, 0, 0],
    'd2.flag': [1, 1],
    'd3.flag': [1, 0, 2],
    'd3-allzero.flag': [1, 0, 2],
    'double-d3.flag': [1, 0, 5],
    'double-d3-allzero.flag': [1, 0, 5],
    'd4.flag': [1, 0, 0, 9],
    'd4-allzero.flag': [1, 0, 0, 9],
    'd5.flag': [1, 0, 0, 0, 44],
    'd7.flag': [1, 0, 0, 0, 0, 0, 1854],
    'medium-test-data.flag': [14237, 39477, 378, 0],
    'd10.flag': [1, 0, 0, 0, 0, 0, 0, 0, 0, 1334961],
}


def test_flagser(flag_file):
    betti_exp = betti[os.path.split(flag_file)[1]]
    flag_matrix = loadflag(flag_file)
    betti_res = flagser(flag_matrix)['betti']
    assert_almost_equal(betti_res, betti_exp)
