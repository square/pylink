#!/usr/bin/env python3
"""
Example 1: RTT Monitor with Auto-Reconnection

Shows how to automatically reconnect RTT when a device reset is detected
using check_connection_health().
"""

import pylink
import time
import sys
import signal


def rtt_monitor_with_reset_detection():
    """RTT monitor that automatically reconnects on device reset"""
    jlink = None
    running = True
    
    def signal_handler(sig, frame):
        """Handle Ctrl+C gracefully"""
        nonlocal running
        print("\n\nStopping RTT monitor...")
        running = False
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        jlink = pylink.JLink()
        jlink.open()
        jlink.set_tif(pylink.JLinkInterfaces.SWD)
        #jlink.connect("NRF54L15_M33") 
        jlink.connect("Cortex-M33") # generic Cortex-M33 core used to test the search ranges as it just won't work on nrf54l15 without specific memory ranges
        
        # Configure RTT search ranges for nRF54L15 (RAM: 0x20000000 - 0x2003FFFF)
        search_ranges = [(0x20000000, 0x2003FFFF)]
        rtt_started = jlink.rtt_start(search_ranges=search_ranges)
        
        if not rtt_started:
            print("Warning: RTT control block not found. Make sure:")
            print("  1. Firmware has RTT enabled (CONFIG_SEGGER_RTT=y)")
            print("  2. Device is running")
            print("  3. RTT buffers are initialized in firmware")
            print("\nContinuing anyway - RTT may start later...")
        
        print("RTT Monitor started. Press Ctrl+C to stop.")
        print("Monitoring for resets...")
        
        last_reset_check = time.time()
        
        while running:
            try:
                # Read RTT data
                try:
                    data = jlink.rtt_read(0, 1024)
                    if data:
                        # Handle both bytes and list of bytes
                        if isinstance(data, list):
                            if len(data) > 0:  # Check list is not empty
                                data = bytes(data)
                            else:
                                data = None
                        elif not isinstance(data, bytes):
                            data = bytes(data)
                        
                        if data:
                            print(data.decode('utf-8', errors='ignore'), end='')
                except (pylink.errors.JLinkRTTException, IndexError, AttributeError) as e:
                    # RTT read errors are normal if no data is available or connection issues
                    # Don't spam errors, just continue
                    pass
                except Exception as e:
                    # Other unexpected errors - log but continue
                    if running:  # Only log if we're still supposed to be running
                        print(f"\n[RTT read error: {e}]")
                
                # Check for reset every 200ms
                if time.time() - last_reset_check > 0.2:
                    try:
                        if not jlink.check_connection_health():
                            print("\n[RESET DETECTED] Reconnecting RTT...")
                            
                            # Stop RTT if it was running
                            try:
                                jlink.rtt_stop()
                            except:
                                pass
                            
                            # Wait for device to stabilize after reset
                            # Device needs time to complete reset and start firmware execution (usually ~1s )
                            time.sleep(1.0)
                            
                            # Verify device is accessible and running before attempting RTT reconnect
                            max_reconnect_attempts = 5
                            reconnect_delay = 1.0  # Start with 1 second delay
                            rtt_started = False
                            
                            for attempt in range(max_reconnect_attempts):
                                # First, verify device is accessible
                                if not jlink.check_connection_health():
                                    # Device still not accessible, wait longer
                                    print(f"  Waiting for device to stabilize (attempt {attempt + 1}/{max_reconnect_attempts})...")
                                    time.sleep(reconnect_delay)
                                    reconnect_delay *= 1.5  # Exponential backoff
                                    continue
                                
                                # Device is accessible, try to start RTT
                                search_ranges = [(0x20000000, 0x2003FFFF)]  # nRF54L15 RAM range
                                print(f"  Attempting RTT reconnection (attempt {attempt + 1}/{max_reconnect_attempts})...")
                                
                                rtt_started = jlink.rtt_start(
                                    search_ranges=search_ranges,
                                    rtt_timeout=15.0  # Timeout per attempt
                                )
                                
                                if rtt_started:
                                    print("[RTT RECONNECTED]")
                                    break
                                else:
                                    # RTT not ready yet, wait before next attempt
                                    if attempt < max_reconnect_attempts - 1:
                                        print(f"  RTT control block not ready, waiting {reconnect_delay:.1f}s...")
                                        time.sleep(reconnect_delay)
                                        reconnect_delay *= 1.5  # Exponential backoff
                            
                            if not rtt_started:
                                print("[RTT RECONNECTION FAILED after all attempts]")
                                print("  Firmware may need more time to initialize RTT")
                                print("  Will continue monitoring and retry on next reset detection")
                    except Exception as e:
                        # Connection health check failed - might be during shutdown
                        if running:
                            print(f"\n[Connection check error: {e}]")
                    last_reset_check = time.time()
                
                time.sleep(0.01)  # Small delay to avoid busy-waiting (CPU friendly)
                
            except KeyboardInterrupt:
                # This shouldn't happen with signal handler, but handle it anyway
                running = False
                break
                
    except KeyboardInterrupt:
        print("\n\nStopping RTT monitor...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean shutdown
        if jlink:
            try:
                jlink.rtt_stop()
            except:
                pass
            try:
                jlink.close()
            except:
                pass


if __name__ == "__main__":
    rtt_monitor_with_reset_detection()
