@connection
Feature: Memory
    As a developer,
    I want to be able to write and read from memory.

    Scenario Outline: Writing to Device Memory
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I write the <size>-bit integer <value> to memory
        Then I should read the <size>-bit integer <value> from memory

        Examples:
            | size | value               |
            | 8    | 254                 |
            | 16   | 32767               |
            | 32   | 2147483637          |
            | 64   | 9223372036854775807 |

    Scenario: Overflow on Writing to Device Memory
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12
        When I write the 8-bit integer 256 to memory
        Then I should read the 8-bit integer 0 from memory

    Scenario: Underflow on Reading from Device Memory
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12
        When I write the 16-bit integer 256 to memory
        Then I should read the 8-bit integer 0 from memory

    Scenario: Reading from Code Memory
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12
        When I write the 8-bit integer 92 to memory
        Then I should read the integer 92 from code memory
