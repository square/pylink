Tutorial
========

In this tutorial, assume that the serial number of the J-Link emulator being
connected to is ``123456789``, and that the target device is an
``Mkxxxxxxxxxx7``.

Connecting to an Emulator
-------------------------

.. code:: python

   >>> import pylink
   >>> jlink = pylink.JLink()
   >>> jlink.open(123456789)
   >>> jlink.product_name
   J-Trace Cortex-M
   >>> jlink.oem
   >>> jlink.opened()
   True
   >>> jlink.connected()
   True
   >>> jlink.target_connected()
   False

Updating the Emulator
---------------------

.. code:: python

   >>> jlink.update_firmware()
   1

Connecting to a Target CPU
--------------------------

.. code:: python

   >>> jlink.connect('MKxxxxxxxxxx7')
   >>> jlink.core_id()
   50331903
   >>> jlink.device_family()
   3
   >>> jlink.target_connected()
   True

Flashing from a File
--------------------

.. code:: python

   >>> jlink.flash_file('/path/to/file', address)
   1337
   >>> jlink.memory_read8(0, 1337)
   [ 0, 0, .... ]

Flashing from a List of Bytes
-----------------------------

.. code:: python

   >>> data = [1, 2, 3, 4]
   >>> jlink.flash(data, 0)
   4
   >>> jlink.memory_read8(0, 4)
   [1, 2, 3, 4]

Unlocking a Device
------------------

.. note::

   Currently unlock is only supported for Kinetis on SWD.

.. code:: python

   >>> pylink.unlock(jlink, 'Kinetis')
   True
