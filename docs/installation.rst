Installation
============

.. warning::

   This package requires the
   `J-Link Software and Development Pack <https://www.segger.com/download>`__
   provided by SEGGER.  If you do not currently have the development pack
   installed, you must install it first before using this Python package.

.. note::

   This library is known to support Python versions 3.7 - 3.9.  Support for
   versions higher than 3.9 is not guaranteed. As of version 2.0, support for
   Python 2.X is no longer available.

Basic Installation
------------------

Installing PyLink with **pip**:

.. code:: bash

   $ pip install pylink-square

Or use **easy_install**:

.. code:: bash

   $ easy_install pylink-square

Building From Source
--------------------

Clone the project into a local repository, then navigate to that directory and
run:

.. code:: bash

   $ python setup.py install

This will give you the tip of **master** (the development branch).  While we
strive for this to be stable at all times, some bugs may be introduced, so it is
best to check out a release branch first before installing.

.. code:: bash

   $ git checkout release-major.minor
   $ python setup.py install

External Dependencies
---------------------

In order to use this library, the
`J-Link Software and Development Pack <https://www.segger.com/downloads/jlink>`__
provided by SEGGER is required.  Once you have a copy of the development pack,
you can start using PyLink.  PyLink will automatically find the library if you
installed it using one of the installers available from SEGGER's site, but for
best results, you should also do one of the following depending on your
operating system:

On Mac
~~~~~~

.. code:: bash

   # Option A: Copy the library file to your libraries directory.
   cp libjlinkarm.dylib /usr/local/lib/

   # Option B: Add SEGGER's J-Link directory to your dynamic libraries path.
   $ export DYLD_LIBRARY_PATH=/Applications/SEGGER/JLink:$DYLD_LIBRARY_PATH

On Windows
~~~~~~~~~~

Windows searches for DLLs in the following order:

1. The current directory of execution.
2. The Windows system directory.
3. The Windows directory.

You can copy the ``JLinkARM.dll`` to any of the directories listed above.
Alternatively, add the SEGGER J-Link directory to your ``%PATH%``.

On Linux
~~~~~~~~

.. code:: bash

   # Option A: Copy the library to your libraries directory.
   $ cp libjlinkarm.so /usr/local/lib/

   # Option B: Add SEGGER's J-Link library path to your libraries path.
   $ export LD_LIBRARY_PATH=/path/to/SEGGER/JLink:$LD_LIBRARY_PATH
