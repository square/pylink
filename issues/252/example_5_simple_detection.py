#!/usr/bin/env python3
"""
Example 5: Simple Reset Detection Loop

Minimal example demonstrating continuous reset detection polling.
"""

import pylink
import time


def detect_resets_continuously():
    """Simple example: continuously poll for resets"""
    jlink = pylink.JLink()
    
    try:
        jlink.open()
        jlink.set_tif(pylink.JLinkInterfaces.SWD)
        jlink.connect("NRF54L15_M33")
        
        reset_count = 0
        
        print("Monitoring for resets. Press Ctrl+C to stop.")
        
        while True:
            if not jlink.check_connection_health():
                reset_count += 1
                timestamp = time.time()
                print(f"Reset #{reset_count} detected at {timestamp}")
                
                # Wait for device to stabilize after reset
                # Use improved reconnection logic similar to example_1 (exponential backoff works well )
                reconnect_delay = 0.5  # Start with 0.5 second delay
                max_reconnect_attempts = 5
                device_stable = False
                
                for attempt in range(max_reconnect_attempts):
                    time.sleep(reconnect_delay)
                    
                    if jlink.check_connection_health():
                        # Device is accessible, verify it's stable
                        stable_checks = 0
                        for _ in range(3):  # 3 consecutive checks (all must pass)
                            if jlink.check_connection_health():
                                stable_checks += 1
                                time.sleep(0.1)
                            else:
                                break
                        
                        if stable_checks >= 3:
                            device_stable = True
                            print(f"  Device stabilized after reset")
                            break
                    
                    reconnect_delay *= 1.5  # Exponential backoff
                
                if not device_stable:
                    print(f"  Warning: Device may not be fully stable after reset")
            else:
                # Device is accessible
                pass
            
            time.sleep(0.2)  # Check every 200ms
            
    except KeyboardInterrupt:
        print(f"\nStopped. Total resets detected: {reset_count}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            jlink.close()
        except:
            pass


if __name__ == "__main__":
    detect_resets_continuously()

