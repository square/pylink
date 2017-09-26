@connection
Feature: Registers
    As a developer,
    I want to be able to write and read from registers.

    Scenario: Writing to a Single Register
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I halt the device
        And I write 42 to register 0
        Then register 0 should have the value 42

    Scenario: Writing to Multiple Registers
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I halt the device
        And I write to the registers:
            | register | value |
            | 0        | 32    |
            | 1        | 43    |
            | 7        | 1337  |
            | 11       | 99    |
        Then I should read from the registers:
            | register | value |
            | 0        | 32    |
            | 1        | 43    |
            | 7        | 1337  |
            | 11       | 99    |
