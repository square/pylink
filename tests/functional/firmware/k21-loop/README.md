# K21 Loop

This build build implements a simple polling loop.

## Bulding the Firmware

To build the firmware, run `make` from within the directory.  This will create
a build directory containing the binary files.

## Firmware Overview

This firmware does the following things on boot:

    1. Stops the watchdog timer.
    2. Enters a polling loop incrementing a value.
