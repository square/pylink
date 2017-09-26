@connection
Feature: Serial Wire Output
    In order to test my firmware
    I want to be able to use Serial Wire Output
    To trace the instructions

    Scenario: Reading from Serial Wire Output
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I flash the firmware K21-SWO
        And I enable SWO on port 0
        Then I should see "You must construct additional pylons."
