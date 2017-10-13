# Examples

This directory contains examples for different scripts and applications that
can be developed using `pylink`.

## Current Examples

### Core Information Printer

#### Source
[Core Information Printer](./core.py)

#### Description
The core information printer prints information about the target core.


### Serial Wire Viewer

#### Source
[Serial Wire Viewer](./swv.py)

#### Description
The serial wire viewer is a tool that uses the Instruction Trace Macrocell
(ITM) and Serial Wire Output (SWO) to provide an asynchronous method of
obtaining information from outside the MCU.  This can be used for tracing,
`printf` style debugging, watchpoints, and timestamping.


### Simple Trace

#### Source
[Simple Trace](./strace.py)

#### Description
Tool demonstrating the use of simple trace.


### Target Endianness

#### Source
[Target Endianess](./endian.py)

#### Description
Prints the endian mode of the target hardware.


### Windows Update

#### Source
[Windows Update](./windows_update.py)

#### Description
Tool for updating J-Links on a Windows platform.


### Real Time Transfer (RTT)

#### Source
[RTT](./rtt.py)

#### Description
Tool for a simple command-line terminal that communicates over RTT.
