Feature: I would like to be able to subscribe to an event, a series of events or the whole calendar.

    Scenario: I add an event to my own calendar.
      Given we add the calendar "food"
        And we set the "tab" parameter to "day"
       When we look at 2024-03-22
        And we click on the event "Head Start Menu (ages 3-5)"
       When we click on the div "Add to My Calendar"
       Then we download the file "2024-03-22 Head Start Menu (ages 3-5).ics"
        
    Scenario: The X-WR-TIMEZONE is added as a component and we see our time in the file name and the / is replaced.
      Given we add the calendar "single-event-with-x-wr-timezone"
        And we set the "tab" parameter to "day"
        And we set the "timezone" parameter to "Asia/Singapore"
       When we look at 2021-12-23
        And we click on the event "Google Calendar says this is noon to 1PM on 12/22/2021"
       When we click on the div "Add to My Calendar"
       Then we download the file "2021-12-23 0100 Google Calendar says this is noon to 1PM on 12-22-2021.ics"

    Scenario: When I add an event from a calendar, all timezones are included.
      Given we add the calendar "issue-206-include-timezones"
        And we set the "tab" parameter to "day"
       When we look at 2025-02-20
        And we click on the event "London Event"
       When we click on the div "Add to My Calendar"
       Then we download the file "2025-02-20 1200 London Event.ics"

    Scenario Outline: When I click on an event with recurrences, then I would like to have the recurrence id included.
      Given we add the calendar "issue-206-include-timezones"
        And we set the "tab" parameter to "day"
        And we set the "starting_hour" parameter to "6"
        And we set the "timezone" parameter to "Europe/London"
       When we look at <day>
        And we click on the event "Recurring Berlin Event"
       When we click on the div "Add to My Calendar"
       Then we download the file "<day> <time> Recurring Berlin Event.ics"

      Examples:
        | day        | time |
        | 2025-02-21 | 0700 |
        | 2025-02-22 | 0700 |
        | 2025-02-23 | 1445 |
