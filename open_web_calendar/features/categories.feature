Feature: The calendar show the categories of the events

    Scenario: show a calendar with one event
       Given we add the calendar "event-with-categories"
        When we look at 2023-03-04
        Then we cannot see the text "| APPOINTMENT | EDUCATION |"
        When we click on the event "event with categories"
        Then we can see the text "| APPOINTMENT | EDUCATION |"

    Scenario: show a calendar with one event that lasts a day
       Given we add the calendar "event-with-categories"
        When we look at 2023-03-04
        Then we cannot see the text "| APPOINTMENT | EDUCATION |"
        When we click on the event "day with categories"
        Then we can see the text "| APPOINTMENT | EDUCATION |"
