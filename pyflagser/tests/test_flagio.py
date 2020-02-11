"""Testing for the python bindings of the C++ flagser library."""

import os
from shutil import rmtree
from tempfile import mkdtemp
from urllib.request import urlopen, urlretrieve

import numpy as np
import pytest
import scipy.sparse as sp
from numpy.testing import assert_almost_equal

from pyflagser import loadflag, saveflag

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
    flag_files_list = bucket_url + 'flag_files_list.txt'
    with urlopen(flag_files_list) as f:
        flag_file_names = f.read().decode('utf8').splitlines()
        flag_files = []
        for fname in flag_file_names:
            url = bucket_url + fname
            fpath = os.path.join(temp_dir, fname)
            urlretrieve(url, fpath)
            flag_files.append(fpath)
    download_files = True


@pytest.mark.parametrize("flag_file", flag_files)
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


if download_files:
    rmtree(temp_dir)
