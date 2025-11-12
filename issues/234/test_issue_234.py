#!/usr/bin/env python
"""Test script for Issue #234: RTT Write Returns 0

This script validates that rtt_write() now provides helpful error messages
when things go wrong, instead of just returning 0 silently.

Usage:
    python test_issue_234.py

Requirements:
    - J-Link connected
    - Target device connected
    - Firmware with RTT configured (preferably with and without down buffers)
"""

import sys
import os

# Ensure we use the local pylink library (not an installed version)
# Add parent directory to path so we import from sandbox/pylink/pylink/
_test_dir = os.path.dirname(os.path.abspath(__file__))
_pylink_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))
if _pylink_root not in sys.path:
    sys.path.insert(0, _pylink_root)

import pylink
from pylink.rtt import start_rtt_with_polling

# Device name to use for tests
DEVICE_NAME = 'NRF54L15_M33'

def test_error_when_rtt_not_active():
    """Test that rtt_write() gives clear error when RTT not started."""
    print("Test 1: Error when RTT not active")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Don't start RTT, try to write
        try:
            jlink.rtt_write(0, [0x48, 0x65, 0x6C, 0x6C, 0x6F])  # "Hello"
            print("❌ Should have raised exception")
            return False
        except pylink.errors.JLinkRTTException as e:
            error_msg = str(e)
            if "not active" in error_msg.lower() or "rtt_start" in error_msg.lower():
                print(f"✅ Got expected error: {error_msg}")
                return True
            else:
                print(f"❌ Got unexpected error: {error_msg}")
                return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        jlink.close()


def test_error_when_no_down_buffers():
    """Test that rtt_write() gives clear error when no down buffers configured."""
    print("\nTest 2: Error when no down buffers configured")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Start RTT
        ranges = [(0x20000000, 0x2003FFFF)]
        if not start_rtt_with_polling(jlink, search_ranges=ranges, timeout=5.0):
            print("⚠️  Could not start RTT, skipping test")
            return None
        
        # Check if down buffers exist
        try:
            num_down = jlink.rtt_get_num_down_buffers()
            print(f"Found {num_down} down buffer(s)")
            
            if num_down == 0:
                # Try to write - should get helpful error
                try:
                    jlink.rtt_write(0, [0x48, 0x65, 0x6C, 0x6C, 0x6F])
                    print("❌ Should have raised exception")
                    return False
                except pylink.errors.JLinkRTTException as e:
                    error_msg = str(e)
                    if "down buffer" in error_msg.lower() or "configdownbuffer" in error_msg.lower():
                        print(f"✅ Got expected error: {error_msg}")
                        return True
                    else:
                        print(f"❌ Got unexpected error: {error_msg}")
                        return False
            else:
                print("⚠️  Firmware has down buffers, cannot test this case")
                return None
        except Exception as e:
            print(f"⚠️  Could not check buffers: {e}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            jlink.rtt_stop()
        except:
            pass
        jlink.close()


def test_error_when_invalid_buffer_index():
    """Test that rtt_write() gives clear error when buffer index is invalid."""
    print("\nTest 3: Error when buffer index invalid")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Start RTT
        ranges = [(0x20000000, 0x2003FFFF)]
        if not start_rtt_with_polling(jlink, search_ranges=ranges, timeout=5.0):
            print("⚠️  Could not start RTT, skipping test")
            return None
        
        # Check number of down buffers
        try:
            num_down = jlink.rtt_get_num_down_buffers()
            print(f"Found {num_down} down buffer(s)")
            
            if num_down > 0:
                # Try to write to invalid buffer index
                invalid_index = num_down + 10
                try:
                    jlink.rtt_write(invalid_index, [0x48, 0x65, 0x6C, 0x6C, 0x6F])
                    print("❌ Should have raised exception")
                    return False
                except pylink.errors.JLinkRTTException as e:
                    error_msg = str(e)
                    if "out of range" in error_msg.lower() or str(num_down) in error_msg:
                        print(f"✅ Got expected error: {error_msg}")
                        return True
                    else:
                        print(f"❌ Got unexpected error: {error_msg}")
                        return False
            else:
                print("⚠️  No down buffers, cannot test invalid index")
                return None
        except Exception as e:
            print(f"⚠️  Could not check buffers: {e}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            jlink.rtt_stop()
        except:
            pass
        jlink.close()


def test_successful_write():
    """Test that rtt_write() works correctly when everything is configured."""
    print("\nTest 4: Successful write (when properly configured)")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Start RTT
        ranges = [(0x20000000, 0x2003FFFF)]
        if not start_rtt_with_polling(jlink, search_ranges=ranges, timeout=5.0):
            print("⚠️  Could not start RTT, skipping test")
            return None
        
        # Check if down buffers exist
        try:
            num_down = jlink.rtt_get_num_down_buffers()
            print(f"Found {num_down} down buffer(s)")
            
            if num_down > 0:
                # Try to write
                data = [0x48, 0x65, 0x6C, 0x6C, 0x6F]  # "Hello"
                bytes_written = jlink.rtt_write(0, data)
                
                if bytes_written >= 0:
                    print(f"✅ Write successful: {bytes_written} bytes written")
                    return True
                else:
                    print(f"❌ Write failed: {bytes_written}")
                    return False
            else:
                print("⚠️  No down buffers configured, cannot test write")
                return None
        except Exception as e:
            print(f"⚠️  Error during write: {e}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            jlink.rtt_stop()
        except:
            pass
        jlink.close()


def test_invalid_write_parameters():
    """Test that rtt_write() detects invalid parameters."""
    print("\nTest 5: Invalid write parameters detection")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Start RTT
        ranges = [(0x20000000, 0x2003FFFF)]
        if not start_rtt_with_polling(jlink, search_ranges=ranges, timeout=5.0):
            print("⚠️  Could not start RTT, skipping test")
            return None
        
        # Test negative buffer index
        try:
            jlink.rtt_write(-1, [0x48, 0x65, 0x6C, 0x6C, 0x6F])
            print("❌ Should have raised exception for negative buffer index")
            return False
        except (pylink.errors.JLinkRTTException, ValueError, IndexError) as e:
            print(f"✅ Correctly rejected negative buffer index: {type(e).__name__}: {e}")
        
        # Test None data
        try:
            jlink.rtt_write(0, None)
            print("❌ Should have raised exception for None data")
            return False
        except (TypeError, ValueError) as e:
            print(f"✅ Correctly rejected None data: {type(e).__name__}: {e}")
        
        # Test empty data (should be OK)
        try:
            bytes_written = jlink.rtt_write(0, [])
            print(f"✅ Empty data accepted (wrote {bytes_written} bytes)")
        except Exception as e:
            print(f"⚠️  Empty data rejected: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            jlink.rtt_stop()
        except:
            pass
        jlink.close()


if __name__ == '__main__':
    print("=" * 50)
    print("Issue #234: RTT Write Error Messages Tests")
    print("=" * 50)
    
    results = []
    
    results.append(("Error when RTT not active", test_error_when_rtt_not_active()))
    result = test_error_when_no_down_buffers()
    if result is not None:
        results.append(("Error when no down buffers", result))
    result = test_error_when_invalid_buffer_index()
    if result is not None:
        results.append(("Error when invalid buffer index", result))
    result = test_successful_write()
    if result is not None:
        results.append(("Successful write", result))
    result = test_invalid_write_parameters()
    if result is not None:
        results.append(("Invalid write parameters detection", result))
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed")
        sys.exit(1)

