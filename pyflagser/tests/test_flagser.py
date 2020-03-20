"""Testing for the python bindings of the C++ flagser library."""

import os
import numpy as np

from numpy.testing import assert_almost_equal

from pyflagser import loadflag, flagser
from flagser_pybind import implemented_filtrations

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

"""
Filtrations are only tested for d5.flag
"""
filtrations_results = {
    'dimension':
    {
        'dgms': [
            np.array([[0.,  1.],
                      [0.,  1.],
                      [0.,  1.],
                      [0.,  1.],
                      [0., float('inf')]]),
            np.array([[1., 2.],
                      [1., 2.],
                      [1., 2.],
                      [1., 2.],
                      [1., 2.],
                      [1., 2.]])]
    },
    'zero':
    {
        'dgms': [
            np.array([[0., float('inf')]])]
    },
    'max':
    {
        'dgms': [
            np.array([[0.44, 1.00999999],
                      [0.36000001, 1.125],
                      [0.33000001, 1.14499998],
                      [0.88999999, 1.17999995],
                      [0.11,        float('inf')]]),
            np.array([[1.29499996, 1.34000003],
                      [1.20000005, 1.65499997]])]
    },
    'max3':
    {
        'dgms': [
            np.array([[0.44, 1.00999999],
                      [0.36000001, 1.125],
                      [0.33000001, 1.14499998],
                      [0.88999999, 1.17999995],
                      [0.11,        float('inf')]]),
            np.array([[1.29499996, 1.34000003],
                      [1.20000005, 1.65499997]])]
    },
    'max_plus_one':
    {
        'dgms': [
            np.array([[0.44, 1.00999999],
                      [0.36000001, 1.125],
                      [0.33000001, 1.14499998],
                      [0.88999999, 1.17999995],
                      [0.11,        float('inf')]]),
            np.array([[1.76999998, 2.76999998],
                      [1.755, 2.75500011],
                      [1.65499997, 2.65499997],
                      [1.34000003, 2.34000015],
                      [1.29499996, 2.34000015],
                      [1.20000005, 2.65499997]])]
    },
    'product':
    {
        'dgms': [
            np.array([[0.44, 1.00999999],
                      [0.36000001, 1.125],
                      [0.33000001, 1.14499998],
                      [0.88999999, 1.17999995],
                      [0.11,        float('inf')]]),
            np.array([[1.76999998, 2.04691648],
                      [1.755, 1.99411869],
                      [1.65499997, 1.97242892],
                      [1.34000003, 1.77884996],
                      [1.29499996, 2.08236003],
                      [1.20000005, 2.27397013]])]
    },
    'sum':
    {
        'dgms': [
            np.array([[0.44, 1.00999999],
                      [0.36000001, 1.125],
                      [0.33000001, 1.14499998],
                      [0.88999999, 1.17999995],
                      [0.11,        float('inf')]]),
            np.array([[1.76999998, 3.92499995],
                      [1.755, 3.8900001],
                      [1.65499997, 3.84500003],
                      [1.34000003, 3.64499998],
                      [1.29499996, 3.83500004],
                      [1.20000005, 4.]])]
    },
    'pmean':
    {
        'dgms': [
            np.array([[0.44, 1.00999999],
                      [0.36000001, 1.125],
                      [0.33000001, 1.14499998],
                      [0.88999999, 1.17999995],
                      [0.11,        float('inf')]]),
            np.array([[1.76999998, 2.54917502],
                      [1.755, 2.52713633],
                      [1.65499997, 2.41156578],
                      [1.34000003, 2.04345369],
                      [1.29499996, 2.07881474],
                      [1.20000005, 2.43602848]])]
    },
    'pmoment':
    {
        'dgms': [
            np.array([[0.44, 1.00999999],
                      [0.36000001, 1.125],
                      [0.33000001, 1.14499998],
                      [0.88999999, 1.17999995],
                      [0.11,        float('inf')]]),
            np.array([[1.76999998, 1.9275918],
                      [1.755, 1.85709834],
                      [1.65499997, 1.7869581],
                      [1.34000003, 1.37369251],
                      [1.29499996, 1.39265192],
                      [1.20000005, 1.81259179]])]
    },
    'remove_edges':
    {
        'dgms': [
            np.array([[0.44, 1.00999999],
                      [0.36000001, 1.125],
                      [0.33000001, 1.14499998],
                      [0.88999999, 1.17999995],
                      [0.11,        float('inf')]]),
            np.array([[1.29499996, 1.34000003],
                      [1.20000005, 1.65499997]])]
    },
}


def test_flagser(flag_file):
    betti_exp = betti[os.path.split(flag_file)[1]]
    flag_matrix = loadflag(flag_file)
    betti_res = flagser(flag_matrix)['betti']
    assert_almost_equal(betti_res, betti_exp)


def are_matrix_equal(m1, m2):
    for i in range(min(len(m1), len(m2))):
        m1f = np.array(m1[i]).flatten()
        m2f = np.array(m2[i]).flatten()
        if not np.isclose(m1f, m2f).all():
            return False
    return True


def test_filtrations(flag_file):
    """
    Testing all filtrations available for dataset d5.flag
    vertex_degree filtrations was disable because it produces a segmentation
    fault.
    """
    if os.path.split(flag_file)[1] == 'd5.flag':
        flag_matrix = loadflag(flag_file)
        for filtration in implemented_filtrations:
            if filtration not in ['vertex_degree']:
                assert filtration in filtrations_results.keys(),\
                    "Test for {} is not implemented, current implemented tests\
                    are {}".format(filtration, filtrations_results.keys())
                res = flagser(flag_matrix, max_dimension=1, directed=False,
                              filtration=filtration)
                for filt, tests in filtrations_results.items():
                    if filtration == filt:
                        tmp = np.array(res['dgms']).tolist()
                        tmp2 = np.array(tests['dgms']).tolist()
                        assert are_matrix_equal(tmp, tmp2), \
                            "diagrams {} \n and {} \n are not equal"\
                            .format(tmp, tmp2)
