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

import string
import time


@behave.when('I enable SWO')
def step_enable_swo(context):
    """Enables Serial Wire Output.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    return step_enable_swo_on_port(context, 0)


@behave.when('I enable SWO on port {port}')
def step_enable_swo_on_port(context, port):
    """Enables Serial Wire Output.

    Args:
      context (Context): the ``Context`` instance
      port (int): the port SWO is enabled on

    Returns:
      ``None``
    """
    jlink = context.jlink

    # Have to halt the CPU before getting its speed.
    jlink.reset()
    jlink.halt()
    assert jlink.halted()

    cpu_speed = jlink.cpu_speed()
    swo_speed = jlink.swo_supported_speeds(cpu_speed, 3)[0]

    # Enable SWO and flush.  This must come before the reset to ensure that no
    # data is present in the SWO buffer when the core restarts.
    jlink.swo_start(swo_speed)
    jlink.swo_flush()

    assert jlink.swo_enabled()

    # Reset the core without halting so that it runs.
    jlink.reset(ms=10, halt=False)
    time.sleep(1)


@behave.then('I should see "{message}"')
def step_should_see(context, message):
    """Asserts that the given message was read.

    Args:
      context (Context): the ``Context`` instance
      message (str): the message at the head of the SWO buffer

    Returns:
      ``None``
    """
    data = context.jlink.swo_read_stimulus(0, 0x800)
    actual = ''.join(map(chr, data))

    print('Actual = %s' % actual)
    print('Expected = %s' % message)
    assert len(actual) == len(message)
    assert actual == message
