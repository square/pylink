#!/usr/bin/env python
"""Test script for Issue #249: RTT Auto-detection Fails

This script validates that RTT auto-detection now works correctly,
especially for devices like nRF54L15 where it previously failed.

Usage:
    python test_issue_249.py

Requirements:
    - J-Link connected
    - Target device connected (e.g., nRF54L15)
    - Firmware with RTT configured
"""

import sys
import os
import time

# Ensure we use the local pylink library (not an installed version)
# Add parent directory to path so we import from sandbox/pylink/pylink/
_test_dir = os.path.dirname(os.path.abspath(__file__))
_pylink_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))
if _pylink_root not in sys.path:
    sys.path.insert(0, _pylink_root)

import pylink
from pylink.rtt import auto_detect_rtt_ranges, start_rtt_with_polling

# Device name to use for tests
DEVICE_NAME = 'NRF54L15_M33'

def test_auto_detect_ranges():
    """Test that auto_detect_rtt_ranges() works."""
    print("Test 1: Auto-detect RTT search ranges")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        ranges = auto_detect_rtt_ranges(jlink)
        if ranges:
            print(f"✅ Auto-detected ranges: {ranges}")
            return True
        else:
            print("❌ Failed to auto-detect ranges")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        jlink.close()


def test_start_with_auto_detection():
    """Test that start_rtt_with_polling() works with auto-detection."""
    print("\nTest 2: Start RTT with auto-detection")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Try auto-detection
        if start_rtt_with_polling(jlink, timeout=5.0):
            print("✅ RTT started successfully with auto-detection")
            
            # Try to read
            try:
                data = jlink.rtt_read(0, 1024)
                print(f"✅ RTT read successful: {len(data)} bytes")
                return True
            except Exception as e:
                print(f"⚠️  RTT started but read failed: {e}")
                return False
        else:
            print("❌ Failed to start RTT with auto-detection")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            jlink.rtt_stop()
        except:
            pass
        jlink.close()


def test_start_with_explicit_ranges():
    """Test that start_rtt_with_polling() works with explicit ranges."""
    print("\nTest 3: Start RTT with explicit search ranges")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Use explicit ranges (nRF54L15 RAM)
        ranges = [(0x20000000, 0x2003FFFF)]
        
        if start_rtt_with_polling(jlink, search_ranges=ranges, timeout=5.0):
            print("✅ RTT started successfully with explicit ranges")
            
            # Try to read
            try:
                data = jlink.rtt_read(0, 1024)
                print(f"✅ RTT read successful: {len(data)} bytes")
                return True
            except Exception as e:
                print(f"⚠️  RTT started but read failed: {e}")
                return False
        else:
            print("❌ Failed to start RTT with explicit ranges")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            jlink.rtt_stop()
        except:
            pass
        jlink.close()


def test_low_level_api():
    """Test that low-level API still works (backward compatibility)."""
    print("\nTest 4: Low-level API backward compatibility")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Use low-level API with explicit ranges
        ranges = [(0x20000000, 0x2003FFFF)]
        jlink.rtt_start(search_ranges=ranges)
        
        # Poll manually for readiness
        timeout = 5.0
        start_time = time.time()
        ready = False
        
        while time.time() - start_time < timeout:
            try:
                num_up = jlink.rtt_get_num_up_buffers()
                if num_up > 0:
                    ready = True
                    break
            except:
                pass
            time.sleep(0.1)
        
        if ready:
            print("✅ Low-level API works correctly")
            return True
        else:
            print("❌ Low-level API failed to detect RTT")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            jlink.rtt_stop()
        except:
            pass
        jlink.close()


def test_invalid_search_ranges():
    """Test that invalid search ranges are detected and rejected."""
    print("\nTest 5: Invalid search ranges detection")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Test empty ranges
        try:
            jlink.rtt_start(search_ranges=[])
            print("❌ Should have raised ValueError for empty ranges")
            return False
        except ValueError as e:
            if "empty" in str(e).lower():
                print(f"✅ Correctly rejected empty ranges: {e}")
            else:
                print(f"❌ Wrong error message: {e}")
                return False
        
        # Test start > end
        try:
            jlink.rtt_start(search_ranges=[(0x2003FFFF, 0x20000000)])
            print("❌ Should have raised ValueError for start > end")
            return False
        except ValueError as e:
            if "start" in str(e).lower() or "end" in str(e).lower():
                print(f"✅ Correctly rejected start > end: {e}")
            else:
                print(f"❌ Wrong error message: {e}")
                return False
        
        # Test range too large (> 16MB)
        try:
            jlink.rtt_start(search_ranges=[(0x20000000, 0x20000000 + 0x1000000 + 1)])
            print("❌ Should have raised ValueError for range > 16MB")
            return False
        except ValueError as e:
            if "16" in str(e) or "mb" in str(e).lower() or "size" in str(e).lower():
                print(f"✅ Correctly rejected range > 16MB: {e}")
            else:
                print(f"⚠️  Got different error (may be OK): {e}")
        
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        jlink.close()


if __name__ == '__main__':
    print("=" * 50)
    print("Issue #249: RTT Auto-detection Tests")
    print("=" * 50)
    
    results = []
    
    results.append(("Auto-detect ranges", test_auto_detect_ranges()))
    results.append(("Start with auto-detection", test_start_with_auto_detection()))
    results.append(("Start with explicit ranges", test_start_with_explicit_ranges()))
    results.append(("Low-level API compatibility", test_low_level_api()))
    results.append(("Invalid search ranges detection", test_invalid_search_ranges()))
    
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

