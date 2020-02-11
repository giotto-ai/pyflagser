"""Testing for the python bindings of the C++ flagser library."""

import os
from shutil import rmtree
from tempfile import mkdtemp
from urllib.request import urlretrieve

import pytest
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

try:
    dirname = os.path.join(os.path.dirname(__file__), "../../flagser/test")
    list_dir = os.listdir(dirname)
    flag_files = [os.path.join(dirname, fname)
                  for fname in os.listdir(dirname)
                  if fname.endswith(".flag")]
    download_files = False
except FileNotFoundError:
    # Download from remote bucket
    temp_dir = mkdtemp()
    bucket_url = 'https://storage.googleapis.com/l2f-open-models/giotto-tda' \
                 '/flagser/test/'
    flag_files = []
    for fname in betti.keys():
        url = bucket_url + fname
        fpath = os.path.join(temp_dir, fname)
        urlretrieve(url, fpath)
        flag_files.append(fpath)
    download_files = True


@pytest.mark.parametrize("flag_file, betti",
                         [(flag_file, betti[os.path.split(flag_file)[1]])
                          for flag_file in flag_files
                          if os.path.split(flag_file)[1] in betti.keys()])
def test_flagser(flag_file, betti):
    flag_matrix = loadflag(flag_file)

    ret = flagser(flag_matrix)
    assert_almost_equal(ret['betti'], betti)


if download_files:
    rmtree(temp_dir)
