# Copyright 2017 Square, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Example simple trace.
#
# Usage: strace.py device trace_address breakpoint_address
# Author: Ford Peprah
# Date: March 23rd, 2017
# Copyright: 2017 Square, Inc.

import pylink

import sys
import time


def strace(device, trace_address, breakpoint_address):
    """Implements simple trace using the STrace API.

    Args:
      device (str): the device to connect to
      trace_address (int): address to begin tracing from
      breakpoint_address (int): address to breakpoint at

    Returns:
      ``None``
    """
    jlink = pylink.JLink()
    jlink.open()

    # Do the initial connection sequence.
    jlink.power_on()
    jlink.set_tif(pylink.JLinkInterfaces.SWD)
    jlink.connect(device)
    jlink.reset()

    # Clear any breakpoints that may exist as of now.
    jlink.breakpoint_clear_all()

    # Start the simple trace.
    op = pylink.JLinkStraceOperation.TRACE_START
    jlink.strace_clear_all()
    jlink.strace_start()

    # Set the breakpoint and trace events, then restart the CPU so that it
    # will execute.
    bphandle = jlink.breakpoint_set(breakpoint_address, thumb=True)
    trhandle = jlink.strace_code_fetch_event(op, address=trace_address)
    jlink.restart()
    time.sleep(1)

    # Run until the CPU halts due to the breakpoint being hit.
    while True:
        if jlink.halted():
            break

    # Print out all instructions that were captured by the trace.
    while True:
        instructions = jlink.strace_read(1)
        if len(instructions) == 0:
            break
        instruction = instructions[0]
        print(jlink.disassemble_instruction(instruction))

    jlink.power_off()
    jlink.close()


if __name__ == '__main__':
    exit(strace(sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16)))
