@connection
Feature: Debugging Firmware
    As a developer,
    I want to be able to trace my code.

    Scenario: Setting a Breakpoint
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        And I enable soft breakpoints
        When I flash the firmware K21-LOOP
        And I reset my device
        And I set a breakpoint at address 0x480
        Then the device should be halted
        And I should have 1 breakpoint

    Scenario: Clearing a Breakpoint
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        And I enable soft breakpoints
        When I flash the firmware K21-LOOP
        And I reset my device
        And I set a breakpoint at address 0x480
        Then I can clear the breakpoints
        And I should have 0 breakpoints

    Scenario: Setting a Watchpoint
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I flash the firmware K21-LOOP
        And I set a watchpoint at address 0x1FFF0000 for data 0x1337
        And I reset my device
        Then I should have 1 watchpoint

    Scenario: Clearing a Watchpoint
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I flash the firmware K21-LOOP
        And I set a watchpoint at address 0x1FFF0000 for data 0x1337
        Then I can clear the watchpoints
        And I should have 0 watchpoints
