Serial Wire Debug
=================

Serial Wire Output (SWO) alongside Serial Wire Debug (SWD) allows for the CPU
to emit real-time trace data.  In particular, when used with an Instrumentation
Trace Macrocell (ITM), it can be used to form a Serial Wire Viewer (SWV).  The
ITM ports are provided by the ARM controller.  The SWV typically implements a
form of ``printf`` style debugging for embedded systems.

Getting Started
---------------

First, get your J-Link set up by instantiating an instance of a ``JLink`` and
connecting to your target device.  Once that is established, you want to call
either ``swo_start()``:

.. code:: python

   speed = 9600
   jlink.swo_start(swo_speed=speed)

or call ``swo_enable()``:

.. code:: python

   swo_speed = 9600
   cpu_speed = 72000000 # 72 MHz
   port_mask = 0x01
   jlink.swo_enable(cpu_speed, swo_speed, port_mask)

Once enabled, you can begin reading data from the target.

Serial Wire Methods
-------------------

.. automodule:: pylink.jlink
    :noindex:

    .. autoclass:: pylink.jlink.JLink
        :noindex:
        :members: swd_read8, swd_read16, swd_read32, swd_write, swd_write8,
                  swd_write16, swd_write32, swd_sync, swo_start, swo_enable,
                  swo_stop, swo_flush, swo_speed_info, swo_num_bytes,
                  swo_set_host_buffer_size, swo_set_emu_buffer_size,
                  swo_supported_speeds, swo_read, swo_read_stimulus

Examples
--------

Serial Wire Viewer
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/swv.py
    :name: swv-py
    :language: python
    :linenos:
