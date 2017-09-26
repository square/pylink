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
# Automatic updating of J-Link software on Windows.
#
# This script demonstrates automatically updating the J-Link firmware to match
# the firmware provided by the J-Link DLL on windows platform.  This is
# particularly useful for automated testing infrastructure where the desire is
# to automatically role out upgrades of the J-Link software.  This would be run
# after the latest version of the DLL is installed.
#
# Usage: windows_update.py
# Author: Ford Peprah
# Date: December 8th, 2016
# Copyright: 2016 Square, Inc.

import pylink

import os


def main():
    """Upgrades the firmware of the J-Links connected to a Windows device.

    Returns:
      None.

    Raises:
      OSError: if there are no J-Link software packages.
    """
    windows_libraries = list(pylink.Library.find_library_windows())
    latest_library = None
    for lib in windows_libraries:
        if os.path.dirname(lib).endswith('JLinkARM'):
            # Always use the one pointed to by the 'JLinkARM' directory.
            latest_library = lib
            break
        elif latest_library is None:
            latest_library = lib
        elif os.path.dirname(lib) > os.path.dirname(latest_library):
            latest_library = lib

    if latest_library is None:
        raise OSError('No J-Link library found.')

    library = pylink.Library(latest_library)
    jlink = pylink.JLink(lib=library)

    print('Found version: %s' % jlink.version)

    for emu in jlink.connected_emulators():
        jlink.disable_dialog_boxes()
        jlink.open(serial_no=emu.SerialNumber)
        jlink.sync_firmware()
        print('Updated emulator with serial number %s' % emu.SerialNumber)

    return None


if __name__ == '__main__':
    exit(main())
