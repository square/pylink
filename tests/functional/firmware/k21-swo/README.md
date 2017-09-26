# K21 SWO

This firmware build demonstrates using Serial Wire Output (SWO) using the
Instruction Trace Macrocell (ITM) ports on K21.  This firmware is known to
work on the `K21F120M` and `K21D50M` evaluation boards.

## Building the Firmware

To build the firmware, run `make` from within the directory.  This will create
a build directory containing the binary files.

## Firmware Overview

This firmware does the following things on boot:

    1. Stops the watchdog timer.
    2. Configures the ITM ports for SWO output.
    3. Outputs a single string via SWO.
    4. Halts.
