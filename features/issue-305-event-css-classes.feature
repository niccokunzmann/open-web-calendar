Feature: I would like to be able to style the events based on their values.

    Scenario: We can see a calendar event with the event class.
       Given we add the calendar "one-event"
         And we set the "start_of_week" parameter to "mo"
         And we set the "tab" parameter to "week"
        When we look at 2019-03-04
        Then we can see an event with UID "UYDQSG9TH4DE0WM3QFL2J" with css class "event"
         And we can see an event with UID "UYDQSG9TH4DE0WM3QFL2J" with css class "UID-UYDQSG9TH4DE0WM3QFL2J"

    Scenario Outline: We can style categories.
      Given we add the calendar "event-with-categories"
        And we set the "tab" parameter to "week"
       When we look at 2023-03-04
       Then we can see an event with UID "UYDQSG9TH4DE0WM3QFL2J-2" with css class "CATEGORY-APPOINTMENT"
       Then we can see an event with UID "UYDQSG9TH4DE0WM3QFL2J" with css class "CATEGORY-EDUCATION"

      Examples:
        | tab    |
        | week   |
        | agenda |
        | day    |
        | month  |

    Scenario: Events of a calendar have css classes
      Given we add the calendar "event-with-categories"
        And we add the calendar "one-day-event"
        And we set the "tab" parameter to "week"
       When we look at 2023-03-04
       Then we can see an event with UID "UYDQSG9TH4DE0WM3QFL2J" with css class "CALENDAR-INDEX-0"

    Scenario: Events of different calendars have different classes depending on their index
      Given we add the calendar "event-with-categories"
        And we add the calendar "one-day-event"
        And we set the "tab" parameter to "month"
       When we look at 2019-03-04
       Then we can see an event with UID "UYDQSG9TH4DE0WM3QFL2J" with css class "CALENDAR-INDEX-1"
