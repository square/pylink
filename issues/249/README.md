# Bug Report for Issue #249

## Environment

- **Operating System**: macOS 24.6.0 (Darwin)
- **J-Link Model**: SEGGER J-Link Pro V4
- **J-Link Firmware**: V4 compiled Sep 22 2022 15:00:37
- **Python Version**: 3.x
- **pylink-square Version**: Latest master branch
- **Target Device**: Seeed Studio nRF54L15 Sense (Nordic nRF54L15 microcontroller)
- **Device RAM**: Start: 0x20000000, Size: 0x00040000 (256 KB)
- **RTT Control Block Address**: 0x200044E0 (verified with SEGGER RTT Viewer)

## Expected Behavior

The `rtt_start()` method should successfully auto-detect the RTT control block on the nRF54L15 device, similar to how SEGGER's RTT Viewer successfully detects and connects to RTT.

Expected flow:
1. Call `jlink.rtt_start()` without parameters
2. Method should automatically detect RTT control block
3. `rtt_get_num_up_buffers()` should return a value greater than 0
4. RTT data can be read from buffers

## Actual Behavior

The `rtt_start()` method fails to auto-detect the RTT control block, raising a `JLinkRTTException`:

```
pylink.errors.JLinkRTTException: The RTT Control Block has not yet been found (wait?)
```

This occurs even though:
- The device firmware has RTT enabled and working (verified with RTT Viewer)
- The RTT control block exists at address 0x200044E0
- SEGGER RTT Viewer successfully connects and reads RTT data
- The device is running and connected via J-Link

## Steps to Reproduce

1. Connect J-Link to nRF54L15 device
2. Flash firmware with RTT enabled
3. Verify RTT works with SEGGER RTT Viewer (optional but recommended)
4. Run the following Python code:

```python
import pylink

jlink = pylink.JLink()
jlink.open()
jlink.connect('NRF54L15_M33', verbose=False)

# This fails with JLinkRTTException
jlink.rtt_start()

# Never reaches here
num_up = jlink.rtt_get_num_up_buffers()
print(f"Found {num_up} up buffers")
```

5. The exception is raised during `rtt_start()` call

## Workaround

Manually set RTT search ranges before calling `rtt_start()`:

```python
jlink.exec_command("SetRTTSearchRanges 20000000 2003FFFF")
jlink.rtt_start()
```

This workaround works, but requires manual configuration and device-specific knowledge.

## Root Cause Analysis

The issue appears to be that `rtt_start()` does not configure RTT search ranges before attempting to start RTT. Some devices, particularly newer ARM Cortex-M devices like the nRF54L15, require explicit search ranges to be set via the `SetRTTSearchRanges` J-Link command.

The J-Link API provides device RAM information via `JLINK_DEVICE_GetInfo()`, which returns `RAMAddr` and `RAMSize`. This information could be used to automatically generate appropriate search ranges, but the current implementation does not do this.

## Additional Information

- **RTT Viewer Configuration**: RTT Viewer uses search range `0x20000000 - 0x2003FFFF` for this device
- **Related Issues**: This may also affect other devices that require explicit search range configuration
- **Impact**: Prevents automated RTT logging in CI/CD pipelines or automated test environments where RTT Viewer's GUI is not available

## Proposed Solution

Enhance `rtt_start()` to:
1. Automatically generate search ranges from device RAM info when available
2. Allow optional `search_ranges` parameter for custom ranges
3. Add polling mechanism to wait for RTT control block initialization
4. Ensure device is running before starting RTT

This would make the method work out-of-the-box for devices like nRF54L15 while maintaining backward compatibility.

