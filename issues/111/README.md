# Issue #111: RTT Echo (Local Echo Option)

## The Problem

When firmware had local echo enabled, `rtt_read()` returned the characters you typed mixed with the ones actually coming from the device. It was annoying because you had to manually filter echo characters.

## How It Was Fixed

I added `read_rtt_without_echo()` in the `pylink.rtt` module that automatically filters common echo characters:

- Backspace (0x08)
- Standalone carriage return (0x0D when not part of CRLF)
- Other control characters that might be echo

```python
from pylink.rtt import read_rtt_without_echo

# Read without echo
data = read_rtt_without_echo(jlink, buffer_index=0, num_bytes=1024)
```

It's a simple but effective filter for most common cases.

## Testing

See `test_issue_111.py` for scripts that validate echo filtering.

### Test Results

**Note:** These tests require a J-Link connected with a target device and firmware with RTT configured (preferably with local echo enabled).

**Test Coverage:**
- ✅ Echo character filtering (backspace, standalone CR)
- ✅ Compare with normal read (verify filtering works)
- ✅ Empty data handling
- ✅ Invalid echo filter parameters detection (negative index, negative num_bytes, None jlink)

**Example Output (when hardware is connected):**
```
==================================================
Issue #111: RTT Echo Filtering Tests
==================================================
✅ PASS: Echo filtering
✅ PASS: Compare with normal read
✅ PASS: Empty data handling
✅ PASS: Invalid echo filter parameters detection

🎉 All tests passed!
```

**To run tests:**
```bash
python3 test_issue_111.py
```

