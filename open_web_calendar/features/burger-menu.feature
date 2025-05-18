Feature: We want to habe a menu to see more information about the calendar.

    Scenario: We choose the burger menu as
       Given we configure the menu
        When we click on the span "Show Menu"
        Then "controls" is specified as ["next", "previous", "today", "date", "menu"]

    Scenario Outline: We can see the menu, open and close it. So, we see more about the calendar.
        Given we set the "controls" parameter to "menu"
          And we add the calendar "rfc-7986-calendar"
          And we set the "<content_paremeter>" parameter to "<content>"
          And we set the "<show_parameter>" parameter to true
         When we look at 2025-01-16
         Then we cannot see the text "<content>"
         When we click on the menu
         Then we can see the text "<content>"
         When we click on the menu
         Then we cannot see the text "<content>"

      Examples:
        | show_parameter                   | content_paremeter | content                                                  |
        | menu_shows_title                 | title             | <a>My Calendar                                           |
        | menu_shows_description           | description       | This is a calendar                                       |
        | menu_shows_calendar_names        | x                 | RFC 7986 compatible calendar                             |
        | menu_shows_calendar_descriptions | x                 | This calendar is really nice. It even has a description! |

    Scenario Outline: We can see the menu, open and close it. We can hide information.
        Given we set the "controls" parameter to "menu"
          And we add the calendar "rfc-7986-calendar"
          And we set the "<show_parameter>" parameter to false
          And we set the "<content_paremeter>" parameter to "<content>"
         When we look at 2025-01-16
         Then we cannot see the text "<content>"
         When we click on the menu
         Then we cannot see the text "<content>"

      Examples:
        | show_parameter                   | content_paremeter | content                                                  |
        | menu_shows_title                 | title             | <a>My Calendar                                           |
        | menu_shows_description           | description       | This is a calendar                                       |
        | menu_shows_calendar_names        | x                 | RFC 7986 compatible calendar                             |
        | menu_shows_calendar_descriptions | x                 | This calendar is really nice. It even has a description! |

    Scenario Outline: We can configure the title in the menu.
       Given we configure the menu
        When we click on the span "<label>"
        Then "<spec>" is specified as <value>
      
      Examples:
        | label                      | spec                                  | value                    |
        | Show Title in Menu         | menu_shows_title                      | false                    |
        | Show Description in Menu   | menu_shows_description                | false                    |
        | List Calendar Names        | menu_shows_calendar_names             | false                    |
        | List Calendar Descriptions | menu_shows_calendar_descriptions      | true                     |
        | Hide/Show Calendars        | menu_shows_calendar_visibility_toggle | true                     |
    
    Scenario Outline: The calendar list items have the color of the calendars in the menu.
        Given we add the calendar "<calendar>"
          And we set the "controls" parameter to "menu"
          And we set the "menu_shows_calendar_descriptions" parameter to "true"
         When we look at 2025-01-16
          And we click on the menu
         Then "<text>" has the background-color "<background-color>"

        Examples:
            | calendar          | text                          | background-color |
            | rfc-7986-calendar | This calendar is really nice. | #e78074        |
            | rfc-7986-calendar | RFC 7986 compatible calendar  | #e78074        |
            # | food              | food                          | #0288D1        |

    Scenario: Calendars can be made invisible.
        Given we add the calendar "food"
          And we set the "controls" parameter to "menu"
          And we set the "menu_shows_calendar_visibility_toggle" parameter to "true"
         When we look at 2024-06-09
         Then we can see the text "Head"
         When we click on the menu
         Then we can see the text "Head"
         When we click on the label "food"
         Then we cannot see the text "Head" 

    Scenario: Usually calendars cannot be hidden.
        Given we add the calendar "food"
          And we set the "controls" parameter to "menu"
         When we look at 2024-06-09
         When we click on the menu
         When we click on the label "food"
         Then we can see the text "Head" 
