# K21 Serial Wire Debug

This firmware build demonstrates semihosting and serial wire debug.  If the
firmware is successful, we should see a single line printed over serial wire
debug.  This firmware is known to work on the `K21F120M` and `K21D50M`
evaluation boards.

## Bulding the Firmware

To build the firmware, run `make` from within the directory.  This will create
a build directory containing the binary files.

## Firmware Overview

This firmware does the following things on boot:

    1. Stops the watchdog timer.
    2. Calls `printf()` to write a message.
    3. Sits in a while-loop forever.

This behaviour has the effect of triggering a `BKPT` instruction in order to
send a `SYS_WRITE` command for the debugger to grab the contents of the write.
