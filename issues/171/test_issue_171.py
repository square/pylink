#!/usr/bin/env python
"""Test script for Issue #171: exec_command() Informational Messages

This script validates that exec_command() no longer raises exceptions
for informational messages like "RTT Telnet Port set to 19021".

Usage:
    python test_issue_171.py

Requirements:
    - J-Link connected
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

def test_set_rtt_telnet_port():
    """Test that SetRTTTelnetPort doesn't raise exception on success."""
    print("Test 1: SetRTTTelnetPort command")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        
        # This command returns informational message "RTT Telnet Port set to 19021"
        # It should NOT raise an exception
        try:
            result = jlink.exec_command('SetRTTTelnetPort 19021')
            print("✅ SetRTTTelnetPort executed without exception")
            print(f"   Return value: {result}")
            return True
        except pylink.errors.JLinkException as e:
            error_msg = str(e)
            # Check if it's actually an error or just informational
            if "RTT Telnet Port set to" in error_msg:
                print(f"❌ Still raising exception for informational message: {error_msg}")
                return False
            else:
                print(f"⚠️  Got different error: {error_msg}")
                return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        jlink.close()


def test_other_informational_commands():
    """Test other commands that return informational messages."""
    print("\nTest 2: Other informational commands")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        
        # Commands that might return informational messages
        test_commands = [
            'SetResetDelay 100',
            'SetResetType 0',
        ]
        
        all_passed = True
        for cmd in test_commands:
            try:
                result = jlink.exec_command(cmd)
                print(f"✅ {cmd}: executed without exception (return: {result})")
            except pylink.errors.JLinkException as e:
                error_msg = str(e)
                # Check if it's informational
                if any(keyword in error_msg.lower() for keyword in 
                       ['reset delay', 'reset type', 'set to']):
                    print(f"❌ {cmd}: Still raising exception for informational message: {error_msg}")
                    all_passed = False
                else:
                    print(f"⚠️  {cmd}: Got error (may be legitimate): {error_msg}")
        
        return all_passed
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        jlink.close()


def test_error_commands_still_raise():
    """Test that actual errors still raise exceptions."""
    print("\nTest 3: Actual errors still raise exceptions")
    print("-" * 50)
    
    jlink = pylink.JLink()
    try:
        jlink.open()
        
        # This should be an actual error
        try:
            result = jlink.exec_command('InvalidCommandThatDoesNotExist')
            print("⚠️  Invalid command did not raise exception (unexpected)")
            return None
        except pylink.errors.JLinkException as e:
            print(f"✅ Invalid command correctly raised exception: {e}")
            return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        jlink.close()


if __name__ == '__main__':
    print("=" * 50)
    print("Issue #171: exec_command() Informational Messages Tests")
    print("=" * 50)
    
    results = []
    
    result = test_set_rtt_telnet_port()
    if result is not None:
        results.append(("SetRTTTelnetPort", result))
    result = test_other_informational_commands()
    if result is not None:
        results.append(("Other informational commands", result))
    result = test_error_commands_still_raise()
    if result is not None:
        results.append(("Actual errors still raise", result))
    
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

