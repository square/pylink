RTT Convenience Functions
==========================

The ``pylink.rtt`` module provides high-level convenience functions for RTT
(Real-Time Transfer) operations. It wraps the low-level JLink API and handles
common use cases like auto-detection, polling, and reconnection.

The low-level API in ``jlink.py`` is kept simple per maintainer feedback. This
module provides convenience features like:

- Automatic search range generation from device RAM info
- Polling for RTT readiness after start
- Automatic reconnection after device resets
- Context manager for automatic cleanup
- Reset detection and monitoring

Quick Start
-----------

The simplest way to use RTT is with the context manager::

    >>> import pylink
    >>> from pylink.rtt import rtt_context
    >>> 
    >>> jlink = pylink.JLink()
    >>> jlink.open()
    >>> jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    >>> jlink.connect('NRF54L15_M33')
    >>> 
    >>> with rtt_context(jlink) as j:
    ...     data = j.rtt_read(0, 1024)
    ...     if data:
    ...         print(bytes(data))

Auto-detection
--------------

The module can automatically detect RTT search ranges from device RAM info::

    >>> from pylink.rtt import auto_detect_rtt_ranges, start_rtt_with_polling
    >>> 
    >>> ranges = auto_detect_rtt_ranges(jlink)
    >>> if ranges:
    ...     start_rtt_with_polling(jlink, search_ranges=ranges)

Polling
-------

Start RTT with automatic polling until ready::

    >>> from pylink.rtt import start_rtt_with_polling
    >>> 
    >>> if start_rtt_with_polling(jlink, timeout=5.0):
    ...     data = jlink.rtt_read(0, 1024)

Reconnection
------------

Reconnect RTT after device reset::

    >>> from pylink.rtt import reconnect_rtt
    >>> 
    >>> jlink.reset()
    >>> if reconnect_rtt(jlink, search_ranges=[(0x20000000, 0x2003FFFF)]):
    ...     print("RTT reconnected!")

Monitoring with Reset Detection
--------------------------------

Monitor RTT with automatic reset detection::

    >>> from pylink.rtt import monitor_rtt_with_reset_detection
    >>> 
    >>> for data in monitor_rtt_with_reset_detection(jlink):
    ...     if data:
    ...         print(bytes(data))

API Reference
-------------

.. automodule:: pylink.rtt
    :members:
    :undoc-members:
    :show-inheritance:

Known Limitations
-----------------

RTT Telnet Port Configuration (Issue #161):
    The J-Link SDK's ``SetRTTTelnetPort`` command sets the port that the J-Link
    device listens on for Telnet connections. This is a server-side port
    configuration that cannot be changed programmatically via pylink.

    Limitations:
    - The Telnet port is set by the J-Link device firmware, not by pylink
    - Multiple J-Link instances may conflict if they use the same port
    - Port conflicts must be resolved by using different J-Link devices or
      configuring ports via SEGGER J-Link software

    Workarounds:
    - Use separate J-Link devices for different RTT sessions
    - Use ``open_tunnel()`` with different client ports if connecting as client
    - Configure ports via SEGGER J-Link Commander or J-Link Settings

    For more details, see Issue #161.

Related Issues
--------------

This module addresses the following GitHub issues:

- `Issue #249 <https://github.com/square/pylink/issues/249>`_: RTT auto-detection fails
- `Issue #209 <https://github.com/square/pylink/issues/209>`_: Option to set RTT Search Range
- `Issue #51 <https://github.com/square/pylink/issues/51>`_: Initialize RTT with address of RTT control block
- `Issue #252 <https://github.com/square/pylink/issues/252>`_: Reset detection via SWD/JTAG
- `Issue #111 <https://github.com/square/pylink/issues/111>`_: RTT Echo (local echo option)
- `Issue #161 <https://github.com/square/pylink/issues/161>`_: Specify RTT Telnet port (limitation documented)

See Also
--------

- :doc:`pylink` - Low-level JLink API
- :doc:`troubleshooting` - Troubleshooting guide
- `SEGGER RTT Documentation <https://www.segger.com/products/debug-probes/j-link/technology/about-real-time-transfer/>`_

