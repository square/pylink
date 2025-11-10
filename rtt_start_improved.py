# Versión Mejorada de rtt_start() con Todas las Mejoras

"""
Este archivo contiene una versión mejorada del método rtt_start() con todas las mejoras propuestas.
Puede usarse como referencia para implementar las mejoras en el código real.
"""

import logging
import time
from typing import List, Tuple, Optional, Union

logger = logging.getLogger(__name__)

# ============================================================================
# FUNCIÓN AUXILIAR: Validación de Search Ranges
# ============================================================================

def _validate_search_range(start: int, end_or_size: int, is_size: bool = False) -> Tuple[int, int]:
    """
    Validates and normalizes a search range.
    
    Args:
        start: Start address (int)
        end_or_size: End address (if is_size=False) or size (if is_size=True)
        is_size: If True, end_or_size is interpreted as size; otherwise as end address
    
    Returns:
        Tuple[int, int]: Normalized (start, size) tuple
    
    Raises:
        ValueError: If range is invalid
    """
    # Normalize to unsigned 32-bit
    start = int(start) & 0xFFFFFFFF
    end_or_size = int(end_or_size) & 0xFFFFFFFF
    
    if is_size:
        size = end_or_size
        if size == 0:
            raise ValueError("Search range size must be greater than 0")
        if size > 0x1000000:  # 16MB max (reasonable limit)
            raise ValueError(f"Search range size 0x{size:X} exceeds maximum of 16MB (0x1000000)")
        end = (start + size - 1) & 0xFFFFFFFF
    else:
        end = end_or_size
        if end < start:
            # Check if this is actually a wrap-around case
            if (end & 0xFFFFFFFF) < (start & 0xFFFFFFFF):
                raise ValueError(
                    f"End address 0x{end:X} must be >= start address 0x{start:X} "
                    f"(or provide size instead of end address)"
                )
        size = (end - start + 1) & 0xFFFFFFFF
        if size == 0:
            raise ValueError("Search range size is zero (start == end)")
        if size > 0x1000000:  # 16MB max
            raise ValueError(f"Search range size 0x{size:X} exceeds maximum of 16MB (0x1000000)")
    
    return (start, size)


# ============================================================================
# MÉTODO MEJORADO: rtt_start()
# ============================================================================

