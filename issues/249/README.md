# Issue #249: RTT Auto-detection Fails

## The Problem

When you tried to use `rtt_start()` on devices like nRF54L15, it just wouldn't work. RTT wouldn't connect even though the firmware had RTT configured correctly and SEGGER RTT Viewer worked perfectly.

The problem was that `rtt_start()` tried to auto-detect the RTT control block but failed on certain devices. There was no way to explicitly specify where to search.

## How It Was Fixed

Basically I simplified `rtt_start()` and moved the auto-detection logic to a convenience module.

**Main changes:**
1. `rtt_start()` now accepts `search_ranges` explicitly - if you don't pass it, it uses J-Link's default detection (which can fail)
2. I created `pylink.rtt` with `auto_detect_rtt_ranges()` that generates ranges from device info
3. And `start_rtt_with_polling()` that does all the heavy lifting: detects ranges, configures, and waits until RTT is ready

**For nRF54L15 specifically:**
```python
# Now it works like this:
import pylink
from pylink.rtt import start_rtt_with_polling

jlink = pylink.JLink()
jlink.open()
jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
jlink.connect('NRF54L15_M33')

# Option 1: Auto-detection (new)
if start_rtt_with_polling(jlink):
    data = jlink.rtt_read(0, 1024)

# Option 2: Explicit ranges (always works)
ranges = [(0x20000000, 0x2003FFFF)]
if start_rtt_with_polling(jlink, search_ranges=ranges):
    data = jlink.rtt_read(0, 1024)
```

## Testing

See `test_issue_249.py` for scripts that validate the fix.

### Test Results

**Note:** These tests require a J-Link connected with a target device (e.g., nRF54L15) and firmware with RTT configured.

**Test Coverage:**
- ✅ Auto-detect RTT search ranges
- ✅ Start RTT with auto-detection
- ✅ Start RTT with explicit search ranges
- ✅ Low-level API backward compatibility
- ✅ Invalid search ranges detection (empty ranges, start > end, range > 16MB)

**Example Output (when hardware is connected):**
```
==================================================
Issue #249: RTT Auto-detection Tests
==================================================
✅ PASS: Auto-detect ranges
✅ PASS: Start with auto-detection
✅ PASS: Start with explicit ranges
✅ PASS: Low-level API compatibility
✅ PASS: Invalid search ranges detection

🎉 All tests passed!
```

**To run tests:**
```bash
python3 test_issue_249.py
```

