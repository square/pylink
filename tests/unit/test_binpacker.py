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

import pylink.binpacker as binpacker

import unittest


class TestBinpacker(unittest.TestCase):
    """Unit test class for the `binpacker` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestBinpacker): the `TestBinpacker` instance

        Returns:
          `None`
        """
        pass

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestBinpacker): the `TestBinpacker` instance

        Returns:
          `None`
        """
        pass

    def test_pack_size_valid(self):
        """Tests the `pack_size()` method.

        Tests that the `pack_size()` method returns the appropriate number of
        bytes based on the value of the integer being passed.

        Args:
          self (TestBinpacker): the `TestBinpacker` instance

        Returns:
          `None`
        """
        self.assertEqual(1, binpacker.pack_size(0))
        self.assertEqual(1, binpacker.pack_size(255))
        self.assertEqual(2, binpacker.pack_size(256))
        self.assertEqual(2, binpacker.pack_size(65535))
        self.assertEqual(3, binpacker.pack_size(65536))
        self.assertEqual(4, binpacker.pack_size(2147483647))
        self.assertEqual(8, binpacker.pack_size(9223372036854775807))

    def test_pack_size_invalid(self):
        """Tests that the `pack_size()` method throws an exception.

        We cannot handle non-strings or negative numbers, so `pack_size()`
        should throw an exception.

        Args:
          self (TestBinpacker): the `TestBinpacker` instance

        Returns:
          `None`
        """
        with self.assertRaises(TypeError):
            binpacker.pack_size('Bender Bending Rodriguez')

        with self.assertRaises(ValueError):
            binpacker.pack_size(-1)

    def test_pack(self):
        """Tests that the `pack()` method packs values explicitly.

        Args:
          self (TestBinpacker): the `TestBinpacker` instance

        Returns:
          `None`
        """
        packed = binpacker.pack(255, 1)
        self.assertEqual(1, len(packed))
        self.assertEqual(255, int(packed[0]))

        packed = binpacker.pack(255, 8)
        self.assertEqual(1, len(packed))
        self.assertEqual(255, int(packed[0]))

        packed = binpacker.pack(255, 16)
        self.assertEqual(2, len(packed))
        self.assertEqual(255, int(packed[0]))
        self.assertEqual(0, int(packed[1]))

        packed = binpacker.pack(255, 32)
        self.assertEqual(4, len(packed))
        self.assertEqual(255, int(packed[0]))
        self.assertEqual(0, int(packed[1]))
        self.assertEqual(0, int(packed[2]))
        self.assertEqual(0, int(packed[3]))

        packed = binpacker.pack(0xFF000000, 32)
        self.assertEqual(4, len(packed))
        self.assertEqual(0, int(packed[0]))
        self.assertEqual(0, int(packed[1]))
        self.assertEqual(0, int(packed[2]))
        self.assertEqual(255, int(packed[3]))

    def test_pack_infer_size(self):
        """Tests that the `pack()` method can pack with an inferred size.

        Args:
          self (TestBinpacker): the `TestBinpacker` instance

        Returns:
          `None`
        """
        packed = binpacker.pack(255)
        self.assertEqual(1, len(packed))
        self.assertEqual(255, int(packed[0]))

        packed = binpacker.pack(256)
        self.assertEqual(2, len(packed))
        self.assertEqual(0, int(packed[0]))
        self.assertEqual(1, int(packed[1]))

        packed = binpacker.pack(0xFF000000)
        self.assertEqual(4, len(packed))
        self.assertEqual(0, int(packed[0]))
        self.assertEqual(0, int(packed[1]))
        self.assertEqual(0, int(packed[2]))
        self.assertEqual(255, int(packed[3]))

    def test_pack_invalid(self):
        """Tests that the `pack()` method raises an exception.

        Non-numbers or integers less than or equal to zero are unsupported.

        Args:
          self (TestBinPacker): the `TestBinpacker` instance

        Returns:
          `None`
        """
        with self.assertRaises(TypeError):
            binpacker.pack('Phillip J. Fry')

        with self.assertRaises(ValueError):
            binpacker.pack(4, 0)

        with self.assertRaises(ValueError):
            binpacker.pack(4, -1)


if __name__ == '__main__':
    unittest.main()
