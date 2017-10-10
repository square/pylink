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
import pylink.protocols.swd as swd
import pylink.unlockers as unlock

import mock

import unittest


class TestUnlockKinetis(unittest.TestCase):
    """Tests the `unlock_kinetis` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestUnlockKinetis): the `TestUnlockKinetis` instance

        Returns:
          `None`
        """
        assertRaisesRegexp = getattr(self, 'assertRaisesRegexp', None)
        self.assertRaisesRegexp = getattr(self, 'assertRaisesRegex', assertRaisesRegexp)

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestUnlockKinetis): the `TestUnlockKinetis` instance

        Returns:
          `None`
        """
        pass

    def test_unlock_kinetis_disconnected(self):
        """Tests unlock Kinetis on a disconnected J-Link.

        This should raise an error.

        Args:
          self (TestUnlockKinetis): the `TestUnlockKinetis` instance

        Returns:
          `None`
        """
        mock_jlink = mock.Mock()
        mock_jlink.connected.return_value = False

        with self.assertRaises(ValueError):
            unlock.unlock_kinetis(mock_jlink)

    def test_unlock_kinetis_unsupported_tif(self):
        """Tests trying to unlock Kinetis with an unsupported TIF.

        Args:
          self (TestUnlockKinetis): the `TestUnlockKinetis` instance

        Returns:
          `None`
        """
        mock_jlink = mock.Mock()

        with self.assertRaises(NotImplementedError):
            mock_jlink.tif = enums.JLinkInterfaces.FINE
            unlock.unlock_kinetis(mock_jlink)

        with self.assertRaises(NotImplementedError):
            mock_jlink.tif = enums.JLinkInterfaces.ICSP
            unlock.unlock_kinetis(mock_jlink)

        with self.assertRaises(NotImplementedError):
            mock_jlink.tif = enums.JLinkInterfaces.SPI
            unlock.unlock_kinetis(mock_jlink)

        with self.assertRaises(NotImplementedError):
            mock_jlink.tif = enums.JLinkInterfaces.C2
            unlock.unlock_kinetis(mock_jlink)

    def test_unlock_kinetis_jtag(self):
        """Tests unlock Kinetis on JTAG.

        Args:
          self (TestUnlockKinetis): the `TestUnlockKinetis` instance

        Returns:
          `None`
        """
        mock_jlink = mock.Mock()
        mock_jlink.tif = enums.JLinkInterfaces.JTAG

        with self.assertRaisesRegexp(NotImplementedError, 'JTAG'):
            unlock.unlock_kinetis(mock_jlink)

    @mock.patch('time.sleep')
    def test_unlock_kinetis_identify_failed(self, mock_sleep):
        """Tests that unlock Kinetis fails if device fails to identify.

        Args:
          self (TestUnlockKinetis): the `TestUnlockKinetis` instance
          mock_sleep (Mock): mocked `time.sleep()` function

        Returns:
          `None`
        """
        mock_jlink = mock.Mock()
        mock_jlink.tif = enums.JLinkInterfaces.SWD
        for flags in [0, (0x2 << 28), ((0x2 << 28) | (0xBA01 << 12))]:
            mock_jlink.coresight_read.return_value = flags
            self.assertFalse(unlock.unlock_kinetis(mock_jlink))

    @mock.patch('time.sleep')
    def test_unlock_kinetis_read_fail(self, mock_sleep):
        """Tests unlock Kinetis failing during a read.

        At any point, the unlock can fail if it tries to read from the an
        MDM-AP register and a fault occurs.

        Args:
          self (TestUnlockKinetis): the `TestUnlockKinetis` instance
          mock_sleep (Mock): mocked `time.sleep()` function

        Returns:
          `None`
        """
        mock_jlink = mock.Mock()
        mock_jlink.tif = enums.JLinkInterfaces.SWD

        flags = (0x2 << 28) | (0xBA01 << 12) | 1
        mock_jlink.coresight_read.side_effect = [flags, 0xFF]

        mock_jlink.swd_write.return_value = 0   # ACK
        mock_jlink.swd_read8.return_value = -1  # Invalid Read
        mock_jlink.swd_read32.return_value = 2  # Data

        res = unlock.unlock_kinetis(mock_jlink)
        self.assertFalse(res)

        self.assertEqual(1, mock_jlink.set_reset_pin_low.call_count)
        self.assertEqual(1, mock_jlink.set_reset_pin_high.call_count)
        self.assertEqual(0, mock_jlink.reset.call_count)

    @mock.patch('time.sleep')
    def test_unlock_kinetis_success(self, mock_sleep):
        """Tests unlock Kinetis succesfully unlocking the device.

        Args:
          self (TestUnlockKinetis): the `TestUnlockKinetis` instance
          mock_sleep (Mock): mocked `time.sleep()` function

        Returns:
          `None`
        """
        mock_jlink = mock.Mock()
        mock_jlink.tif = enums.JLinkInterfaces.SWD

        flags = (0x2 << 28) | (0xBA01 << 12) | 1
        mock_jlink.coresight_read.side_effect = [flags, 0xFF]

        ack = swd.Response.STATUS_ACK
        wait = swd.Response.STATUS_WAIT

        mocked_data = mock.Mock()
        mocked_data.read_data = [
            0x0,  # Wait
            0x1,  # Ack
            0x3,  # Flash Ready Bit Set
            0x1,  # Ack
            0x3,  # Erase Command Bit Set
            0x1,  # Ack
            0x0,  # Flash Erase In Progress Bit Cleared
        ]

        mocked_data.status_and_parity_data = [
            ack,   # Error clearing write request.
            ack,   # Selecting the MDM-AP Status Register
            wait,  # First poll, wait
            ack,   # Second poll, continue
            0x1,   # Parity
            ack,   # Flash Ready ACK
            0x0,   # Flash Ready Parity
            0x1,   # Mass Erase Request
            ack,   # Erase Command ACK
            0x1,   # Erase Command Parity
            ack,   # Erase Command ACK
            0x0,   # Erase Command Parity
            ack,   # Flash Erase Command ACK
            0x1,   # Flash Erase Command Parity
            ack,   # Flash Erase Command ACK
            0x0,   # Flash Erase Command Parity
        ]

        # ACK
        mock_jlink.swd_write.return_value = 0

        # Status and Parity
        mock_jlink.swd_read8.side_effect = mocked_data.status_and_parity_data

        # Data
        mock_jlink.swd_read32.side_effect = mocked_data.read_data

        res = unlock.unlock_kinetis(mock_jlink)
        self.assertTrue(res)

        self.assertEqual(1, mock_jlink.reset.call_count)
        self.assertEqual(1, mock_jlink.set_reset_pin_low.call_count)
        self.assertEqual(1, mock_jlink.set_reset_pin_high.call_count)


if __name__ == '__main__':
    unittest.main()
