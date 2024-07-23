Feature: The week days of the calendar can be configured.

    Scenario: View the week Mo-Su
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "mo"
         And we set the "tab" parameter to "week"
        When we look at 2024-01-18
        Then we can see the text "Mon 15"
         And we can see the text "Tue 16"
         And we can see the text "Wed 17"
         And we can see the text "Thu 18"
         And we can see the text "Fri 19"
         And we can see the text "Sat 20"
         And we can see the text "Sun 21"
         And we cannot see the text "Sun 14"


    Scenario: View the week Mo-Fr
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "work"
         And we set the "tab" parameter to "week"
        When we look at 2024-01-18
        Then we can see the text "Mon 15"
         And we can see the text "Tue 16"
         And we can see the text "Wed 17"
         And we can see the text "Thu 18"
         And we can see the text "Fri 19"
         And we cannot see the text "Sat"
         And we cannot see the text "Sun"

    Scenario: View the week Su-Mo
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "su"
         And we set the "tab" parameter to "week"
        When we look at 2024-01-18
        Then we can see the text "Sun 14"
         And we can see the text "Mon 15"
         And we can see the text "Tue 16"
         And we can see the text "Wed 17"
         And we can see the text "Thu 18"
         And we can see the text "Fri 19"
         And we can see the text "Sat 20"
         And we cannot see the text "Sun 21"

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

    Scenario: When I configure the week to be a work week and I skip through
              the days, I would like to skip Saturday and Sunday.
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "work"
         And we set the "tab" parameter to "day"
        When we look at 2024-03-08
        Then we can see the text "8 Mar 2024"
        When we click on >
        Then we can see the text "11 Mar 2024"
        When we click on <
        Then we can see the text "8 Mar 2024"

    Scenario Outline: I can navigate backwards and forwards with the arrows.
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "<week>"
         And we set the "tab" parameter to "<tab>"
        When we look at <date>
         And we click on <go>
        Then we can see the text "<text>"

       Examples:
         | week | tab   | date       | go | text                      |
         | work | month | 2024-03-04 | >  | April 2024                |
         | mo   | month | 2024-03-04 | >  | April 2024                |
         | su   | month | 2024-03-04 | >  | April 2024                |
         | work | month | 2024-03-04 | <  | February 2024             |
         | mo   | month | 2024-03-04 | <  | February 2024             |
         | su   | month | 2024-03-04 | <  | February 2024             |
         | work | week  | 2024-03-04 | >  | 11 Mar 2024 – 15 Mar 2024 |
         | mo   | week  | 2024-03-04 | >  | 11 Mar 2024 – 17 Mar 2024 |
         | su   | week  | 2024-03-04 | >  | 10 Mar 2024 – 16 Mar 2024 |
         | work | week  | 2024-03-04 | <  | 26 Feb 2024 – 1 Mar 2024  |
         | mo   | week  | 2024-03-04 | <  | 26 Feb 2024 – 3 Mar 2024  |
         | su   | week  | 2024-03-04 | <  | 25 Feb 2024 – 2 Mar 2024  |
         | work | day   | 2024-03-04 | >  | 5 Mar 2024                |
         | work | day   | 2024-03-05 | >  | 6 Mar 2024                |
         | work | day   | 2024-03-06 | >  | 7 Mar 2024                |
         | work | day   | 2024-03-07 | >  | 8 Mar 2024                |
         | work | day   | 2024-03-08 | >  | 11 Mar 2024               |
         | work | day   | 2024-03-04 | <  | 1 Mar 2024                |
         | work | day   | 2024-03-05 | <  | 4 Mar 2024                |
         | work | day   | 2024-03-06 | <  | 5 Mar 2024                |
         | work | day   | 2024-03-07 | <  | 6 Mar 2024                |
         | work | day   | 2024-03-08 | <  | 7 Mar 2024                |
         | su   | day   | 2024-03-04 | >  | 5 Mar 2024                |
         | su   | day   | 2024-03-05 | >  | 6 Mar 2024                |
         | su   | day   | 2024-03-06 | >  | 7 Mar 2024                |
         | su   | day   | 2024-03-07 | >  | 8 Mar 2024                |
         | su   | day   | 2024-03-08 | >  | 9 Mar 2024                |
         | su   | day   | 2024-03-09 | >  | 10 Mar 2024               |
         | su   | day   | 2024-03-10 | >  | 11 Mar 2024               |
         | su   | day   | 2024-03-06 | <  | 5 Mar 2024                |
         | su   | day   | 2024-03-07 | <  | 6 Mar 2024                |
         | su   | day   | 2024-03-08 | <  | 7 Mar 2024                |
         | su   | day   | 2024-03-09 | <  | 8 Mar 2024                |
         | su   | day   | 2024-03-10 | <  | 9 Mar 2024                |
         | su   | day   | 2024-03-11 | <  | 10 Mar 2024               |
         | su   | day   | 2024-03-12 | <  | 11 Mar 2024               |
         | mo   | day   | 2024-03-04 | >  | 5 Mar 2024                |
         | mo   | day   | 2024-03-05 | >  | 6 Mar 2024                |
         | mo   | day   | 2024-03-06 | >  | 7 Mar 2024                |
         | mo   | day   | 2024-03-07 | >  | 8 Mar 2024                |
         | mo   | day   | 2024-03-08 | >  | 9 Mar 2024                |
         | mo   | day   | 2024-03-09 | >  | 10 Mar 2024               |
         | mo   | day   | 2024-03-10 | >  | 11 Mar 2024               |
         | mo   | day   | 2024-03-06 | <  | 5 Mar 2024                |
         | mo   | day   | 2024-03-07 | <  | 6 Mar 2024                |
         | mo   | day   | 2024-03-08 | <  | 7 Mar 2024                |
         | mo   | day   | 2024-03-09 | <  | 8 Mar 2024                |
         | mo   | day   | 2024-03-10 | <  | 9 Mar 2024                |
         | mo   | day   | 2024-03-11 | <  | 10 Mar 2024               |
         | mo   | day   | 2024-03-12 | <  | 11 Mar 2024               |
