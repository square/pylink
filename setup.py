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

import sys

# Stub the 'psutil' module that is required by this package in order to enable
# the main module to be imported.
try:
    import psutil
except ImportError:
    sys.modules['psutil'] = {}

import pylink

import os
import setuptools
import shutil
import subprocess


class CleanCommand(setuptools.Command):
    """Custom clean command."""

    description = 'clean the project build files'

    user_options = []

    def initialize_options(self):
        """Initialize the Command.

        Args:
          self (CleanCommand): the ``CleanCommand`` instance

        Returns:
          ``None``
        """
        self.cwd = None
        self.build_dirs = None
        self.build_artifacts = None

    def finalize_options(self):
        """Populate the attributes.

        Args:
          self (CleanCommand): the ``CleanCommand`` instance

        Returns:
          ``None``
        """
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.build_dirs = [
            os.path.join(self.cwd, 'build'),
            os.path.join(self.cwd, 'htmlcov'),
            os.path.join(self.cwd, 'dist'),
            os.path.join(self.cwd, 'pylink_square.egg-info')
        ]
        self.build_artifacts = ['.pyc', '.o', '.elf', '.bin']

    def run(self):
        """Runs the command.

        Args:
          self (CleanCommand): the ``CleanCommand`` instance

        Returns:
          ``None``
        """
        for build_dir in self.build_dirs:
            if os.path.isdir(build_dir):
                sys.stdout.write('Removing %s%s' % (build_dir, os.linesep))
                shutil.rmtree(build_dir)

        for (root, dirs, files) in os.walk(self.cwd):
            for name in files:
                fullpath = os.path.join(root, name)
                if any(fullpath.endswith(ext) for ext in self.build_artifacts):
                    sys.stdout.write('Removing %s%s' % (fullpath, os.linesep))
                    os.remove(fullpath)


class CoverageCommand(setuptools.Command):
    """Custom command for generating coverage information."""

    description = 'generate coverage information'

    user_options = []

    def initialize_options(self):
        """Initializes the command.

        Args:
          self (CoverageCommand): the ``CoverageCommand`` instance

        Returns:
          ``None``
        """
        self.cwd = None
        self.test_dir = None

    def finalize_options(self):
        """Finalizes the command's options.

        Args:
          self (CoverageCommand): the ``CoverageCommand`` instance

        Returns:
          ``None``
        """
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.test_dir = os.path.join(self.cwd, 'tests')

    def run(self):
        """Runs the command to generate coverage information.

        Args:
          self (CoverageCommand): the ``CoverageCommand`` instance

        Returns:
          ``None``
        """
        import coverage
        subprocess.call(['coverage', 'run', '--source', 'pylink', 'setup.py', 'test'])
        subprocess.call(['coverage', 'report'])
        subprocess.call(['coverage', 'html'])


class BDDTestCommand(setuptools.Command):
    """BDD test command."""

    description = 'run the behaviour tests'

    user_options = []

    def initialize_options(self):
        """Initialize the Command.

        Args:
          self (BDDTestCommand): the ``BDDTestCommand`` instance

        Returns:
          ``None``
        """
        self.cwd = None
        self.firmware_dirs = None
        self.features_dir = None

    def finalize_options(self):
        """Populate the attributes.

        Args:
          self (BDDTestCommand): the ``BDDTestCommand`` instance

        Returns:
          ``None``
        """
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.features_dir = os.path.join(self.cwd, 'tests', 'functional', 'features')
        self.firmware_dirs = []

        root = os.path.join(self.cwd, 'tests', 'functional', 'firmware')
        for f in os.listdir(root):
            fullpath = os.path.join(root, f)
            if os.path.isdir(fullpath):
                self.firmware_dirs.append(fullpath)

    def run(self):
        """Runs the command.

        Args:
          self (BDDTestCommand): the ``BDDTestCommand`` instance

        Returns:
          ``True`` on success, otherwise ``False``.

        Raises:
          ValueError: if a build fails
        """
        import behave.__main__ as behave

        for d in self.firmware_dirs:
            original_dir = os.getcwd()
            os.chdir(d)

            output = ''
            try:
                output = subprocess.check_output('make', shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                if output:
                    sys.stdout.write('Captured Output:%s%s%s' % (os.linesep, output, os.linesep))
                os.chdir(original_dir)
                raise e

            os.chdir(original_dir)

        return behave.main([self.features_dir])


def long_description():
    """Reads and returns the contents of the README.

    On failure, returns the project long description.

    Returns:
      The project's long description.
    """
    cwd = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(cwd, 'README.md')
    if not os.path.exists(readme_path):
        return pylink.__long_description__

    try:
        import pypandoc
        return pypandoc.convert_file(readme_path, 'rst')
    except (IOError, ImportError):
        pass

    return open(readme_path, 'r').read()


setuptools.setup(
    # Project information.
    name='pylink-square',
    version=pylink.__version__,

    #  Metadata for upload to PyPI.
    author=pylink.__author__,
    author_email=pylink.__author_email__,
    description=pylink.__description__,
    long_description=long_description(),
    license=pylink.__license__,
    keywords='SEGGER J-Link',
    url=pylink.__url__,

    # Packages and package data.
    packages=[
        'pylink',
        'pylink.protocols',
        'pylink.unlockers'
    ],
    package_data={
        'pylink': [
        ]
    },

    # Dependencies.
    install_requires=[
        'psutil >= 5.2.2',
        'future',
        'six'
    ],

    # Tests
    test_suite='tests',

    # Test requirements
    tests_require=[
        'mock == 2.0.0'
    ],

    # Additional scripts.
    scripts=[
        os.path.join('examples', 'pylink-rtt'),
        os.path.join('examples', 'pylink-swv'),
    ],

    # Entry points.
    entry_points={
        'console_scripts': [
            'pylink = pylink.__main__:main'
        ]
    },

    # Custom commands
    cmdclass={
        'clean': CleanCommand,
        'coverage': CoverageCommand,
        'bddtest': BDDTestCommand
    }
)
