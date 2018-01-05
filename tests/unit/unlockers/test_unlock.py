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

import pylink.unlockers as unlock

import mock

import unittest


class TestUnlock(unittest.TestCase):
    """Tests the `unlockers` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestUnlock): the `TestUnlock` instance

        Returns:
          `None`
        """
        pass

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestUnlock): the `TestUnlock` instance

        Returns:
          `None`
        """
        pass

    def test_unlock_unsupported(self):
        """Tests calling `unlock()` for an unsupported MCU.

        Args:
          self (TestUnlock): the `TestUnlock` instance

        Returns:
          `None`
        """
        jlink = mock.Mock()
        with self.assertRaises(NotImplementedError):
            unlock.unlock(jlink, 'kinetisf')

        with self.assertRaises(NotImplementedError):
            unlock.unlock(jlink, 'dsafdsafdas')

    @mock.patch('pylink.unlockers.unlock_kinetis')
    def test_unlock_supported(self, mock_unlock):
        """Tests calling `unlock()` with a supported MCU.

        Args:
          self (TestUnlock): the `TestUnlock` instance
          mock_unlock (function): the mocked unlock function

        Returns:
          `None`
        """
        jlink = mock.Mock()
        supported = ['Kinetis', 'kinetis', 'NXP']
        mock_unlock.return_value = True
        for mcu in supported:
            self.assertTrue(unlock.unlock(jlink, mcu))


if __name__ == '__main__':
    unittest.main()
