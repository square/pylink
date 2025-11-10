# Issue #234 Analysis: RTT Write Returns 0

## Problem Summary

**Issue**: [RTT no writing #234](https://github.com/square/pylink/issues/234)

**Symptoms**:
- `rtt_write()` always returns 0 (no bytes written)
- `rtt_read()` works correctly (can read boot banner)
- Setup works with deprecated `pynrfjprog` library

**Environment**:
- pylink-square 1.4.0
- JLink V7.96i
- nRF5340 JLink OB (nRF9151-DK)
- Ubuntu 24.04

---

## Root Cause Analysis

### Understanding RTT Buffers

RTT has two types of buffers:
1. **Up buffers** (target → host): Used for reading data FROM the target
2. **Down buffers** (host → target): Used for writing data TO the target

### Most Likely Causes

#### 1. **Missing Down Buffers in Firmware** ⚠️ **MOST LIKELY**

**Problem**: The firmware may not have configured any down buffers. If there are no down buffers, `rtt_write()` will return 0.

**Solution**: Check if down buffers exist:
```python
num_down = jlink.rtt_get_num_down_buffers()
print(f"Number of down buffers: {num_down}")
```

If `num_down == 0`, the firmware needs to be configured with down buffers.

#### 2. **Wrong Buffer Index**

**Problem**: User might be trying to write to an up buffer (for reading) instead of a down buffer (for writing).

**Solution**: 
- Up buffers are for reading: `rtt_read(buffer_index, ...)`
- Down buffers are for writing: `rtt_write(buffer_index, ...)`
- Buffer indices are separate for up and down buffers
- Typically, down buffers start at index 0, but this depends on firmware configuration

#### 3. **Buffer Full**

**Problem**: The down buffer might be full and the target is not reading from it.

**Solution**: Check buffer status and ensure the target firmware is reading from RTT down buffers.

#### 4. **RTT Not Properly Started**

**Problem**: RTT might not be fully initialized or the control block wasn't found correctly.

**Solution**: Verify RTT is active:
```python
if jlink.rtt_is_active():
    print("RTT is active")
else:
    print("RTT is not active - need to start it")
```

---

## Diagnostic Steps

### Step 1: Check RTT Status

```python
import pylink

jlink = pylink.JLink()
jlink.open()
jlink.rtt_start()

# Check if RTT is active
print(f"RTT active: {jlink.rtt_is_active()}")

# Get comprehensive info
info = jlink.rtt_get_info()
print(f"Up buffers: {info.get('num_up_buffers')}")
print(f"Down buffers: {info.get('num_down_buffers')}")
```

### Step 2: Verify Down Buffers Exist

```python
try:
    num_down = jlink.rtt_get_num_down_buffers()
    print(f"Number of down buffers configured: {num_down}")
    
    if num_down == 0:
        print("ERROR: No down buffers configured in firmware!")
        print("You need to configure down buffers in your firmware.")
except Exception as e:
    print(f"Error getting down buffers: {e}")
```

### Step 3: Try Writing to Buffer 0

```python
# Try writing to down buffer 0 (most common)
data = list(b"Hello from host\n")
bytes_written = jlink.rtt_write(0, data)
print(f"Bytes written: {bytes_written}")

if bytes_written == 0:
    print("Warning: No bytes written. Possible causes:")
    print("1. No down buffers configured in firmware")
    print("2. Wrong buffer index")
    print("3. Buffer is full and target not reading")
```

---

## Firmware Configuration

### For nRF Connect SDK / Zephyr

The firmware needs to configure RTT down buffers. Example:

```c
#include <SEGGER_RTT.h>

// In your firmware initialization:
SEGGER_RTT_ConfigUpBuffer(0, "RTT", NULL, 0, SEGGER_RTT_MODE_NO_BLOCK_SKIP);
SEGGER_RTT_ConfigDownBuffer(0, "RTT", NULL, 0, SEGGER_RTT_MODE_NO_BLOCK_SKIP);

// To read from down buffer in firmware:
char buffer[256];
int num_read = SEGGER_RTT_Read(0, buffer, sizeof(buffer));
```

### Common Issue: Only Up Buffer Configured

Many firmware examples only configure up buffers (for printf/logging) but forget down buffers (for host-to-target communication).

---

## Comparison with pynrfjprog

`pynrfjprog` might have:
1. Different default buffer handling
2. Automatic buffer detection
3. Different buffer index assumptions

The user should check:
- What buffer index `pynrfjprog` was using
- Whether `pynrfjprog` was checking for down buffers

---

## Recommended Solution

### For the User:

1. **Check if down buffers exist**:
   ```python
   num_down = jlink.rtt_get_num_down_buffers()
   if num_down == 0:
       # Need to configure down buffers in firmware
   ```

2. **Verify buffer index**: Try buffer 0 first (most common)

3. **Check firmware**: Ensure firmware has down buffers configured

4. **Use `rtt_get_info()`**: Get comprehensive RTT state information

### Potential Code Improvement:

We could add better error messages or validation in `rtt_write()`:

```python
def rtt_write(self, buffer_index, data):
    # Check if down buffers exist
    try:
        num_down = self.rtt_get_num_down_buffers()
        if num_down == 0:
            raise errors.JLinkRTTException(
                "No down buffers configured. "
                "RTT write requires down buffers to be configured in firmware."
            )
        if buffer_index >= num_down:
            raise errors.JLinkRTTException(
                f"Buffer index {buffer_index} out of range. "
                f"Only {num_down} down buffer(s) available."
            )
    except errors.JLinkRTTException:
        raise
    except Exception:
        pass  # Continue if check fails
    
    # ... existing code ...
```

---

## Conclusion

**Most likely cause**: The firmware doesn't have down buffers configured. RTT write requires down buffers in the firmware, while RTT read only needs up buffers (which are more commonly configured).

**Next steps for user**:
1. Check `rtt_get_num_down_buffers()` - if 0, configure down buffers in firmware
2. Verify buffer index is correct (try 0 first)
3. Ensure firmware is reading from RTT down buffers

**Potential improvement**: Add validation and better error messages in `rtt_write()` to help diagnose this common issue.

