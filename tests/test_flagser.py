#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: test_flagser.py
Description: This file contains test to check if flagser works.
"""
__license__ = "Apache 2.0"

from flagser_binding import flagser

def test_flagser_works():
    ret = flagser('large-test-data.flag')
    assert len(ret) == 1
    assert ret[0]['betti'] == [0, 90999, 378, 0]
