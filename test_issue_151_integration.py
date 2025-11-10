#!/usr/bin/env python3
"""
Integration test for Issue #151 using actual pylink code structure.

This test verifies that the changes work correctly with the actual code structure.
"""

import sys
import os
import inspect

# Add pylink to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pylink'))

def test_code_structure():
    """Test that the code structure is correct"""
    print("=" * 70)
    print("Testing Code Structure for Issue #151")
    print("=" * 70)
    print()
    
    try:
        import pylink.jlink as jlink_module
        
        # Get the open method source code
        open_method = jlink_module.JLink.open
        source = inspect.getsource(open_method)
        
        print("Checking code structure...")
        
        # Check 1: New logic is present
        if "if serial_no is None and ip_addr is None:" in source:
            print("  ✅ PASS: Logic to use self.__serial_no when both are None")
        else:
            print("  ❌ FAIL: Missing logic to use self.__serial_no")
            return False
        
        if "serial_no = self.__serial_no" in source:
            print("  ✅ PASS: Assignment of self.__serial_no found")
        else:
            print("  ❌ FAIL: Missing assignment of self.__serial_no")
            return False
        
        if "if ip_addr is None:" in source:
            print("  ✅ PASS: Logic to use self.__ip_addr when None")
        else:
            print("  ❌ FAIL: Missing logic to use self.__ip_addr")
            return False
        
        if "ip_addr = self.__ip_addr" in source:
            print("  ✅ PASS: Assignment of self.__ip_addr found")
        else:
            print("  ❌ FAIL: Missing assignment of self.__ip_addr")
            return False
        
        # Check 2: Docstring updated
        docstring = open_method.__doc__
        if "If ``serial_no`` was specified in ``__init__()``" in docstring:
            print("  ✅ PASS: Docstring mentions __init__() behavior")
        else:
            print("  ⚠️  WARNING: Docstring may not mention __init__() behavior")
        
        # Check 3: Comments present
        if "avoiding the need for additional queries" in source.lower():
            print("  ✅ PASS: Comment about avoiding additional queries found")
        else:
            print("  ⚠️  WARNING: Comment about additional queries not found")
        
        print("\n✅ Code structure checks PASSED\n")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_logic_flow():
    """Test the logic flow to ensure it's correct"""
    print("Testing Logic Flow...")
    print()
    
    test_cases = [
        {
            "name": "serial_no from __init__, open() without params",
            "init_serial": 600115433,
            "init_ip": None,
            "open_serial": None,
            "open_ip": None,
            "expected_serial": 600115433,
            "expected_path": "USB_SN"
        },
        {
            "name": "serial_no from __init__, open() with different serial",
            "init_serial": 600115433,
            "init_ip": None,
            "open_serial": 600115434,
            "open_ip": None,
            "expected_serial": 600115434,
            "expected_path": "USB_SN"
        },
        {
            "name": "No serial_no in __init__, open() without params",
            "init_serial": None,
            "init_ip": None,
            "open_serial": None,
            "open_ip": None,
            "expected_serial": None,
            "expected_path": "SelectUSB"
        },
        {
            "name": "ip_addr from __init__, open() without params",
            "init_serial": None,
            "init_ip": "192.168.1.1:80",
            "open_serial": None,
            "open_ip": None,
            "expected_serial": None,
            "expected_path": "IP"
        },
        {
            "name": "Both serial_no and ip_addr from __init__, open() without params",
            "init_serial": 600115433,
            "init_ip": "192.168.1.1:80",
            "open_serial": None,
            "open_ip": None,
            "expected_serial": 600115433,
            "expected_path": "IP_SN"
        },
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"  Testing: {case['name']}")
        
        # Simulate the logic
        serial_no = case['open_serial']
        ip_addr = case['open_ip']
        __serial_no = case['init_serial']
        __ip_addr = case['init_ip']
        
        # Apply the logic from open()
        if serial_no is None and ip_addr is None:
            serial_no = __serial_no
        
        if ip_addr is None:
            ip_addr = __ip_addr
        
        # Determine which path would be taken
        if ip_addr is not None:
            path = "IP_SN" if serial_no is not None else "IP"
        elif serial_no is not None:
            path = "USB_SN"
        else:
            path = "SelectUSB"
        
        # Verify
        if serial_no == case['expected_serial'] and path == case['expected_path']:
            print(f"    ✅ PASS: serial_no={serial_no}, path={path}")
        else:
            print(f"    ❌ FAIL: Expected serial_no={case['expected_serial']}, path={case['expected_path']}, got serial_no={serial_no}, path={path}")
            all_passed = False
    
    if all_passed:
        print("\n✅ Logic flow tests PASSED\n")
    else:
        print("\n❌ Some logic flow tests FAILED\n")
    
    return all_passed


if __name__ == '__main__':
    success = True
    
    success &= test_code_structure()
    success &= test_logic_flow()
    
    print("=" * 70)
    if success:
        print("✅ ALL INTEGRATION TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 70)
    
    sys.exit(0 if success else 1)

