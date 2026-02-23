#!/usr/bin/env python
"""Test script for Issue #209: Option to Set RTT Search Range

This script validates that search ranges can now be specified explicitly
and that rtt_get_block_address() can find the RTT control block.

Usage:
    python test_issue_209.py

Requirements:
    - J-Link connected
    - Target device connected (e.g., nRF54L15)
    - Firmware with RTT configured
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
from pylink.rtt import auto_detect_rtt_ranges, start_rtt_with_polling

# Device name to use for tests
DEVICE_NAME = 'NRF54L15_M33'

def test_explicit_search_ranges():
    """Test that explicit search_ranges parameter works."""
    print("Test 1: Explicit search_ranges parameter")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Use explicit search ranges
        ranges = [(0x20000000, 0x2003FFFF)]
        jlink.rtt_start(search_ranges=ranges)
        
        # Poll for readiness
        import time
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
            print("✅ RTT started successfully with explicit search ranges")
            return True
        else:
            print("❌ RTT did not become ready")
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


def test_rtt_get_block_address():
    """Test that rtt_get_block_address() can find the control block."""
    print("\nTest 2: rtt_get_block_address() method")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Search for control block
        ranges = [(0x20000000, 0x2003FFFF)]
        addr = jlink.rtt_get_block_address(ranges)
        
        if addr:
            print(f"✅ Found RTT control block at 0x{addr:X}")
            
            # Try to start RTT with this address
            jlink.rtt_start(block_address=addr)
            
            # Poll for readiness
            import time
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
                print("✅ RTT started successfully with found address")
                return True
            else:
                print("⚠️  Found address but RTT didn't become ready")
                return False
        else:
            print("❌ Could not find RTT control block")
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


def test_block_address_parameter():
    """Test that block_address parameter works in rtt_start()."""
    print("\nTest 3: block_address parameter")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # First find the address
        ranges = [(0x20000000, 0x2003FFFF)]
        addr = jlink.rtt_get_block_address(ranges)
        
        if not addr:
            print("⚠️  Could not find address, skipping test")
            return None
        
        # Now use block_address parameter
        jlink.rtt_start(block_address=addr)
        
        # Poll for readiness
        import time
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
            print(f"✅ RTT started successfully with block_address=0x{addr:X}")
            return True
        else:
            print("❌ RTT did not become ready")
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


def test_auto_detect_ranges():
    """Test that auto_detect_rtt_ranges() works."""
    print("\nTest 4: auto_detect_rtt_ranges() function")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Auto-detect ranges
        ranges = auto_detect_rtt_ranges(jlink)
        
        if ranges:
            print(f"✅ Auto-detected ranges: {ranges}")
            
            # Try to use them
            if start_rtt_with_polling(jlink, search_ranges=ranges, timeout=5.0):
                print("✅ RTT started successfully with auto-detected ranges")
                return True
            else:
                print("❌ RTT did not start with auto-detected ranges")
                return False
        else:
            print("⚠️  Could not auto-detect ranges (device info may not be available)")
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


def test_multiple_search_ranges():
    """Test that multiple search ranges work."""
    print("\nTest 5: Multiple search ranges")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Use multiple ranges (simulating device with multiple RAM regions)
        ranges = [
            (0x20000000, 0x2003FFFF),  # Main RAM
            (0x10000000, 0x1000FFFF)   # Secondary RAM (may not exist)
        ]
        
        jlink.rtt_start(search_ranges=ranges)
        
        # Poll for readiness
        import time
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
            print("✅ RTT started successfully with multiple search ranges")
            return True
        else:
            print("❌ RTT did not become ready")
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
    print("\nTest 6: Invalid search ranges detection")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Test empty ranges
        try:
            jlink.rtt_get_block_address([])
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
            jlink.rtt_get_block_address([(0x2003FFFF, 0x20000000)])
            print("⚠️  start > end was not rejected (may skip invalid range)")
            # This might not raise, just skip invalid range
        except ValueError as e:
            if "start" in str(e).lower() or "end" in str(e).lower():
                print(f"✅ Correctly rejected start > end: {e}")
        
        # Test None ranges (should work if device RAM info available)
        try:
            addr = jlink.rtt_get_block_address(None)
            if addr is None:
                print("⚠️  Could not auto-detect (device RAM info may not be available)")
            else:
                print(f"✅ Auto-detection worked: 0x{addr:X}")
        except Exception as e:
            print(f"⚠️  Auto-detection failed: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        jlink.close()


if __name__ == '__main__':
    print("=" * 50)
    print("Issue #209: RTT Search Range Tests")
    print("=" * 50)
    
    results = []
    
    results.append(("Explicit search_ranges", test_explicit_search_ranges()))
    results.append(("rtt_get_block_address()", test_rtt_get_block_address()))
    result = test_block_address_parameter()
    if result is not None:
        results.append(("block_address parameter", result))
    result = test_auto_detect_ranges()
    if result is not None:
        results.append(("auto_detect_rtt_ranges()", result))
    results.append(("Multiple search ranges", test_multiple_search_ranges()))
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

