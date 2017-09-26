@connection
Feature: Unlocking a Device
    When my device is locked
    I want to be able to unlock it.

    Scenario: Unlocking a Kinetis Device
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When my Kinetis device is locked
        And I unlock it
        Then I should be able to write to flash
