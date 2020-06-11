"""Testing for the python bindings of the C++ flagser library."""

import os

from numpy.testing import assert_almost_equal

from pyflagser import load_unweighted_flag, load_weighted_flag, \
    flagser_count_unweighted, flagser_count_weighted


cell_count = {
    'a.flag': [5, 7, 1],
    'b.flag': [4, 6, 3],
    'c.flag': [8, 12],
    'd.flag': [5, 9, 6],
    'e.flag': [5, 9, 7, 2],
    'f.flag': [3, 5, 3],
    'd2.flag': [2, 2],
    'd3.flag': [3, 6, 6],
    'd3-allzero.flag': [3, 6, 6],
    'double-d3.flag': [4, 10, 12],
    'double-d3-allzero.flag': [4, 10, 12],
    'd4.flag': [4, 12, 24, 24],
    'd4-allzero.flag': [4, 12, 24, 24],
    'd5.flag': [5, 20, 60, 120, 120],
    'd7.flag': [7, 42, 210, 840, 2520, 5040, 5040],
    'medium-test-data.flag': [31346, 68652, 12694, 250],
    'd10.flag': [10, 90, 720, 5040, 30240, 151200, 604800,
                 1814400, 3628800, 3628800],
}


def test_unweighted(flag_file):
    adjacency_matrix = load_unweighted_flag(flag_file, fmt='dense')
    cell_count_exp = cell_count[os.path.split(flag_file)[1]]
    cell_count_res = flagser_count_unweighted(adjacency_matrix)
    assert_almost_equal(cell_count_res, cell_count_exp)


def test_weighted(flag_file):
    adjacency_matrix = load_weighted_flag(flag_file, fmt='coo')
    cell_count_exp = cell_count[os.path.split(flag_file)[1]]
    cell_count_res = flagser_count_weighted(adjacency_matrix)
    assert_almost_equal(cell_count_res, cell_count_exp)
