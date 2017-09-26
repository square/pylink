# Troubleshooting

This document describes troubleshooting for common exceptions and issues that
you may run into using the library.


## Unspecified Error during Open

If you see the unspecified error during `open()`, it means that one of the
following is true:

  - Your J-Link is not connected to your computer.
  - Your J-Link is connected to your computer, but is currently held open by
    another application.


## Unspecified Error during Connect

If you see the unspecified error during `connect()`, it means that any of the
following is not true:

  - The target device's chip name you passed to `connect()` is not the chip
    name of the actual target.
  - You're trying to connect to the target over `JTAG` when it only supports
    `SWD`.
  - You're trying to connect to the target, but the target is not plugged in.
  - You're trying to connect to the target using a J-Link that does not have
    the target plugged in under its "Target" port.
  - The connection speed is bad (try `'auto'` instead).


## Unspecified Error during Erase

If you see the unspecified error during `erase()`, it means that your device is
not properly halted.  IF you're using a Cortex-M device, try setting the reset
strategy to `JLinkResetStrategyCortexM3.RESETPIN` to avoid your device's
application running when the system is booted; this is particularly useful if
your application launches the watchdog or another service which would interpret
the J-Link when erasing.


## Unspecified Error during Flash

If you see the unspecified error during `flash()`, it means that either:

   - Your device is not properly halt.  While `flash()` attempts to halt the
     CPU, it cannot if the device is breakpointed or similar.
   - The device is locked, in which case you have to unlock the device first by
     calling `unlock()`.


## Unspecified Error in Coresight

If you see an unspecified error while using a Coresight method, it means that
you are trying to read from / write to an invalid register.
