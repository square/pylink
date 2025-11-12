# Device Name Validation and Suggestions Tests

This directory contains tests for the improved device name validation and suggestion functionality in `pylink.jlink.get_device_index()` and `pylink.jlink.connect()`.

## Overview

The tests verify that:
- Invalid inputs (None, empty strings, whitespace) are properly validated
- Common naming variations are suggested (e.g., `CORTEX_M33` → `Cortex-M33`)
- Error messages are informative and helpful
- Valid device names connect successfully

## Test Script

### `test_device_name_validation.py`

Comprehensive test suite covering all validation and suggestion scenarios.

**Usage:**
```bash
cd sandbox/pylink/issues/device_name_validation
python3 test_device_name_validation.py
```

**Configuration:**
- Adjust the `DEVICE_NAME` constant at the top of the script to match your hardware
- Default: `'NRF54L15_M33'`

## Test Cases

### 1. None Device Name
- **Input**: `None`
- **Expected**: `ValueError` with informative message
- **Purpose**: Validates that None is caught early

### 2. Empty String Device Name
- **Input**: `''`
- **Expected**: `ValueError` with informative message
- **Purpose**: Validates that empty strings are rejected

### 3. Whitespace-Only Device Name
- **Input**: `'   '`
- **Expected**: `ValueError` (after `.strip()`)
- **Purpose**: Validates that whitespace-only strings are treated as empty

### 4. Cortex Naming Variation
- **Input**: `'CORTEX_M33'`
- **Expected**: `JLinkException` suggesting `'Cortex-M33'`
- **Purpose**: Tests common Cortex naming pattern correction

### 5. Nordic Naming Variation
- **Input**: `'NRF54L15'`
- **Expected**: `JLinkException` suggesting `'NRF54L15_M33'`
- **Purpose**: Tests common Nordic naming pattern correction

### 6. Completely Wrong Device Name
- **Input**: `'WRONG_DEVICE_NAME_XYZ'`
- **Expected**: `JLinkException` with basic error message
- **Purpose**: Tests that completely invalid names don't cause crashes

### 7. Valid Device Name
- **Input**: `DEVICE_NAME` (configurable)
- **Expected**: Successful connection
- **Purpose**: Validates that valid names still work correctly

### 8. Direct `get_device_index()` Calls
- **Input**: Various invalid inputs
- **Expected**: Appropriate exceptions
- **Purpose**: Tests the low-level API directly

## Implementation Details

### Validation Logic
- **Location**: `pylink/jlink.py::get_device_index()`
- **Validation**: Checks for None, non-string types, and empty strings (after `.strip()`)
- **Performance**: O(1) - no iteration or heavy computation

### Suggestion Logic
- **Location**: `pylink/jlink.py::_try_device_name_variations()`
- **Approach**: Lightweight pattern matching for common variations
- **Performance**: O(1) - only tries a few predefined patterns
- **No heavy searching**: Does not iterate through all devices

### Common Patterns Handled
1. **Cortex naming**: `CORTEX_M33` → `Cortex-M33`
2. **Nordic naming**: `NRF54L15` → `NRF54L15_M33`

## Test Results

```
Total: 8 tests
Passed: 8
Failed: 0

🎉 All tests passed!
```

## Notes

- Tests require a J-Link device to be connected
- Test 7 (valid device name) will fail if no hardware is connected
- Adjust `DEVICE_NAME` constant if your hardware uses a different name
- The suggestion logic is lightweight and non-intrusive - it only tries a few common patterns without searching through all devices

## Related Issues

- **Issue #249**: RTT auto-detection improvements
  - Device name validation was added as part of my work on Issue #249
  - Improves UX when using `connect()` which is required for RTT operations
- Part of the broader RTT improvements and device name validation enhancements I made

