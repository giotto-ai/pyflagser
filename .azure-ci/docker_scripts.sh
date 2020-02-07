#!/bin/bash

set -x

# upgrading pip and setuptools
PYTHON_PATH=$(eval find "/opt/python/*${python_ver}*" -print)
export PATH=${PYTHON_PATH}/bin:${PATH}
pip install --upgrade pip==19.3.1 setuptools

# installing cmake
pip install cmake

# installing and uninstalling pyflagser
cd /io
pip install -e ".[doc, tests]"
pip uninstall -y pyflagser

# testing, linting
pytest --cov . --cov-report xml
flake8 --exit-zero /io/

# building wheels
pip install wheel twine
python setup.py sdist bdist_wheel
