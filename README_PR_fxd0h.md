# Pull Request: Improve RTT Auto-Detection for nRF54L15 and Similar Devices

## Motivation

The `rtt_start()` method in pylink-square was failing to auto-detect the RTT (Real-Time Transfer) control block on certain devices, specifically the nRF54L15 microcontroller. While SEGGER's RTT Viewer successfully detects and connects to RTT on these devices, pylink's implementation was unable to find the control block, resulting in `JLinkRTTException: The RTT Control Block has not yet been found (wait?)` errors.

This issue affects users who want to use pylink for automated RTT logging and debugging, particularly in CI/CD pipelines or automated test environments where RTT Viewer's GUI is not available.

## Problem Analysis

### Root Causes Identified

1. **Missing Search Range Configuration**: The original `rtt_start()` implementation did not configure RTT search ranges before attempting to start RTT. Some devices, particularly newer ARM Cortex-M devices like the nRF54L15, require explicit search ranges to be set via the `SetRTTSearchRanges` J-Link command.

2. **Insufficient Device State Management**: The implementation did not ensure the target device was running before attempting to start RTT. RTT requires an active CPU to function properly.

3. **Lack of Polling Mechanism**: After sending the RTT START command, the original code did not poll for RTT readiness. Some devices need time for the J-Link library to locate and initialize the RTT control block in memory.

4. **No Auto-Generation of Search Ranges**: When search ranges were not provided, the code made no attempt to derive them from device information available through the J-Link API.

### Device-Specific Findings

For the nRF54L15 device:
- RAM Start Address: `0x20000000`
- RAM Size: `0x00040000` (256 KB)
- Required Search Range: `0x20000000 - 0x2003FFFF` (matches RTT Viewer configuration)
- RTT Control Block Location: `0x200044E0` (within the search range)

The J-Link API provides device RAM information via `JLINK_DEVICE_GetInfo()`, which returns `RAMAddr` and `RAMSize`. This information can be used to automatically generate appropriate search ranges.

## Solution

### Changes Implemented

The `rtt_start()` method has been enhanced with the following improvements:

1. **New Optional Parameters**:
   - `search_ranges`: List of tuples specifying (start, end) address ranges for RTT control block search
   - `reset_before_start`: Boolean flag to reset the device before starting RTT

2. **Automatic Search Range Generation**: 
   - When `search_ranges` is not provided, the method now automatically generates search ranges from device RAM information obtained via the J-Link API
   - Uses the full RAM range: `ram_start` to `ram_start + ram_size - 1`
   - Falls back to a 64KB range if RAM size information is unavailable

3. **Device State Management**:
   - Ensures RTT is fully stopped before starting (multiple stop calls for clean state)
   - Re-confirms device name is set correctly (required for auto-detection per SEGGER KB)
   - Checks if the device is halted and resumes it if necessary
   - Uses direct DLL calls (`JLINKARM_IsHalted()`, `JLINKARM_Go()`) for more reliable state checking
   - Only resumes device if definitely halted (`is_halted == 1`), trusts RTT Viewer behavior for ambiguous states

4. **Polling Mechanism**:
   - After sending the RTT START command, waits 0.5 seconds for initialization
   - Polls `rtt_get_num_up_buffers()` with exponential backoff (0.05s to 0.5s intervals)
   - Maximum wait time of 10 seconds
   - Verifies buffers persist before returning (double-check for stability)
   - Returns immediately when RTT buffers are detected and verified

5. **Backward Compatibility**:
   - All new parameters are optional with sensible defaults
   - Existing code using `rtt_start()` or `rtt_start(block_address)` continues to work unchanged
   - The method maintains the same return value and exception behavior

### Code Changes

The implementation adds approximately 100 lines to the `rtt_start()` method in `pylink/jlink.py`, including:
- Device state verification and resume logic
- Search range configuration via `exec_command("SetRTTSearchRanges ...")`
- Polling loop with timeout handling
- Comprehensive error handling

## Testing

### Test Environment

- Hardware: Seeed Studio nRF54L15 Sense development board
- J-Link: SEGGER J-Link Pro V4
- Firmware: Zephyr RTOS with RTT enabled
- Python: 3.x
- pylink-square: Latest master branch

### Test Scenarios

All tests were performed with the device running firmware that has RTT enabled and verified working with SEGGER RTT Viewer.

1. **Auto-Detection Test**: 
   - Call `rtt_start()` without parameters
   - Verify automatic search range generation from device RAM info
   - Confirm RTT buffers are detected

