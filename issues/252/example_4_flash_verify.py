#!/usr/bin/env python3
"""
Example 4: Flash Programming with Reset Verification

Verifying device reset after flashing firmware using check_connection_health().
"""

import pylink
import time
import sys
import os


def flash_and_verify(firmware_path, address=0x0):
    """Flash firmware and verify device reset"""
    jlink = pylink.JLink()
    
    try:
        jlink.open()
        jlink.set_tif(pylink.JLinkInterfaces.SWD)
        jlink.connect("NRF54L15_M33")
        
        # Check if firmware file exists
        if not os.path.exists(firmware_path):
            print(f"Error: Firmware file not found: {firmware_path}")
            return False
        
        # Flash firmware
        print(f"Flashing {firmware_path} to address 0x{address:X}...")
        jlink.flash_file(firmware_path, address)
        print("Flash complete")
        
        # Wait for reset and verify device comes back online
        print("Waiting for device reset...")
        max_wait = 10.0  # 10 seconds max (should be enough for most devices)
        start_time = time.time()
        reset_detected = False
        reconnect_delay = 0.5  # Start with 0.5 second delay
        max_reconnect_attempts = 5
        
        while time.time() - start_time < max_wait:
            if not jlink.check_connection_health():
                # Device is resetting
                if not reset_detected:
                    reset_detected = True
                    print("Reset detected, waiting for device to stabilize...")
                time.sleep(0.1)
                continue
            elif reset_detected:
                # Device reset complete - verify it's stable with multiple checks
                print("Device accessible after reset, verifying stability...")
                
                # Verify device is stable with multiple health checks
                stable_checks = 0
                required_stable_checks = 3  # Need 3 consecutive successful checks
                
                for attempt in range(max_reconnect_attempts):
                    if jlink.check_connection_health():
                        stable_checks += 1
                        if stable_checks >= required_stable_checks:
                            print("Device reset complete and running stably!")
                            return True
                    else:
                        # Device became inaccessible again, reset counter
                        stable_checks = 0
                        print(f"  Device unstable, waiting {reconnect_delay:.1f}s...")
                        time.sleep(reconnect_delay)
                        reconnect_delay *= 1.5  # Exponential backoff
                
                if stable_checks < required_stable_checks:
                    print("Device did not stabilize after reset")
                    return False
        
        if reset_detected:
            print("Timeout waiting for device to come back online after reset")
        else:
            print("No reset detected (device may not have reset)")
        
        return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        try:
            jlink.close()
        except:
            pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 example_4_flash_verify.py <firmware.hex> [address]")
        print("Example: python3 example_4_flash_verify.py firmware.hex 0x0")
        sys.exit(1)
    
    firmware_path = sys.argv[1]
    address = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x0
    
    success = flash_and_verify(firmware_path, address)
    if success:
        print("Flash and verification successful!")
    else:
        print("Flash verification failed")
    
    sys.exit(0 if success else 1)

