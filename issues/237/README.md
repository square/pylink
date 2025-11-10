# Issue #237: Fix flash_file() return value documentation

## Problem

The `flash_file()` method had misleading variable naming and documentation:
- Variable name `bytes_flashed` suggested it returns number of bytes written
- But `JLINK_DownloadFile()` actually returns a **status code**, not bytes written
- Docstring said "Has no significance" but didn't clarify it's a status code

## Solution

### Changes Made

1. **Renamed variable**: `bytes_flashed` → `status_code`
2. **Updated docstring**: Clarified that return value is a status code from J-Link SDK
3. **Added comment**: Explained that `JLINK_DownloadFile()` returns status code, not bytes
4. **Updated Raises section**: Clarified exception is raised when status code < 0

### Code Changes

**File**: `pylink/jlink.py`  
**Method**: `flash_file()` (lines 2248-2296)

**Before**:
```python
bytes_flashed = self._dll.JLINK_DownloadFile(os.fsencode(path), addr)
if bytes_flashed < 0:
    raise errors.JLinkFlashException(bytes_flashed)
return bytes_flashed
```

**After**:
```python
# Note: JLINK_DownloadFile returns a status code, not the number of bytes written.
# A value >= 0 indicates success, < 0 indicates an error.
status_code = self._dll.JLINK_DownloadFile(os.fsencode(path), addr)
if status_code < 0:
    raise errors.JLinkFlashException(status_code)
return status_code
```

### Documentation Changes

**Returns section**:
- **Before**: "Integer value greater than or equal to zero. Has no significance."
- **After**: "Status code from the J-Link SDK. A value greater than or equal to zero indicates success. The exact value has no significance and should not be relied upon. This is returned for backward compatibility only."

**Raises section**:
- **Before**: "JLinkException: on hardware errors."
- **After**: "JLinkFlashException: on hardware errors (when status code < 0)."

## Impact

- ✅ **Backward compatible**: Return value unchanged, only documentation improved
- ✅ **No breaking changes**: Existing code continues to work
- ✅ **Clearer intent**: Variable name and documentation now accurately reflect behavior
- ✅ **Better developer experience**: Users understand what the return value represents

## Testing

Existing tests continue to pass:
- `test_jlink_flash_file_success()` - expects return value of 0 (status code)
- `test_jlink_flash_file_fail_to_flash()` - expects exception when status < 0

## References

- Issue #237: https://github.com/square/pylink/issues/237
- SEGGER J-Link SDK documentation: `JLINK_DownloadFile()` returns status code



