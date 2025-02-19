Feature: I would like to be able to subscribe to an event, a series of events or the whole calendar.

    Scenario: I add an event to my own calendar.
      Given we add the calendar "food"
        And we set the "tab" parameter to "day"
       When we look at 2024-03-22
        And we click on the event "Head Start Menu (ages 3-5)"
       When we click on the div "Add to My Calendar"
       Then we download the file "2024-03-22 Head Start Menu (ages 3-5).ics"

        
