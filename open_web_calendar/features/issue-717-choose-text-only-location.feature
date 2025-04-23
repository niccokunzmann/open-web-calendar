Feature: Sometimes, there is no service to look up the location of an event. So, I would like to choose that there is only text for the location.

    Scenario: When the map link templates are empty, the link does nothing.
        Given we add the calendar "issue-23-location-berlin"
          And we set the "event_url_location" parameter to ""
          And we set the "event_url_geo" parameter to ""
         When we look at 2025-01-10
          And we click on the event "Event in Berlin!"
         Then the link "Berlin" opens ""

    Scenario: When I configure the calendar, I would like to disable links to a map.
        Given we configure the map
         When we choose "Text Without Link" in "select-map"
         Then "event_url_location" is specified as ""
         Then "event_url_geo" is specified as ""

