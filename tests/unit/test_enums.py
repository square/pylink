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

import pylink.enums as enums

import unittest


class TestEnums(unittest.TestCase):
    """Unit test for the `enums` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestEnums): the ``TestEnums`` instance

        Returns:
          ``None``
        """
        pass

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestEnums): the ``TestEnums`` instance

        Returns:
          ``None``
        """
        pass

    def test_jlink_global_errors(self):
        """Tests the global errors.

        The J-Link DLL defines a set of global error codes, which start at -256
        and run until -274.

        Values from -1 to -255 are reserved for function specific error codes.

        This test checks that an error message is defined for those from -256
        to -274, and not for -1 to -255.

        Args:
          self (TestEnums): the ``TestEnums`` instance

        Returns:
          ``None``
        """
        for i in range(-255, -1):
            with self.assertRaises(ValueError):
                enums.JLinkGlobalErrors.to_string(i)

        for i in range(-274, -255):
            error_message = enums.JLinkGlobalErrors.to_string(i)
            self.assertTrue(isinstance(error_message, str))

    def test_jlink_global_errors_unspecified(self):
        """Tests the unspecified error case.

        Args:
          self (TestEnums): the ``TestEnums`` instance

        Returns:
          ``None``
        """
        error_message = enums.JLinkGlobalErrors.to_string(-1)
        self.assertEqual('Unspecified error.', error_message)

    def test_jlink_write_errors(self):
        """Tests write specific errors.

        Args:
          self (TestEnums): the ``TestEnums`` instance

        Returns:
          ``None``
        """
        error_message = enums.JLinkWriteErrors.to_string(-5)
        self.assertTrue(isinstance(error_message, str))

        error_message = enums.JLinkWriteErrors.to_string(-1)
        self.assertEqual('Unspecified error.', error_message)

    def test_jlink_read_errors(self):
        """Tests read specific errors.

        Args:
          self (TestEnums): the ``TestEnums`` instance

        Returns:
          ``None``
        """
        error_message = enums.JLinkReadErrors.to_string(-5)
        self.assertTrue(isinstance(error_message, str))

        error_message = enums.JLinkReadErrors.to_string(-1)
        self.assertEqual('Unspecified error.', error_message)

    def test_jlink_data_event_errors(self):
        """Tests the data event errors.

        Args:
          self (TestEnums): the ``TestEnums`` instance

        Returns:
          ``None``
        """
        error_codes = [
            0x80000000, 0x80000001, 0x80000002, 0x80000004, 0x80000020,
            0x80000040, 0x80000080
        ]

        for error_code in error_codes:
            error_message = enums.JLinkDataErrors.to_string(error_code)
            self.assertTrue(isinstance(error_message, str))

        error_message = enums.JLinkDataErrors.to_string(-1)
        self.assertEqual('Unspecified error.', error_message)

    def test_jlink_flash_errors(self):
        """Tests flash specific errors.

        Args:
          self (TestEnums): the ``TestEnums`` instance

        Returns:
          ``None``
        """
        for i in range(-4, -1):
            error_message = enums.JLinkFlashErrors.to_string(i)
            self.assertTrue(isinstance(error_message, str))

        error_message = enums.JLinkFlashErrors.to_string(-1)
        self.assertEqual('Unspecified error.', error_message)

    def test_jlink_erase_errors(self):
        """Tests erase specific errors.

        Args:
          self (TestEnums): the ``TestEnums`` instance

        Returns:
          ``None``
        """
        for i in range(-5, -4):
            error_message = enums.JLinkEraseErrors.to_string(i)
            self.assertTrue(isinstance(error_message, str))

        error_message = enums.JLinkEraseErrors.to_string(-1)
        self.assertEqual('Unspecified error.', error_message)


if __name__ == '__main__':
    unittest.main()
