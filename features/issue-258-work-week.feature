Feature: The week days of the calendar can be configured.

    Scenario: View the week Mo-Su
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "mo"
         And we set the "tab" parameter to "week"
        When we look at 2024-01-18
        Then we can see the text "Mon, January 15"
         And we can see the text "Tue, January 16"
         And we can see the text "Wed, January 17"
         And we can see the text "Thu, January 18"
         And we can see the text "Fri, January 19"
         And we can see the text "Sat, January 20"
         And we can see the text "Sun, January 21"
         And we cannot see the text "Sun, January 14"


    Scenario: View the week Mo-Fr
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "work"
         And we set the "tab" parameter to "week"
        When we look at 2024-01-18
        Then we can see the text "Mon, January 15"
         And we can see the text "Tue, January 16"
         And we can see the text "Wed, January 17"
         And we can see the text "Thu, January 18"
         And we can see the text "Fri, January 19"
         And we cannot see the text "Sat"
         And we cannot see the text "Sun"

    Scenario: View the week Su-Mo
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "su"
         And we set the "tab" parameter to "week"
        When we look at 2024-01-18
        Then we can see the text "Sun, January 14"
         And we can see the text "Mon, January 15"
         And we can see the text "Tue, January 16"
         And we can see the text "Wed, January 17"
         And we can see the text "Thu, January 18"
         And we can see the text "Fri, January 19"
         And we can see the text "Sat, January 20"
         And we cannot see the text "Sun, January 21"

    Scenario: View the week Mo-Fr on the month view
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "work"
        When we look at 2024-01-18
        Then we can see the text "Monday"
         And we can see the text "Tuesday"
         And we can see the text "Wednesday"
         And we can see the text "Thursday"
         And we can see the text "Friday"
         And we cannot see the text "Saturday"
         And we cannot see the text "Sunday"

    Scenario: View the week Mo-Su on the month view
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "mo"
        When we look at 2024-01-18
        Then we can see the text "Monday"
         And we can see the text "Tuesday"
         And we can see the text "Wednesday"
         And we can see the text "Thursday"
         And we can see the text "Friday"
         And we can see the text "Saturday"
         And we can see the text "Sunday"
