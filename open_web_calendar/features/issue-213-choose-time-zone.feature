Feature: We can choose to see the calendar in another time zone

    Scenario: When we go to the about page, we can select Europe/Berlin
       Given we add the calendar "one-event"
        When we look at 2019-03-04
         And we open the about page
        When we select "Europe/Berlin"
        Then we see 1 event
        Then we see that event "UYDQSG9TH4DE0WM3QFL2J" has the text "08:00 test1"

    Scenario: When we go to the about page, we can select Europe/London
       Given we add the calendar "one-event"
        When we look at 2019-03-04
         And we open the about page
        When we select "Europe/London"
        Then we see 1 event
        Then we see that event "UYDQSG9TH4DE0WM3QFL2J" has the text "07:00 test1"
