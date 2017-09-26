@connection
Feature: Serial Wire Debug
    In order to debug my firmware
    I want to be able to use semihosting
    To receive semihosted operations

    Scenario: Calling printf under semihosting
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I flash the firmware K21-SWD
        And I enable semihosting
        And I reset my device
        Then the device should be halted
        And I should see over SWD:
            """
            You must construct additional pylons.
            """
