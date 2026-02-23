# Issue #251: Specify JLink Home Path

## The Problem

If you had multiple J-Link SDK versions installed or a custom installation, there was no way to tell pylink "use this specific version". The code always searched in system default locations.

This was especially annoying in CI/CD or when you needed a specific SDK version.

## How It Was Fixed

Now you can specify the J-Link SDK directory directly:

```python
# Specify the SDK directory
jlink = JLink(jlink_path="/opt/SEGGER/JLink_8228")

# Or on Windows
jlink = JLink(jlink_path="C:/Program Files/SEGGER/JLink_8228")
```

The code automatically finds the correct DLL/SO in that directory based on your platform (Windows/Mac/Linux).

I also added `Library.from_directory()` if you need more control:

```python
from pylink.library import Library
lib = Library.from_directory("/opt/SEGGER/JLink_8228")
jlink = JLink(lib=lib)
```

Everything is still backward compatible - if you don't specify anything, it uses the default behavior.

## Testing

See `test_issue_251.py` for scripts that validate the `jlink_path` parameter.

### Test Results

**Note:** These tests require J-Link SDK to be installed. They do NOT require hardware to be connected.

**Test Coverage:**
- ✅ jlink_path parameter (custom SDK directory)
- ✅ Library.from_directory() method
- ✅ Invalid directory handling (non-existent paths)
- ✅ Backward compatibility (default behavior)
- ✅ Invalid jlink_path types detection (int, list, dict)

**Actual Test Results:**
```
==================================================
Issue #251: JLink Path Specification Tests
==================================================
✅ PASS: jlink_path parameter
✅ PASS: Library.from_directory()
✅ PASS: Invalid directory handling
✅ PASS: Backward compatibility
✅ PASS: Invalid jlink_path types detection

🎉 All tests passed!
```

**To run tests:**
```bash
python3 test_issue_251.py
# Or with custom path:
python3 test_issue_251.py /path/to/JLink
```

