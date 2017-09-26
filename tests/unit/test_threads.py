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

import pylink.threads as threads

import unittest


class TestThreads(unittest.TestCase):
    """Unit test for the `threads` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestThreads): the `TestThreads` instance

        Returns:
          `None`
        """
        pass

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestThreads): the `TestThreads` instance

        Returns:
          `None`
        """
        pass

    def test_thread(self):
        """Tests that a thread can be created and joined for a return value.

        Args:
          self (TestThreads): the `TestThreads` instance

        Returns:
          `None`
        """
        def thread_func():
            return 4

        def thread_func_with_args(x, y):
            return (x + y)

        thread = threads.ThreadReturn(target=thread_func)
        thread.start()
        self.assertEqual(4, thread.join())

        thread = threads.ThreadReturn(target=thread_func_with_args, args=(2, 3))
        thread.start()
        self.assertEqual(5, thread.join())


if __name__ == '__main__':
    unittest.main()
