# K21 ETM

This firmware build demonstrates using Embedded Trace Macrocell on K21.
This firmware is known to work on the `K21F120M` evaluation board.

## Building the Firmware

To build the firmware, run `make` from within the directory.  This will create
a build directory containing the binary files.

## Using ETM

To inspect the instruction trace, load the .elf file into SEGGER Ozone. The
instruction trace will be populated at each breakpoint, after the ETM module is
initialized in firmware.
Reference: https://www.segger.com/ozone-trace-tutorial.html
