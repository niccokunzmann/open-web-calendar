Feature: Many plugins are available and should be configurable.

    Scenario: The details plugin can be deactivated.
        Given we add the calendar "issue-23-location-bus-to-cheb"
          And we set the "plugin_event_details" parameter to "false"
         When we look at 2025-01-10
          And we click on the event "#8965268597"
         Then we cannot see the text "50.1075325012207"

    Scenario: The details plugin is activated by default.
        Given we add the calendar "issue-23-location-bus-to-cheb"
         When we look at 2025-01-10
          And we click on the event "#8965268597"
         Then we can see the text "50.1075325012207"