2. **Explicit Search Ranges Test**:
   - Call `rtt_start(search_ranges=[(0x20000000, 0x2003FFFF)])`
   - Verify custom ranges are used
   - Confirm RTT buffers are detected

3. **Specific Address Test**:
   - Call `rtt_start(block_address=0x200044E0)`
   - Verify specific control block address is used
   - Confirm RTT buffers are detected

4. **Backward Compatibility Test**:
   - Call `rtt_start()` with no parameters (original API)
   - Verify existing code continues to work
   - Confirm RTT buffers are detected

5. **Reset Before Start Test**:
   - Call `rtt_start(reset_before_start=True)`
   - Verify device reset occurs before RTT start
   - Confirm RTT buffers are detected

6. **Combined Parameters Test**:
   - Call `rtt_start()` with multiple optional parameters
   - Verify all parameters work together correctly
   - Confirm RTT buffers are detected

7. **RTT Data Read Test**:
   - Start RTT successfully
   - Read data from RTT buffers
   - Verify data can be retrieved

### Test Results

All 7 test scenarios passed successfully:
- Auto-detection: PASS
- Explicit ranges: PASS
- Specific address: PASS
- Backward compatibility: PASS
- Reset before start: PASS
- Combined parameters: PASS
- RTT data read: PASS

### Comparison with RTT Viewer

The implementation now matches RTT Viewer's behavior:
- Uses the same search range: `0x20000000 - 0x2003FFFF` for nRF54L15
- Detects the same control block address: `0x200044E0`
- Successfully establishes RTT connection and reads data

## Technical Details

### Search Range Configuration

The `SetRTTSearchRanges` command is executed via `exec_command()` before calling `JLINK_RTTERMINAL_Control(START)`. According to SEGGER UM08001 documentation, the command format is:
```
SetRTTSearchRanges <start_addr> <size>
```

Note: The format is `(start, size)`, not `(start, end)`. The implementation converts `(start, end)` tuples to `(start, size)` format internally.

For nRF54L15, this becomes:
```
SetRTTSearchRanges 20000000 40000
```

Where `0x40000` is the size (256 KB) of the RAM range starting at `0x20000000`.

### Polling Implementation

The polling mechanism uses exponential backoff:
- Initial interval: 0.1 seconds
- Maximum interval: 0.5 seconds
- Growth factor: 1.5x per iteration
- Maximum wait time: 10 seconds

The polling checks `rtt_get_num_up_buffers()` which internally calls `JLINK_RTTERMINAL_Control(GETNUMBUF)`. When this returns a value greater than 0, RTT is considered ready.

### Error Handling

The implementation handles several error scenarios gracefully:
- Device state cannot be determined: Assumes device is running and proceeds
- Search range configuration fails: Continues with RTT start attempt
- Device connection state unclear: Proceeds optimistically (RTT Viewer works in similar conditions)

For auto-detection mode (no `block_address` specified), if polling times out, the method returns without raising an exception, allowing the caller to implement fallback strategies. If `block_address` is specified and polling times out, a `JLinkRTTException` is raised.

## Backward Compatibility

This change is fully backward compatible:
- Existing code using `rtt_start()` continues to work
- Existing code using `rtt_start(block_address)` continues to work
- No breaking changes to the API
- All new functionality is opt-in via optional parameters

## Related Issues

This PR addresses:
- Issue #249: RTT auto-detection fails on nRF54L15
- Issue #209: RTT search ranges not configurable

## Code Quality

- Follows pylink-square coding conventions (Google Python Style Guide)
- Maximum line length: 120 characters
- Comprehensive docstrings with Args, Returns, and Raises sections
- No linter errors
- Uses only existing J-Link APIs (no external dependencies)
- No XML parsing or file system access

## Future Considerations

While this implementation solves the immediate problem, future enhancements could include:
- Device-specific search range presets for common devices
- Configurable polling timeout
- More sophisticated device state detection
- Support for multiple simultaneous RTT connections

However, these enhancements are beyond the scope of this PR and can be addressed in future contributions.

## Conclusion

This PR improves RTT auto-detection reliability for devices that require explicit search range configuration, particularly the nRF54L15. The changes are minimal, backward-compatible, and follow pylink-square's design principles of using existing J-Link APIs without adding external dependencies.

The implementation has been tested and verified to work correctly with the nRF54L15 device, matching the behavior of SEGGER's RTT Viewer.

