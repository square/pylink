#!/usr/bin/env python3
"""
Simple RTT test - Quick verification
"""
import pylink
import time

print("Testing pylink RTT functionality...")
print("=" * 70)

try:
    # Open J-Link
    print("\n[1] Opening J-Link...")
    jlink = pylink.JLink()
    jlink.open()
    print("  ✓ J-Link opened")
    
    # Connect to device
    print("\n[2] Connecting to device...")
    jlink.connect('NRF54L15_M33', verbose=False)
    print("  ✓ Connected to NRF54L15_M33")
    print(f"    RAM: 0x{jlink._device.RAMAddr:08X} - 0x{jlink._device.RAMAddr + jlink._device.RAMSize - 1:08X}")
    
    time.sleep(2.0)
    
    # Start RTT with auto-detection
    print("\n[3] Starting RTT (auto-detection)...")
    jlink.rtt_start()
    print("  ✓ RTT started")
    
    time.sleep(2.0)
    
    # Get buffers
    print("\n[4] Getting RTT buffers...")
    num_up = jlink.rtt_get_num_up_buffers()
    num_down = jlink.rtt_get_num_down_buffers()
    print(f"  ✓ Found {num_up} up buffers, {num_down} down buffers")
    
    if num_up > 0:
        # Try to read
        print("\n[5] Reading RTT data...")
        data = jlink.rtt_read(0, 1024)
        print(f"  ✓ Read {len(data)} bytes")
        if data:
            text = bytes(data).decode('utf-8', errors='replace')
            print(f"  Sample: {repr(text[:100])}")
    
    print("\n" + "=" * 70)
    print("✓ Test completed successfully!")
    
    jlink.rtt_stop()
    jlink.close()
    
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

