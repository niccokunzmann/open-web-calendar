Feature: displaying calendar files

    Scenario: show a calendar with one event
       Given we add the calendar "one-event"
        When we look at 2019-03-04
        Then we see 1 event