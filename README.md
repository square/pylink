# pylink

[![Build Status](https://travis-ci.org/square/pylink.svg?branch=master)](https://travis-ci.org/square/pylink)

Python interface for the SEGGER J-Link.


## Requirements

- [Python >= 2.7](https://www.python.org/downloads/)
- [GNU ARM Embedded Toolchain](https://launchpad.net/gcc-arm-embedded) (for functional tests)
- [SEGGER J-Link Tools >= 6.0b](https://www.segger.com/downloads/jlink)


## Installation

Clone the project into a local repository, then navigate to the directory and
run:

```
$ python setup.py install
```


### External Dependencies

In order to use this library, you will need to have installed the SEGGER tools.
The tools can be installed from the SEGGER website
[here](https://www.segger.com/downloads/jlink).  This package is compatible
with versions of the SEGGER tool `>= 6.0b`.  Download the software under
`J-Link Software and Documentation Pack` for your specific hardware.  `PyLink`
will automatically find the library if you have installed it this way, but for
best results, you should use one of the two methods listed below depending on
your operating system:

#### On Mac

```
# Option A: Copy the library to your libraries directory.
$ cp libjlinkarm.dylib /usr/local/lib/

# Option B: Add SEGGER's J-Link directory to your dynamic libraries path.
$ export DYLD_LIBRARY_PATH=/Applications/SEGGER/JLink:$DYLD_LIBRARY_PATH
```


#### On Windows

Windows searches for DLLs in the following order:

  1. The current directory of execution.
  2. The Windows system directory.
  3. The Windows directory.

You can copy the `JLinkARM.dll` to any of the directories listed above.
Alternatively, add the SEGGER J-Link directory to your `%PATH%`.


#### On Linux

```
# Option A: Copy the library to your libraries directory.
$ cp libjlinkarm.so /usr/local/lib/

# Option B: Add SEGGER's J-Link library path to your libraries path.
$ export LD_LIBRARY_PATH=/path/to/SEGGER/JLink:$LD_LIBRARY_PATH
```


## Usage

```
import pylink

if __name__ == '__main__':
   serial_no = '123456789'
   jlink = pylink.JLink()

   # Open a connection to your J-Link.
   jlink.open(serial_no)

   # Connect to the target device.
   jlink.connect('device', verbose=True)

   # Do whatever you want from here on in.
   jlink.flash(firmware, 0x0)
   jlink.reset()
```


## Troubleshooting

Should you run into any issues, refer to the documentation, as well as check
out our [troubleshooting](./TROUBLESHOOTING.md) document.


## Documentation

Documentation follows the
[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html),
and uses [Sphinx](http://www.sphinx-doc.org/en/stable/) documentation
generator with the
[Napoleon](http://www.sphinx-doc.org/en/stable/ext/napoleon.html) extension
to provide Google style Python support.  To generate the documentation, these
packages will need to be installed (they are included in the provided
`requirements.txt` file).  With these packages installed, you can generate the
documentation as follows:

```
$ cd docs
$ make html
```


## Developing for PyLink

First install the development requirements by running:

```
pip install -e ".[dev,test]"
```

After you've installed the requirements, decide on the development work you
want to do.  See the documentation about [contributing](./CONTRIBUTING.md)
before you begin your development work.


## Testing

To run tests, execute the following:

```
# Unit tests
$ python setup.py test

# Functional tests
$ python setup.py bddtest
```

There are two types of tests: `functional` and `unit`.  Information about both
can be found under [tests/README.md](tests/README.md).


### Coverage

Code coverage can be generated as follows:

```
$ python setup.py coverage
$ open htmlcov/index.html
```


## Contributing

Please see the documentation on [contributing](./CONTRIBUTING.md).

## License

```
Copyright 2017 Square, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

See terms and conditions [here](./LICENSE.md).
