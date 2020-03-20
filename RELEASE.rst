Release 0.2.1
==============

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

We are also grateful to all who filed issues or helped resolve them, asked and
answered questions, and were part of inspiring discussions.


Release 0.2.0
==============

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

We are also grateful to all who filed issues or helped resolve them, asked and
answered questions, and were part of inspiring discussions.


Release 0.1.0
==============

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

We are also grateful to all who filed issues or helped resolve them, asked and
answered questions, and were part of inspiring discussions.
