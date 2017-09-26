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


@behave.when('I write {value} to ICE register {register}')
def step_write_to_ice_register(context, value, register):
    """Writes a value to a single ICE register.

    Args:
      context (Context): the ``Context`` instance
      value (str): the value to write to the register
      register (str): the register to write to

    Returns:
      ``None``
    """
    jlink = context.jlink
    register = int(register, 0)
    value = int(value, 0)
    jlink.ice_register_write(register, value)


@behave.when('I write {value} to register {register}')
def step_write_to_register(context, value, register):
    """Writes a value to a single register.

    Args:
      context (Context): the ``Context`` instance
      value (str): the value to write to the register
      register (str): the register to write to

    Returns:
      ``None``
    """
    jlink = context.jlink
    jlink.register_write(int(register), int(value))


@behave.when('I write to the registers')
def step_write_to_registers(context):
    """Writes multiple values to multiple registers.

    The values and registers are loaded from the context's table.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    registers, values = [], []
    for row in context.table:
        registers.append(int(row['register']))
        values.append(int(row['value']))
    jlink.register_write_multiple(registers, values)


@behave.then('ICE register {register} should have the value {value}')
def step_ice_register_has_value(context, register, value):
    """Checks that an ICE register has a particular value.

    Args:
      context (Context): the ``Context`` instance
      register (str): the ICE register to read from
      value (str): the value the ICE register should have

    Returns:
      ``None``
    """
    jlink = context.jlink
    register = int(register, 0)
    expected = int(value, 0)
    assert jlink.ice_register_read(register) == expected


@behave.then('register {register} should have the value {value}')
def step_register_has_value(context, register, value):
    """Reads a single value from a single register and asserts equality.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    actual = jlink.register_read(int(register))
    assert actual == int(value)


@behave.then('I should read from the registers')
def step_registers_have_values(context):
    """Reads multiple values from multiple registers and asserts equality.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    registers, expected_values = [], []
    for row in context.table:
        registers.append(int(row['register']))
        expected_values.append(int(row['value']))
    assert expected_values == jlink.register_read_multiple(registers)
