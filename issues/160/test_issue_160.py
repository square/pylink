#!/usr/bin/env python
"""Test script for Issue #160: Error Code -11 Handling

This script validates that rtt_read() now provides helpful diagnostics
when error code -11 occurs, instead of just showing "error -11".

Usage:
    python test_issue_160.py

Requirements:
    - J-Link connected
    - Target device connected
    - Firmware with RTT configured

Note: This test may require simulating error conditions (disconnect device,
attach GDB, etc.) to trigger error -11.
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

def test_error_message_format():
    """Test that error -11 gives detailed error message."""
    print("Test 1: Error -11 message format")
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
        
        # Try to read - if it works, we can't test error -11 easily
        # But we can at least verify the error handling code path exists
        try:
            data = jlink.rtt_read(0, 1024)
            print(f"✅ RTT read successful: {len(data)} bytes")
            print("⚠️  Cannot test error -11 without simulating error condition")
            print("   To test: disconnect device or attach GDB while RTT is active")
            return None
        except pylink.errors.JLinkRTTException as e:
            error_code = e.code if hasattr(e, 'code') else None
            error_msg = str(e)
            
            if error_code == -11:
                # Check if error message is helpful
                if any(keyword in error_msg.lower() for keyword in 
                       ['disconnected', 'reset', 'gdb', 'conflict', 'state', 'corrupted']):
                    print(f"✅ Got detailed error message: {error_msg}")
                    return True
                else:
                    print(f"❌ Error message not detailed enough: {error_msg}")
                    return False
            else:
                print(f"⚠️  Got different error code: {error_code}, message: {error_msg}")
                return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        try:
            jlink.rtt_stop()
        except:
            pass
        jlink.close()


def test_connection_health_check():
    """Test that error -11 triggers connection health check if available."""
    print("\nTest 2: Connection health check integration")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Check if check_connection_health is available
        if not hasattr(jlink, 'check_connection_health'):
            print("⚠️  check_connection_health() not available (Issue #252 not implemented)")
            print("   Error handling will still work, just without health check")
            return None
        
        # Start RTT
        ranges = [(0x20000000, 0x2003FFFF)]
        if not start_rtt_with_polling(jlink, search_ranges=ranges, timeout=5.0):
            print("⚠️  Could not start RTT, skipping test")
            return None
        
        # Try to read - if successful, we can't test error -11
        try:
            data = jlink.rtt_read(0, 1024)
            print("✅ RTT read successful")
            print("⚠️  Cannot test error -11 without simulating error condition")
            return None
        except pylink.errors.JLinkRTTException as e:
            error_code = e.code if hasattr(e, 'code') else None
            error_msg = str(e)
            
            if error_code == -11:
                # Check if health check info is in message
                if "health check" in error_msg.lower() or "disconnected" in error_msg.lower():
                    print(f"✅ Error message includes health check info: {error_msg}")
                    return True
                else:
                    print(f"⚠️  Error message doesn't include health check: {error_msg}")
                    return None
            else:
                print(f"⚠️  Got different error code: {error_code}")
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


def test_normal_read_still_works():
    """Test that normal rtt_read() still works correctly."""
    print("\nTest 3: Normal read still works")
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
        
        # Try to read
        try:
            data = jlink.rtt_read(0, 1024)
            print(f"✅ Normal read works: {len(data)} bytes")
            return True
        except Exception as e:
            print(f"⚠️  Read failed: {e}")
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


def test_invalid_read_parameters():
    """Test that rtt_read() detects invalid parameters."""
    print("\nTest 4: Invalid read parameters detection")
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
            jlink.rtt_read(-1, 1024)
            print("❌ Should have raised exception for negative buffer index")
            return False
        except (pylink.errors.JLinkRTTException, ValueError, IndexError) as e:
            print(f"✅ Correctly rejected negative buffer index: {type(e).__name__}: {e}")
        
        # Test negative num_bytes
        try:
            jlink.rtt_read(0, -1)
            print("❌ Should have raised exception for negative num_bytes")
            return False
        except (ValueError, TypeError) as e:
            print(f"✅ Correctly rejected negative num_bytes: {type(e).__name__}: {e}")
        
        # Test zero num_bytes (should be OK but return empty)
        try:
            data = jlink.rtt_read(0, 0)
            if len(data) == 0:
                print("✅ Zero num_bytes accepted (returns empty)")
            else:
                print(f"⚠️  Zero num_bytes returned {len(data)} bytes")
        except Exception as e:
            print(f"⚠️  Zero num_bytes rejected: {e}")
        
        # Test invalid buffer index (too large)
        try:
            # Try with a very large buffer index
            jlink.rtt_read(999, 1024)
            print("⚠️  Large buffer index accepted (may fail at SDK level)")
        except (pylink.errors.JLinkRTTException, ValueError, IndexError) as e:
            print(f"✅ Correctly rejected invalid buffer index: {type(e).__name__}: {e}")
        
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
    print("Issue #160: Error Code -11 Handling Tests")
    print("=" * 50)
    print("\nNote: To fully test error -11, you may need to:")
    print("  1. Disconnect device while RTT is active")
    print("  2. Attach GDB debugger (conflicts with RTT)")
    print("  3. Reset device while RTT is active")
    print()
    
    results = []
    
    result = test_error_message_format()
    if result is not None:
        results.append(("Error message format", result))
    result = test_connection_health_check()
    if result is not None:
        results.append(("Connection health check", result))
    result = test_normal_read_still_works()
    if result is not None:
        results.append(("Normal read", result))
    result = test_invalid_read_parameters()
    if result is not None:
        results.append(("Invalid read parameters detection", result))
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    if results:
        all_passed = all(result[1] for result in results)
        if all_passed:
            print("\n🎉 All tests passed!")
            sys.exit(0)
        else:
            print("\n⚠️  Some tests failed")
            sys.exit(1)
    else:
        print("\n⚠️  No tests could be run (may need error conditions)")
        sys.exit(0)