def rtt_start_improved(
    self,
    block_address=None,
    search_ranges=None,
    reset_before_start=False,
    rtt_timeout=10.0,          # Maximum time to wait for RTT (seconds)
    poll_interval=0.05,         # Initial polling interval (seconds)
    max_poll_interval=0.5,      # Maximum polling interval (seconds)
    backoff_factor=1.5,         # Exponential backoff multiplier
    verification_delay=0.1,     # Delay before verification check (seconds)
    allow_resume=True,          # If False, never resume device even if halted
    force_resume=False,         # If True, resume even if state is ambiguous
):
    """
    Starts RTT processing, including background read of target data.
    
    This method has been enhanced with automatic search range generation,
    improved device state management, and configurable polling parameters
    for better reliability across different devices.
    
    Args:
        self (JLink): the ``JLink`` instance
        block_address (int, optional): Optional configuration address for the RTT block.
            If None, auto-detection will be attempted first.
        search_ranges (List[Tuple[int, int]], optional): Optional list of (start, end)
            address ranges to search for RTT control block. Uses SetRTTSearchRanges command.
            Format: [(start_addr, end_addr), ...]
            Example: [(0x20000000, 0x2003FFFF)] for nRF54L15 RAM range.
            If None, automatically generated from device RAM info.
            Only the first range is used if multiple are provided.
            Range is validated: start <= end, size > 0, size <= 16MB.
        reset_before_start (bool, optional): If True, reset the device before starting RTT.
            Default: False
        rtt_timeout (float, optional): Maximum time (seconds) to wait for RTT detection.
            Default: 10.0
        poll_interval (float, optional): Initial polling interval (seconds).
            Default: 0.05
        max_poll_interval (float, optional): Maximum polling interval (seconds).
            Default: 0.5
        backoff_factor (float, optional): Exponential backoff multiplier.
            Default: 1.5
        verification_delay (float, optional): Delay (seconds) before verification check.
            Default: 0.1
        allow_resume (bool, optional): If True, resume device if halted. Default: True.
        force_resume (bool, optional): If True, resume device even if state is ambiguous.
            Default: False
    
    Returns:
        ``None``
    
    Raises:
        JLinkRTTException: if the underlying JLINK_RTTERMINAL_Control call fails
            or RTT control block not found (only when block_address specified).
        ValueError: if search_ranges are invalid.
        JLinkException: if device state operations fail and force_resume=True.
    
    Examples:
        >>> # Auto-detection with default settings
        >>> jlink.rtt_start()
        
        >>> # Explicit search range
        >>> jlink.rtt_start(search_ranges=[(0x20000000, 0x2003FFFF)])
        
        >>> # Specific control block address
        >>> jlink.rtt_start(block_address=0x200044E0)
        
        >>> # Custom timeout for slow devices
        >>> jlink.rtt_start(rtt_timeout=20.0)
        
        >>> # Don't modify device state
        >>> jlink.rtt_start(allow_resume=False)
    """
    # Stop RTT if it's already running (to ensure clean state)
    # Multiple stops ensure RTT is fully stopped and ranges are cleared
    logger.debug("Stopping any existing RTT session...")
    for i in range(3):
        try:
            self.rtt_stop()
            time.sleep(0.1)
        except Exception as e:
            if i == 0:  # Log only first attempt
                logger.debug(f"RTT stop attempt {i+1} failed (may not be running): {e}")
    time.sleep(0.3)  # Wait for RTT to fully stop before proceeding
    
    # Ensure device is properly configured for RTT auto-detection
    # According to SEGGER KB, Device name must be set correctly before RTT start
    if hasattr(self, '_device') and self._device:
        try:
            device_name = self._device.name
            logger.debug(f"Re-confirming device name: {device_name}")
            self.exec_command(f'Device = {device_name}')
            time.sleep(0.1)
        except Exception as e:
            logger.warning(f"Failed to re-confirm device name: {e}")
    
    # Reset if requested
    if reset_before_start and self.target_connected():
        try:
            logger.debug("Resetting device before RTT start...")
            self.reset(ms=1)
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"Failed to reset device: {e}")
    
    # Ensure device is running (RTT requires running CPU)
    if allow_resume:
        try:
            is_halted = self._dll.JLINKARM_IsHalted()
            if is_halted == 1:  # Device is definitely halted
                logger.debug("Device is halted, resuming...")
                self._dll.JLINKARM_Go()
                time.sleep(0.3)
            elif force_resume and is_halted == -1:  # Ambiguous state
                logger.debug("Device state ambiguous, forcing resume...")
                self._dll.JLINKARM_Go()
                time.sleep(0.3)
            elif is_halted == 0:
                logger.debug("Device is running")
            # is_halted == -1 and not force_resume: ambiguous, assume running
        except Exception as e:
            logger.warning(f"Failed to check/resume device state: {e}")
            if force_resume:
                raise errors.JLinkException(f"Device state check failed: {e}")
            # Otherwise, assume device is running
    
    # Set search ranges if provided or if we can derive from device info
    # IMPORTANT: SetRTTSearchRanges must be called BEFORE rtt_control(START)
    # NOTE: According to UM08001, SetRTTSearchRanges expects (start_address, size) format
    search_range_used = None
    
    if search_ranges and len(search_ranges) > 0:
        # Validate and use the first range
        start_addr, end_addr = search_ranges[0]
        try:
            start_addr, size = _validate_search_range(start_addr, end_addr, is_size=False)
            search_range_used = f"0x{start_addr:X} - 0x{(start_addr + size - 1) & 0xFFFFFFFF:X} (size: 0x{size:X})"
            logger.debug(f"Using provided search range: {search_range_used}")
            
            cmd = f"SetRTTSearchRanges {start_addr:X} {size:X}"
            try:
                result = self.exec_command(cmd)
                if result != 0:
                    logger.warning(f"SetRTTSearchRanges returned non-zero: {result}")
                time.sleep(0.3)
            except errors.JLinkException as e:
                logger.error(f"Failed to set RTT search ranges: {e}")
                # Continue anyway - auto-detection may work without explicit ranges
            except Exception as e:
                logger.error(f"Unexpected error setting search ranges: {e}")
        except ValueError as e:
            logger.error(f"Invalid search range: {e}")
            raise  # Re-raise ValueError for invalid input
        
        # Log if multiple ranges provided (only first is used)
        if len(search_ranges) > 1:
            logger.warning(
                f"Multiple search ranges provided ({len(search_ranges)}), "
                f"only using first: {search_range_used}"
            )
    
    elif hasattr(self, '_device') and self._device and hasattr(self._device, 'RAMAddr'):
        # Auto-generate search ranges from device RAM info
        ram_start = self._device.RAMAddr
        ram_size = self._device.RAMSize if hasattr(self._device, 'RAMSize') else None
        
        if ram_size:
            try:
                ram_start = int(ram_start) & 0xFFFFFFFF
                ram_size = int(ram_size) & 0xFFFFFFFF
                search_range_used = f"0x{ram_start:X} - 0x{(ram_start + ram_size - 1) & 0xFFFFFFFF:X} (auto, size: 0x{ram_size:X})"
                logger.debug(f"Auto-generated search range from device RAM: {search_range_used}")
                
                cmd = f"SetRTTSearchRanges {ram_start:X} {ram_size:X}"
                try:
                    result = self.exec_command(cmd)
                    if result != 0:
                        logger.warning(f"SetRTTSearchRanges returned non-zero: {result}")
                    time.sleep(0.1)
                except errors.JLinkException as e:
                    logger.warning(f"Failed to set auto-generated search ranges: {e}")
                except Exception as e:
                    logger.warning(f"Unexpected error setting auto-generated ranges: {e}")
            except Exception as e:
                logger.warning(f"Error generating search ranges from RAM info: {e}")
        else:
            # Fallback: use common 64KB range
            try:
                ram_start = int(ram_start) & 0xFFFFFFFF
                fallback_size = 0x10000  # 64KB
                search_range_used = f"0x{ram_start:X} - 0x{(ram_start + fallback_size - 1) & 0xFFFFFFFF:X} (fallback, size: 0x{fallback_size:X})"
                logger.debug(f"Using fallback search range: {search_range_used}")
                
                cmd = f"SetRTTSearchRanges {ram_start:X} {fallback_size:X}"
                try:
                    result = self.exec_command(cmd)
                    if result != 0:
                        logger.warning(f"SetRTTSearchRanges returned non-zero: {result}")
                    time.sleep(0.1)
                except errors.JLinkException as e:
                    logger.warning(f"Failed to set fallback search ranges: {e}")
                except Exception as e:
                    logger.warning(f"Unexpected error setting fallback ranges: {e}")
            except Exception as e:
                logger.warning(f"Error setting fallback search range: {e}")
    
    # Start RTT
    config = None
    if block_address is not None:
        config = structs.JLinkRTTerminalStart()
        config.ConfigBlockAddress = block_address
        logger.debug(f"Starting RTT with specific control block address: 0x{block_address:X}")
    else:
        logger.debug("Starting RTT with auto-detection...")
    
    self.rtt_control(enums.JLinkRTTCommand.START, config)
    
    # Wait after START command before polling
    time.sleep(0.5)
    
    # Poll for RTT to be ready
    start_time = time.time()
    wait_interval = poll_interval
    attempt_count = 0
    
    logger.debug(f"Polling for RTT buffers (timeout: {rtt_timeout}s, initial interval: {poll_interval}s)...")
    
    while (time.time() - start_time) < rtt_timeout:
        attempt_count += 1
        time.sleep(wait_interval)
        
        try:
            num_buffers = self.rtt_get_num_up_buffers()
            if num_buffers > 0:
                # Found buffers, verify they persist
                time.sleep(verification_delay)
                try:
                    num_buffers_check = self.rtt_get_num_up_buffers()
                    if num_buffers_check > 0:
                        elapsed = time.time() - start_time
                        logger.info(
                            f"RTT control block found after {attempt_count} attempts "
                            f"({elapsed:.2f}s). Search range: {search_range_used or 'none'}"
                        )
                        return  # Success - RTT control block found and stable
                except errors.JLinkRTTException:
                    continue
        except errors.JLinkRTTException as e:
            # Exponential backoff
            if attempt_count % 10 == 0:  # Log every 10 attempts
                elapsed = time.time() - start_time
                logger.debug(
                    f"RTT detection attempt {attempt_count} ({elapsed:.2f}s elapsed): {e}"
                )
            wait_interval = min(wait_interval * backoff_factor, max_poll_interval)
            continue
    
    # Timeout reached
    elapsed = time.time() - start_time
    logger.warning(
        f"RTT control block not found after {attempt_count} attempts "
        f"({elapsed:.2f}s elapsed, timeout={rtt_timeout}s). "
        f"Search range: {search_range_used or 'none'}"
    )
    
    # If block_address was specified, raise exception
    if block_address is not None:
        try:
            self.rtt_stop()
        except:
            pass
        raise errors.JLinkRTTException(
            enums.JLinkRTTErrors.RTT_ERROR_CONTROL_BLOCK_NOT_FOUND,
            f"RTT control block not found after {attempt_count} attempts "
            f"({elapsed:.2f}s elapsed, timeout={rtt_timeout}s). "
            f"Search range: {search_range_used or 'none'}"
        )

