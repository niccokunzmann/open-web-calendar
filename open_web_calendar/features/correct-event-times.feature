Feature: The calendar shows the event times

    Scenario: show a calendar with one event
       Given we add the calendar "one-event"
        When we look at 2019-03-04
        Then we see 1 event

    Scenario: show a calendar with one event
       Given we add the calendar "one-event"
        When we look at 2019-03-04
        Then we see 1 event
        Then we see that event "UYDQSG9TH4DE0WM3QFL2J" has the text "10:00 test1"

    Scenario: remove the time from an event that lasts a day
       Given we add the calendar "one-day-event"
        When we look at 2019-03-04
        Then we see that event "UYDQSG9TH4DE0WM3QFL2J" has the text "test2"

    Scenario: Holidays last one day and should not have 0:00 in them!
       Given we add the calendar "german-holidays"
        When we look at 2023-01-01
        Then we see that event "636a08ed96ccc1667893485@calendarlabs.com" has the text "New Year's Day"
