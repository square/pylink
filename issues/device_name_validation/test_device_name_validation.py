#!/usr/bin/env python
"""Test script for device name validation and suggestions.

This script tests the improved device name validation and suggestion functionality
in pylink.jlink.get_device_index() and pylink.jlink.connect().

Tests cover:
- None/empty string validation
- Invalid device names
- Common naming variations (CORTEX_M33 -> Cortex-M33)
- Nordic device naming patterns (NRF54L15 -> NRF54L15_M33)
- Error message quality
"""

import sys
import os

# Add pylink to path
_test_dir = os.path.dirname(os.path.abspath(__file__))
_pylink_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))
if _pylink_root not in sys.path:
    sys.path.insert(0, _pylink_root)

import pylink
import pylink.enums
import pylink.errors

# Device name that should work (adjust based on your hardware)
DEVICE_NAME = 'NRF54L15_M33'

def test_none_device_name():
    """Test that None device name raises ValueError."""
    print("=" * 70)
    print("Test 1: None device name")
    print("=" * 70)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        
        try:
            jlink.connect(None)
            print("❌ FAIL: Should have raised ValueError for None")
            return False
        except ValueError as e:
            print(f"✅ PASS: Correctly raised ValueError")
            print(f"   Message: {str(e)}")
            if "cannot be None" in str(e) or "None" in str(e):
                print("   ✅ Error message is informative")
            else:
                print("   ⚠️  Error message could be more specific")
            return True
        except Exception as e:
            print(f"❌ FAIL: Raised {type(e).__name__} instead of ValueError: {e}")
            return False
        finally:
            jlink.close()
    except Exception as e:
        print(f"❌ FAIL: Setup error: {e}")
        return False


def test_empty_device_name():
    """Test that empty string device name raises ValueError."""
    print("\n" + "=" * 70)
    print("Test 2: Empty string device name")
    print("=" * 70)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        
        try:
            jlink.connect('')
            print("❌ FAIL: Should have raised ValueError for empty string")
            return False
        except ValueError as e:
            print(f"✅ PASS: Correctly raised ValueError")
            print(f"   Message: {str(e)}")
            if "cannot be empty" in str(e) or "empty" in str(e).lower():
                print("   ✅ Error message is informative")
            else:
                print("   ⚠️  Error message could be more specific")
            return True
        except Exception as e:
            print(f"❌ FAIL: Raised {type(e).__name__} instead of ValueError: {e}")
            return False
        finally:
            jlink.close()
    except Exception as e:
        print(f"❌ FAIL: Setup error: {e}")
        return False


def test_whitespace_device_name():
    """Test that whitespace-only device name raises ValueError."""
    print("\n" + "=" * 70)
    print("Test 3: Whitespace-only device name")
    print("=" * 70)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        
        try:
            jlink.connect('   ')
            print("❌ FAIL: Should have raised ValueError for whitespace-only string")
            return False
        except ValueError as e:
            print(f"✅ PASS: Correctly raised ValueError")
            print(f"   Message: {str(e)}")
            return True
        except Exception as e:
            print(f"❌ FAIL: Raised {type(e).__name__} instead of ValueError: {e}")
            return False
        finally:
            jlink.close()
    except Exception as e:
        print(f"❌ FAIL: Setup error: {e}")
        return False


def test_cortex_naming_variation():
    """Test that CORTEX_M33 suggests Cortex-M33."""
    print("\n" + "=" * 70)
    print("Test 4: Cortex naming variation (CORTEX_M33 -> Cortex-M33)")
    print("=" * 70)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        
        try:
            jlink.connect('CORTEX_M33')
            print("❌ FAIL: Should have raised JLinkException for invalid name")
            return False
        except pylink.errors.JLinkException as e:
            print(f"✅ PASS: Correctly raised JLinkException")
            error_msg = str(e)
            print(f"   Message: {error_msg}")
            
            # Check if suggestion is present
            if 'Cortex-M33' in error_msg:
                print("   ✅ Error message suggests 'Cortex-M33'")
                return True
            else:
                print("   ⚠️  Error message doesn't suggest 'Cortex-M33'")
                print(f"   Expected: Contains 'Cortex-M33'")
                return False
        except Exception as e:
            print(f"❌ FAIL: Raised {type(e).__name__} instead of JLinkException: {e}")
            return False
        finally:
            jlink.close()
    except Exception as e:
        print(f"❌ FAIL: Setup error: {e}")
        return False


