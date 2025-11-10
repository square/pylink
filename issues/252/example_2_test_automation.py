#!/usr/bin/env python3
"""
Example 2: Long-Running Test Automation

Using check_connection_health() in test automation to detect unexpected
device resets during test execution.
"""

import pylink
import time
import sys


def test_function_1(jlink):
    """Example test function 1"""
    print("Running test_function_1...")
    time.sleep(0.5)  # Simulate test execution
    return True


def test_function_2(jlink):
    """Example test function 2"""
    print("Running test_function_2...")
    time.sleep(0.5)  # Simulate test execution
    return True


def test_function_3(jlink):
    """Example test function 3"""
    print("Running test_function_3...")
    time.sleep(0.5)  # Simulate test execution
    return True


def run_test_suite():
    """Test suite with reset detection"""
    jlink = pylink.JLink()
    
    try:
        jlink.open()
        jlink.set_tif(pylink.JLinkInterfaces.SWD)
        jlink.connect("NRF54L15_M33")
        
        test_suite = [
            test_function_1,
            test_function_2,
            test_function_3,
        ]
        
        for test in test_suite:
            # Before each test, verify device is still connected (check health )
            if not jlink.check_connection_health():
                raise RuntimeError("Device reset detected before test")
            
            # Run the test
            result = test(jlink)
            
            if not result:
                raise RuntimeError(f"Test failed: {test.__name__}")
            
            # After test, verify device didn't reset during execution (sometimes happens )
            if not jlink.check_connection_health():
                raise RuntimeError("Device reset during test execution")
            
            print(f"✓ Test passed: {test.__name__}")
        
        print("\n✓ All tests passed!")
        
    except RuntimeError as e:
        print(f"\n✗ Test suite failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False
    finally:
        try:
            jlink.close()
        except:
            pass
    
    return True


if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)

