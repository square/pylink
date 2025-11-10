#!/usr/bin/env python3
"""
RTT Diagnostic Script - Detailed debugging
"""

import pylink
import time
import sys

def main():
    print("=" * 70)
    print("RTT Diagnostic Script - nRF54L15")
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
        print(f"    RAM Size: 0x{jlink._device.RAMSize:08X}")
        
        time.sleep(2.0)
        
        # Step 3: Check device state
        print("\n[3] Checking device state...")
        try:
            is_connected = jlink._dll.JLINKARM_IsConnected()
            print(f"  IsConnected: {is_connected}")
            
            is_halted = jlink._dll.JLINKARM_IsHalted()
            print(f"  IsHalted: {is_halted}")
            
            if is_halted == 1:
                print("  → Resuming device...")
                jlink._dll.JLINKARM_Go()
                time.sleep(1.0)
                is_halted = jlink._dll.JLINKARM_IsHalted()
                print(f"  IsHalted after resume: {is_halted}")
        except Exception as e:
            print(f"  ⚠ Could not check device state: {e}")
        
        # Step 4: Set search ranges manually
        print("\n[4] Setting RTT search ranges...")
        ram_start = jlink._device.RAMAddr
        ram_end = ram_start + jlink._device.RAMSize - 1
        print(f"  Setting range: 0x{ram_start:08X} - 0x{ram_end:08X}")
        
        try:
            result = jlink.exec_command(f"SetRTTSearchRanges {ram_start:X} {ram_end:X}")
            print(f"  ✓ SetRTTSearchRanges result: {result}")
        except Exception as e:
            print(f"  ✗ SetRTTSearchRanges failed: {e}")
        
        time.sleep(0.5)
        
        # Step 5: Start RTT
        print("\n[5] Starting RTT...")
        try:
            config = None
            jlink.rtt_control(pylink.enums.JLinkRTTCommand.START, config)
            print("  ✓ RTT START command sent")
        except Exception as e:
            print(f"  ✗ RTT START failed: {e}")
            return 1
        
        # Step 6: Poll for buffers with detailed logging
        print("\n[6] Polling for RTT buffers...")
        max_wait = 15.0
        start_time = time.time()
        wait_interval = 0.2
        
        found_buffers = False
        last_exception = None
        
        while (time.time() - start_time) < max_wait:
            elapsed = time.time() - start_time
            try:
                num_up = jlink.rtt_get_num_up_buffers()
                num_down = jlink.rtt_get_num_down_buffers()
                
                if num_up > 0 or num_down > 0:
                    print(f"  ✓ Found buffers at {elapsed:.2f}s: {num_up} up, {num_down} down")
                    
                    # Verify persistence
                    time.sleep(0.3)
                    try:
                        num_up_check = jlink.rtt_get_num_up_buffers()
                        num_down_check = jlink.rtt_get_num_down_buffers()
                        if num_up_check > 0 or num_down_check > 0:
                            print(f"  ✓ Buffers still present: {num_up_check} up, {num_down_check} down")
                            found_buffers = True
                            break
                        else:
                            print(f"  ⚠ Buffers disappeared!")
                    except Exception as e:
                        print(f"  ⚠ Buffers disappeared: {e}")
                else:
                    if int(elapsed * 5) % 5 == 0:  # Print every second
                        print(f"  ... waiting ({elapsed:.1f}s) - no buffers yet")
            except pylink.errors.JLinkRTTException as e:
                last_exception = e
                if int(elapsed * 5) % 5 == 0:  # Print every second
                    print(f"  ... waiting ({elapsed:.1f}s) - {e}")
            except Exception as e:
                print(f"  ✗ Unexpected error: {e}")
                import traceback
                traceback.print_exc()
                break
            
            time.sleep(wait_interval)
        
        if not found_buffers:
            print(f"\n  ✗ Failed to find buffers after {max_wait}s")
            if last_exception:
                print(f"  Last error: {last_exception}")
            return 1
        
        # Step 7: Try to read from buffers
        print("\n[7] Testing RTT read...")
        try:
            data = jlink.rtt_read(0, 1024)
            print(f"  ✓ Read {len(data)} bytes from buffer 0")
            if data:
                try:
                    text = bytes(data).decode('utf-8', errors='replace')
                    print(f"  Content: {repr(text[:100])}")
                except:
                    print(f"  Content (hex): {bytes(data[:20]).hex()}")
        except Exception as e:
            print(f"  ✗ Read failed: {e}")
        
        print("\n" + "=" * 70)
        print("Diagnostic complete")
        return 0
        
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

