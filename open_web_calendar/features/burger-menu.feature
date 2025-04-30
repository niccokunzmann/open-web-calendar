Feature: We want to habe a menu to see more information about the calendar.

    Scenario: We choose the burger menu as
       Given we configure the tabs
        When we click on the span "Burger Menu"
        Then "controls" is specified as ["next", "previous", "today", "date", "menu"]

    Scenario: We can see the menu, open and close it. So, we see more about the calendar.
        Given we add the calendar "issue-23-location-berlin"
          And we set the "controls" parameter to "menu"
          And we set the "title" parameter to "My Calendar"
         When we look at 2025-01-16
         Then we cannot see the text "My Calendar"
         When we click on the menu
         Then we can see the text "My Calendar"
         When we click on the menu
         Then we cannot see the text "My Calendar"

    Scenario: We can configure the title in the menu.
    
    Scenario: We can configure the description in the menu.

    Scenario: We can configure the calendar titles in the menu.

    Scenario: We can configure the calendar descriptions in the menu.

    Scenario: The calendar list items have the color of the calendars in the menu.
