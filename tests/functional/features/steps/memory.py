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

MEMORY_ADDR = 0x500


@behave.when('I write the {size}-bit integer {value} to memory')
def step_write_memory(context, size, value):
    """Writes a value to the memory of the device.

    Args:
      context (Context): the ``Context`` instance
      size (str): the number of bits to use for the value
      value (str): the value to write

    Returns:
      ``None``
    """
    jlink = context.jlink
    methods = {
        '8': jlink.memory_write8,
        '16': jlink.memory_write16,
        '32': jlink.memory_write32,
        '64': jlink.memory_write64
    }

    method = methods.get(size, None)
    assert method is not None

    data = [int(value)]
    num_bytes = method(MEMORY_ADDR, data)
    expected_num_bytes = int(size) / 8
    assert num_bytes == expected_num_bytes


@behave.then('I should read the {size}-bit integer {value} from memory')
def step_read_memory(context, size, value):
    """Reads a value from the memory of the device.

    Args:
      context (Context): the ``Context`` instance
      size (str): the number of bits to use for the value
      value (str): the value to read

    Returns:
      ``None``
    """
    jlink = context.jlink
    methods = {
        '8': jlink.memory_read8,
        '16': jlink.memory_read16,
        '32': jlink.memory_read32,
        '64': jlink.memory_read64
    }

    method = methods.get(size, None)
    assert method is not None

    expected = int(value)
    actual = method(MEMORY_ADDR, 1)[0]
    assert expected == actual


@behave.then('I should read the integer {value} from code memory')
def step_read_code_memory(context, value):
    """Reads and checks a value from code memory.

    Args:
      context (Context): the ``Context`` instance
      value (str): the value that should be read

    Returns:
      ``None``
    """
    actual = context.jlink.code_memory_read(MEMORY_ADDR, 1)[0]
    expected = int(value)
    assert actual == expected
