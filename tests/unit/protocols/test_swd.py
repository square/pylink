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

import pylink.protocols.swd as swd
import pylink.util

import mock

import unittest


class TestSerialWireDebug(unittest.TestCase):
    """Tests the `protocols.swd` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        pass

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        pass

    def test_swd_response_ack(self):
        """Tests creating an ACK response.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        response = swd.Response(swd.Response.STATUS_ACK)
        self.assertTrue(response.ack())
        self.assertFalse(response.wait())
        self.assertFalse(response.fault())
        self.assertFalse(response.invalid())

    def test_swd_response_wait(self):
        """Tests creating a WAIT response.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        response = swd.Response(swd.Response.STATUS_WAIT)
        self.assertTrue(response.wait())
        self.assertFalse(response.ack())
        self.assertFalse(response.fault())
        self.assertFalse(response.invalid())

    def test_swd_response_fault(self):
        """Tests creating a FAULT response.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        response = swd.Response(swd.Response.STATUS_FAULT)
        self.assertTrue(response.fault())
        self.assertFalse(response.wait())
        self.assertFalse(response.ack())
        self.assertFalse(response.invalid())

    def test_swd_response_invalid(self):
        """Tests creating an invalid response.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        response = swd.Response(swd.Response.STATUS_INVALID)
        self.assertTrue(response.invalid())
        self.assertFalse(response.fault())
        self.assertFalse(response.wait())
        self.assertFalse(response.ack())

    def test_swd_read_request_initialize(self):
        """Tests creating a SWD Read Request.

        When a SWD Read Request is created, there is a structure specifying
        what the underlying bits should look like.  This test verifies a
        number of different valid bitfields.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        values = [165, 141, 149, 189, 165]
        for (index, value) in enumerate(values):
            request = swd.ReadRequest(index, ap=False)
            self.assertEqual(value, request.value)

        values = [135, 175, 183, 159, 135]
        for (index, value) in enumerate(values):
            request = swd.ReadRequest(index, ap=True)
            self.assertEqual(value, request.value)

    def test_swd_read_request_send_nack(self):
        """Tests sending a SWD Read Request that is NACK'd.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        request = swd.ReadRequest(0, True)

        ack = 1
        status = swd.Response.STATUS_WAIT
        data = 2

        mock_jlink = mock.Mock()
        mock_jlink.swd_write.return_value = ack
        mock_jlink.swd_read8.return_value = status
        mock_jlink.swd_read32.return_value = data

        response = request.send(mock_jlink)

        self.assertFalse(response.ack())
        self.assertTrue(response.wait())

        self.assertEqual(2, mock_jlink.swd_write8.call_count)
        mock_jlink.swd_write8.assert_any_call(0xFF, request.value)  # data command
        mock_jlink.swd_write8.assert_any_call(0xFC, 0x0)  # status command

        self.assertEqual(1, mock_jlink.swd_write32.call_count)
        mock_jlink.swd_write32.assert_any_call(0x0, 0x0)

        self.assertEqual(1, mock_jlink.swd_write.call_count)
        mock_jlink.swd_write.assert_any_call(0x0, 0x0, 3)  # ack

        self.assertEqual(1, mock_jlink.swd_read8.call_count)
        mock_jlink.swd_read8.assert_any_call(ack)  # status read

        self.assertEqual(1, mock_jlink.swd_read32.call_count)
        mock_jlink.swd_read32.assert_any_call(ack + 3)  # data read

    def test_swd_read_request_send_ack(self):
        """Tests sending a SWD Read Request that is ACK'd.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        request = swd.ReadRequest(0, True)

        ack = 1
        status = swd.Response.STATUS_ACK
        data = 1

        mock_jlink = mock.Mock()
        mock_jlink.swd_write.return_value = ack
        mock_jlink.swd_read8.return_value = status
        mock_jlink.swd_read32.return_value = data

        response = request.send(mock_jlink)

        self.assertTrue(response.ack())

        self.assertEqual(2, mock_jlink.swd_write8.call_count)
        mock_jlink.swd_write8.assert_any_call(0xFF, request.value)  # data command
        mock_jlink.swd_write8.assert_any_call(0xFC, 0x0)  # status command

        self.assertEqual(1, mock_jlink.swd_write32.call_count)
        mock_jlink.swd_write32.assert_any_call(0x0, 0x0)

        self.assertEqual(1, mock_jlink.swd_write.call_count)
        mock_jlink.swd_write.assert_any_call(0x0, 0x0, 3)  # ack

        self.assertEqual(2, mock_jlink.swd_read8.call_count)
        mock_jlink.swd_read8.assert_any_call(ack)  # status read
        mock_jlink.swd_read8.assert_any_call(ack + 35)  # parity check

        self.assertEqual(1, mock_jlink.swd_read32.call_count)
        mock_jlink.swd_read32.assert_any_call(ack + 3)  # data read

    def test_swd_read_request_send_ack_parity_mismatch(self):
        """Tests sending a SWD Request that is ACK'd, but the parity is wrong.

        When a SWD Read Request reads data from the target, their is a parity
        field that is set, and can be is to verify that the data is valid.  In
        this test, the parity check fails.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        request = swd.ReadRequest(0, True)

        ack = 1
        status = swd.Response.STATUS_ACK
        data = 3

        mock_jlink = mock.Mock()
        mock_jlink.swd_write.return_value = ack
        mock_jlink.swd_read8.return_value = status
        mock_jlink.swd_read32.return_value = data

        response = request.send(mock_jlink)

        self.assertFalse(response.ack())
        self.assertTrue(response.invalid())

        self.assertEqual(2, mock_jlink.swd_write8.call_count)
        mock_jlink.swd_write8.assert_any_call(0xFF, request.value)  # data command
        mock_jlink.swd_write8.assert_any_call(0xFC, 0x0)  # status command

        self.assertEqual(1, mock_jlink.swd_write32.call_count)
        mock_jlink.swd_write32.assert_any_call(0x0, 0x0)

        self.assertEqual(1, mock_jlink.swd_write.call_count)
        mock_jlink.swd_write.assert_any_call(0x0, 0x0, 3)  # ack

        self.assertEqual(2, mock_jlink.swd_read8.call_count)
        mock_jlink.swd_read8.assert_any_call(ack)  # status read
        mock_jlink.swd_read8.assert_any_call(ack + 35)  # parity check

        self.assertEqual(1, mock_jlink.swd_read32.call_count)
        mock_jlink.swd_read32.assert_any_call(ack + 3)  # data read

    def test_swd_write_request_initialize(self):
        """Tests creating a SWD Write Request.

        When a SWD Write Request is created, there is a structure specifying
        what the underlying bits should look like.  This test verifies a number
        of different valid bitfields.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        data = 4
        values = [129, 169, 177, 153]
        for (index, value) in enumerate(values):
            request = swd.WriteRequest(index, data=data, ap=False)
            self.assertEqual(value, request.value)

        values = [163, 139, 147, 187]
        for (index, value) in enumerate(values):
            request = swd.WriteRequest(index, data=data, ap=True)
            self.assertEqual(value, request.value)

    def test_swd_write_request_send(self):
        """Tests sending a SWD Read Request.

        Args:
          self (TestSerialWireDebug): the `TestSerialWireDebug` instance

        Returns:
          `None`
        """
        data = 2
        parity = pylink.util.calculate_parity(data)
        request = swd.WriteRequest(0, True, data)

        ack = 2
        mock_jlink = mock.Mock()
        mock_jlink.swd_write.return_value = ack
        mock_jlink.swd_read8.return_value = 1

        response = request.send(mock_jlink)
        self.assertTrue(response.ack())

        self.assertEqual(2, mock_jlink.swd_write.call_count)
        mock_jlink.swd_write.assert_any_call(0x0, 0x0, 3)  # Ack
        mock_jlink.swd_write.assert_any_call(0x0, 0x0, 2)  # Turnaround

        self.assertEqual(2, mock_jlink.swd_write8.call_count)
        mock_jlink.swd_write8.assert_any_call(0xFF, request.value)
        mock_jlink.swd_write8.assert_any_call(0xFF, parity)

        self.assertEqual(1, mock_jlink.swd_write32.call_count)
        mock_jlink.swd_write32.assert_called_once_with(0xFFFFFFFF, data)

        self.assertEqual(1, mock_jlink.swd_read8.call_count)
        mock_jlink.swd_read8.assert_called_once_with(ack)


if __name__ == '__main__':
    unittest.main()
