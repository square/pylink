#!/usr/bin/env python3
"""
RTT Connection Test Script - Debug Version
Connects to nRF54L15 via J-Link and displays RTT logs in real-time
"""

import pylink
import time
import sys
import signal

# Global flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print("\n\nStopping RTT monitor...")
    running = False

def main():
    """Main function to test RTT connection and display logs"""
    global running
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 70)
    print("RTT Connection Test - nRF54L15 (Debug Mode)")
    print("=" * 70)
    
    jlink = None
    
    try:
        # Step 1: Open J-Link
        print("\n[1/5] Opening J-Link connection...")
        jlink = pylink.JLink()
        jlink.open()
        print("  ✓ J-Link opened successfully")
        
        # Step 2: Connect to device
        print("\n[2/5] Connecting to device...")
        device_name = None
        for name in ['NRF54L15_M33', 'NRF54L15 M33']:
            try:
                jlink.connect(name, verbose=False)
                device_name = name
                print(f"  ✓ Connected to device: {name}")
                print(f"    RAM Start: 0x{jlink._device.RAMAddr:08X}")
                print(f"    RAM Size:  0x{jlink._device.RAMSize:08X}")
                break
            except Exception as e:
                print(f"  ✗ Failed to connect as '{name}': {e}")
                continue
        
        if not device_name:
            print("  ✗ Could not connect to device with any name")
            return 1
        
        # Wait for device to stabilize
        print("\n  Waiting for device to stabilize...")
        time.sleep(2.0)
        
        # Step 3: Start RTT with explicit search ranges
        print("\n[3/5] Starting RTT...")
        try:
            # Use explicit search ranges matching RTT Viewer
            ram_start = jlink._device.RAMAddr
            ram_size = jlink._device.RAMSize
            ram_end = ram_start + ram_size - 1
            
            print(f"  Using search range: 0x{ram_start:08X} - 0x{ram_end:08X}")
            
            # Try auto-detection first, but fallback to specific address if needed
            # Known control block address for nRF54L15: 0x200044E0
            control_block_addr = 0x200044E0
            
            try:
                # First try auto-detection
                jlink.rtt_start(search_ranges=[(ram_start, ram_end)])
                print("  ✓ RTT started with auto-detection")
                
                # Wait and check if buffers are found
                time.sleep(2.0)
                num_up = jlink.rtt_get_num_up_buffers()
                if num_up > 0:
                    print("  ✓ Auto-detection successful")
                else:
                    raise pylink.errors.JLinkRTTException("Auto-detection failed")
            except Exception as e:
                print(f"  ⚠ Auto-detection failed: {e}")
                print(f"  → Trying with specific control block address: 0x{control_block_addr:08X}")
                jlink.rtt_stop()  # Stop previous attempt
                time.sleep(0.5)
                jlink.rtt_start(block_address=control_block_addr, search_ranges=[(ram_start, ram_end)])
                print("  ✓ RTT started with specific address")
            
            # Wait for RTT to stabilize
            print("  Waiting for RTT to stabilize...")
            time.sleep(1.0)
        except Exception as e:
            print(f"  ✗ Failed to start RTT: {e}")
            import traceback
            traceback.print_exc()
            return 1
        
        # Step 4: Get RTT buffer information (with retries)
        print("\n[4/5] Getting RTT buffer information...")
        num_up = 0
        num_down = 0
        
        # Retry getting buffer info
        for attempt in range(10):
            try:
                num_up = jlink.rtt_get_num_up_buffers()
                num_down = jlink.rtt_get_num_down_buffers()
                print(f"  ✓ Found {num_up} up buffers, {num_down} down buffers")
                break
            except pylink.errors.JLinkRTTException as e:
                if attempt < 9:
                    if attempt % 2 == 0:  # Print every 2 attempts
                        print(f"  Waiting for buffers... (attempt {attempt + 1}/10)")
                    time.sleep(0.5)
                else:
                    print(f"  ✗ Failed to get buffer info after 10 attempts: {e}")
                    print("\n  Debugging info:")
                    print("    - RTT START command was sent")
                    print("    - Search ranges were configured")
                    print("    - But control block not found")
                    print("\n  Possible issues:")
                    print("    - Firmware may not have RTT initialized")
                    print("    - Device may not be running")
                    print("    - RTT control block address may be outside search range")
                    return 1
            except Exception as e:
                print(f"  ✗ Unexpected error: {e}")
                import traceback
                traceback.print_exc()
                return 1
        
        if num_up == 0:
            print("  ⚠ Warning: No up buffers found.")
            return 1
        
        # Step 5: Monitor RTT output
        print("\n[5/5] Monitoring RTT output...")
        print("  Press Ctrl+C to stop")
        print("  Will auto-exit after 60 seconds of inactivity\n")
        print("-" * 70)
        
        buffer_index = 0  # Usually buffer 0 is used for terminal output
        read_size = 1024  # Read up to 1024 bytes at a time
        
        bytes_received = 0
        start_time = time.time()
        last_data_time = time.time()
        max_idle_time = 60.0  # Auto-exit after 60 seconds without data
        
        while running:
            try:
                # Check for idle timeout
                if time.time() - last_data_time > max_idle_time:
                    print(f"\n⚠ No data received for {max_idle_time:.0f} seconds. Auto-exiting...")
                    break
                
                # Read data from RTT buffer
                data = jlink.rtt_read(buffer_index, read_size)
                
                if data:
                    last_data_time = time.time()  # Update last data time
                    # Convert bytes to string and print
                    try:
                        # Handle both text and binary data
                        text = bytes(data).decode('utf-8', errors='replace')
                        sys.stdout.write(text)
                        sys.stdout.flush()
                        bytes_received += len(data)
                    except Exception as e:
                        # If text conversion fails, show hex
                        hex_str = ' '.join(f'{b:02x}' for b in data[:16])
                        print(f"\n[Binary data ({len(data)} bytes): {hex_str}...]")
                        bytes_received += len(data)
                
                # Small delay to avoid CPU spinning
                time.sleep(0.1)
                
            except pylink.errors.JLinkRTTException as e:
                # RTT buffer might be empty or error occurred
                error_msg = str(e)
                if "not found" in error_msg.lower() or "wait" in error_msg.lower():
                    # Control block not found - check timeout
                    if time.time() - last_data_time > max_idle_time:
                        print(f"\n⚠ No data received for {max_idle_time:.0f} seconds. Auto-exiting...")
                        break
                    time.sleep(0.1)
                    continue
                else:
                    print(f"\n✗ RTT exception: {e}")
                    break
            except Exception as e:
                if running:
                    print(f"\n✗ Error reading RTT: {type(e).__name__}: {e}")
                    import traceback
                    traceback.print_exc()
                break
        
        elapsed_time = time.time() - start_time
        print("\n" + "-" * 70)
        print(f"\n✓ RTT monitoring stopped")
        print(f"  Total bytes received: {bytes_received}")
        print(f"  Duration: {elapsed_time:.2f} seconds")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 0
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        if jlink:
            try:
                print("\nCleaning up...")
                jlink.rtt_stop()
                jlink.close()
                print("  ✓ Cleanup complete")
            except Exception as e:
                print(f"  ⚠ Cleanup warning: {e}")

if __name__ == '__main__':
    sys.exit(main())
