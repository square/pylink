# Testing
The tests for this project are split into two sections: unit tests, and
functional tests.  Functional tests live under the `functional` directory,
while unit tests live under the `unit` directory.


## Unit Tests
Unit tests are those that verify the behaviour of the library.  These use
mocked calls for calls that require actual hardware (such as the J-Link DLL
calls).  Unit tests should be created for every function to test that the
correct behaviour is there.  This is especially necessary since Python is a
dynamic language, so things such as misspellings will not be caught until the
actual code is run.


## Functional Tests
Functional Tests live under the `functional` directory.  The functional tests
are implemented using [`behave`](http://pythonhosted.org/behave/), a Behaviour
Driven Development (BDD) library.


### Firmware
Firmware goes underneath the `firmware` directory within the `functional`
directory.  It must include a `Makefile` that builds its dependency underneath
a `build` directory within the same directory (the output firmware should be
labelled `firmware.{elf,bin}`.
