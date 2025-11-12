# RTT Issues - Test Scripts and Documentation

This directory contains test scripts and documentation for RTT-related issues that were fixed.

Each issue has its own directory with:
- `README.md` - Relaxed summary of the problem and how it was solved
- `test_issue_XXX.py` - Test script that validates the fix

## Issues Fixed

### Critical Issues
- **[Issue #249](249/)** - RTT Auto-detection Fails
- **[Issue #233](249/)** - RTT doesn't connect (same root cause as #249)
- **[Issue #209](209/)** - Option to Set RTT Search Range
- **[Issue #51](51/)** - Initialize RTT with Address

### High Priority Issues
- **[Issue #171](171/)** - exec_command() Raises Exception on Success
- **[Issue #234](234/)** - RTT Write Returns 0
- **[Issue #160](160/)** - Error Code -11 Handling

### Medium Priority Issues
- **[Issue #251](251/)** - Specify JLink Home Path
- **[Issue #111](111/)** - RTT Echo (Local Echo Option)
- **[Issue #161](161/)** - Specify RTT Telnet Port (SDK limitation documented)

### Improvements
- **[Device Name Validation](device_name_validation/)** - Improved device name validation and error messages (related to Issue #249)

## Running Tests

Each test script can be run independently:

```bash
# Test Issue #249
cd issues/249
python3 test_issue_249.py

# Test Issue #234
cd ../234
python3 test_issue_234.py

# etc.
```

Most tests require:
- J-Link hardware connected
- Target device connected
- Firmware with RTT configured

Some tests may skip if hardware is not available or if specific conditions aren't met (e.g., firmware without down buffers for Issue #234).

## Test Results

All tests use a consistent format:
- ✅ PASS - Test passed
- ❌ FAIL - Test failed
- ⚠️  SKIP - Test skipped (conditions not met)

Tests exit with code 0 if all tests pass, code 1 if any test fails.

