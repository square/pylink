#!/usr/bin/env python3
"""
Example 6: Detailed Health Check

Using check_connection_health(detailed=True) to get detailed information
about each health check component (IDCODE, CPUID, registers).
"""

import pylink
import time


def detailed_health_check():
    """Example using detailed health check"""
    jlink = pylink.JLink()
    
    try:
        jlink.open()
        jlink.set_tif(pylink.JLinkInterfaces.SWD)
        jlink.connect("NRF54L15_M33")
        
        print("Detailed health check monitoring. Press Ctrl+C to stop.")
        print("-" * 60)
        
        while True:
            health = jlink.check_connection_health(detailed=True)
            
            if health['all_accessible']:
                print("Device accessible:")
                if health['idcode']:
                    print(f"  IDCODE: 0x{health['idcode']:08X}")
                if health['cpuid']:
                    print(f"  CPUID: 0x{health['cpuid']:08X}")
                if health['register_r0']:
                    print(f"  R0: 0x{health['register_r0']:08X}")
                else:
                    print("  R0: Not available (CPU may be running, can't read registers)")
            else:
                print("Device not accessible (reset or disconnection)")
            
            print("-" * 60)
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            jlink.close()
        except:
            pass


if __name__ == "__main__":
    detailed_health_check()

