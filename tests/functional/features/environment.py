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

try:
    import StringIO
except ImportError:
    import io as StringIO
import sys
import time


def create_jlink(context):
    """Creates an instance of a J-Link, attaching it to the context.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``JLink``
    """
    context.log = StringIO.StringIO()
    context.jlink = pylink.JLink(log=context.log.write,
                                 detailed_log=context.log.write)

    emulators = context.jlink.connected_emulators()
    if len(emulators) > 0:
        serial_no = emulators[0].SerialNumber
        context.jlink.disable_dialog_boxes()
        context.jlink.open(serial_no=serial_no)

    return context.jlink


def reset_jlink(context):
    """Resets the context's J-Link instance by destroying it.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    context.jlink.close()
    return create_jlink(context)


def extract_tag(tags, prefix):
    """Extracts a tag and its value.

    Consumes a tag prefix, and extracts the value corresponding to it.

    Args:
      tags (list): the list of tags to check
      prefix (str): the tag prefix

    Returns:
      A tuple of tag and tag value.
    """
    for tag in tags:
        if tag.startswith(prefix):
            suffix = tag[len(prefix):]
            if len(suffix) <= 1 or not suffix[0] == '=':
                raise ValueError('Invalid tag: \'%s\'' % tag)
            return prefix, suffix[1:]
    return None, None


def should_exclude(context, section):
    """Returns whether the given section should be skipped.

    Args:
      context (Context): the ``Context`` instance
      section: the section to skip

    Returns:
      ``True`` if section should be skipped, otherwise ``False``.
    """
    if len(section.tags) == 0:
        return False

    if 'connection' in section.tags:
        if not context.jlink.connected():
            return True
    elif 'nix' in section.tags:
        return sys.platform.startswith('win')

    return False


def before_all(context):
    """Runs before all tests.

    Syncs the J-Link firmware before running tests.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    jlink = create_jlink(context)
    jlink.sync_firmware()

    print('using J-Link Firmware: %s' % jlink.firmware_version)
    print('using J-Link DLL: %s' % jlink.version)
    print('')


def after_all(context):
    """Runs after all tests.

    Args:
      context (Context): the ``Context`` instance

    Returns:
      ``None``
    """
    pass


def before_feature(context, feature):
    """Runs before each feature.

    Args:
      context (Context): the ``Context`` instance
      feature (Feature): the feature that is next to run

    Returns:
      ``None``
    """
    reset_jlink(context)

    if should_exclude(context, feature):
        feature.skip(reason='Windows platform or no J-Link connection in Feature')


def after_feature(context, feature):
    """Runs after each feature.

    Args:
      context (Context): the ``Context`` instance
      feature (Feature): the feature that has just ran

    Returns:
      ``None``
    """
    pass


def before_scenario(context, scenario):
    """Runs before each scenario.

    Args:
      context (Context): the ``Context`` instance
      scenario (Scenario): the scenario that is next to run

    Returns:
      ``None``
    """
    reset_jlink(context)

    if should_exclude(context, scenario):
        scenario.skip(reason='Windows platform or no J-Link connection in Scenario')

    context.scenario = scenario


def after_scenario(context, scenario):
    """Runs after each scenario.

    Args:
      context (Context): the ``Context`` instance
      scenario (Scenario): the scenario that has just ran

    Returns:
      ``None``
    """
    if getattr(scenario, 'skip_reason', None) is not None:
        sys.stdout.write('    Skipped Scenario.  Reason: %s\n' % scenario.skip_reason)

    jlink = context.jlink
    if jlink.connected():
        if jlink.swo_enabled():
            jlink.swo_stop()

        if len(jlink.custom_licenses) > 0:
            jlink.erase_licenses()

    jlink.close()


def before_tag(context, tag):
    """Runs before each section with the given tag.

    Args:
      context (Context): the ``Context`` instance
      tag (Tag): the section's tag

    Returns:
      ``None``
    """
    pass


def after_tag(context, tag):
    """Runs after each section with the given tag.

    Args:
      context (Context): the ``Context`` instance
      tag (Tag): the section's tag

    Returns:
      ``None``
    """
    pass


def before_step(context, step):
    """Runs before each step.

    Args:
      context (Context): the ``Context`` instance
      step (Step): the step that is next to run

    Returns:
      ``None``
    """
    context.step = step


def after_step(context, step):
    """Runs after each step.

    Args:
      context (Context): the ``Context`` instance
      step (Step): the step that has just ran

    Returns:
      ``None``
    """
    pass
