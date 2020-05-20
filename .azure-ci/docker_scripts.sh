#!/bin/bash

set -x

# Upgrade pip and setuptools. TODO: Monitor status of pip versions
PYTHON_PATH=$(eval find "/opt/python/*${python_ver}*" -print)
export PATH=${PYTHON_PATH}/bin:${PATH}
pip install --upgrade pip==19.3.1 setuptools

# Install CMake
pip install cmake

# Install dev environment
cd /io
pip install -e ".[doc, tests]"

# Test dev install with pytest and flake8
pytest pyflagser --cov --cov-report xml
flake8 --exit-zero /io/

# Uninstal pyflagser dev
pip uninstall -y pyflagser

# Build wheels
pip install wheel==0.34.1 auditwheel==3.1.0
python setup.py bdist_wheel

# Repair wheels with auditwheel
auditwheel repair dist/*whl -w dist/
# remove wheels that are not manylinux2010
rm -rf dist/*-linux*.whl
