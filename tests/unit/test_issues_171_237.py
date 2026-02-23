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

"""Unit tests for Issues #171 and #237 fixes."""

import unittest
from unittest import mock

import pylink.errors
from pylink.errors import JLinkException


class TestIssue171(unittest.TestCase):
    """Tests for Issue #171: exec_command() informational messages."""

    def setUp(self):
        """Sets up the test case."""
        import pylink.jlink
        self.jlink = pylink.jlink.JLink()
        self.dll = mock.Mock()
        self.jlink._dll = self.dll

    def test_exec_command_informational_message_rtt_telnet_port(self):
        """Tests that RTT Telnet Port informational message doesn't raise exception.

        This is the specific case reported in Issue #171.
        """
        def mock_exec(cmd, err_buf, err_buf_len):
            msg = b'RTT Telnet Port set to 19021'
            for i, ch in enumerate(msg):
                if i < err_buf_len:
                    err_buf[i] = ch
            return 0

        self.dll.JLINKARM_ExecCommand = mock_exec
        # Should not raise exception
        result = self.jlink.exec_command('SetRTTTelnetPort 19021')
        self.assertEqual(0, result)

    def test_exec_command_informational_message_device_selected(self):
        """Tests that 'Device selected' informational message doesn't raise exception."""
        def mock_exec(cmd, err_buf, err_buf_len):
            msg = b'Device selected'
            for i, ch in enumerate(msg):
                if i < err_buf_len:
                    err_buf[i] = ch
            return 0

        self.dll.JLINKARM_ExecCommand = mock_exec
        # Should not raise exception
        result = self.jlink.exec_command('SelectDevice')
        self.assertEqual(0, result)

    def test_exec_command_informational_message_device_equals(self):
        """Tests that 'Device =' informational message doesn't raise exception."""
        def mock_exec(cmd, err_buf, err_buf_len):
            msg = b'Device = nRF54L15'
            for i, ch in enumerate(msg):
                if i < err_buf_len:
                    err_buf[i] = ch
            return 0

        self.dll.JLINKARM_ExecCommand = mock_exec
        # Should not raise exception
        result = self.jlink.exec_command('Device = nRF54L15')
        self.assertEqual(0, result)

    def test_exec_command_real_error_raises_exception(self):
        """Tests that real errors still raise exceptions."""
        def mock_exec(cmd, err_buf, err_buf_len):
            msg = b'Error: Invalid command'
            for i, ch in enumerate(msg):
                if i < err_buf_len:
                    err_buf[i] = ch
            return 0

        self.dll.JLINKARM_ExecCommand = mock_exec
        # Should raise exception
        with self.assertRaises(JLinkException):
            self.jlink.exec_command('InvalidCommand')

    def test_exec_command_empty_buffer_no_exception(self):
        """Tests that empty buffer doesn't raise exception."""
        def mock_exec(cmd, err_buf, err_buf_len):
            # Empty buffer
            return 0

        self.dll.JLINKARM_ExecCommand = mock_exec
        # Should not raise exception
        result = self.jlink.exec_command('ValidCommand')
        self.assertEqual(0, result)

    def test_exec_command_all_informational_patterns(self):
        """Tests all known informational message patterns."""
        patterns = [
            'RTT Telnet Port set to 19021',
            'Device selected: nRF54L15',
            'Device = nRF52840',
            'Speed = 4000',
            'Target interface set to SWD',
            'Target voltage = 3.3V',
            'Reset delay = 100ms',
            'Reset type = Normal',
        ]

        for pattern in patterns:
            with self.subTest(pattern=pattern):
                def mock_exec(cmd, err_buf, err_buf_len):
                    msg = pattern.encode()
                    for i, ch in enumerate(msg):
                        if i < err_buf_len:
                            err_buf[i] = ch
                    return 0

                self.dll.JLINKARM_ExecCommand = mock_exec
                # Should not raise exception
                result = self.jlink.exec_command('TestCommand')
                self.assertEqual(0, result)

    def test_exec_command_case_insensitive_matching(self):
        """Tests that pattern matching is case-insensitive."""
        def mock_exec(cmd, err_buf, err_buf_len):
            msg = b'DEVICE SELECTED'  # Uppercase
            for i, ch in enumerate(msg):
                if i < err_buf_len:
                    err_buf[i] = ch
            return 0

        self.dll.JLINKARM_ExecCommand = mock_exec
        # Should not raise exception (case-insensitive match)
        result = self.jlink.exec_command('SelectDevice')
        self.assertEqual(0, result)


class TestIssue237(unittest.TestCase):
    """Tests for Issue #237: flash_file() return value documentation.

    Note: These tests verify that the behavior is unchanged (backward compatible).
    The fix was documentation-only, so existing tests should continue to pass.
    """

    def setUp(self):
        """Sets up the test case."""
        import pylink.jlink
        self.jlink = pylink.jlink.JLink()
        self.dll = mock.Mock()
        self.jlink._dll = self.dll
        self.jlink.halt = mock.Mock()
        self.jlink.power_on = mock.Mock()
        # Mock the open() method to avoid connection requirements
        self.jlink._open_refcount = 1

    def test_flash_file_returns_status_code(self):
        """Tests that flash_file() returns status code (not bytes written)."""
        self.dll.JLINK_DownloadFile.return_value = 0
        result = self.jlink.flash_file('path', 0)
        # Should return status code (0 = success)
        self.assertEqual(0, result)

    def test_flash_file_status_code_not_bytes(self):
        """Tests that return value is status code, not number of bytes."""
        # Status code can be any value >= 0, not necessarily related to bytes
        self.dll.JLINK_DownloadFile.return_value = 42  # Arbitrary success code
        result = self.jlink.flash_file('path', 0)
        # Should return the status code, not bytes written
        self.assertEqual(42, result)

    def test_flash_file_error_raises_exception(self):
        """Tests that error status code (< 0) raises exception."""
        self.dll.JLINK_DownloadFile.return_value = -1
        with self.assertRaises(pylink.errors.JLinkFlashException):
            self.jlink.flash_file('path', 0)
