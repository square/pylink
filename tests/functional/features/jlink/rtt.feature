@connection
Feature: RTT
    In order to debug my firmware
    I want to be able to use RTT
    To write and receive real-time debug information

    Scenario: Echoing data over RTT
        Given my J-Link is connected
        And target interface SWD
        And device MK21FX512xxx12 (ALLOW SECURITY)
        When I flash the firmware K21-RTT
        And I reset my device
        And I enable RTT with config block 0x1FFF0424
        When I write "aardvark" to RTT channel 0
        Then I should read "aardvark" on RTT channel 0
