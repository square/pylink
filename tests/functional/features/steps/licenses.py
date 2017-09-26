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


@behave.given('has the license')
@behave.when('I add the license')
def step_add_license(context):
    """Adds a license to the J-Link.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    assert jlink.add_license(str(context.text))


@behave.when('I erase the licenses')
def step_erase_licenses(context):
    """Erases the J-Link's licenses.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    assert jlink.erase_licenses()


@behave.then('my J-Link should have the license')
def step_has_license(context):
    """Asserts the J-Link has the given licenese.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = context.jlink
    expected = context.text.strip()
    actual = jlink.custom_licenses.strip()
    assert actual.startswith(expected)
    assert jlink.erase_licenses()


@behave.then('my J-Link should have no licenses')
def step_no_licenses(context):
    """Asserts the J-Link has no licenses.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    assert len(context.jlink.custom_licenses) == 0
