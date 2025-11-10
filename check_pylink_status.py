#!/usr/bin/env python3
"""
Pylink System Status Checker
"""
import sys
import os

print("=" * 70)
print("PYLINK SYSTEM STATUS")
print("=" * 70)

# Check pip installation
print("\n[1] Pip Installation Status:")
try:
    import subprocess
    result = subprocess.run(['pip3', 'show', 'pylink-square'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✓ pylink-square is installed via pip")
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                print(f"    {line}")
            elif line.startswith('Location:'):
                print(f"    {line}")
    else:
        print("  ✗ pylink-square not found in pip")
except Exception as e:
    print(f"  ⚠ Could not check pip: {e}")

# Check Python import
print("\n[2] Python Import Status:")
try:
    import pylink
    print("  ✓ pylink imported successfully")
    
    pylink_path = pylink.__file__
    print(f"  Location: {pylink_path}")
    
    # Determine installation type
    if 'site-packages' in pylink_path:
        print("  Type: Normal installation (site-packages)")
    elif 'sandbox' in pylink_path:
        print("  Type: Development/Editable installation (sandbox)")
    else:
        print("  Type: Unknown location")
    
    version = getattr(pylink, '__version__', 'unknown')
    print(f"  Version: {version}")
    
except ImportError as e:
    print(f"  ✗ Failed to import pylink: {e}")
    sys.exit(1)

# Check modifications
print("\n[3] Code Modifications Check:")
try:
    import inspect
    src = inspect.getsource(pylink.jlink.JLink.rtt_start)
    
    modifications = {
        'search_ranges parameter': 'search_ranges=None' in src,
        'reset_before_start parameter': 'reset_before_start=False' in src,
        'SetRTTSearchRanges command': 'SetRTTSearchRanges' in src,
        'Auto-generate search ranges from RAM': 'ram_start = self._device.RAMAddr' in src,
        'Polling mechanism (10s timeout)': 'max_wait = 10.0' in src,
        'Device state check (IsHalted)': 'JLINKARM_IsHalted' in src,
        'Device resume (Go)': 'JLINKARM_Go' in src,
    }
    
    all_present = True
    for feature, present in modifications.items():
        status = '✓' if present else '✗'
        print(f"  {status} {feature}")
        if not present:
            all_present = False
    
    if all_present:
        print("\n  ✓ All modifications are present!")
        print("  ✓ Using modified version with RTT improvements")
    else:
        print("\n  ✗ Some modifications are missing!")
        print("  ⚠ May be using original/unmodified version")
        
except Exception as e:
    print(f"  ✗ Error checking modifications: {e}")
    import traceback
    traceback.print_exc()

# Check if it's the modified version from sandbox
print("\n[4] Version Source:")
try:
    expected_sandbox_path = "/Users/fx/Documents/gitstuff/Seeed-Xiao-nRF54L15/dmic-ble-gatt/sandbox/pylink"
    if expected_sandbox_path in pylink_path:
        print("  ✓ Using modified version from sandbox/pylink")
    elif 'site-packages' in pylink_path:
        print("  ⚠ Using installed version from site-packages")
        print("  → This should be the modified version if installed correctly")
    else:
        print(f"  ⚠ Using version from: {os.path.dirname(pylink_path)}")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 70)
print("Status check complete")
print("=" * 70)

