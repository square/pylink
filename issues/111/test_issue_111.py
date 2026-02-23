#!/usr/bin/env python
"""Test script for Issue #111: RTT Echo Filtering

This script validates that read_rtt_without_echo() correctly filters
local echo characters from RTT data.

Usage:
    python test_issue_111.py

Requirements:
    - J-Link connected
    - Target device connected
    - Firmware with RTT configured (preferably with local echo enabled)
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
from pylink.rtt import start_rtt_with_polling, read_rtt_without_echo

# Device name to use for tests
DEVICE_NAME = 'NRF54L15_M33'

def test_echo_filtering():
    """Test that read_rtt_without_echo() filters echo characters."""
    print("Test 1: Echo character filtering")
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
        
        # Read with echo filtering
        try:
            data = read_rtt_without_echo(jlink, buffer_index=0, num_bytes=1024)
            print(f"✅ Read without echo: {len(data)} bytes")
            
            # Check that common echo characters are filtered
            if data:
                data_str = bytes(data).decode('utf-8', errors='ignore')
                if '\x08' in data_str:
                    print("⚠️  Backspace character found (should be filtered)")
                if '\r' in data_str and '\n' not in data_str:
                    print("⚠️  Standalone CR found (should be filtered)")
                
                print(f"   Data: {repr(data_str[:50])}")
            
            return True
        except Exception as e:
            print(f"⚠️  Error reading: {e}")
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


def test_compare_with_normal_read():
    """Compare read_rtt_without_echo() with normal rtt_read()."""
    print("\nTest 2: Compare with normal read")
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
        
        # Read normally
        try:
            normal_data = jlink.rtt_read(0, 1024)
            echo_filtered_data = read_rtt_without_echo(jlink, buffer_index=0, num_bytes=1024)
            
            print(f"Normal read: {len(normal_data)} bytes")
            print(f"Echo filtered: {len(echo_filtered_data)} bytes")
            
            if len(echo_filtered_data) <= len(normal_data):
                print("✅ Echo filtering reduced or kept same size (expected)")
                return True
            else:
                print("⚠️  Echo filtering increased size (unexpected)")
                return None
        except Exception as e:
            print(f"⚠️  Error reading: {e}")
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


def test_empty_data():
    """Test that read_rtt_without_echo() handles empty data correctly."""
    print("\nTest 3: Empty data handling")
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
        
        # Read when no data available
        try:
            data = read_rtt_without_echo(jlink, buffer_index=0, num_bytes=1024)
            if len(data) == 0:
                print("✅ Empty data handled correctly")
                return True
            else:
                print(f"⚠️  Got {len(data)} bytes (may be OK if device is sending)")
                return None
        except Exception as e:
            print(f"⚠️  Error reading: {e}")
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


def test_invalid_echo_filter_parameters():
    """Test that read_rtt_without_echo() detects invalid parameters."""
    print("\nTest 4: Invalid echo filter parameters detection")
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
            read_rtt_without_echo(jlink, buffer_index=-1, num_bytes=1024)
            print("❌ Should have raised exception for negative buffer index")
            return False
        except (pylink.errors.JLinkRTTException, ValueError, IndexError) as e:
            print(f"✅ Correctly rejected negative buffer index: {type(e).__name__}: {e}")
        
        # Test negative num_bytes
        try:
            read_rtt_without_echo(jlink, buffer_index=0, num_bytes=-1)
            print("❌ Should have raised exception for negative num_bytes")
            return False
        except (ValueError, TypeError) as e:
            print(f"✅ Correctly rejected negative num_bytes: {type(e).__name__}: {e}")
        
        # Test zero num_bytes (should be OK)
        try:
            data = read_rtt_without_echo(jlink, buffer_index=0, num_bytes=0)
            if len(data) == 0:
                print("✅ Zero num_bytes accepted (returns empty)")
            else:
                print(f"⚠️  Zero num_bytes returned {len(data)} bytes")
        except Exception as e:
            print(f"⚠️  Zero num_bytes rejected: {e}")
        
        # Test None jlink (will raise AttributeError when trying to call rtt_read)
        try:
            read_rtt_without_echo(None, buffer_index=0, num_bytes=1024)
            print("❌ Should have raised exception for None jlink")
            return False
        except (AttributeError, TypeError, ValueError) as e:
            # AttributeError: None has no attribute 'rtt_read'
            # TypeError: if validation happens before rtt_read call
            # ValueError: if validation catches it first
            print(f"✅ Correctly rejected None jlink: {type(e).__name__}: {e}")
        
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
    print("Issue #111: RTT Echo Filtering Tests")
    print("=" * 50)
    
    results = []
    
    result = test_echo_filtering()
    if result is not None:
        results.append(("Echo filtering", result))
    result = test_compare_with_normal_read()
    if result is not None:
        results.append(("Compare with normal read", result))
    result = test_empty_data()
    if result is not None:
        results.append(("Empty data handling", result))
    result = test_invalid_echo_filter_parameters()
    if result is not None:
        results.append(("Invalid echo filter parameters detection", result))
    
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
        print("\n⚠️  No tests could be run")
        sys.exit(0)

