# Issue #51: Initialize RTT with Address of RTT Control Block

## The Problem

This is the oldest RTT issue (from 2019). If you already knew the exact address of the RTT control block (e.g., from the linker .map file), there was no way to tell `rtt_start()` "use this address directly".

You had to let the code search, even when you already knew where it was.

## How It Was Fixed

Now you can pass the exact address directly to `rtt_start()` with the `block_address` parameter:

```python
# If you know the address from .map file
jlink.rtt_start(block_address=0x20004620)  # Example address for nRF54L15

# Or find it first
addr = jlink.rtt_get_block_address([(0x20000000, 0x2003FFFF)])
if addr:
    jlink.rtt_start(block_address=addr)
```

It's faster and more reliable than searching, especially when you already have the linker information.

## Testing

See `test_issue_51.py` for scripts that validate the `block_address` parameter.

### Test Results

**Note:** These tests require a J-Link connected with a target device (e.g., nRF54L15) and firmware with RTT configured.

**Test Coverage:**
- ✅ block_address parameter (using explicit address)
- ✅ block_address validation (reject 0, accept None, reject invalid addresses)
- ✅ block_address precedence over search_ranges

**Example Output (when hardware is connected):**
```
==================================================
Issue #51: Block Address Parameter Tests
==================================================
✅ PASS: block_address parameter
✅ PASS: block_address validation
✅ PASS: block_address precedence

🎉 All tests passed!
```

**To run tests:**
```bash
python3 test_issue_51.py
```

