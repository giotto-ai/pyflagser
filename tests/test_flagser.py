"""Testing for the python bindings of the C++ flagser library."""
# License : Apache 2.0

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

print(flag_files)

def test_flagio():
    for flag_file in flag_files:
        flag_matrix = loadflag(flag_file)
        _, fname_temp = os.path.split(flag_file)
        saveflag(fname_temp, flag_matrix)
        flag_matrix_temp = loadflag(fname_temp)
        print(flag_matrix)
        print('-----------')
        print(flag_matrix_temp)

        assert_almost_equal(flag_matrix.diagonal(), flag_matrix_temp.diagonal())
        assert_almost_equal(np.sort(np.hstack([sp.find(flag_matrix)])),
                            np.sort(np.hstack([sp.find(flag_matrix_temp)])))
#        break

# def test_flagser():
#     dirname = os.path.dirname(__file__)
#     filename = os.path.join(dirname, 'large-test-data.flag')

#     flag_matrix = loadflag(filename)

#     ret = flagser(flag_matrix)
#     print('The H0 value is different from what is shown in stdout: ', ret['betti'])
#     assert ret['betti'] == [0, 90999, 378, 0]
#     # assert False
