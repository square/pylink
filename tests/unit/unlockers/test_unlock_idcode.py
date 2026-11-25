# Copyright 2025 Jeremiah Gillis
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
from pylink.errors import JLinkException
import pylink.unlockers as unlock
import ctypes

import mock

import unittest


class TestUnlockIDCODE(unittest.TestCase):
    """Tests the `unlock_idcode` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestUnlockIDCODE): the `TestUnlockIDCODE` instance

        Returns:
          `None`
        """
        pass

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestUnlockIDCODE): the `TestUnlockIDCODE` instance

        Returns:
          `None`
        """
        pass

    def test_set_unlock_idcode_errors(self):
        """Tests calling `set_unlock_idcode()` for errors.

        Args:
          self (TestUnlockIDCODE): the `TestUnlockIDCODE` instance

        Returns:
          `None`
        """
        jlink = mock.Mock()

        with self.assertRaises(ValueError):
            unlock.set_unlock_idcode(jlink, '')

        with self.assertRaises(ValueError):
            unlock.set_unlock_idcode(jlink, '00112233445566778899AABBCCDDEEHH')

        jlink._dll.JLINK_GetpFunc.return_value = None
        with self.assertRaises(JLinkException):
            unlock.set_unlock_idcode(jlink, '00112233445566778899AABBCCDDEEFF')

    def test_set_unlock_idcode(self):
        """Tests calling `set_unlock_idcode()` for success.

        Args:
          self (TestUnlockIDCODE): the `TestUnlockIDCODE` instance

        Returns:
          `None`
        """
        jlink = mock.Mock()

        def dummy_function(address):
            return

        ptr_type = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
        jlink._dll.JLINK_GetpFunc.return_value = ptr_type(dummy_function)
        result = unlock.set_unlock_idcode(jlink, '00112233445566778899AABBCCDDEEFF')
        self.assertIsNone(result)

        id_code_t = ctypes.c_byte * 16
        id_code = id_code_t()
        id_code_p = ctypes.cast(ctypes.pointer(id_code), ctypes.c_void_p)
        result = jlink.unlock_idcode_cb(ctypes.c_char_p('Test'.encode('utf-8')),
                                        ctypes.c_char_p('Unlock IDCODE'.encode('utf-8')),
                                        4,
                                        id_code_p,
                                        16)
        self.assertEqual(result, enums.JLinkFlags.DLG_BUTTON_OK)
        self.assertEqual(bytes(id_code).hex().upper(), '00112233445566778899AABBCCDDEEFF')


if __name__ == '__main__':
    unittest.main()
