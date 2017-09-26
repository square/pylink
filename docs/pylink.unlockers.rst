Unlocking
=========

Sometimes a user error may result in a device becoming **locked**.  When a
device is locked, it's memory cannot be written to, nor can it's memory be
read from.  This is a security feature in many MCUs.

This module provides functions for unlocking a locked device.

.. note::

   Unlocking a device results in a mass-erase.  Do not unlock a device if you
   do not want it be erased.

.. automodule:: pylink.unlockers
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: pylink.unlockers.unlock_kinetis
    :members:
    :undoc-members:
    :show-inheritance:
