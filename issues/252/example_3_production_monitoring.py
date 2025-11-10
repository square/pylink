#!/usr/bin/env python3
"""
Example 3: Production Monitoring

Background monitoring of device resets using check_connection_health()
in a separate thread. Works without firmware cooperation.
"""

import pylink
import threading
import time
import sys


class DeviceMonitor:
    """Monitor device resets in production"""
    
    def __init__(self, jlink):
        self.jlink = jlink
        self.reset_count = 0
        self.monitoring = False
        self.monitor_thread = None
        self.lock = threading.Lock()
    
    def monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            try:
                if not self.jlink.check_connection_health():
                    with self.lock:
                        self.reset_count += 1
                        reset_num = self.reset_count
                    self.on_reset_detected(reset_num)
                    
                    # Wait for device to stabilize after reset
                    # Use improved reconnection logic with exponential backoff (works better than fixed delays )
                    reconnect_delay = 0.5  # Start with 0.5 second delay
                    max_reconnect_attempts = 5
                    device_stable = False
                    
                    for attempt in range(max_reconnect_attempts):
                        time.sleep(reconnect_delay)
                        
                        if self.jlink.check_connection_health():
                            # Device is accessible, verify it's stable
                            stable_checks = 0
                            for _ in range(3):  # 3 consecutive checks (need all to pass)
                                if self.jlink.check_connection_health():
                                    stable_checks += 1
                                    time.sleep(0.1)
                                else:
                                    break
                            
                            if stable_checks >= 3:
                                device_stable = True
                                break
                        
                        reconnect_delay *= 1.5  # Exponential backoff
                    
                    if not device_stable:
                        print(f"  Warning: Device may not be fully stable after reset #{reset_num}")
                
                time.sleep(0.2)  # Poll every 200ms
            except Exception as e:
                print(f"Error in monitor loop: {e}")
                break
    
    def on_reset_detected(self, reset_num):
        """Called when reset is detected"""
        timestamp = time.time()
        print(f"Reset #{reset_num} detected at {timestamp}")
        # Handle reset (e.g., log to file, send alert, etc.)
    
    def start_monitoring(self):
        """Start background monitoring"""
        if self.monitoring:
            return  # Already monitoring
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("Monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        with self.lock:
            count = self.reset_count
        print(f"Monitoring stopped. Total resets detected: {count}")


def main():
    """Example usage"""
    jlink = pylink.JLink()
    
    try:
        jlink.open()
        jlink.set_tif(pylink.JLinkInterfaces.SWD)
        jlink.connect("NRF54L15_M33")
        
        monitor = DeviceMonitor(jlink)
        monitor.start_monitoring()
        
        print("Production monitoring active. Press Ctrl+C to stop.")
        
        # Your main application code here
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            monitor.stop_monitoring()
            jlink.close()
        except:
            pass


if __name__ == "__main__":
    main()

