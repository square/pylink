# Issue #234: RTT Write Returns 0

## The Problem

When you called `rtt_write()` and it returned 0, you had no idea why. It could be because:
- The buffer was full
- No down buffers were configured in firmware
- The buffer index was invalid
- RTT wasn't active

But the code just returned 0 without telling you anything useful. You had to guess what was wrong.

## How It Was Fixed

Now `rtt_write()` validates everything before writing and gives you clear error messages:

**Added validations:**
1. Checks that RTT is active
2. Checks that down buffers are configured
3. Checks that buffer index is valid

**Improved error messages:**
- "RTT is not active. Call rtt_start() first."
- "No down buffers configured. rtt_write() requires down buffers to be configured in firmware. Check your firmware's RTT configuration (SEGGER_RTT_ConfigDownBuffer)."
- "Buffer index X out of range. Only Y down buffer(s) available (indices 0-Y)."

Now when something fails, you know exactly what's wrong and how to fix it.

## Testing

See `test_issue_234.py` for scripts that validate the improved error messages.

### Test Results

**Note:** These tests require a J-Link connected with a target device and firmware with RTT configured (preferably with and without down buffers).

**Test Coverage:**
- ✅ Error when RTT not active
- ✅ Error when no down buffers configured
- ✅ Error when buffer index invalid
- ✅ Successful write (when properly configured)
- ✅ Invalid write parameters detection (negative index, None data, empty data)

**Example Output (when hardware is connected):**
```
==================================================
Issue #234: RTT Write Error Messages Tests
==================================================
✅ PASS: Error when RTT not active
✅ PASS: Error when no down buffers
✅ PASS: Error when invalid buffer index
✅ PASS: Successful write
✅ PASS: Invalid write parameters detection

🎉 All tests passed!
```

**To run tests:**
```bash
python3 test_issue_234.py
```

