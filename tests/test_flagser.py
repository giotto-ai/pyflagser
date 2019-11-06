"""Testing for the python bindings of the C++ flagser library."""
# License : Apache 2.0

import numpy as np
import os
import pytest
from flagser_binding import flagser, flagser_file


def test_flagser_on_file_works():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'large-test-data.flag')

    ret = flagser_file(filename)
    assert len(ret) == 1
    assert ret[0]['betti'] == [0, 90999, 378, 0]


def test_flagser_works():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'large-test-data.flag')

    is_dim0 = True
    edges = []
    # Convert flagser format file to numpy arrays
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line == 'dim 1':
                is_dim0 = False
                continue
            if line == 'dim 0':
                continue

            if is_dim0:
                vertices = np.asarray(list(map(float, line.split(' '))))
            else:
                edges.append(list(map(float, line.split(' '))))

    edges = np.asarray(edges)
    ret = flagser(vertices, edges)
    assert len(ret) == 1
    assert ret[0]['betti'] == [0, 90999, 378, 0]
