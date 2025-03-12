Feature: I want to be able to see who is attending the event.

    Scenario: Normally, I cannot see who is attending.
        Given we add the calendar "issue-680-nextcloud"
         When we look at 2025-04-05
         Then we cannot see the text "Participants"
         When we click on the event "More People"
         Then we cannot see the text "Participants"

    Scenario: Only the organizer is visible.
        Given we add the calendar "issue-680-nextcloud"
          And we set the "show_organizers" parameter to "true"
         When we look at 2025-04-05
          And we click on the event "More People"
         When we click on the summary "Participants"
         Then the link "Test User" opens "mailto:niccokunzmann+test.quelltext.ocloud.de@gmail.com"
          And we cannot see the text "Nicco"

    Scenario: Only the attendees are visible.
        Given we add the calendar "issue-680-nextcloud"
          And we set the "show_attendees" parameter to "true"
         When we look at 2025-04-05
          And we click on the event "More People"
         When we click on the summary "Participants"
         Then the link "Nicco" opens "mailto:nicco@posteo.net"
          And we cannot see the text "Test User"
          And we can see the text "Yemaya"

    Scenario: We see all participants
        Given we add the calendar "issue-680-nextcloud"
          And we set the "show_attendees" parameter to "true"
          And we set the "show_organizers" parameter to "true"
         When we look at 2025-04-05
          And we click on the event "More People"
         When we click on the summary "Participants"
         Then the link "Test User" opens "mailto:niccokunzmann+test.quelltext.ocloud.de@gmail.com"
          And the link "Yemaya" opens "mailto:yemaya@posteo.net"

    Scenario Outline: If the event has no praticipants, I do not wat to be teased by an empty section.
        Given we add the calendar "one-event"
          And we set the "<parameter>" parameter to "true"
         When we look at 2019-03-04
          And we click on the event "test1"
         Then we cannot see the text "Participants"

      Examples:
        | parameter |
        | show_attendees |
        | show_organizers |