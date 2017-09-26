# K21 Stack Canary

This firmware build demonstrates implementing a stack canary.  If the build is
successfull, the canary will cause a hard fault, otherwise the firmware will
sit in a while loop forever.  This firmware is known to work on the `K21F120M`
and `K21D50M` evaluation boards.

## Bulding the Firmware

To build the firmware, run `make` from within the directory.  This will create
a build directory containing the binary files.

## Firmware Overview

This firmware does the following things on boot:

    1. Stops the watchdog timer.
    2. Calls a function that overflows its stack.
    3. Sits in a while-loop forever if the canary was not triggered.

Provided the stack canary was hit, it should trigger a `BKPT` instruction,
which will halt the CPU.
