Feature: I want to customize the links to the location of an event.

    Scenario: Open Street Map is the default choice.
        Given we are on the configuration page
         When we choose "OpenStreetMap" in "select-map"
         Then "event_url_location" is not specified
         Then "event_url_geo" is not specified

    Scenario Outline: I choose which map to use.
        Given we are on the configuration page
         When we choose "<name>" in "select-map"
         Then "event_url_location" is specified as "<search>"
         Then "event_url_geo" is specified as "<geo>"

        # Berlin, the capital city of Germany, has a latitude of 52.520008 and a longitude of 13.404954. 
        Examples:
            | name | search | geo |
            | Bing Maps | https://www.bing.com/maps?q={location}&lvl={zoom} | https://www.bing.com/maps?brdr=1&cp={lat}%7E{lon}&lvl={zoom} |
            | Google Maps | https://www.google.com/maps/search/{location} | https://www.google.com/maps/@{lat},{lon},{zoom}z |
    
    Scenario: I would like to click the location of an event.
        Given we add the calendar "issue-23-location-berlin"
          And we set the "event_url_geo" parameter to "geo:{lat},{lon}"
         When we look at 2025-01-16
          And we click on the event "Event in Mountain View with Geo link"
         Then the link "Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika" opens "geo:37.386013,-122.082932"

    Scenario: By default, I open OpenStreetMap.
        Given we add the calendar "issue-23-location-berlin"
         When we look at 2025-01-10
          And we click on the event "Event in Berlin!"
         Then the link "Berlin" opens "https://www.openstreetmap.org/search?query=Berlin"

    Scenario: I can open my map for the bus to Cheb even if the geo location is malformed.
        Given we add the calendar "issue-23-location-bus-to-cheb"
         When we look at 2025-01-10
          And we click on the event "#8965268597"
         Then the link "50.1075325012207, 14.2693090438843" opens "https://www.openstreetmap.org/#map=16/50.1075325012207/14.2693090438843"