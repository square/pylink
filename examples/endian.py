# -*- coding: utf-8 *-*
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
# Example Endianness.
#
# This module demonstrates getting the endianess of the target.
#
# Usage: endian.py jlink_serial_number device
# Author: Ford Peprah
# Date: October 11th, 2016
# Copyright: 2016 Square, Inc.

import pylink

import StringIO
import sys


def main(jlink_serial, device):
    """Main function.

    Args:
      jlink_serial (str): the J-Link serial number
      device (str): the target CPU

    Returns:
      ``None``

    Raises:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pylink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open(serial_no=jlink_serial)

    jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
    jlink.connect(device, verbose=True)

    # Figure out our original endianess first.
    big_endian = jlink.set_little_endian()
    if big_endian:
        jlink.set_big_endian()

    print('Target Endian Mode: %s Endian' % ('Big' if big_endian else 'Little'))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
