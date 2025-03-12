Feature: The calendar has a configuration page that displays and changes the
         calendar along with its specification.

    Scenario: The default specification is almost empty.
       Given we load the api recording "with-no-content"
         And we configure the urls
        When we write "https://localhost:12345/example.ics" into "add-url-url"
         And we click the button "Add"
        Then "url" is specified as "https://localhost:12345/example.ics"

    Scenario: We can specify two URLs.
       Given we load the api recording "with-no-content"
         And we configure the urls
        When we write "https://localhost:12345/example.ics" into "add-url-url"
         And we click the button "Add"
         And we write "https://localhost/example.ics" into "add-url-url"
         And we click the button "Add"
        Then "url" is specified as ["https://localhost:12345/example.ics","https://localhost/example.ics"]

    Scenario: We choose a title for our calendar.
       Given we configure the title
        When we write "My Family Calendar" into "calendar-title"
        Then "title" is specified as "My Family Calendar"

    Scenario: We choose the date which the calendar displays
       Given we configure the starting-date
        When we write the date 14/02/2024 into "starting-date"
        Then "date" is specified as "2024-02-14"

    Scenario: We choose the start and end hour
       Given we configure the time-and-hour
        When we write "6" into "starting-hour"
         And we write "19" into "ending-hour"
        Then "ending_hour" is specified as "19"
         And "starting_hour" is specified as "6"

    Scenario: We choose a time zone to display
       Given we configure the timezone
        When we choose "Europe/London" in "select-timezone"
        Then "timezone" is specified as "Europe/London"

    Scenario: We choose the tab to display
       Given we configure the tabs
        When we choose "Week" in "select-tab"
        Then "tab" is specified as "week"
        When we choose "Day" in "select-tab"
        Then "tab" is specified as "day"
        When we choose "Agenda" in "select-tab"
        Then "tab" is specified as "agenda"

    Scenario: We choose the loader
       Given we configure the loader
        When we choose "no loader" in "select-loader"
        Then "loader" is specified as ""

    Scenario: We choose the days of the week
       Given we configure the week
        When we choose "Sunday - Saturday" in "select-start-of-week"
        Then "start_of_week" is specified as "su"
        When we choose "Monday - Friday" in "select-start-of-week"
        Then "start_of_week" is specified as "work"

    Scenario: We choose the calendar tabs
       Given we configure the tabs
        When we click on the span "Month"
        Then "tabs" is specified as ["week","day"]
        When we click on the span "Week"
        Then "tabs" is specified as ["day"]
        When we click on the span "Day"
        Then "tabs" is specified as []
        When we click on the span "Agenda"
        Then "tabs" is specified as ["agenda"]

    Scenario: We choose which controls are visible
       Given we configure the tabs
        When we click on the span "Date"
        Then "controls" is specified as ["next","previous","today"]
        When we click on the span "Previous"
        Then "controls" is specified as ["next","today"]
        When we click on the span "Today"
        Then "controls" is specified as ["next"]
        When we click on the span "Next"
         And we click on the span "Date"
        Then "controls" is specified as ["date"]

    Scenario: We choose the designs
       Given we configure the skins
        When we choose "Flat" in "select-skin"
        Then "skin" is specified as "flat"

    Scenario: We choose to divide the hours
       Given we configure the time-and-hour
        When we click on the span "10 minutes"
        Then "hour_division" is specified as "6"
        When we click on the span "15 minutes"
        Then "hour_division" is specified as "4"
        When we click on the span "30 minutes"
        Then "hour_division" is specified as "2"
        When we click on the span "1 hour"
        Then "hour_division" is not specified

    Scenario: We choose the language of the calendar
       Given we configure the languages
        When we choose "Cymraeg (cy)" in "select-language"
        Then "language" is specified as "cy"

    Scenario Outline: Checkboxes can be checked
       Given we configure the event-status
        Then "<id>" is not specified
        When we click on the span "<name>"
        Then "<id>" is specified as true

      Examples:
        | name      | id                           |
        | tentative | style-event-status-tentative |
        | confirmed | style-event-status-confirmed |
        | cancelled | style-event-status-cancelled |

    Scenario: By default we display the calendar in one language
       Given we configure the languages
        Then the checkbox with id "prefer_browser_language_false" is checked
         And the checkbox with id "prefer_browser_language_true" is not checked
         And "prefer_browser_language" is not specified

    Scenario: We can choose to display the calendar in the language of the viewer
       Given we configure the languages
        When we click on the span "The calendar is in the language of the viewer."
        Then the checkbox with id "prefer_browser_language_false" is not checked
         And the checkbox with id "prefer_browser_language_true" is checked
         And "prefer_browser_language" is specified as true

    Scenario: By default we display the calendar in the language of the viewer
       Given we configure the languages
        When we click on the span "The calendar is in the language of the viewer."
         And we click on the span "The calendar is always in this language:"
        Then "prefer_browser_language" is not specified

    Scenario: By default, we do not see participants.
       Given we configure the participants
        Then "show_organizers" is not specified
        Then "show_attendees" is not specified
        Then "show_participant_status" is not specified
        Then "show_participant_type" is not specified
        Then "show_participant_role" is not specified

     Scenario Outline: We change the visibility
       Given we configure the participants
        When we click on the span "<label>"
        Then "<spec>" is specified as true
      
      Examples:
        | label                  | spec                    |
        | who organizes          | show_organizers         |
        | who attends            | show_attendees          |
        | status of participants | show_participant_status |
        | individual             | show_participant_type   |
        | role                   | show_participant_role   |
