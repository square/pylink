@connection
Feature: J-Link Communication
    As a developer,
    I want to be able to communicate with my J-Links.

    Scenario: Disconnecting from the J-Link
        Given my J-Link is connected
        And I close the J-Link
        Then the emulator should not be connected

    Scenario: Accessing multiple J-links from the same process
        Given my J-Link is connected
        Then a new J-Link should not be connected

    @nix
    Scenario: Accessing one J-link from multiple processes
        Given my J-Link is connected
        When I create a new process with my J-Link
        Then that process's J-Link is also connected

    Scenario: Accessing the same J-Link multiple times
        Given my J-Link is connected
        Then I should not be able to open a new connection to it
