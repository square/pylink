Protocols
=========

The J-Link has multiple ways of communicating with a target: Serial Wire
Debug (SWD), Serial Wire Output (SWO), Memory, Coresight, Registers, etc.  For
some of these communication methods, there is a specific protocol that defines
how the communication takes place.

This module provides definitions to facilate communicating over the different
protocols.  All the methods use a ``JLink`` instance, but take care of the
housekeeping work involved with each protocol.

Serial Wire Debug (SWD)
-----------------------

This subsection defines the classes and methods needed to use the SWD protocol.

.. automodule:: pylink.protocols.swd
    :members:
    :undoc-members:
    :show-inheritance:
