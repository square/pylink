# -*- coding: utf-8 -*-
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
# Example Serial Wire Debug Viewer.
#
# This module demonstrates implementing a Serial Wire Viewer using the PyLink
# library.
#
# Usage: swd.py jlink_serial_number device
# Author: Ford Peprah
# Date: Friday, September 23rd, 2016
# Copyright: 2016 Square, Inc.

import pylink

import StringIO
import string
import sys
import time


def serial_wire_viewer(jlink_serial, device):
    """Implements a Serial Wire Viewer (SWV).

    A Serial Wire Viewer (SWV) allows us implement real-time logging of output
    from a connected device over Serial Wire Output (SWO).

    Args:
      jlink_serial (str): the J-Link serial number
      device (str): the target CPU

    Returns:
      Always returns ``0``.

    Raises:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pylink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open(serial_no=jlink_serial)

    # Use Serial Wire Debug as the target interface.  Need this in order to use
    # Serial Wire Output.
    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect(device, verbose=True)
    jlink.coresight_configure()
    jlink.set_reset_strategy(pylink.enums.JLinkResetStrategyCortexM3.RESETPIN)

    # Have to halt the CPU before getitng its speed.
    jlink.reset()
    jlink.halt()

    # Output the information about the program.
    sys.stdout.write('Serial Wire Viewer\n')
    sys.stdout.write('Press Ctrl-C to Exit\n')
    sys.stdout.write('Reading data from port 0:\n\n')

    # Reset the core without halting so that it runs.
    jlink.reset(ms=10, halt=False)

    # Use the `try` loop to catch a keyboard interrupt in order to stop logging
    # serial wire output.
    try:
        while True:
            # Check the vector catch.
            if jlink.register_read(0x0) != 0x05:
                continue

            offset = jlink.register_read(0x1)
            handle, ptr, num_bytes = jlink.memory_read32(offset, 3)
            read = ''.join(map(chr, jlink.memory_read8(ptr, num_bytes)))

            if num_bytes == 0:
                # If no bytes exist, sleep for a bit before trying again.
                time.sleep(1)
                continue

            jlink.register_write(0x0, 0)
            jlink.step(thumb=True)
            jlink.restart(2, skip_breakpoints=True)

            sys.stdout.write(read)
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass

    sys.stdout.write('\n')

    return 0


if __name__ == '__main__':
    exit(serial_wire_viewer(sys.argv[1], sys.argv[2]))
