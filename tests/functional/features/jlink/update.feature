@connection
Feature: Firmware Update
    In order to get the latest bug fixes
    I want to be able to update my J-Link's firmware

    Scenario: Updating the Firmware
        Given my J-Link is connected
        Then I can update the firmware

    Scenario: Forcing a Firmware Update
        Given my J-Link is connected
        And I invalidate the firmware
        Then I can force a firmware update
