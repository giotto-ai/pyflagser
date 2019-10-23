.. image:: https://www.giotto.ai/static/vector/logo.svg
   :width: 850

|Azure|_ |Azure-cov|_ |Azure-test|_

.. |Azure| image:: https://dev.azure.com/giotto-learn/flagser-pybind/_apis/build/status/giotto-learn.flagser-pybind?branchName=master
.. _Azure: https://dev.azure.com/giotto-learn/flagser-pybind/

.. |Azure-cov| image:: https://img.shields.io/badge/Coverage-93%25-passed
.. _Azure-cov: https://dev.azure.com/giotto-learn/flagser-pybind/_build/results?buildId=342&view=codecoverage-tab

.. |Azure-test| image:: https://img.shields.io/badge/Testing-Passed-brightgreen
.. _Azure-test: https://dev.azure.com/giotto-learn/flagser-pybind/_build/results?buildId=342&view=ms.vss-test-web.build-test-results-tab


flagser-pybind
============


flagser-pybind is a python API for the flagser C++ library by Daniel Lütgehetmann which computes the homology of directed flag complexes. Please check out the original `luetge/flagser
<https://github.com/luetge/flagser>`_ GitHub repository for more information.


Website: http://www.giotto.ai


Installation
------------

Dependencies
~~~~~~~~~~~~

flagser-pybind requires:

- Python (>= 3.5)
- numpy (>= 1.17.0)
- scipy (>= 0.17.0)

User installation
~~~~~~~~~~~~~~~~~

The easiest way to install flagser-pybind is using ``pip``   ::

    pip install -U flagser-pybind

Documentation
-------------

- HTML documentation (stable release): Upcoming

Contributing
------------

We welcome new contributors of all experience levels. The Giotto
community goals are to be helpful, welcoming, and effective. To learn more about
making a contribution to flagser-pybind, please see the `CONTRIBUTING.rst
<https://github.com/giotto-learn/flagser-pybind/blob/master/CONTRIBUTING.rst>`_ file.

Developer installation
~~~~~~~~~~~~~~~~~~~~~~~

C++ dependencies:
'''''''''''''''''

-  C++14 compatible compiler
-  CMake >= 3.9

Source code
'''''''''''

You can check the latest sources with the command::

    git clone https://github.com/giotto-learn/flagser-pybind.git


To install:
'''''''''''

.. code-block:: bash

   cd flagser-pybind
   pip install -e .

From there any change in the library files will be immediately available on your machine.

Testing
~~~~~~~

After installation, you can launch the test suite from outside the
source directory::

    pytest flagser_pybind


Changelog
---------

See the `RELEASE.rst <https://github.com/giotto-learn/flagser-pybind/blob/master/RELEASE.rst>`__ file
for a history of notable changes to flagser-pybind.

Important links
~~~~~~~~~~~~~~~

- Official source code repo: https://github.com/giotto-learn/flagser-pybind
- Download releases: https://pypi.org/project/giotto-learn/
- Issue tracker: https://github.com/giotto-learn/flagser-pybind/issues


Contacts:
---------

maintainers@giotto.ai
