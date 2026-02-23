# Copyright 2018 Square, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Convenience functions for RTT operations.

This module provides high-level RTT functionality that wraps the low-level
JLink API. It handles common use cases like auto-detection, polling, and
reconnection.

The low-level API in `jlink.py` is kept simple per maintainer feedback.
This module provides convenience features like:
- Automatic search range generation from device RAM info
- Polling for RTT readiness after start
- Automatic reconnection after device resets
- Context manager for automatic cleanup

Known Limitations:
------------------

RTT Telnet Port Configuration (Issue #161):
    The J-Link SDK's `SetRTTTelnetPort` command sets the port that the J-Link
    device listens on for Telnet connections. This is a server-side port
    configuration that cannot be changed programmatically via pylink.

    Limitations:
    - The Telnet port is set by the J-Link device firmware, not by pylink
    - Multiple J-Link instances may conflict if they use the same port
    - Port conflicts must be resolved by using different J-Link devices or
      configuring ports via SEGGER J-Link software

    Workarounds:
    - Use separate J-Link devices for different RTT sessions
    - Use `open_tunnel()` with different client ports if connecting as client
    - Configure ports via SEGGER J-Link Commander or J-Link Settings

    For more details, see Issue #161.
"""

import logging
import time

logger = logging.getLogger(__name__)

# Default constants for polling and timeouts
DEFAULT_RTT_TIMEOUT = 10.0
DEFAULT_POLL_INTERVAL = 0.05
DEFAULT_MAX_POLL_INTERVAL = 0.5
DEFAULT_BACKOFF_FACTOR = 1.5
DEFAULT_VERIFICATION_DELAY = 0.1
DEFAULT_FALLBACK_SIZE = 0x10000  # 64KB fallback if RAM size unknown (matches jlink.py)


def auto_detect_rtt_ranges(jlink):
    """Auto-generate RTT search ranges from device RAM info.

    This function generates search ranges from the device's RAM information,
    which is useful when you don't know the exact RAM layout or when working
    with multiple devices.

    Args:
        jlink: JLink instance (must be opened and connected to device)

    Returns:
        list: List of (start, end) address tuples for RTT search ranges.
              Returns None if device RAM info is not available.
              Format: [(start_addr, end_addr), ...]

    Example:
        Auto-detect ranges and start RTT::

            >>> ranges = auto_detect_rtt_ranges(jlink)
            >>> if ranges:
            ...     start_rtt_with_polling(jlink, search_ranges=ranges)

    Note:
        This function uses the device's RAM address and size from the J-Link
        device database. If RAM info is not available, returns None.

    Related:
        - start_rtt_with_polling(): Use auto-detected ranges to start RTT
        - Issue #209: Option to set RTT Search Range
    """
    if not hasattr(jlink, '_device') or not jlink._device:
        logger.warning("Device info not available for auto-detecting RTT ranges")
        return None

    try:
        ram_start = getattr(jlink._device, 'RAMAddr', None)
        ram_size = getattr(jlink._device, 'RAMSize', None)

        if ram_start is None or ram_start == 0:
            logger.warning("RAM address not available in device info")
            return None

        ram_start = int(ram_start) & 0xFFFFFFFF

        if ram_size is not None and ram_size > 0:
            ram_size = int(ram_size) & 0xFFFFFFFF
            ram_end = ram_start + ram_size - 1
        else:
            # Use fallback size if RAM size not available
            logger.debug("RAM size not available, using fallback size")
            ram_end = ram_start + DEFAULT_FALLBACK_SIZE - 1

        # Validate that we have a valid range
        if ram_start >= ram_end:
            logger.warning("Invalid RAM range detected (start >= end), cannot auto-detect")
            return None

        ranges = [(ram_start, ram_end)]
        logger.info("Auto-detected RTT search range: 0x%X - 0x%X", ram_start, ram_end)
        return ranges

    except Exception as e:
        logger.warning("Error auto-detecting RTT ranges: %s", e)
        return None


def start_rtt_with_polling(jlink, search_ranges=None, block_address=None,
                          timeout=DEFAULT_RTT_TIMEOUT,
                          poll_interval=DEFAULT_POLL_INTERVAL,
                          max_poll_interval=DEFAULT_MAX_POLL_INTERVAL,
                          backoff_factor=DEFAULT_BACKOFF_FACTOR,
                          verification_delay=DEFAULT_VERIFICATION_DELAY,
                          allow_resume=True, force_resume=False):
    """Start RTT with automatic polling until ready.

    This convenience function wraps `jlink.rtt_start()` and adds polling logic
    to wait for RTT to be ready. It handles search range auto-detection and
    exponential backoff polling.

    Args:
        jlink: JLink instance (must be opened and connected to device)
        search_ranges (list, optional): List of (start, end) address tuples.
                                       If None, auto-generates from device RAM.
                                       Format: [(start_addr, end_addr), ...]
        block_address (int, optional): Explicit RTT control block address.
                                      If provided, uses this address directly.
        timeout (float): Maximum time to wait for RTT to be ready (seconds).
                        Default: 10.0
        poll_interval (float): Initial polling interval (seconds).
                               Default: 0.05
        max_poll_interval (float): Maximum polling interval (seconds).
                                  Default: 0.5
        backoff_factor (float): Exponential backoff multiplier.
                                Must be > 1.0. Default: 1.5
        verification_delay (float): Delay after RTT start before first poll (seconds).
                                   Default: 0.1
        allow_resume (bool): If True, resume device if halted. Default: True
        force_resume (bool): If True, resume device even if state ambiguous.
                            Default: False

    Returns:
        bool: True if RTT started successfully and is ready, False if timeout.

    Raises:
        ValueError: If polling parameters are invalid.
        JLinkRTTException: If RTT start fails.

    Example:
        Start RTT with auto-detected ranges::

            >>> if start_rtt_with_polling(jlink):
            ...     data = jlink.rtt_read(0, 1024)

        Start RTT with explicit search range::

            >>> ranges = [(0x20000000, 0x2003FFFF)]
            >>> if start_rtt_with_polling(jlink, search_ranges=ranges, timeout=5.0):
            ...     print("RTT ready!")

        Start RTT with explicit block address::

            >>> addr = jlink.rtt_get_block_address()
            >>> if addr and start_rtt_with_polling(jlink, block_address=addr):
            ...     print("RTT ready!")

    Note:
        This function polls by checking `rtt_get_num_up_buffers()` > 0.
        If RTT is not ready within the timeout, returns False.

        The polling uses exponential backoff: poll_interval increases by
        backoff_factor each iteration, up to max_poll_interval.

    Related:
        - jlink.rtt_start(): Low-level RTT start (no polling)
        - auto_detect_rtt_ranges(): Auto-generate search ranges
        - Issue #249: RTT auto-detection fails
    """
    # Validate polling parameters
    if timeout <= 0:
        raise ValueError('timeout must be greater than 0, got %f' % timeout)
    if poll_interval <= 0:
        raise ValueError('poll_interval must be greater than 0, got %f' % poll_interval)
    if max_poll_interval < poll_interval:
        raise ValueError(
            'max_poll_interval (%f) must be >= poll_interval (%f)' % (
                max_poll_interval, poll_interval
            )
        )
    if backoff_factor <= 1.0:
        raise ValueError(
            'backoff_factor must be greater than 1.0, got %f' % backoff_factor
        )
    if verification_delay < 0:
        raise ValueError(
            'verification_delay must be >= 0, got %f' % verification_delay
        )

    # Auto-generate search ranges if not provided and block_address not provided
    if search_ranges is None and block_address is None:
        search_ranges = auto_detect_rtt_ranges(jlink)
        if search_ranges is None:
            logger.warning("Could not auto-detect search ranges, trying without ranges")
            # Continue anyway - J-Link might find it with default detection

    # Start RTT (low-level API - no polling)
    jlink.rtt_start(
        block_address=block_address,
        search_ranges=search_ranges,
        allow_resume=allow_resume,
        force_resume=force_resume
    )

    # Wait for verification delay before first poll
    if verification_delay > 0:
        time.sleep(verification_delay)

    # Poll for RTT readiness
    start_time = time.time()
    current_interval = poll_interval

    while time.time() - start_time < timeout:
        try:
            # Check if RTT is ready by checking for up buffers
            num_up = jlink.rtt_get_num_up_buffers()
            if num_up > 0:
                logger.info("RTT is ready with %d up buffer(s)", num_up)
                return True
        except Exception as e:
            # RTT might not be ready yet, continue polling
            logger.debug("RTT not ready yet: %s", e)

        # Wait before next poll
        time.sleep(current_interval)

        # Exponential backoff
        current_interval = min(
            current_interval * backoff_factor,
            max_poll_interval
        )

    # Timeout
    logger.warning("RTT did not become ready within %f seconds", timeout)
    return False


def reconnect_rtt(jlink, search_ranges=None, block_address=None,
                  reset_delay=0.5, **kwargs):
    """Reconnect RTT after device reset.

    This function handles reconnecting RTT after a device reset. It stops
    any existing RTT session, waits for the device to stabilize, and then
    reconfigures all necessary parameters before restarting RTT.

    Important: After a device reset, search ranges and other configuration
    parameters must be reconfigured. This function handles this automatically.

    Args:
        jlink: JLink instance (must be opened and connected to device)
        search_ranges (list, optional): List of (start, end) address tuples.
                                       If None, auto-generates from device RAM.
                                       Format: [(start_addr, end_addr), ...]
        block_address (int, optional): Explicit RTT control block address.
                                      If provided, uses this address directly.
        reset_delay (float): Delay after reset before reconnecting (seconds).
                           Default: 0.5
        **kwargs: Additional arguments passed to start_rtt_with_polling():
                 - timeout, poll_interval, max_poll_interval, backoff_factor,
                   verification_delay, allow_resume, force_resume

    Returns:
        bool: True if RTT reconnected successfully, False if timeout.

    Raises:
        ValueError: If parameters are invalid.
        JLinkRTTException: If RTT start fails.

    Example:
        Reconnect RTT after reset::

            >>> jlink.reset()
            >>> if reconnect_rtt(jlink, search_ranges=[(0x20000000, 0x2003FFFF)]):
            ...     print("RTT reconnected!")

        Reconnect with auto-detected ranges::

            >>> jlink.reset()
            >>> if reconnect_rtt(jlink):
            ...     data = jlink.rtt_read(0, 1024)

    Note:
        This function:
        1. Stops any existing RTT session
        2. Waits for device to stabilize (reset_delay)
        3. Reconfigures search ranges (critical after reset)
        4. Restarts RTT with polling

        The search ranges MUST be reconfigured after a reset because the
        RTT control block address may have changed.

    Related:
        - start_rtt_with_polling(): Start RTT with polling
        - Issue #252: Reset detection via SWD/JTAG
    """
    # Stop any existing RTT session
    try:
        jlink.rtt_stop()
        logger.debug("Stopped existing RTT session")
    except Exception as e:
        logger.debug("No existing RTT session to stop: %s", e)

    # Wait for device to stabilize after reset
    if reset_delay > 0:
        logger.debug("Waiting %f seconds for device to stabilize after reset", reset_delay)
        time.sleep(reset_delay)

    # Reconfigure and restart RTT
    # Important: search_ranges must be reconfigured after reset
    return start_rtt_with_polling(
        jlink,
        search_ranges=search_ranges,
        block_address=block_address,
        **kwargs
    )


def rtt_context(jlink, search_ranges=None, block_address=None, **kwargs):
    """Context manager for automatic RTT cleanup.

    This context manager automatically starts RTT when entering and stops
    it when exiting, ensuring proper cleanup even if an exception occurs.

    Args:
        jlink: JLink instance (must be opened and connected to device)
        search_ranges (list, optional): List of (start, end) address tuples.
                                       If None, auto-generates from device RAM.
        block_address (int, optional): Explicit RTT control block address.
        **kwargs: Additional arguments passed to start_rtt_with_polling():
                 - timeout, poll_interval, max_poll_interval, backoff_factor,
                   verification_delay, allow_resume, force_resume

    Yields:
        JLink: The JLink instance for use in the context.

    Example:
        Use RTT in a context manager::

            >>> with rtt_context(jlink, search_ranges=[(0x20000000, 0x2003FFFF)]) as j:
            ...     data = j.rtt_read(0, 1024)
            ...     print(data)
            # RTT automatically stopped when exiting context

        With auto-detected ranges::

            >>> with rtt_context(jlink) as j:
            ...     while True:
            ...         data = j.rtt_read(0, 1024)
            ...         if data:
            ...             print(bytes(data))

    Note:
        RTT is automatically stopped when exiting the context, even if an
        exception occurs. This ensures proper cleanup.

    Related:
        - start_rtt_with_polling(): Start RTT with polling
    """
    from contextlib import contextmanager

    @contextmanager
    def _rtt_context():
        try:
            success = start_rtt_with_polling(
                jlink,
                search_ranges=search_ranges,
                block_address=block_address,
                **kwargs
            )
            if not success:
                logger.warning("RTT did not start successfully in context manager")
            yield jlink
        finally:
            try:
                jlink.rtt_stop()
                logger.debug("Stopped RTT in context manager cleanup")
            except Exception as e:
                logger.debug("Error stopping RTT in context manager: %s", e)

    return _rtt_context()


def monitor_rtt_with_reset_detection(jlink, search_ranges=None,
                                     block_address=None,
                                     reset_check_interval=1.0,
                                     **kwargs):
    """Monitor RTT with automatic reset detection and reconnection.

    This function continuously monitors RTT and automatically reconnects if
    a device reset is detected. It uses `check_connection_health()` if available
    to detect resets.

    Args:
        jlink: JLink instance (must be opened and connected to device)
        search_ranges (list, optional): List of (start, end) address tuples.
                                       If None, auto-generates from device RAM.
        block_address (int, optional): Explicit RTT control block address.
        reset_check_interval (float): Interval between reset checks (seconds).
                                     Default: 1.0
        **kwargs: Additional arguments passed to start_rtt_with_polling():
                 - timeout, poll_interval, max_poll_interval, backoff_factor,
                   verification_delay, allow_resume, force_resume

    Yields:
        bytes: Data read from RTT buffer 0.

    Example:
        Monitor RTT with reset detection::

            >>> for data in monitor_rtt_with_reset_detection(jlink):
            ...     if data:
            ...         print(bytes(data))

    Note:
        This is a generator function that yields data from RTT buffer 0.
        It automatically detects resets and reconnects RTT when needed.

        Reset detection uses `check_connection_health()` if available
        (from Issue #252). If not available, it detects resets by checking
        if RTT becomes inactive.

    Related:
        - start_rtt_with_polling(): Start RTT with polling
        - reconnect_rtt(): Reconnect RTT after reset
        - Issue #252: Reset detection via SWD/JTAG
    """
    # Start RTT initially
    if not start_rtt_with_polling(
        jlink,
        search_ranges=search_ranges,
        block_address=block_address,
        **kwargs
    ):
        logger.error("Failed to start RTT for monitoring")
        return

    last_reset_check = time.time()

    try:
        while True:
            # Check for reset periodically
            if time.time() - last_reset_check >= reset_check_interval:
                last_reset_check = time.time()

                reset_detected = False

                # Try to use check_connection_health() if available (Issue #252)
                if hasattr(jlink, 'check_connection_health'):
                    try:
                        if not jlink.check_connection_health():
                            reset_detected = True
                            logger.info("Reset detected via connection health check")
                    except Exception as e:
                        logger.debug("Connection health check failed: %s", e)
                else:
                    # Fallback: check if RTT is still active
                    try:
                        if not jlink.rtt_is_active():
                            reset_detected = True
                            logger.info("Reset detected via RTT inactive check")
                    except Exception as e:
                        logger.debug("RTT active check failed: %s", e)
                        reset_detected = True  # Assume reset if check fails

                if reset_detected:
                    logger.info("Device reset detected, reconnecting RTT...")
                    if reconnect_rtt(
                        jlink,
                        search_ranges=search_ranges,
                        block_address=block_address,
                        **kwargs
                    ):
                        logger.info("RTT reconnected successfully")
                    else:
                        logger.error("Failed to reconnect RTT after reset")
                        break

            # Read data from RTT
            try:
                data = jlink.rtt_read(0, 1024)
                if data:
                    yield bytes(data)
            except Exception as e:
                # RTT read failed - might be reset or other issue
                logger.debug("RTT read failed: %s", e)
                # Check for reset on next iteration
                time.sleep(0.1)

    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    finally:
        # Stop RTT when done
        try:
            jlink.rtt_stop()
        except Exception:
            pass


def read_rtt_without_echo(jlink, buffer_index=0, num_bytes=1024):
    """Read RTT data without local echo.

    This helper function reads data from RTT and filters out local echo
    characters, which is useful when RTT is configured with local echo enabled.

    Args:
        jlink: JLink instance (RTT must be started)
        buffer_index (int): RTT buffer index to read from. Default: 0
        num_bytes (int): Maximum number of bytes to read. Default: 1024

    Returns:
        bytes: Data read from RTT, with local echo characters filtered out.

    Raises:
        ValueError: If buffer_index is negative or num_bytes is negative.
        JLinkRTTException: If RTT read fails (from underlying rtt_read()).

    Example:
        Read RTT without echo::

            >>> data = read_rtt_without_echo(jlink)
            >>> print(data.decode('utf-8', errors='ignore'))

    Note:
        This function filters out common local echo characters:
        - Backspace (0x08)
        - Carriage return (0x0D) when followed by newline
        - Other control characters that might be echo artifacts

        This is a simple filter - for more complex echo handling, implement
        custom logic based on your firmware's echo behavior.

    Related:
        - jlink.rtt_read(): Low-level RTT read
        - Issue #111: Local echo option
    """
    # Validate parameters
    if jlink is None:
        raise ValueError("jlink cannot be None")
    if buffer_index < 0:
        raise ValueError("Buffer index cannot be negative: %d" % buffer_index)
    if num_bytes < 0:
        raise ValueError("Number of bytes cannot be negative: %d" % num_bytes)
    
    try:
        data = jlink.rtt_read(buffer_index, num_bytes)
        if not data:
            return b''

        # Filter out local echo characters
        # Common echo patterns:
        # - Backspace (0x08)
        # - Carriage return (0x0D) when it's just echo (not part of CRLF)
        filtered = []
        i = 0
        while i < len(data):
            byte = data[i]

            # Skip backspace
            if byte == 0x08:
                i += 1
                continue

            # Skip standalone carriage return (might be echo)
            # Keep CRLF sequences (0x0D 0x0A)
            if byte == 0x0D:
                if i + 1 < len(data) and data[i + 1] == 0x0A:
                    # CRLF - keep both
                    filtered.append(byte)
                    filtered.append(data[i + 1])
                    i += 2
                    continue
                else:
                    # Standalone CR - might be echo, skip it
                    i += 1
                    continue

            filtered.append(byte)
            i += 1

        return bytes(filtered)

    except Exception as e:
        logger.debug("Error reading RTT without echo: %s", e)
        return b''