def test_nordic_naming_variation():
    """Test that NRF54L15 suggests NRF54L15_M33."""
    print("\n" + "=" * 70)
    print("Test 5: Nordic naming variation (NRF54L15 -> NRF54L15_M33)")
    print("=" * 70)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        
        try:
            jlink.connect('NRF54L15')
            print("❌ FAIL: Should have raised JLinkException for invalid name")
            return False
        except pylink.errors.JLinkException as e:
            print(f"✅ PASS: Correctly raised JLinkException")
            error_msg = str(e)
            print(f"   Message: {error_msg}")
            
            # Check if suggestion is present
            if 'NRF54L15_M33' in error_msg:
                print("   ✅ Error message suggests 'NRF54L15_M33'")
                return True
            else:
                print("   ⚠️  Error message doesn't suggest 'NRF54L15_M33'")
                print(f"   Expected: Contains 'NRF54L15_M33'")
                return False
        except Exception as e:
            print(f"❌ FAIL: Raised {type(e).__name__} instead of JLinkException: {e}")
            return False
        finally:
            jlink.close()
    except Exception as e:
        print(f"❌ FAIL: Setup error: {e}")
        return False


def test_completely_wrong_device_name():
    """Test that completely wrong device name gives basic error."""
    print("\n" + "=" * 70)
    print("Test 6: Completely wrong device name")
    print("=" * 70)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        
        try:
            jlink.connect('WRONG_DEVICE_NAME_XYZ')
            print("❌ FAIL: Should have raised JLinkException for invalid name")
            return False
        except pylink.errors.JLinkException as e:
            print(f"✅ PASS: Correctly raised JLinkException")
            error_msg = str(e)
            print(f"   Message: {error_msg}")
            
            # Should include the attempted name
            if 'WRONG_DEVICE_NAME_XYZ' in error_msg:
                print("   ✅ Error message includes attempted device name")
            else:
                print("   ⚠️  Error message doesn't include attempted device name")
            
            # May or may not have suggestions (depends on implementation)
            if 'Try:' in error_msg or 'Did you mean:' in error_msg:
                print("   ✅ Error message includes suggestions")
            else:
                print("   ℹ️  No suggestions (acceptable for completely wrong names)")
            
            return True
        except Exception as e:
            print(f"❌ FAIL: Raised {type(e).__name__} instead of JLinkException: {e}")
            return False
        finally:
            jlink.close()
    except Exception as e:
        print(f"❌ FAIL: Setup error: {e}")
        return False


def test_valid_device_name():
    """Test that valid device name connects successfully."""
    print("\n" + "=" * 70)
    print(f"Test 7: Valid device name ({DEVICE_NAME})")
    print("=" * 70)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        
        try:
            jlink.connect(DEVICE_NAME)
            print(f"✅ PASS: Successfully connected to '{DEVICE_NAME}'")
            return True
        except Exception as e:
            print(f"❌ FAIL: Failed to connect to valid device name: {e}")
            print(f"   Note: This test requires hardware. If no device is connected,")
            print(f"   this test will fail. Adjust DEVICE_NAME constant if needed.")
            return False
        finally:
            jlink.close()
    except Exception as e:
        print(f"❌ FAIL: Setup error: {e}")
        return False


def test_get_device_index_directly():
    """Test get_device_index() directly with various inputs."""
    print("\n" + "=" * 70)
    print("Test 8: Direct get_device_index() calls")
    print("=" * 70)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        
        test_cases = [
            (None, ValueError, "None"),
            ('', ValueError, "empty string"),
            ('   ', ValueError, "whitespace"),
            ('INVALID_DEVICE', pylink.errors.JLinkException, "invalid device"),
        ]
        
        passed = 0
        failed = 0
        
        for chip_name, expected_exception, description in test_cases:
            try:
                jlink.get_device_index(chip_name)
                print(f"   ❌ FAIL ({description}): Should have raised {expected_exception.__name__}")
                failed += 1
            except expected_exception as e:
                print(f"   ✅ PASS ({description}): Correctly raised {expected_exception.__name__}")
                print(f"      Message: {str(e)[:80]}...")
                passed += 1
            except Exception as e:
                print(f"   ❌ FAIL ({description}): Raised {type(e).__name__} instead of {expected_exception.__name__}: {e}")
                failed += 1
        
        print(f"\n   Summary: {passed} passed, {failed} failed")
        return failed == 0
    except Exception as e:
        print(f"❌ FAIL: Setup error: {e}")
        return False
    finally:
        jlink.close()


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("Device Name Validation and Suggestions Test Suite")
    print("=" * 70)
    print(f"\nTesting with device: {DEVICE_NAME}")
    print("(Adjust DEVICE_NAME constant if your hardware uses a different name)\n")
    
    tests = [
        ("None device name", test_none_device_name),
        ("Empty string device name", test_empty_device_name),
        ("Whitespace-only device name", test_whitespace_device_name),
        ("Cortex naming variation", test_cortex_naming_variation),
        ("Nordic naming variation", test_nordic_naming_variation),
        ("Completely wrong device name", test_completely_wrong_device_name),
        ("Valid device name", test_valid_device_name),
        ("Direct get_device_index() calls", test_get_device_index_directly),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ FAIL: Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    failed = sum(1 for _, result in results if not result)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-" * 70)
    print(f"Total: {len(results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())

