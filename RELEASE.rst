Release 0.4.2
=============

Major Features and Improvements
-------------------------------

- Wheels for Python 3.9 have been added.
- The ``flagser`` submodule has been updated to the latest upstream version, integrating the following changes:

  - ``flagser`` now trows exceptions instead of exiting the computation;
  - ``flagser`` now supports a number of threads as input parameter and, by default, it will use the maximum numbre of logic cores available.

Bug Fixes
---------

An error encountered when running multiple instances of ``pyflagser`` in parallel (due to clashes between temporary file names) has been fixed.

Backwards-Incompatible Changes
------------------------------

None.

Thanks to our Contributors
--------------------------

This release contains contributions from many people:

Julian Burella Pérez and Umberto Lupo.

We are also grateful to all who filed issues or helped resolve them, asked and answered questions, and were part of inspiring discussions.


Release 0.4.1
=============

Bug Fixes
---------

A bug was fixed which caused some computations to hang when the prime for the finite field of coefficients used is greater than 2.

Backwards-Incompatible Changes
------------------------------

None.

Thanks to our Contributors
--------------------------

This release contains contributions from many people:

Julian Burella Pérez and Umberto Lupo.

We are also grateful to all who filed issues or helped resolve them, asked and answered questions, and were part of inspiring discussions.


Release 0.4.0
=============

Major Features and Improvements
-------------------------------

- ``flagser_count_unweighted`` and ``flagser_count_weighted`` were added to provide fast computations of simplex counts per dimension.
- ``flagser_unweighted`` and ``flagser_weighted``'s performance was improved when ``coeff`` is 2 by using a compiled version of C++ ``flagser`` without the ``USE_COEFFICIENTS`` flag.
- All C++ library files were moved to ``pyflagser/modules/`` upon compilation.
- The documentation of ``flagser_unweighted`` and ``flagser_weighted`` was further improved.
- Python bindings were made clearer, and documented for future maintenance.

Bug Fixes
---------

- A bug was fixed which caused ``flagser_unweighted`` and ``flagser_weighted``'s output persistence diagrams to be of shape ``(0,)`` instead of ``(0, 2)`` if empty.

Backwards-Incompatible Changes
------------------------------

None.

Thanks to our Contributors
--------------------------

This release contains contributions from many people:

Guillaume Tauzin, Umberto Lupo, and Julian Burella Pérez.

We are also grateful to all who filed issues or helped resolve them, asked and answered questions, and were part of inspiring discussions.


Release 0.3.1
=============

Major Features and Improvements
-------------------------------

- Clarity of the code of ``flagser_unweighted`` and ``flagser_weighted`` was improved.
- Auditwheel repair is now run in the manylinux jobs.
- ``twine check`` is now run as part of the CI.

Bug Fixes
---------

- Fix bug causing ``flagser_weighted``'s output persistence diagrams to be a list of list of tuples instead of a list of ``numpy.ndarrays`` of shape (n_points, 2).

Backwards-Incompatible Changes
------------------------------

- Installation from tarballs is no longer supported.

Thanks to our Contributors
--------------------------

This release contains contributions from many people:

Umberto Lupo and Guillaume Tauzin.

We are also grateful to all who filed issues or helped resolve them, asked and answered questions, and were part of inspiring discussions.


Release 0.3.0
==============

Major Features and Improvements
-------------------------------

This is a major release. The whole library has been fully refactored and all functions have been renamed. In particular:

- All functions have been split into an ``unweighted`` and a ``weighted`` version.

  - The ``unweighted`` functions process unweighted graphs. In the adjacency matrices passed to them, off-diagonal, ``0`` or ``False`` values denote absent edges while non-``0`` or ``True`` values denote edges which are present. Diagonal values are ignored.
  - The ``weighted`` functions process weighted graphs. In the adjacency matrices passed to them, the way zero values are handled depends on the format of the matrix. If the matrix is a dense ``numpy.ndarray``, zero values denote zero-weighted edges. If the matrix is a sparse ``scipy.sparse`` matrix, explicitly stored off-diagonal zeros and all diagonal zeros denote zero-weighted edges. Off-diagonal values that have not been explicitely stored are treated by ``scipy.sparse`` as zeros but will be understood as infinitely-valued edges, i.e., edges absent from the filtration. Diagonal elements are vertex weights.

- ``saveflag`` has been split into ``save_unweighted_flag`` and a ``save_weighted_flag``:

  - ``save_unweighted_flag`` focuses on saving adjacency matrices of unweighted graphs into a `.flag` file understandable by C++ `flagser`.
  - ``save_weighted_flag`` focuses on saving adjacency matrices of weighted graphs into a `.flag` file understandable by C++ `flagser`.  It now takes a ``max_edge_weight`` argument. All edge weights greater than that value will be considered as infinitely-valued, i.e., absent from the filtration.

