Feature: I want to customize the links to the location of an event.

    Scenario: Open Street Map is the default choice.
        Given we are on the configuration page
         When we choose "Open Street Map" in "select-map"
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
            # | Open Street Map | https://www.bing.com/maps?q={location}&lvl={zoom} | https://www.bing.com/maps?brdr=1&cp={lat}%7E{lon}&lvl={zoom} |
            | Google Maps | https://www.google.co.uk/maps/search/{location} | https://www.google.co.uk/maps/@{lat},{lon},{zoom}z |
    
    # Scenario Outline: A custom URL can specify a search query

    #   Examples:
    #     | event name        | url |
    #     | event with location text 1 |  ...   |
    #     | event with location text 2 |  ...   |
    

    # Scenario: If the event has an ALTREP in it, it uses this as location

    # Scenario: If the event description has a URL in it, it uses that as link.

    # Scenario: If the event has a GEO in it, it uses this as link

    # Scenario: Priority is ALTREP, link, geo, search
