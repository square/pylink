@connection
Feature: Licenses
    As a J-Link owner,
    I want to be able to control the licenses on my J-Link
    In order to enable or disable functionality for third party software.

    Scenario: Adding a license
        Given my J-Link is connected
        When I add the license:
            """
            IAR
            """
        Then my J-Link should have the license
            """
            IAR
            """

    Scenario: Erasing a license
        Given my J-Link is connected
        And has the license:
            """
            VCOM
            """
        When I erase the licenses
        Then my J-Link should have no licenses
