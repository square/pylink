# Issue #209: Option to Set RTT Search Range

## The Problem

There was no way to specify where to search for the RTT control block. The code tried to auto-detect but failed on many devices, especially newer ones like nRF54L15.

If you knew where RTT was in memory (e.g., from the linker map), there was no way to tell the code "search here".

## How It Was Fixed

Now you can explicitly specify search ranges or even the exact address of the control block.

**New options:**

1. **`search_ranges` in `rtt_start()`** - Specify where to search:
```python
ranges = [(0x20000000, 0x2003FFFF)]  # nRF54L15 RAM
jlink.rtt_start(search_ranges=ranges)
```

2. **`rtt_get_block_address()`** - Search for the block in memory and get the address:
```python
addr = jlink.rtt_get_block_address([(0x20000000, 0x2003FFFF)])
if addr:
    print(f"Found at 0x{addr:X}")
    jlink.rtt_start(block_address=addr)
```

3. **`block_address` in `rtt_start()`** - If you already know the exact address:
```python
jlink.rtt_start(block_address=0x20004620)  # Example address for nRF54L15
```

4. **`auto_detect_rtt_ranges()` in `pylink.rtt`** - Auto-generates ranges:
```python
from pylink.rtt import auto_detect_rtt_ranges
ranges = auto_detect_rtt_ranges(jlink)
```

Now you have full control over where to search for RTT.

## Testing

See `test_issue_209.py` for scripts that validate all these options.

### Test Results

**Note:** These tests require a J-Link connected with a target device (e.g., nRF54L15) and firmware with RTT configured.

**Test Coverage:**
- ✅ Explicit search_ranges parameter
- ✅ rtt_get_block_address() method
- ✅ block_address parameter
- ✅ auto_detect_rtt_ranges() function
- ✅ Multiple search ranges
- ✅ Invalid search ranges detection (empty ranges, start > end)

**Example Output (when hardware is connected):**
```
==================================================
Issue #209: RTT Search Range Tests
==================================================
✅ PASS: Explicit search_ranges
✅ PASS: rtt_get_block_address()
✅ PASS: block_address parameter
✅ PASS: auto_detect_rtt_ranges()
✅ PASS: Multiple search ranges
✅ PASS: Invalid search ranges detection

🎉 All tests passed!
```

**To run tests:**
```bash
python3 test_issue_209.py
```