- ``loadflag`` has been split into ``load_unweighted_flag`` and a ``load_weighted_flag``.

  - ``load_unweighted_flag`` focuses on loading ``.flag`` files as adjacency matrices of unweighted graphs.
  - ``load_weighted_flag`` focuses on loading ``.flag`` files as adjacency matrices of weighted graphs. It now take an ``infinity_value`` parameter which is the value to use to denote an absence of edge. It is only useful when the output adjacency matrix is set to be a ``numpy.ndarray`` by passing `fmt` as ``'dense'``. If ``None``, it is set to the maximum value allowed by the passed `dtype`.

- ``flagser`` has been split into ``flagser_unweighted`` and a ``flagser_weighted``.

  - ``flagser_unweighted`` focuses on the computation of homology and outputs Betti numbers, cell counts per dimension, and Euler characteristic.
  - ``flagser_weighted`` focuses on the computation of persistent homology  and outputs persistence diagrams, Betti numbers, cell counts per dimension, and Euler characteristic. It now takes a ``max_edge_weight`` argument. All edge weights greater than that value will be considered as infinitely-valued, i.e., absent from the filtration.

Additionally,

- The documentation have been strongly improved both in docstrings and in the code.
- The handling of default parameters has been improved and warnings are now issued.
- Sparse matrix efficiency warnings have been turned off (``lil_matrix`` cannot be used because it ignores explicitly set 0 values).
- Core functions to transform an adjacency matrix into the data structures understood by C++ ``flagser`` have been moved to the new ``_utils.py``.
- Tests have been extended according to cover the new functionalities.

Bug Fixes
---------

The following bug fixes were introduced:

- A bug fix from C++ ``flagser`` on ``vertex_degree`` filtration has been propagated to pyflagser.

- A bug in the C++ ``flagser`` bindings causing persistence diagrams and cell counts to be wrong based on the values of ``min_dimension`` and ``max_dimension`` has been fixed.

- Tests were updated accordingly and `conftest.py` has been improved.

- Bugs in the ``pyflagser`` ``flagser`` functions causing incompatibilities with sparse matrix and non-float datatype have been fixed.

- ``CMakeLists`` has been updated to use C++14. This addresses problem when compiling on MacOS.

Backwards-Incompatible Changes
------------------------------

The library has been fully refactored, which means that most changes were backwards-incompatible. In particular:

- All functions have been renamed as they now include an ``unweighted`` and a ``weighted`` version.
- The ``flag_matrix`` argument have been renamed ``adjacency_matrix``.

Please check the documentation for more information.

Thanks to our Contributors
--------------------------

This release contains contributions from many people:

Guillaume Tauzin, Umberto Lupo, and Julian Burella Pérez.

We are also grateful to all who filed issues or helped resolve them, asked and answered questions, and were part of inspiring discussions.


Release 0.2.1
=============

Major Features and Improvements
-------------------------------

``CMakeLists`` updated to enable compile flags on MSVC. This improves performance on Windows systems.

Bug Fixes
---------

Hotfix addressing multiples issues where forwarding arguments to C++ ``flagser``:

- ``filtration`` was not correctly forwarded and it always fallback to zero filtration.
- ``max-dim`` and ``min-dim`` were always equal to 0.

``CMakeLists`` updated to disable AVX instructions. This addresses incompatibilities observed with specific hardware setups.

Backwards-Incompatible Changes
------------------------------

None.

Thanks to our Contributors
--------------------------

This release contains contributions from many people:

Julian Burella Pérez, Umberto Lupo, and Guillaume Tauzin.

We are also grateful to all who filed issues or helped resolve them, asked and answered questions, and were part of inspiring discussions.


Release 0.2.0
=============

Major Features and Improvements
-------------------------------

The ``flagser`` method now accepts ``filtration`` as an argument. All filtrations available for the C++ flagser software can be used.

Bug Fixes
---------

Fixed bug related to the generation of a file by C++ ``flagser``. Whenever pyflagser's ``flagser`` method was interrupted, it would not remove the generated file, which would prevent the ``flagser`` method to be called again.

Backwards-Incompatible Changes
------------------------------

None.

Thanks to our Contributors
--------------------------

This release contains contributions from many people:

Julian Burella Pérez, Umberto Lupo, and Guillaume Tauzin.

We are also grateful to all who filed issues or helped resolve them, asked and answered questions, and were part of inspiring discussions.


Release 0.1.0
=============

Initial release of ``pyflagser``.

Major Features and Improvements
-------------------------------

The following methods where added:

-  ``loadflag`` enable the user to load a ``.flag`` file into a ``scipy`` or ``numpy`` matrix.
-  ``saveflag`` enables the user to save a ``scipy`` or ``numpy`` matrix into a ``.flag`` file.
-  ``flagser`` computes the persistent homology of directed/undirected flag complexes.

Bug Fixes
---------


Backwards-Incompatible Changes
------------------------------


Thanks to our Contributors
--------------------------

This release contains contributions from many people:

Guillaume Tauzin, Julian Burella Pérez and Umberto Lupo.

We are also grateful to all who filed issues or helped resolve them, asked and answered questions, and were part of inspiring discussions.
