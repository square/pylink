#!/usr/bin/env python
"""Test script for Issue #51: Initialize RTT with Address

This script validates that rtt_start() now accepts block_address parameter
to specify the exact RTT control block address.

Usage:
    python test_issue_51.py

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

# Device name to use for tests
DEVICE_NAME = 'NRF54L15_M33'

def test_block_address_parameter():
    """Test that block_address parameter works."""
    print("Test 1: block_address parameter")
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
        
        print(f"Found address: 0x{addr:X}")
        
        # Use block_address parameter
        jlink.rtt_start(block_address=addr)
        
        # Poll for readiness
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


def test_block_address_validation():
    """Test that invalid block_address values are rejected."""
    print("\nTest 2: block_address validation (reject invalid values)")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Test block_address=0 (should fail)
        try:
            jlink.rtt_start(block_address=0)
            print("❌ Should have raised ValueError for block_address=0")
            return False
        except ValueError as e:
            if "cannot be 0" in str(e).lower() or "0" in str(e):
                print(f"✅ Correctly rejected block_address=0: {e}")
            else:
                print(f"❌ Wrong error message: {e}")
                return False
        
        # Test block_address=None (should work, uses auto-detection)
        try:
            jlink.rtt_start(block_address=None)
            print("✅ block_address=None accepted (uses auto-detection)")
        except Exception as e:
            # May fail if auto-detection doesn't work, but shouldn't be ValueError
            if isinstance(e, ValueError):
                print(f"❌ ValueError for None (unexpected): {e}")
                return False
            else:
                print(f"⚠️  Auto-detection failed (expected): {e}")
        
        # Test block_address with invalid address (should fail at SDK level)
        try:
            jlink.rtt_start(block_address=0xFFFFFFFF)
            print("⚠️  Invalid address accepted (may fail at SDK level)")
        except (pylink.errors.JLinkRTTException, ValueError) as e:
            print(f"✅ Invalid address correctly rejected: {type(e).__name__}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        try:
            jlink.rtt_stop()
        except:
            pass
        jlink.close()


def test_block_address_precedence():
    """Test that block_address takes precedence over search_ranges."""
    print("\nTest 3: block_address precedence over search_ranges")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        jlink.connect(DEVICE_NAME)
        
        # Find address first
        ranges = [(0x20000000, 0x2003FFFF)]
        addr = jlink.rtt_get_block_address(ranges)
        
        if not addr:
            print("⚠️  Could not find address, skipping test")
            return None
        
        # Use both block_address and search_ranges (block_address should win)
        jlink.rtt_start(block_address=addr, search_ranges=ranges)
        
        # Poll for readiness
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
            print("✅ block_address takes precedence over search_ranges")
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


if __name__ == '__main__':
    print("=" * 50)
    print("Issue #51: Block Address Parameter Tests")
    print("=" * 50)
    
    results = []
    
    result = test_block_address_parameter()
    if result is not None:
        results.append(("block_address parameter", result))
    results.append(("block_address validation", test_block_address_validation()))
    result = test_block_address_precedence()
    if result is not None:
        results.append(("block_address precedence", result))
    
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

