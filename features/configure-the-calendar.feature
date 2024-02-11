Feature: The calendar has a configuration page that displays and changes the
         calendar along with its specification.

    Scenario: The default specification is almost empty.
       Given we are on the configuration page
        When we write "https://localhost:12345/example.ics" into "calendar-url-input-0"
        Then "url" is specified as "https://localhost:12345/example.ics"


    Scenario: We can specify two URLs.
       Given we are on the configuration page
        When we write "https://localhost:12345/example.ics" into "calendar-url-input-0"
         And we write "https://localhost/example.ics" into "calendar-url-input-1"
        Then "url" is specified as ["https://localhost:12345/example.ics","https://localhost/example.ics"]
