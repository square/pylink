#!/usr/bin/env python3
"""
Verification script to check pylink installation
"""
import sys
import os

print("=" * 70)
print("Pylink Installation Verification")
print("=" * 70)

try:
    import pylink
    print("\n✓ pylink imported successfully")
    
    # Check location
    pylink_path = pylink.__file__
    print(f"\nLocation: {pylink_path}")
    
    # Check if it's the modified version
    expected_path = "/Users/fx/Documents/gitstuff/Seeed-Xiao-nRF54L15/dmic-ble-gatt/sandbox/pylink"
    if expected_path in pylink_path:
        print("✓ Using modified version from sandbox/pylink")
    else:
        print(f"⚠ Using version from: {os.path.dirname(pylink_path)}")
    
    # Verify modified rtt_start function
    import inspect
    try:
        src = inspect.getsource(pylink.jlink.JLink.rtt_start)
        
        checks = {
            'search_ranges parameter': 'search_ranges=None' in src,
            'reset_before_start parameter': 'reset_before_start=False' in src,
            'SetRTTSearchRanges command': 'SetRTTSearchRanges' in src,
            'Auto-generate search ranges': 'Auto-generate search ranges' in src or 'ram_start = self._device.RAMAddr' in src,
            'Polling mechanism': 'max_wait = 10.0' in src and 'num_buffers = self.rtt_get_num_up_buffers()' in src,
        }
        
        print("\nModified features check:")
        all_ok = True
        for feature, present in checks.items():
            status = "✓" if present else "✗"
            print(f"  {status} {feature}")
            if not present:
                all_ok = False
        
        if all_ok:
            print("\n✓ All modifications are present!")
        else:
            print("\n✗ Some modifications are missing!")
            
    except Exception as e:
        print(f"\n✗ Error checking source: {e}")
        import traceback
        traceback.print_exc()
    
    # Check version
    version = getattr(pylink, '__version__', 'unknown')
    print(f"\nVersion: {version}")
    
    print("\n" + "=" * 70)
    print("Verification complete")
    
except ImportError as e:
    print(f"\n✗ Failed to import pylink: {e}")
    print("\nPlease install with: pip3 install -e /path/to/sandbox/pylink")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

