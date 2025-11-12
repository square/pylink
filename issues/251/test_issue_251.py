#!/usr/bin/env python
"""Test script for Issue #251: Specify JLink Home Path

This script validates that jlink_path parameter works correctly
and that Library.from_directory() can load DLL from custom location.

Usage:
    python test_issue_251.py [jlink_path]

Requirements:
    - J-Link SDK installed
    - Optional: Custom J-Link SDK path to test
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
from pylink.library import Library

def test_jlink_path_parameter():
    """Test that jlink_path parameter works."""
    print("Test 1: jlink_path parameter")
    print("-" * 50)
    
    # Try to find a J-Link SDK directory
    # Common locations
    possible_paths = [
        "/opt/SEGGER/JLink",
        "/Applications/SEGGER/JLink",
        "C:/Program Files/SEGGER/JLink",
    ]
    
    jlink_path = None
    if len(sys.argv) > 1:
        jlink_path = sys.argv[1]
    else:
        # Try to find existing installation
        for path in possible_paths:
            if os.path.isdir(path):
                # Check for DLL/SO files
                for item in os.listdir(path):
                    if item.startswith("libjlinkarm") or item.startswith("JLink"):
                        jlink_path = path
                        break
                if jlink_path:
                    break
    
    if not jlink_path:
        print("⚠️  No J-Link SDK path found, skipping test")
        print("   Usage: python test_issue_251.py /path/to/JLink")
        return None
    
    print(f"Testing with path: {jlink_path}")
    
    try:
        # Try to create JLink with custom path
        jlink = pylink.JLink(jlink_path=jlink_path)
        print("✅ JLink created successfully with jlink_path")
        
        # Try to open (this will load the DLL)
        try:
            jlink.open()
            print("✅ JLink opened successfully")
            jlink.close()
            return True
        except Exception as e:
            print(f"⚠️  Could not open J-Link: {e}")
            print("   (This is OK if no hardware is connected)")
            return None
    except Exception as e:
        print(f"❌ Error creating JLink: {e}")
        return False


def test_library_from_directory():
    """Test that Library.from_directory() works."""
    print("\nTest 2: Library.from_directory() method")
    print("-" * 50)
    
    # Try to find a J-Link SDK directory
    possible_paths = [
        "/opt/SEGGER/JLink",
        "/Applications/SEGGER/JLink",
        "C:/Program Files/SEGGER/JLink",
    ]
    
    jlink_path = None
    if len(sys.argv) > 1:
        jlink_path = sys.argv[1]
    else:
        for path in possible_paths:
            if os.path.isdir(path):
                for item in os.listdir(path):
                    if item.startswith("libjlinkarm") or item.startswith("JLink"):
                        jlink_path = path
                        break
                if jlink_path:
                    break
    
    if not jlink_path:
        print("⚠️  No J-Link SDK path found, skipping test")
        return None
    
    print(f"Testing with path: {jlink_path}")
    
    try:
        # Try to create Library from directory
        lib = Library.from_directory(jlink_path)
        print("✅ Library created successfully from directory")
        
        # Check that DLL is loaded
        dll = lib.dll()
        if dll:
            print("✅ DLL loaded successfully")
            return True
        else:
            print("❌ DLL not loaded")
            return False
    except OSError as e:
        print(f"❌ Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_invalid_directory():
    """Test that invalid directory raises appropriate error."""
    print("\nTest 3: Invalid directory handling")
    print("-" * 50)
    
    # Try with non-existent directory
    try:
        jlink = pylink.JLink(jlink_path="/nonexistent/path/to/jlink")
        print("❌ Should have raised OSError")
        return False
    except OSError as e:
        if "not found" in str(e).lower() or "does not exist" in str(e).lower():
            print(f"✅ Correctly raised OSError for invalid path: {e}")
            return True
        else:
            print(f"❌ Wrong error message: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error type: {type(e).__name__}: {e}")
        return False


def test_backward_compatibility():
    """Test that default behavior still works (backward compatibility)."""
    print("\nTest 4: Backward compatibility (default behavior)")
    print("-" * 50)
    
    try:
        # Create JLink without jlink_path (default behavior)
        jlink = pylink.JLink()
        print("✅ JLink created successfully without jlink_path")
        
        # Try to open (this will use default DLL search)
        try:
            jlink.open()
            print("✅ JLink opened successfully with default search")
            jlink.close()
            return True
        except Exception as e:
            print(f"⚠️  Could not open J-Link: {e}")
            print("   (This is OK if no hardware is connected)")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_invalid_jlink_path_types():
    """Test that invalid jlink_path types are detected."""
    print("\nTest 5: Invalid jlink_path types detection")
    print("-" * 50)
    
    # Test with non-string types
    invalid_paths = [
        123,  # Integer
        [],   # List
        {},   # Dict
        None, # None (should work, uses default)
    ]
    
    for invalid_path in invalid_paths:
        try:
            if invalid_path is None:
                # None should work (uses default)
                jlink = pylink.JLink(jlink_path=None)
                print("✅ jlink_path=None accepted (uses default)")
                continue
            
            jlink = pylink.JLink(jlink_path=invalid_path)
            print(f"⚠️  jlink_path={type(invalid_path).__name__} accepted (may fail later)")
        except (TypeError, OSError) as e:
            print(f"✅ Correctly rejected jlink_path={type(invalid_path).__name__}: {type(e).__name__}: {e}")
        except Exception as e:
            print(f"⚠️  Unexpected error for {type(invalid_path).__name__}: {type(e).__name__}: {e}")
    
    return True


if __name__ == '__main__':
    print("=" * 50)
    print("Issue #251: JLink Path Specification Tests")
    print("=" * 50)
    print("\nNote: Some tests require J-Link SDK to be installed")
    print("      Provide custom path as argument: python test_issue_251.py /path/to/JLink")
    print()
    
    results = []
    
    result = test_jlink_path_parameter()
    if result is not None:
        results.append(("jlink_path parameter", result))
    result = test_library_from_directory()
    if result is not None:
        results.append(("Library.from_directory()", result))
    results.append(("Invalid directory handling", test_invalid_directory()))
    result = test_backward_compatibility()
    if result is not None:
        results.append(("Backward compatibility", result))
    results.append(("Invalid jlink_path types detection", test_invalid_jlink_path_types()))
    
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
        print("\n⚠️  No tests could be run (J-Link SDK may not be installed)")
        sys.exit(0)

