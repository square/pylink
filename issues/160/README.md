# Issue #160: Invalid Error Code -11 from rtt_read()

## The Problem

When `rtt_read()` failed with error -11, you had no idea what it meant. The code just showed you "error -11" and that's it. You had to search SEGGER's documentation or guess what was wrong.

Error -11 can mean several things:
- Device disconnected or reset
- GDB is connected (conflicts with RTT)
- Device is in an invalid state
- RTT control block is corrupted

But without additional information, it was impossible to know which problem it was.

## How It Was Fixed

Now when `rtt_read()` returns error -11, it gives you a detailed message with all possible causes and even tries to verify connection health if available.

**Improved error message:**
```
RTT read failed (error -11). Possible causes:
  1. Device disconnected or reset
  2. GDB server attached (conflicts with RTT)
  3. Device in bad state
  4. RTT control block corrupted or invalid
Enable DEBUG logging for more details.
```

And if `check_connection_health()` is available (Issue #252), it also checks the connection and tells you if the device is disconnected.

Now when you see error -11, you know exactly what to check.

## Testing

See `test_issue_160.py` for scripts that validate the improved error -11 handling.

### Test Results

**Note:** These tests require a J-Link connected with a target device and firmware with RTT configured. To fully test error -11, you may need to simulate error conditions (disconnect device, attach GDB, reset device).

**Test Coverage:**
- ✅ Error -11 message format (detailed diagnostics)
- ✅ Connection health check integration (if available)
- ✅ Normal read still works
- ✅ Invalid read parameters detection (negative index, negative num_bytes, invalid buffer index)

**Example Output (when hardware is connected):**
```
==================================================
Issue #160: Error Code -11 Handling Tests
==================================================
✅ PASS: Error message format
✅ PASS: Connection health check
✅ PASS: Normal read
✅ PASS: Invalid read parameters detection

🎉 All tests passed!
```

**To run tests:**
```bash
python3 test_issue_160.py
```

**To test error -11 scenarios:**
1. Disconnect device while RTT is active
2. Attach GDB debugger (conflicts with RTT)
3. Reset device while RTT is active

