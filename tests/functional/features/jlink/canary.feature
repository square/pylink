@connection
Feature: Stack Canary
    In order to prevent unusual behaviour
    When my stack is corrupted
    I want the stack canary to trigger

    Scenario: Buffer Overflow
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I flash the firmware K21-Canary
        And I reset my device
        Then the device should be halted
