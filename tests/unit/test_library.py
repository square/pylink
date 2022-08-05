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

from platform import platform
import pylink.library as library
import pylink.util as util

import mock

import unittest


class TestLibrary(unittest.TestCase):
    """Unit test for the ``library`` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance

        Returns:
          ``None``
        """
        assertRaisesRegexp = getattr(self, 'assertRaisesRegexp', None)
        self.assertRaisesRegexp = getattr(self, 'assertRaisesRegex', assertRaisesRegexp)
        self.lib_path = '/'

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance

        Returns:
          ``None``
        """
        pass

    def mock_directories(self, mock_os, structure, sep):
        """Mocks a directory structure.

        This function is used to mock a directory structure, so that checking
        if something is a file, is a directory, or listing directories will use
        our mocked structure instead.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): the mocked ``os`` module
          structure (list): a list of directories or files
          sep (str): the operating system seperator

        Returns:
          ``None``
        """
        def isfile(f):
            """Returns whether the file exists in the structure."""
            if not any(s.endswith(f) for s in structure):
                return False
            return '.' in f.split(sep)[-1]

        mock_os.path.isfile.side_effect = isfile

        def isdir(f):
            """Returns whether the directory exists within the structure."""
            if not any(s.startswith(f) for s in structure):
                return False
            return not isfile(f)

        mock_os.path.isdir.side_effect = isdir

        def join(*args):
            """Joins several strings to form a path."""
            s = ''
            for arg in args:
                if not s.endswith(sep) and len(s) > 0:
                    s += sep
                s += arg
            return s

        mock_os.path.join.side_effect = join

        def listdir(f):
            """List the files and directories within the directory."""
            if not isdir(f):
                return list()

            directories = []
            for s in structure:
                if s.startswith(f):
                    s = s[len(f):]
                    if s.startswith(sep):
                        s = s[len(sep):]
                    directories.append(s.split(sep)[0])
            return directories

        mock_os.listdir.side_effect = listdir

        def mock_walk(b):
            r = list()
            dirname = b
            if not isdir(dirname):
                return []

            subdirs = filter(len, list(set([d for d in listdir(dirname) if isdir(join(dirname, d))])))
            subfiles = filter(len, list(set([f for f in listdir(dirname) if isfile(join(dirname, f))])))
            r.append((dirname, subdirs, subfiles))
            for subdir in subdirs:
                r.extend(mock_walk(join(dirname, subdir)))

            return r

        mock_os.walk.return_value = mock_walk(sep)

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    def test_initialize_default(self, mock_load_library, mock_find_library, mock_open):
        """Tests creating a library and finding the default DLL.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): mock for mocking the
            ``ctypes.util.find_library()`` call
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = self.lib_path

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        mock_open.assert_called_with(self.lib_path, 'rb')
        mock_load_library.assert_called_once()

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('os.path.isdir')
    def test_initialiaze_no(self, mock_isdir, mock_load_library, mock_find_library, mock_open):
        """Tests creating a library when the default DLL does not exist.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_isdir (Mock): mock for mocking the call to ``os.path.isdir``
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): mock for mocking the
            ``ctypes.util.find_library()`` call
          mock_open (Mock): mock for mocking the clal to ``open()``

        Returns:
          ``None``
        """
        mock_isdir.return_value = False
        mock_find_library.return_value = None

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(0, mock_load_library.call_count)

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    def test_initialize_with_path(self, mock_load_library, mock_find_library, mock_open):
        """Tests creating a library when passing in a DLL path.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): mock for mocking the
            ``ctypes.util.find_library()`` call
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = None

        lib = library.Library(self.lib_path)
        lib.unload = mock.Mock()

        self.assertEqual(0, mock_find_library.call_count)

        mock_open.assert_called_with(self.lib_path, 'rb')
        mock_load_library.assert_called_once()

    @mock.patch('sys.platform', new='windows')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('pylink.library.ctypes')
    def test_initialize_windows(self, mock_ctypes, mock_find_library, mock_open):
        """Tests creating a library on a Windows machine.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_ctypes (Mock): a mocked version of the ctypes library
          mock_find_library (Mock): mock for mocking the
            ``ctypes.util.find_library()`` call
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_windll = mock.Mock()
        mock_windll.__getitem__ = mock.Mock()

        mock_cdll = mock.Mock()
        mock_cdll.__getitem__ = mock.Mock()

        mock_ctypes.windll = mock_windll
        mock_ctypes.cdll = mock_cdll
        mock_find_library.return_value = self.lib_path

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.WINDOWS_64_JLINK_SDK_NAME)
        mock_open.assert_called_with(self.lib_path, 'rb')
        mock_cdll.LoadLibrary.assert_called_once()
        mock_windll.LoadLibrary.assert_called_once()

    @mock.patch('sys.platform', new='windows')
    @mock.patch('sys.maxsize', new=(2**31-1))
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('pylink.library.ctypes')
    def test_initialize_windows_32bit(self, mock_ctypes, mock_find_library, mock_open):
        """Tests creating a library on a Windows machine with 32bit Python.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_ctypes (Mock): a mocked version of the ctypes library
          mock_find_library (Mock): mock for mocking the
            ``ctypes.util.find_library()`` call
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_windll = mock.Mock()
        mock_windll.__getitem__ = mock.Mock()

        mock_cdll = mock.Mock()
        mock_cdll.__getitem__ = mock.Mock()

        mock_ctypes.windll = mock_windll
        mock_ctypes.cdll = mock_cdll
        mock_find_library.return_value = self.lib_path

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.WINDOWS_32_JLINK_SDK_NAME)
        mock_open.assert_called_with(self.lib_path, 'rb')
        mock_cdll.LoadLibrary.assert_called_once()
        mock_windll.LoadLibrary.assert_called_once()

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    def test_load(self, mock_load_library, mock_find_library, mock_open):
        """Tests that we can pass in a path to a DLL to load.

        If the path is valid, loads the given ``DLL``, otherwise stays the
        same.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): mock for mocking the
            ``ctypes.util.find_library()`` call
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = self.lib_path

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        self.assertEqual(1, mock_find_library.call_count)

        mock_open.assert_called_with(self.lib_path, 'rb')
        self.assertEqual(1, mock_load_library.call_count)

        new_path = '\\'
        lib.load(new_path)

        mock_open.assert_called_with(new_path, 'rb')
        self.assertEqual(2, mock_load_library.call_count)

        lib.load(None)
        mock_open.assert_called_with(new_path, 'rb')
        self.assertEqual(3, mock_load_library.call_count)

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('pylink.library.open', new=mock.MagicMock())
    @mock.patch('pylink.library.ctypes')
    @mock.patch('os.remove')
    def test_unload_no_library(self, mock_remove, mock_ctypes):
        """Tests unloading the library when no DLL is loaded.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_remove (Mock): the mocked call to ``os.remove()``
          mock_ctypes (Mock): mocked ``ctypes`` module

        Returns:
          ``None``
        """
        lib = library.Library('')
        setattr(lib, '_lib', None)
        setattr(lib, '_temp', None)

        self.assertFalse(lib.unload())

        mock_remove.assert_not_called()

    @mock.patch('sys.platform', new='windows')
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('pylink.library.open', new=mock.MagicMock())
    @mock.patch('pylink.library.ctypes')
    @mock.patch('os.remove')
    def test_unload_windows(self, mock_remove, mock_ctypes):
        """Tests unloading the library on Windows.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_remove (Mock): the mocked call to ``os.remove()``
          mock_ctypes (Mock): mocked ``ctypes`` module

        Returns:
          ``None``
        """
        lib = library.Library('')

        self.assertTrue(lib.unload())

        self.assertEqual(2, mock_ctypes.windll.kernel32.FreeLibrary.call_count)

        mock_remove.assert_called_once()

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('pylink.library.open', new=mock.MagicMock())
    @mock.patch('pylink.library.ctypes')
    @mock.patch('os.remove')
    def test_unload_darwin_linux(self, mock_remove, mock_ctypes):
        """Tests unloading the library on Darwin and Linux platforms.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_remove (Mock): the mocked call to ``os.remove()``
          mock_ctypes (Mock): mocked ``ctypes`` module

        Returns:
          ``None``
        """
        lib = library.Library('')

        self.assertTrue(lib.unload())

        mock_remove.assert_called_once()

        self.assertEqual(None, lib._lib)
        self.assertEqual(None, lib._temp)

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    def test_dll_getter(self, mock_load_library, mock_find_library, mock_open):
        """Tests that the ``.dll()`` getter returns the set ``DLL``.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): mock for mocking the
            ``ctypes.util.find_library()`` call
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = self.lib_path
        mock_load_library.return_value = 0xDEADBEEF

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        self.assertEqual(1, mock_find_library.call_count)

        mock_open.assert_called_with(self.lib_path, 'rb')
        mock_load_library.assert_called_once()

        self.assertEqual(0xDEADBEEF, lib.dll())

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('pylink.library.os')
    def test_darwin_4_98_e(self, mock_os, mock_load_library, mock_find_library, mock_open):
        """Tests finding the DLL on Darwin through the SEGGER application for V4.98E-.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = None
        directories = [
            '/Applications/SEGGER/JLink 1/libjlinkarm.dylib'
        ]

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(1, mock_load_library.call_count)

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('pylink.library.os')
    def test_darwin_5_0_0(self, mock_os, mock_load_library, mock_find_library, mock_open):
        """Tests finding the DLL on Darwin through the SEGGER application for V5.0.0+.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = None
        directories = [
            '/Applications/SEGGER/JLink/libjlinkarm.5.12.10.dylib',
            '/Applications/SEGGER/JLink/libjlinkarm.5.dylib'
        ]

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(1, mock_load_library.call_count)

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('pylink.library.os')
    def test_darwin_6_0_0(self, mock_os, mock_load_library, mock_find_library, mock_open):
        """Tests finding the DLL on Darwin through the SEGGER application for V6.0.0+.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = None
        directories = [
            '/Applications/SEGGER/JLink/libjlinkarm.dylib'
        ]

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(1, mock_load_library.call_count)

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('pylink.library.os')
    def test_darwin_empty(self, mock_os, mock_load_library, mock_find_library, mock_open):
        """Tests finding the DLL on Darwin through the SEGGER application for V6.0.0+.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = None
        directories = [
            '/Applications/SEGGER/JLink/'
        ]

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(0, mock_load_library.call_count)

    @mock.patch('sys.platform', new='windows')
    @mock.patch('sys.maxsize', new=(2**31 - 1))
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('pylink.library.ctypes')
    @mock.patch('pylink.library.os')
    def test_windows_4_98_e(self, mock_os, mock_ctypes, mock_find_library, mock_open):
        """Tests finding the DLL on Windows through the SEGGER application for V4.98E-.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_ctypes (Mock): a mocked version of the ctypes library
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_windll = mock.Mock()
        mock_windll.__getitem__ = mock.Mock()

        mock_cdll = mock.Mock()
        mock_cdll.__getitem__ = mock.Mock()

        mock_ctypes.windll = mock_windll
        mock_ctypes.cdll = mock_cdll
        mock_find_library.return_value = None

        directories = [
            'C:\\Program Files\\SEGGER\\JLink_V49e\\JLinkARM.dll'
        ]

        self.mock_directories(mock_os, directories, '\\')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.WINDOWS_32_JLINK_SDK_NAME)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(1, mock_windll.LoadLibrary.call_count)
        self.assertEqual(1, mock_cdll.LoadLibrary.call_count)

    @mock.patch('sys.platform', new='windows')
    @mock.patch('sys.maxsize', new=(2**31-1))
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('pylink.library.ctypes')
    @mock.patch('pylink.library.os')
    def test_windows_5_10_0(self, mock_os, mock_ctypes, mock_find_library, mock_open):
        """Tests finding the DLL on Windows through the SEGGER application for V5.0.0+.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_ctypes (Mock): a mocked version of the ctypes library
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_windll = mock.Mock()
        mock_windll.__getitem__ = mock.Mock()

        mock_cdll = mock.Mock()
        mock_cdll.__getitem__ = mock.Mock()

        mock_ctypes.windll = mock_windll
        mock_ctypes.cdll = mock_cdll
        mock_find_library.return_value = None

        directories = [
            'C:\\Program Files (x86)\\SEGGER\\JLink_V510l\\JLinkARM.dll'
        ]

        self.mock_directories(mock_os, directories, '\\')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.WINDOWS_32_JLINK_SDK_NAME)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(1, mock_windll.LoadLibrary.call_count)
        self.assertEqual(1, mock_cdll.LoadLibrary.call_count)

    @mock.patch('sys.platform', new='windows')
    @mock.patch('sys.maxsize', new=(2**31-1))
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('pylink.library.ctypes')
    @mock.patch('pylink.library.os')
    def test_windows_jlinkarm(self, mock_os, mock_ctypes, mock_find_library, mock_open):
        """Tests finding the DLL on Windows through the SEGGER JLinkARM folder.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_ctypes (Mock): a mocked version of the ctypes library
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_windll = mock.Mock()
        mock_windll.__getitem__ = mock.Mock()

        mock_cdll = mock.Mock()
        mock_cdll.__getitem__ = mock.Mock()

        mock_ctypes.windll = mock_windll
        mock_ctypes.cdll = mock_cdll
        mock_find_library.return_value = None

        directories = [
            'C:\\Program Files (x86)\\SEGGER\\JLinkARM\\JLinkARM.dll'
        ]

        self.mock_directories(mock_os, directories, '\\')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.WINDOWS_32_JLINK_SDK_NAME)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(1, mock_windll.LoadLibrary.call_count)
        self.assertEqual(1, mock_cdll.LoadLibrary.call_count)

    @mock.patch('sys.platform', new='windows')
    @mock.patch('sys.maxsize', new=(2**31 - 1))
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('pylink.library.ctypes')
    @mock.patch('pylink.library.os')
    def test_windows_empty(self, mock_os, mock_ctypes, mock_find_library, mock_open):
        """Tests finding the DLL on Windows through the SEGGER application for V6.0.0+.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_ctypes (Mock): a mocked version of the ctypes library
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open``

        Returns:
          ``None``
        """
        mock_windll = mock.Mock()
        mock_windll.__getitem__ = mock.Mock()

        mock_cdll = mock.Mock()
        mock_cdll.__getitem__ = mock.Mock()

        mock_ctypes.windll = mock_windll
        mock_ctypes.cdll = mock_cdll
        mock_find_library.return_value = None

        directories = [
            'C:\\Program Files\\',
            'C:\\Program Files (x86)\\'
        ]

        self.mock_directories(mock_os, directories, '\\')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.WINDOWS_32_JLINK_SDK_NAME)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(0, mock_windll.LoadLibrary.call_count)
        self.assertEqual(0, mock_cdll.LoadLibrary.call_count)

    @mock.patch('sys.platform', new='cygwin')
    @mock.patch('sys.maxsize', new=(2**31-1))
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('pylink.library.os')
    def test_cygwin(self, mock_os, mock_load_library, mock_find_library, mock_open):
        """Tests finding the DLL when running within Cygwin.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = None

        directories = [
            'C:\\Program Files (x86)\\SEGGER\\JLinkARM\\JLinkARM.dll',
            'C:\\Program Files (x86)\\SEGGER\\JLink_V500l\\JLinkARM.dll'
        ]

        self.mock_directories(mock_os, directories, '\\')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.WINDOWS_32_JLINK_SDK_NAME)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(1, mock_load_library.call_count)

    @mock.patch('sys.platform', new='linux')
    @mock.patch('pylink.util.is_os_64bit', return_value=False)
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('pylink.library.os')
    def test_linux_4_98_e(self, mock_os, mock_load_library, mock_find_library, mock_open, mock_is_os_64bit):
        """Tests finding the DLL on Linux through the SEGGER application for V4.98E-.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = None
        directories = [
            '/opt/SEGGER/JLink_Linux_V498e_i386/libjlinkarm.so',
        ]

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()
        load_library_args, load_libary_kwargs = mock_load_library.call_args
        self.assertEqual(directories[0], lib._path)

    @mock.patch('sys.platform', new='linux2')
    @mock.patch('pylink.util.is_os_64bit', return_value=False)
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('pylink.library.os')
    def test_linux_6_10_0_32bit(self, mock_os, mock_load_library, mock_find_library, mock_open, mock_is_os_64bit):
        """Tests finding the DLL on Linux through the SEGGER application for V6.0.0+ on 32 bit linux.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``
          mock_is_os_64bit (Mock): mock for mocking the call to ``is_os_64bit``, returns False

        Returns:
          ``None``
        """
        mock_find_library.return_value = None
        directories = [
            '/opt/SEGGER/JLink_Linux_V610d_x86_64/libjlinkarm_x86.so.6.10',
            '/opt/SEGGER/JLink_Linux_V610d_x86_64/libjlinkarm.so.6.10',
        ]

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()
        load_library_args, load_libary_kwargs = mock_load_library.call_args
        self.assertEqual(directories[0], lib._path)

        directories = [
            '/opt/SEGGER/JLink_Linux_V610d_x86_64/libjlinkarm.so.6.10',
        ]

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()
        load_library_args, load_libary_kwargs = mock_load_library.call_args
        self.assertEqual(None, lib._path)

    @mock.patch('sys.platform', new='linux2')
    @mock.patch('pylink.util.is_os_64bit', return_value=True)
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('pylink.library.os')
    def test_linux_6_10_0_64bit(self, mock_os, mock_load_library, mock_find_library, mock_open, mock_is_os_64bit):
        """Tests finding the DLL on Linux through the SEGGER application for V6.0.0+ on 64 bit linux.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``
          mock_is_os_64bit (Mock): mock for mocking the call to ``is_os_64bit``, returns True

        Returns:
          ``None``
        """
        mock_find_library.return_value = None
        directories = [
            '/opt/SEGGER/JLink_Linux_V610d_x86_64/libjlinkarm_x86.so.6.10',
            '/opt/SEGGER/JLink_Linux_V610d_x86_64/libjlinkarm.so.6.10',
        ]

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()
        load_library_args, load_libary_kwargs = mock_load_library.call_args
        self.assertEqual(directories[1], lib._path)

        directories = [
            '/opt/SEGGER/JLink_Linux_V610d_x86_64/libjlinkarm_x86.so.6.10',
        ]

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()
        self.assertEqual(None, lib._path)

    @mock.patch('sys.platform', new='linux')
    @mock.patch('pylink.library.open')
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    @mock.patch('pylink.library.os')
    def test_linux_empty(self, mock_os, mock_load_library, mock_find_library, mock_open):
        """Tests finding the DLL on Linux through the SEGGER application for V6.0.0+.

        Args:
          self (TestLibrary): the ``TestLibrary`` instance
          mock_os (Mock): a mocked version of the ``os`` module
          mock_load_library (Mock): a mocked version of the library loader
          mock_find_library (Mock): a mocked call to ``ctypes`` find library
          mock_open (Mock): mock for mocking the call to ``open()``

        Returns:
          ``None``
        """
        mock_find_library.return_value = None
        directories = []

        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        self.assertEqual(1, mock_find_library.call_count)
        self.assertEqual(0, mock_load_library.call_count)

    @mock.patch('os.name', new='posix')
    @mock.patch('sys.platform', new='linux')
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('pylink.library.open')
    @mock.patch('pylink.library.os')
    @mock.patch('pylink.util.is_os_64bit', return_value=True)
    @mock.patch('pylink.platform.libc_ver', return_value=('libc', '1.0'))
    @mock.patch('ctypes.util.find_library', return_value='libjlinkarm.so.7')
    @mock.patch('pylink.library.JLinkarmDlInfo.__init__')
    @mock.patch('ctypes.cdll.LoadLibrary')
    def test_linux_glibc_unavailable(self, mock_load_library, mock_dlinfo_ctr, mock_find_library,
                                     mock_libc_ver, mock_is_os_64bit, mock_os,  mock_open):
        """Confirms the whole JLinkarmDlInfo code path is not involved when GNU libc
        extensions are unavailable on a Linux system, and that we'll successfully fallback
        to the "search by file name".

        Test case:
        - initial find_library('jlinkarm') succeeds
        - but the host system does not provide GNU libc extensions
        - we should then skip the dlinfo() dance and proceed
          to the "search by file name" code path, aka find_library_linux()
        - and "successfully load" a mock library file from /opt/SEGGER/JLink
        """
        directories = [
            # Library.find_library_linux() should find this.
            '/opt/SEGGER/JLink/libjlinkarm.so.6'
        ]
        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_called_once_with(library.Library.JLINK_SDK_OBJECT)
        # JLinkarmDlInfo has not been instantiated.
        self.assertEquals(0, mock_dlinfo_ctr.call_count)
        # Fallback to "search by file name" has succeeded.
        self.assertEquals(1, mock_load_library.call_count)
        self.assertEqual(directories[0], lib._path)

    @mock.patch('os.name', new='posix')
    @mock.patch('sys.platform', new='linux')
    @mock.patch('tempfile.NamedTemporaryFile', new=mock.Mock())
    @mock.patch('os.remove', new=mock.Mock())
    @mock.patch('pylink.library.open')
    @mock.patch('pylink.library.os')
    @mock.patch('pylink.util.is_os_64bit', return_value=True)
    @mock.patch('pylink.platform.libc_ver', return_value=('glibc', '2.34'))
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    def test_linux_dl_unavailable(self, mock_load_library, mock_find_library, mock_libc_ver,
                                  mock_is_os_64bit, mock_os,  mock_open):
        """Confirms we successfully fallback to the "search by file name" code path when libdl is
        unavailable despite the host system presenting itself as POSIX (GNU/Linux).

        Test case:
        - initial find_library('jlinkarm') succeeds
        - the host system presents itself as GNU/Linux, but does not provide libdl
        - we should then skip the dlinfo() dance and proceed
          to the "search by file name" code path, aka find_library_linux()
        - and "successfully load" a mock library file from /opt/SEGGER/JLink
        """
        mock_find_library.side_effect = [
            # find_library('jlinkarm')
            'libjlinkarm.so.6',
            # find_library('dl')
            None
        ]

        directories = [
            '/opt/SEGGER/JLink/libjlinkarm.so.6'
        ]
        self.mock_directories(mock_os, directories, '/')

        lib = library.Library()
        lib.unload = mock.Mock()

        mock_find_library.assert_any_call(library.Library.JLINK_SDK_OBJECT)
        mock_find_library.assert_any_call('dl')
        self.assertEquals(2, mock_find_library.call_count)
        # Called once in JLinkarmDlInfo and once in Library.
        self.assertEquals(2, mock_load_library.call_count)
        # The dlinfo() dance silently failed, but will answer None resolved path.
        self.assertIsNone(library.Library._dlinfo.path)
        # Fallback to "search by file name" has succeeded.
        self.assertEqual(directories[0], lib._path)

    @mock.patch('os.name', new='posix')
    @mock.patch('sys.platform', new='linux')
    @mock.patch('pylink.platform.libc_ver', return_value=('glibc', '2.34'))
    @mock.patch('ctypes.util.find_library')
    @mock.patch('ctypes.cdll.LoadLibrary')
    def test_linux_dl_oserror(self, mock_load_library, mock_find_library, mock_libc_ver):
        """Confirms ctype API exceptions actually propagate from JLinkarmDlInfo to call site.

        Test case:
        - initial find_library('jlinkarm') succeeds
        - the host system presents itself as GNU/Linux, and we successfully load libdl
        - but loading libdl raises OSError
        """

        mock_find_library.side_effect = [
            # find_library('jlinkarm')
            'libjlinkarm.so.6',
            # find_library('dl')
            'libdl.so.2'
        ]
        mock_load_library.side_effect = [
            # load JLink DLL
            mock.Mock(),
            # load libdl
            OSError()
        ]

        with self.assertRaises(OSError):
            lib = library.Library()
            lib.unload = mock.Mock()

        mock_find_library.assert_any_call(library.Library.JLINK_SDK_OBJECT)
        mock_find_library.assert_any_call('dl')
        self.assertEquals(2, mock_find_library.call_count)
        self.assertEquals(2, mock_load_library.call_count)


if __name__ == '__main__':
    unittest.main()
