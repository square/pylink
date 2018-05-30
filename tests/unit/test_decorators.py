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

import pylink.decorators as decorators

import mock

import threading
import unittest


class TestDecorators(unittest.TestCase):
    """Unit test for the `decorators` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestDecorators): the `TestDecorators` instance

        Returns:
          `None`
        """
        self.callback = mock.Mock()

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestDecorators): the `TestDecorators` instance

        Returns:
          `None`
        """
        pass

    def test_async_decorator_invalid(self):
        """Tests that the decorator raises an exception on invalid args.

        Args:
          self (TestDecorators): the `TestDecorators` instance

        Returns:
          `None`
        """
        @decorators.async_decorator
        def foo():
            return 4

        with self.assertRaises(TypeError):
            foo(callback='callback')

    def test_async_decorator_sync_call(self):
        """Tests that we can call the decorated method synchronously.

        Args:
          self (TestDecorators): the `TestDecorators` instance

        Returns:
          `None`
        """
        @decorators.async_decorator
        def foo():
            return 4

        self.assertEqual(4, foo())

    def test_async_decorator_join(self):
        """Tests that the returned object is a thread that can be joined and
        waited for termination.

        Args:
          self (TestDecorators): the `TestDecorators` instance

        Returns:
          `None`
        """
        @decorators.async_decorator
        def foo():
            return 4

        def callback(exception, result):
            return result

        thread = foo(callback=self.callback)
        self.assertTrue(isinstance(thread, threading.Thread))

        result = thread.join()
        self.assertTrue(isinstance(result, mock.Mock))
        self.callback.assert_called_with(None, 4)

        thread = foo(callback=callback)
        self.assertTrue(isinstance(thread, threading.Thread))

        result = thread.join()
        self.assertEqual(4, result)

    def test_async_decorator_exception(self):
        """Tests that exceptions raised in the async call are passed to the
        callback.

        Args:
          self (TestDecorators): the `TestDecorators` instance

        Returns:
          `None`
        """
        @decorators.async_decorator
        def failure():
            raise Exception('I HAVE FAILED!')

        thread = failure(callback=self.callback)
        thread.join()

        self.assertEqual(1, len(self.callback.call_args_list))
        self.assertTrue(self.callback.call_args is not None)

        exception = self.callback.call_args[0][0]
        self.assertTrue(isinstance(exception, BaseException))
        self.assertEqual('I HAVE FAILED!', str(exception))

        res = self.callback.call_args[0][1]
        self.assertEqual(None, res)


if __name__ == '__main__':
    unittest.main()
