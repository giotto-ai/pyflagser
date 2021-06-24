#!/bin/bash

set -x

# Upgrade pip and setuptools, install wheel package
# TODO: Monitor status of pip versions
PYTHON_PATH=$(eval find "/opt/python/*cp${python_ver}*" -print)
export PATH=${PYTHON_PATH}/bin:${PATH}
pip install --upgrade pip setuptools

# Install CMake
pip install cmake

# Install dev environment
cd /io
pip install -e ".[doc, tests]"

# Test dev install with pytest
pytest pyflagser --no-cov --no-coverage-upload

# Uninstal pyflagser dev
pip uninstall -y pyflagser

# Build wheels
python setup.py bdist_wheel

# Repair wheels with auditwheel
pip install auditwheel
auditwheel repair dist/*whl -w dist/
# remove wheels that are not manylinux2010
rm -rf dist/*-linux*.whl
