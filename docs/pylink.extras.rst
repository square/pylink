Extras
======

PyLink makes use of a number of different submodules as a part of its
implementation.  These submdules are *extras*, and the user should not need to
use them explicitly.

Binpacker
---------

This submodule provides functions for creating arrays of bytes from an integer.

.. automodule:: pylink.binpacker
    :members:
    :undoc-members:
    :show-inheritance:

Decorators
----------

This submodule provides different decorator functions.

.. automodule:: pylink.decorators
    :members:
    :undoc-members:
    :show-inheritance:

Registers
---------

This submodule provides `ctypes` bindings for different registers.

.. automodule:: pylink.registers
    :members:
    :undoc-members:
    :show-inheritance:

Threads
-------

This submodule provides custom `threading.Thread` types.

.. automodule:: pylink.threads
    :members:
    :undoc-members:
    :show-inheritance:

Util
----

This submodule provides different utility functions.

.. automodule:: pylink.util
    :members:
    :undoc-members:
    :show-inheritance:

RTT Convenience Functions
--------------------------

This submodule provides high-level convenience functions for RTT (Real-Time Transfer)
operations. It wraps the low-level JLink API and handles common use cases like
auto-detection, polling, and reconnection.

The low-level API in `jlink.py` is kept simple per maintainer feedback. This module
provides convenience features like:

- Automatic search range generation from device RAM info
- Polling for RTT readiness after start
- Automatic reconnection after device resets
- Context manager for automatic cleanup
- Reset detection and monitoring

.. automodule:: pylink.rtt
    :members:
    :undoc-members:
    :show-inheritance:
