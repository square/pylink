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


@behave.given('I enable soft breakpoints')
def step_enable_soft_breakpoints(context):
    """Enables software breakpoints.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    context.jlink.enable_soft_breakpoints()


@behave.when('I set a breakpoint at address {addr}')
def step_set_breakpoint(context, addr):
    """Sets a breakpoint at the given address.

    Args:
      context (Context): the ``Context`` instance
      addr (str): the address to set the breakpoint at

    Returns:
      ``None``

    Raises:
      TypeError: if the given address cannot be converted to an int.
    """
    addr = int(addr, 0)
    context.handle = context.jlink.breakpoint_set(addr, thumb=True)

    assert context.jlink.breakpoint_find(addr) == context.handle

    bp = context.jlink.breakpoint_info(context.handle)
    assert bp.Addr == addr


@behave.then('I should have {num} breakpoint')
@behave.then('I should have {num} breakpoints')
def step_num_breakpoints(context, num):
    """Asserts that there are the specified number of breakpoints.

    Args:
      context (Context): the ``Context`` instance
      num (str): number of breakpoints that should exist

    Returns:
      ``None``

    Raises:
      TypeError: if the given number cannot be converted to an int.
    """
    assert int(num) == context.jlink.num_active_breakpoints()


@behave.then('I should be breakpointed at address {addr}')
def step_should_be_breakpointed(context, addr):
    """Asserts that we are breakpointed at the given address.

    Args:
      context (Context): the ``Context`` instance
      addr (str): the address we should be breakpointed at

    Returns:
      ``None``

    Raises:
      TypeError: if the given address cannot be converted to an int.
    """
    jlink = context.jlink
    assert jlink.halted()

    cpu_halt_reasons = jlink.cpu_halt_reasons()
    assert len(cpu_halt_reasons) == 1

    halt_reason = cpu_halt_reasons[0]
    assert halt_reason.code_breakpoint()

    pc = jlink.register_read(15)
    assert pc == int(addr, 0)


@behave.then('I can clear the breakpoints')
def step_clear_breakpoints(context):
    """Asserts clearing the breakpoints.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    assert context.jlink.breakpoint_clear_all()


@behave.when('I set a watchpoint at address {addr} for data {data}')
def step_set_watchpoint(context, addr, data):
    """Sets a watchpoint at the given address for the given data value.

    Args:
      context (Context): the ``Context`` instance
      addr (str): the address the watchpoint should be set at
      data (str): the data value to trigger the watchpoint on

    Returns:
      ``None``

    Raises:
      TypeError: if the given address or data cannot be converted to an int.
    """
    addr = int(addr, 0)
    data = int(data, 0)
    context.handle = context.jlink.watchpoint_set(addr, data=data)

    wp = context.jlink.watchpoint_info(context.handle)
    assert wp.Addr == addr
    assert wp.Handle == context.handle
    assert wp.Data == data


@behave.then('I should have {num} watchpoint')
@behave.then('I should have {num} watchpoints')
def step_num_watchpoints(context, num):
    """Asserts that there are the specified number of watchpoints.

    Args:
      context (Context): the ``Context`` instance
      num (str): number of watchpoints that should exist

    Returns:
      ``None``

    Raises:
      TypeError: if the given number cannot be converted to an int.
    """
    assert int(num) == context.jlink.num_active_watchpoints()


@behave.then('I should hit the watchpoint at address {addr}')
def step_should_hit_watchpoint(context, addr):
    """Checks that the watchpoint is hit at the given address.

    Args:
      context (Context): the ``Context`` instance
      addr (str): the address the watchpoint is expected to trigger on

    Returns:
      ``None``

    Raises:
      TypeError: if the given address cannot be converted to an int.
    """
    jlink = context.jlink

    while not jlink.halted():
        time.sleep(1)

    cpu_halt_reasons = jlink.cpu_halt_reasons()
    assert len(cpu_halt_reasons) == 1

    halt_reason = cpu_halt_reasons[0]
    assert halt_reason.data_breakpoint()

    index = halt_reason.Index
    wp = jlink.watchpoint_info(index=index)
    addr = int(addr, 0)
    assert addr == wp.Addr


@behave.then('I can clear the watchpoints')
def step_clear_watchpoints(context):
    """Asserts clearing the watchpoints.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    assert context.jlink.watchpoint_clear_all()
