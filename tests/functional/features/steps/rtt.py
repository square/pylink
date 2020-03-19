# Copyright 2019 Square, Inc.
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
import pylink

import time


@behave.when('I enable RTT with config block {block_address}')
def step_enable_rtt(context, block_address):
    """Enables RTT.

    Args:
      context (Context): the ``Context`` instance
      block_address (str): the RTT config block address

    Returns:
      ``None``
    """
    jlink = context.jlink
    jlink.rtt_start(int(block_address, 16))
    while True:
        try:
            jlink.rtt_get_num_up_buffers()
            jlink.rtt_get_num_down_buffers()
            break
        except pylink.errors.JLinkRTTException as e:
            time.sleep(0.1)

    assert jlink.rtt_get_num_up_buffers() > 0
    assert jlink.rtt_get_num_down_buffers() > 0


@behave.when('I write "{message}" to RTT channel {channel}')
def step_write_rtt_channel(context, message, channel):
    """Writes a message to an RTT channel.

    Args:
      context (Context): the ``Context`` instance
      message (str): the message to write
      channel (str): the RTT channel to write to

    Returns:
      ``None``
    """
    bytes_to_write = list(bytearray(message, 'utf-8') + b'\x0A\x00')
    jlink = context.jlink
    bytes_written = jlink.rtt_write(int(channel), bytes_to_write)
    assert len(bytes_to_write) == bytes_written


@behave.then('I should read "{message}" on RTT channel {channel}')
def step_read_rtt_channel(context, message, channel):
    """Checks that the expected message is read over the RTT channel.

    Args:
      context (Context): the ``Context`` instance
      message (str): the expected message
      channel (str): the RTT channel to read from

    Returns:
      ``None``
    """
    jlink = context.jlink
    expected = str(message)

    bytes_read = []
    while len(bytes_read) < len(message):
        bytes_read += jlink.rtt_read(int(channel), 1024)
        time.sleep(0.1)

    actual = ''.join(map(chr, bytes_read)).strip()
    assert expected == actual
