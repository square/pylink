# RTT Connection Test Script

## Usage

```bash
cd sandbox/pylink
python3 test_rtt_connection.py
```

Or make it executable and run directly:

```bash
chmod +x test_rtt_connection.py
./test_rtt_connection.py
```

## What it does

1. **Opens J-Link connection** - Connects to your J-Link probe
2. **Connects to device** - Connects to nRF54L15_M33 device
3. **Starts RTT** - Uses the improved `rtt_start()` with auto-detection
4. **Gets buffer info** - Shows number of RTT buffers found
5. **Monitors output** - Displays RTT logs in real-time on console

## Features

- Real-time RTT log display
- Graceful shutdown with Ctrl+C
- Error handling and cleanup
- Shows connection status and statistics
- Automatically uses improved RTT auto-detection

## Stopping

Press `Ctrl+C` to stop monitoring. The script will clean up RTT and close connections gracefully.

## Example Output

```
======================================================================
RTT Connection Test - nRF54L15
======================================================================

[1/5] Opening J-Link connection...
  ✓ J-Link opened successfully

[2/5] Connecting to device...
  ✓ Connected to device: NRF54L15_M33
    RAM Start: 0x20000000
    RAM Size:  0x00040000

[3/5] Starting RTT...
  ✓ RTT started successfully

[4/5] Getting RTT buffer information...
  ✓ Found 3 up buffers, 3 down buffers

[5/5] Monitoring RTT output...
  Press Ctrl+C to stop

----------------------------------------------------------------------
[Your RTT logs will appear here in real-time]
----------------------------------------------------------------------
```

