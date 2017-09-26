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

import pylink

import os
import subprocess
import sys


def root_dir():
    """Retrives the root testing directory.

    Returns:
      The root testing directory.
    """
    dirname = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(dirname, os.pardir))


def firmware_path(firmware):
    """Returns the path to given firmware, provided it exists.

    Args:
      firmware (str): the firmware to search for

    Returns:
      The file path to the firmware if it exists, otherwise ``None``.
    """
    fw = os.path.join(root_dir(), 'firmware', firmware, 'build', 'firmware.bin')
    if not os.path.isfile(fw):
        return None

    if not sys.platform.startswith('cygwin'):
        return fw

    cygpath_exe = os.path.join(os.path.abspath(os.sep), 'bin', 'cygpath.exe')
    cygpath_cmd = [cygpath_exe, '-a', '-m', '-f', '-']
    cygpath_proc = subprocess.Popen(cygpath_cmd,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)
    cygpath_proc.stdin.write(fw + os.sep)
    return cygpath_proc.stdout.readline().rstrip()


def flash(jlink, firmware):
    """Flashes the given firmware to the target.

    Args:
      jlink (JLink): the connected ``JLink`` instance
      firmware (str): the path to the firmware to flash

    Returns:
      The number of bytes flashed.
    """
    return jlink.flash_file(firmware, 0)


def flash_k21(jlink, firmware):
    """Flashes the given firmware onto K21.

    Args:
      jlink (JLink): the connected ``JLink`` instance
      firmware (str): the path to the firmware to flash

    Returns:
      The number of bytes flashed.
    """
    jlink.power_on()
    jlink.set_reset_strategy(pylink.enums.JLinkResetStrategyCortexM3.RESETPIN)
    jlink.reset()

    if not pylink.unlock_kinetis(jlink):
        jlink.power_off()
        return -1

    res = jlink.flash_file(firmware, 0)
    jlink.reset()
    jlink.power_off()

    return res
