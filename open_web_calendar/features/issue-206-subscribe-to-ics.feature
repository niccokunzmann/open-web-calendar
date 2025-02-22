Feature: I would like to be able to subscribe to an event, a series of events or the whole calendar.

    Scenario: I add an event to my own calendar.
      Given we add the calendar "food"
        And we set the "tab" parameter to "day"
       When we look at 2024-03-22
        And we click on the event "Head Start Menu (ages 3-5)"
       When we click on the div "Add to My Calendar"
       Then we download the file "2024-03-22 Head Start Menu (ages 3-5).ics"

        
    Scenario: X-WR-TIMEZONE is considered

    Scenario: When I add an event from a calendar, all timezones are included.
      Given we add the calendar "issue-206-include-timezones"
        And we set the "tab" parameter to "day"
       When we look at 2025-02-20
        And we click on the event "London Event"
       When we click on the div "Add to My Calendar"
       Then we download the file "2025-02-20 1200 London Event.ics"
