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

import behave

import time


@behave.when('my {device} device is locked')
def step_device_locked(context, device):
    """Locks the specified device.

    Note:
      Currently only supports Kinetis.

    Args:
      context (Context): the ``Context`` instance
      device (str): the type of device to lock

    Returns:
      ``None``
    """
    assert device.lower() == 'kinetis'

    context.device = device

    # Security bytes.  These bytes control the device security.  We want to
    # secure the device, but still allow it to be mass-erased (otherwise the
    # device will be permanently locked.
    fcf_offset = 0x400
    fcf_bytes = [
        0xFF,  # Backdoor comparison key (unused, 8 bytes long)
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,  # Flash protection settings (4 bytes long)
        0xFF,
        0xFF,
        0xFF,
        0x03,  # FSEC register - mass erase enabled, flash security enabled
        0x07,  # FOPT register - NMI enabled, EzPort enabled, normal boot
        0xFF,  # Data flash protection settings (unused)
        0xFF,  # EEPROM settings (unused)
    ]
    assert context.jlink.flash_write(fcf_offset, fcf_bytes) >= 0

    # Reset the device for the changes to take.
    context.jlink.reset()
    context.jlink.halt()

    try:
        # This write should fail as the device is flash protected now.
        context.jlink.flash_write(fcf_offset, fcf_bytes)
    except Exception as e:
        pass
    else:
        assert False

    time.sleep(1)


@behave.when('I unlock it')
def step_unlock_device(context):
    """Unlocks the connected device.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    device = context.device

    assert jlink.halt()

    jlink.set_reset_strategy(pylink.JLinkResetStrategyCortexM3.RESETPIN)
    jlink.reset()
    jlink.set_reset_strategy(pylink.JLinkResetStrategyCortexM3.NORMAL)

    assert jlink.target_connected()
    assert jlink.unlock()


@behave.then('I should be able to write to flash')
def step_check_write_to_flash(context):
    """Checks that the target can be written to over flash.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    assert jlink.target_connected()
    assert context.jlink.flash_write(0x40C, [0x2]) >= 0
