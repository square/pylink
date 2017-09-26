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

import behave

import time


@behave.when('I enable semihosting')
def step_enable_semihosting(context):
    """Enables semihosting by setting a SVC break instruction.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    jlink.set_vector_catch(1 << 2)


@behave.then('I should see over SWD')
def step_should_see_swd(context):
    """Asserts that the text over the SWD interface matches the given text.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    expected_strings = context.text.split('\n')

    # r0 holds the type of command that resulted in the SVC exception.  For a
    # full list of what these commands can be, please see the J-Link
    # documentation on semihosting ``UM8001_JLink.pdf``
    command_register = 0x0

    # r1 holds a pointer to an address on the target that holds the additional
    # function arguments as 32-bit aligned words.
    command_info_register = 0x1

    while len(expected_strings) > 0:
        if not jlink.halted():
            time.sleep(1)
            continue

        # The CPU is halted after a Vector Catch, so we can now examine why
        # the CPU halted.
        sys_write = 0x05
        command = jlink.register_read(command_register)
        assert command == sys_write

        command_info = jlink.register_read(command_info_register)
        handle, ptr, num_bytes = jlink.memory_read32(command_info, 3)
        actual_string = ''.join(map(chr, jlink.memory_read8(ptr, num_bytes))).strip()
        print(actual_string)

        actual_stripped = ''.join(actual_string.strip().split())
        expected_stripped = ''.join(expected_strings.pop(0).strip().split())
        assert actual_stripped.startswith(expected_stripped)

        # Resume execution to the original mode.  Have to write the result of
        # the SVC call (always 0), and step over the breakpointed instruction.
        jlink.register_write(0x0, 0)
        jlink.step(thumb=True)
        assert jlink.restart(num_instructions=2, skip_breakpoints=True)
