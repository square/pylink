# K21 RTT

This firmware build demonstrates using Real-Time Transfer (RTT) to send and
receive data on a K21.  This firmware is known to work on the `K21F120M`
evaluation board.

## Building the Firmware

To build the firmware, run `make` from within the directory.  This will create
a build directory containing the binary files.

## Firmware Overview

This firmware does the following things on boot:

     1. Initializes the RTT control block.
     2. Sets names for each of the 3 up and down buffers.
     3. Reads a single character from RTT channel 0.
     4. Writes the read character from step three to RTT channel 0.
     5. Repeats again from step 3.
