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
import pylink.util as util

import mock

try:
    import StringIO
except ImportError:
    import io as StringIO
import unittest


class TestUtil(unittest.TestCase):
    """Unit test for the `util` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestUtil): the `TestUtil` instance

        Returns:
          `None`
        """
        pass

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestUtil): the `TestUtil` instance

        Returns:
          `None`
        """
        pass

    def test_is_integer(self):
        """Tests that the `is_integer()` method returns correctly.

        Args:
          self (TestUtil): the `TestUtil` instance

        Returns:
          `None`
        """
        self.assertTrue(util.is_integer(4))
        self.assertTrue(util.is_integer(0))
        self.assertTrue(util.is_integer(-1))

        self.assertFalse(util.is_integer('4'))
        self.assertFalse(util.is_integer('Stranger Things'))

    def test_is_natural(self):
        """Tests that the `is_natural()` method returns correctly.

        Args:
          self (TestUtil): the `TestUtil` instance

        Returns:
          `None`
        """
        self.assertTrue(util.is_natural(4))
        self.assertTrue(util.is_natural(0))

        self.assertFalse(util.is_natural(-1))
        self.assertFalse(util.is_natural('4'))
        self.assertFalse(util.is_natural('The 100'))

    def test_is_os_64bit(self):
        """Tests that the ``is_os_64bit()`` method returns correctly.

        It should return ``True`` on 64-bit platforms, otherwise ``False``.

        Args:
          self (TestUtil): the ``TestUtil`` instance

        Returns:
          ``None``
        """
        with mock.patch('platform.machine') as mock_machine:
            mock_machine.return_value = 'i386'
            self.assertFalse(util.is_os_64bit())

            mock_machine.return_value = ''
            self.assertFalse(util.is_os_64bit())

            mock_machine.return_value = 'i686'
            self.assertFalse(util.is_os_64bit())

            mock_machine.return_value = 'x86_64'
            self.assertTrue(util.is_os_64bit())

    def test_noop(self):
        """Tests that the `noop()` method does nothing and takes any args.

        Args:
          self (TestUtil): the `TestUtil` instance

        Returns:
          `None`
        """
        self.assertEqual(None, util.noop())
        self.assertEqual(None, util.noop(*range(100)))
        self.assertEqual(None, util.noop(arg=4))

    def test_unsecure_hook_dialog(self):
        """Tests that the unsecure hook dialog always returns `YES`.

        Args:
          self (TestUtil): the `TestUtil` instance

        Returns:
          `None`
        """
        self.assertEqual(enums.JLinkFlags.DLG_BUTTON_NO,
                         util.unsecure_hook_dialog('', '', 0))

    @mock.patch('sys.stdout', new_callable=StringIO.StringIO)
    def test_progress_bar(self, stream):
        """Tests the progress bar calls the appropriate stream functions.

        When percent is full, the `progress_bar()` should append a newline to
        the stream, otherwise not.

        Args:
          self (TestUtil): the `TestUtil` instance
          stream (StringIO): the mock output stream

        Returns:
          `None`
        """
        self.assertEqual(None, util.progress_bar(0, 100))
        self.assertFalse(stream.getvalue() == '\n')

        self.assertEqual(None, util.progress_bar(100, 100))

        messages = stream.getvalue().split('\n')
        self.assertEqual(2, len(messages))
        self.assertTrue(messages.pop(0).endswith(' '))
        self.assertTrue(messages.pop(0) == '')

    @mock.patch('sys.stdout', new_callable=StringIO.StringIO)
    def test_flash_progress_callback(self, stream):
        """Tests that the callback triggers a progress bar.

        Args:
          self (TestUtil): the `TestUtil` instance
          stream (StringIO): the mock output stream

        Returns:
          `None`
        """
        self.assertEqual(None, util.flash_progress_callback('compare', '', 0))
        self.assertEqual('', stream.getvalue())

        self.assertEqual(None, util.flash_progress_callback('Erase', '', 0))
        self.assertTrue(len(stream.getvalue()) > 0)

    def test_calculate_parity(self):
        """Tests that the parity is properly calculated.

        Args:
          self (TestUtil): the `TestUtil` instance

        Returns:
          `None`
        """
        self.assertEqual(1, util.calculate_parity(1))
        self.assertEqual(1, util.calculate_parity(2))
        self.assertEqual(0, util.calculate_parity(3))

    def test_calculate_parity_invalid(self):
        """Tests that an exception is raised for invalid args to `parity()`.

        Args:
          self (TestUtil): the `TestUtil` instance

        Returns:
          `None`
        """
        with self.assertRaises(ValueError):
            util.calculate_parity('4')

        with self.assertRaises(ValueError):
            util.calculate_parity(-1)


if __name__ == '__main__':
    unittest.main()
