#!/usr/bin/env python
"""Example: Using RTT with convenience functions.

This example demonstrates how to use the pylink.rtt convenience module
for common RTT operations like auto-detection, polling, and reconnection.
"""

import pylink
from pylink.rtt import (
    auto_detect_rtt_ranges,
    start_rtt_with_polling,
    reconnect_rtt,
    rtt_context,
    monitor_rtt_with_reset_detection,
    read_rtt_without_echo
)

# Example 1: Basic RTT usage with auto-detection
def example_basic_rtt():
    """Basic RTT usage with auto-detected search ranges."""
    jlink = pylink.JLink()
    jlink.open()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect('nRF54L15')

    # Auto-detect search ranges from device RAM
    ranges = auto_detect_rtt_ranges(jlink)
    if ranges:
        print(f"Auto-detected RTT search ranges: {ranges}")

        # Start RTT with polling
        if start_rtt_with_polling(jlink, search_ranges=ranges):
            print("RTT started successfully!")

            # Read data from RTT buffer 0
            data = jlink.rtt_read(0, 1024)
            if data:
                print(f"Received: {bytes(data)}")

            # Stop RTT
            jlink.rtt_stop()

    jlink.close()


# Example 2: Using explicit search ranges (recommended for nRF54L15)
def example_explicit_ranges():
    """Using explicit search ranges for nRF54L15."""
    jlink = pylink.JLink()
    jlink.open()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect('nRF54L15')

    # nRF54L15 RAM range
    ranges = [(0x20000000, 0x2003FFFF)]

    if start_rtt_with_polling(jlink, search_ranges=ranges, timeout=5.0):
        print("RTT ready!")

        # Read data
        while True:
            data = jlink.rtt_read(0, 1024)
            if data:
                print(bytes(data).decode('utf-8', errors='ignore'), end='')
            else:
                break

    jlink.rtt_stop()
    jlink.close()


# Example 3: Using context manager for automatic cleanup
def example_context_manager():
    """Using context manager for automatic RTT cleanup."""
    from contextlib import contextmanager

    jlink = pylink.JLink()
    jlink.open()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect('nRF54L15')

    ranges = [(0x20000000, 0x2003FFFF)]

    # RTT automatically stopped when exiting context
    with rtt_context(jlink, search_ranges=ranges) as j:
        data = j.rtt_read(0, 1024)
        if data:
            print(f"Received: {bytes(data)}")

    # RTT is already stopped here
    jlink.close()


# Example 4: Reconnecting after device reset
def example_reconnect():
    """Reconnecting RTT after device reset."""
    jlink = pylink.JLink()
    jlink.open()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect('nRF54L15')

    ranges = [(0x20000000, 0x2003FFFF)]

    # Start RTT initially
    if start_rtt_with_polling(jlink, search_ranges=ranges):
        print("RTT started")

    # Device reset occurs...
    jlink.reset()

    # Reconnect RTT (search ranges are automatically reconfigured)
    if reconnect_rtt(jlink, search_ranges=ranges):
        print("RTT reconnected after reset!")

    jlink.rtt_stop()
    jlink.close()


# Example 5: Monitoring with reset detection
def example_monitor_with_reset():
    """Monitoring RTT with automatic reset detection."""
    jlink = pylink.JLink()
    jlink.open()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect('nRF54L15')

    ranges = [(0x20000000, 0x2003FFFF)]

    try:
        # Monitor RTT - automatically reconnects on reset
        for data in monitor_rtt_with_reset_detection(
            jlink,
            search_ranges=ranges,
            reset_check_interval=1.0
        ):
            if data:
                print(data.decode('utf-8', errors='ignore'), end='')
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

    jlink.close()


# Example 6: Reading without local echo
def example_no_echo():
    """Reading RTT data without local echo characters."""
    jlink = pylink.JLink()
    jlink.open()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect('nRF54L15')

    ranges = [(0x20000000, 0x2003FFFF)]

    if start_rtt_with_polling(jlink, search_ranges=ranges):
        # Read without echo
        data = read_rtt_without_echo(jlink, buffer_index=0, num_bytes=1024)
        if data:
            print(data.decode('utf-8', errors='ignore'))

    jlink.rtt_stop()
    jlink.close()


# Example 7: Using explicit block address
def example_block_address():
    """Using explicit RTT control block address."""
    jlink = pylink.JLink()
    jlink.open()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect('nRF54L15')

    # Find control block address
    addr = jlink.rtt_get_block_address([(0x20000000, 0x2003FFFF)])
    if addr:
        print(f"Found RTT control block at 0x{addr:X}")

        # Start RTT with explicit address
        if start_rtt_with_polling(jlink, block_address=addr):
            print("RTT started with explicit address!")

            data = jlink.rtt_read(0, 1024)
            if data:
                print(f"Received: {bytes(data)}")

    jlink.rtt_stop()
    jlink.close()


# Example 8: Low-level API usage (without convenience module)
def example_low_level():
    """Using low-level API directly (no polling)."""
    jlink = pylink.JLink()
    jlink.open()
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect('nRF54L15')

    # Low-level: configure search ranges explicitly
    ranges = [(0x20000000, 0x2003FFFF)]
    jlink.rtt_start(search_ranges=ranges)

    # Poll manually for RTT readiness
    import time
    timeout = 10.0
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            num_up = jlink.rtt_get_num_up_buffers()
            if num_up > 0:
                print(f"RTT ready with {num_up} up buffer(s)")
                break
        except Exception:
            pass
        time.sleep(0.1)
    else:
        print("RTT did not become ready")

    # Read data
    if jlink.rtt_is_active():
        data = jlink.rtt_read(0, 1024)
        if data:
            print(f"Received: {bytes(data)}")

    jlink.rtt_stop()
    jlink.close()


if __name__ == '__main__':
    print("RTT Examples")
    print("=" * 50)
    print("\n1. Basic RTT usage:")
    # example_basic_rtt()

    print("\n2. Explicit search ranges:")
    # example_explicit_ranges()

    print("\n3. Context manager:")
    # example_context_manager()

    print("\n4. Reconnect after reset:")
    # example_reconnect()

    print("\n5. Monitor with reset detection:")
    # example_monitor_with_reset()

    print("\n6. Read without echo:")
    # example_no_echo()

    print("\n7. Explicit block address:")
    # example_block_address()

    print("\n8. Low-level API:")
    # example_low_level()

    print("\nUncomment the examples you want to run.")

