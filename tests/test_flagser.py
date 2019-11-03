#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: test_flagser.py
Description: This file contains test to check if flagser works.
"""
__license__ = "Apache 2.0"

from flagser_binding import flagser, flagser_file
import numpy as np


def test_flagser_on_file_works():
    ret = flagser_file('large-test-data.flag')
    assert len(ret) == 1
    assert ret[0]['betti'] == [0, 90999, 378, 0]


def test_flagser_works():
    data_file = 'large-test-data.flag'
    is_dim0 = True
    vertices = []
    # Convert flagser format file to numpy arrays
    with open(data_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line == 'dim 1':
                is_dim0 = False
                continue
            if line == 'dim 0':
                continue

            if is_dim0:
                vertexes = np.asarray(list(map(float, line.split(' '))))
            else:
                vertices.append(list(map(float, line.split(' '))))

    vertices = np.asarray(vertices)
    ret = flagser(vertexes, vertices)
    assert len(ret) == 1
    assert ret[0]['betti'] == [0, 90999, 378, 0]

