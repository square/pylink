#!/usr/bin/env python3
"""
RTT Diagnostic Script - Testing with specific control block address
"""

import pylink
import time
import sys

def main():
    print("=" * 70)
    print("RTT Diagnostic Script - Using Specific Control Block Address")
    print("=" * 70)
    
    jlink = None
    
    try:
        # Step 1: Open J-Link
        print("\n[1] Opening J-Link...")
        jlink = pylink.JLink()
        jlink.open()
        print("  ✓ J-Link opened")
        
        # Step 2: Connect to device
        print("\n[2] Connecting to device...")
        device_name = 'NRF54L15_M33'
        jlink.connect(device_name, verbose=False)
        print(f"  ✓ Connected: {device_name}")
        print(f"    RAM: 0x{jlink._device.RAMAddr:08X} - 0x{jlink._device.RAMAddr + jlink._device.RAMSize - 1:08X}")
        
        time.sleep(2.0)
        
        # Step 3: Check device state
        print("\n[3] Checking device state...")
        try:
            is_halted = jlink._dll.JLINKARM_IsHalted()
            print(f"  IsHalted: {is_halted}")
            
            if is_halted == 1:
                print("  → Resuming device...")
                jlink._dll.JLINKARM_Go()
                time.sleep(1.0)
        except Exception as e:
            print(f"  ⚠ Could not check device state: {e}")
        
        # Step 4: Set search ranges
        print("\n[4] Setting RTT search ranges...")
        ram_start = jlink._device.RAMAddr
        ram_end = ram_start + jlink._device.RAMSize - 1
        print(f"  Range: 0x{ram_start:08X} - 0x{ram_end:08X}")
        
        try:
            jlink.exec_command(f"SetRTTSearchRanges {ram_start:X} {ram_end:X}")
            print("  ✓ Search ranges set")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
        
        time.sleep(0.5)
        
        # Step 5: Start RTT with specific control block address
        print("\n[5] Starting RTT with specific control block address...")
        control_block_addr = 0x200044E0
        print(f"  Control block address: 0x{control_block_addr:08X}")
        
        try:
            # Use rtt_start with block_address parameter
            jlink.rtt_start(block_address=control_block_addr)
            print("  ✓ RTT started with specific address")
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            return 1
        
        # Step 6: Check for buffers
        print("\n[6] Checking for RTT buffers...")
        time.sleep(1.0)
        
        for attempt in range(5):
            try:
                num_up = jlink.rtt_get_num_up_buffers()
                num_down = jlink.rtt_get_num_down_buffers()
                print(f"  ✓ Found {num_up} up buffers, {num_down} down buffers")
                
                if num_up > 0:
                    # Try to read
                    print("\n[7] Testing RTT read...")
                    data = jlink.rtt_read(0, 1024)
                    print(f"  ✓ Read {len(data)} bytes")
                    if data:
                        try:
                            text = bytes(data).decode('utf-8', errors='replace')
                            print(f"  Content: {repr(text[:200])}")
                        except:
                            print(f"  Content (hex): {bytes(data[:40]).hex()}")
                    return 0
                break
            except pylink.errors.JLinkRTTException as e:
                if attempt < 4:
                    print(f"  Waiting... (attempt {attempt + 1}/5)")
                    time.sleep(0.5)
                else:
                    print(f"  ✗ Failed after 5 attempts: {e}")
                    return 1
        
        return 1
        
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if jlink:
            try:
                jlink.rtt_stop()
                jlink.close()
            except:
                pass

if __name__ == '__main__':
    sys.exit(main())

