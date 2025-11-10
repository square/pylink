# Issue #171: Fix exec_command() raising exception on informational messages

## Problem

The `exec_command()` method was raising `JLinkException` for **any** content in the error buffer (`err_buf`), even when the message was informational rather than an error.

### Specific Issue

Command `SetRTTTelnetPort 19021` returns the informational message `"RTT Telnet Port set to 19021"` in `err_buf` when successful, but the code was treating this as an error and raising an exception.

### Root Cause

The J-Link SDK uses `err_buf` for both:
- **Error messages** (should raise exception)
- **Informational messages** (should not raise exception)

The code was checking `if len(err_buf) > 0:` and always raising an exception, without distinguishing between errors and informational messages.

## Solution

### Changes Made

1. **Added informational message patterns**: Created class constant `_INFORMATIONAL_MESSAGE_PATTERNS` with known informational message patterns
2. **Pattern matching**: Check if message matches informational pattern before raising exception
3. **Debug logging**: Log informational messages at DEBUG level instead of raising exception
4. **Updated docstring**: Added Note section explaining informational message handling

### Code Changes

**File**: `pylink/jlink.py`  
**Method**: `exec_command()` (lines 975-1026)

**Added class constant** (lines 73-84):
```python
# Informational message patterns returned by some J-Link commands in err_buf
# even when successful. These should not be treated as errors.
_INFORMATIONAL_MESSAGE_PATTERNS = [
    'RTT Telnet Port set to',
    'Device selected',
    'Device =',
    'Speed =',
    'Target interface set to',
    'Target voltage',
    'Reset delay',
    'Reset type',
]
```

**Modified exec_command() logic**:
```python
if len(err_buf) > 0:
    err_msg = err_buf.strip()
    
    # Check if this is an informational message, not an error
    is_informational = any(
        pattern.lower() in err_msg.lower()
        for pattern in self._INFORMATIONAL_MESSAGE_PATTERNS
    )
    
    if is_informational:
        # Log at debug level but don't raise exception
        logger.debug('J-Link informational message: %s', err_msg)
    else:
        # This appears to be a real error
        raise errors.JLinkException(err_msg)
```

### Informational Message Patterns

The following patterns are recognized as informational (case-insensitive):
- `'RTT Telnet Port set to'` - SetRTTTelnetPort command
- `'Device selected'` - Device selection commands
- `'Device ='` - Device configuration
- `'Speed ='` - Speed configuration
- `'Target interface set to'` - Interface configuration
- `'Target voltage'` - Voltage configuration
- `'Reset delay'` - Reset delay configuration
- `'Reset type'` - Reset type configuration

### Documentation Changes

**Added Note section**:
```
Note:
  Some commands return informational messages in the error buffer even
  when successful (e.g., "RTT Telnet Port set to 19021"). These are
  automatically detected and not treated as errors, but are logged at
  DEBUG level.
```

## Impact

- ✅ **Backward compatible**: Real errors still raise exceptions as before
- ✅ **Fixes broken functionality**: Commands like `SetRTTTelnetPort` now work correctly
- ✅ **Better user experience**: No need to catch and ignore exceptions for informational messages
- ✅ **Extensible**: Easy to add more informational patterns as discovered
- ✅ **Debugging support**: Informational messages logged at DEBUG level for troubleshooting

## Testing

### Test Cases

1. **Informational message** (should NOT raise exception):
   ```python
   jlink.exec_command('SetRTTTelnetPort 19021')
   # Should succeed, message logged at DEBUG level
   ```

2. **Real error** (should raise exception):
   ```python
   jlink.exec_command('InvalidCommand')
   # Should raise JLinkException
   ```

3. **Empty buffer** (should succeed):
   ```python
   jlink.exec_command('ValidCommand')
   # Should succeed normally
   ```

## References

- Issue #171: https://github.com/square/pylink/issues/171
- CHANGELOG note about `exec_command()` behavior (line 428-431)
- SEGGER J-Link documentation: Some commands return informational messages in `err_buf`

## Future Improvements

- Consider adding more informational patterns as they are discovered
- Could potentially use return code as additional signal (though CHANGELOG says it's unreliable)
- Could add option to suppress informational message logging





