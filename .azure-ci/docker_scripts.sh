#!/bin/bash

set -x

# Upgrade pip and setuptools
PYTHON_PATH=$(eval find "/opt/python/*${python_ver}*" -print)
export PATH=${PYTHON_PATH}/bin:${PATH}
pip install --upgrade pip==19.3.1 setuptools

# Install cmake
pip install cmake

# Install pyflagser dev
cd /io
pip install -e ".[doc, tests]"

# Test de
pytest --cov pyflagser --no-cov --no-coverage-upload
flake8 --exit-zero /io/

# Uninstal pyflagser dev
pip uninstall -y pyflagser

# Build wheels
pip install wheel
python setup.py sdist bdist_wheel
