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

import pylink.errors as errors

import unittest


class TestErrors(unittest.TestCase):
    """Unit test for the `errors` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestErrors): the `TestErrors` instance

        Returns:
          `None`
        """
        pass

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestErrors): the `TestErrors` instance

        Returns:
          `None`
        """
        pass

    def test_jlink_exception_with_message(self):
        """Tests that a `JLinkException` can be created with a message.

        Args:
          self (TestErrors): the `TestErrors` instance

        Returns:
          `None`
        """
        message = 'message'
        exception = errors.JLinkException(message)
        self.assertTrue(isinstance(exception.message, str))
        self.assertEqual(message, exception.message)
        self.assertEqual(None, getattr(exception, 'code', None))

    def test_jlink_exception_with_code(self):
        """Tests that a `JLinkException` can be created with a numeric code.

        Args:
          self (TestErrors): the `TestErrors` instance

        Returns:
          `None`
        """
        code = -1
        exception = errors.JLinkException(code)
        self.assertTrue(isinstance(exception.message, str))
        self.assertEqual('Unspecified error.', exception.message)
        self.assertEqual(code, getattr(exception, 'code', None))


if __name__ == '__main__':
    unittest.main()
