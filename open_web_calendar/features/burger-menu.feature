Feature: We want to habe a menu to see more information about the calendar.

    Scenario: We choose the burger menu as
       Given we configure the menu
        When we click on the span "Show Menu"
        Then "controls" is specified as ["next", "previous", "today", "date", "menu"]

    Scenario Outline: We can see the menu, open and close it. So, we see more about the calendar.
        Given we set the "controls" parameter to "menu"
          And we set the "<content_paremeter>" parameter to "<content>"
          And we set the "<show_parameter>" parameter to true
         When we look at 2025-01-16
         Then we cannot see the text "<content>"
         When we click on the menu
         Then we can see the text "<content>"
         When we click on the menu
         Then we cannot see the text "<content>"

      Examples:
        | show_parameter        | content_paremeter | content            |
        | menu_shows_title       | title             | <a>My Calendar     |
        | menu_shows_description | description       | This is a calendar |

    Scenario Outline: We can see the menu, open and close it. We can hide information.
        Given we set the "controls" parameter to "menu"
          And we set the "<show_parameter>" parameter to false
          And we set the "<content_paremeter>" parameter to "<content>"
         When we look at 2025-01-16
         Then we cannot see the text "<content>"
         When we click on the menu
         Then we cannot see the text "<content>"

      Examples:
        | show_parameter         | content_paremeter | content            |
        | menu_shows_title       | title             | <a>My Calendar     |
        | menu_shows_description | description       | This is a calendar |

    Scenario Outline: We can configure the title in the menu.
       Given we configure the menu
        When we click on the span "<label>"
        Then "<spec>" is specified as <value>
      
      Examples:
        | label                    | spec                     | value                    |
        | Show Title in Menu       | menu_shows_title         | false                    |
        | Show Description in Menu | menu_shows_description   | false                    |
    
    Scenario: We can configure the description in the menu.

    Scenario: We can configure the calendar titles in the menu.

    Scenario: We can configure the calendar descriptions in the menu.

    Scenario: The calendar list items have the color of the calendars in the menu.
