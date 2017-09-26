@connection
Feature: Flashing Firmware
    In order to use my device
    I want to be able to flash firmware.

    Scenario: Flashing New Firmware From a File
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        Then I can flash the firmware K21-SWO with 0 retries

    Scenario: Flashing New Firmware From a Bytestream
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I read the firmware K21-SWO into a bytestream
        Then I can flash the firmware with 0 retries
