Feature: We enable people to sign up to events.

    Scenario: Usually, I cannot see the signup button.
        Given we add the calendar "issue-23-location-berlin"
         When we look at 2025-01-10
          And we click on the event "Event in Berlin!"
         Then we cannot see the text "Sign Up"
          And we cannot see the text "SIGN UP"

    Scenario: The calendar allows signing up to certain events.
       Given we load the api recording "issue-680-sign-up-for-event"
         And we set the "show_attendees" parameter to "true"
         And we set the "show_organizers" parameter to "true"
         And we set the "show_participant_role" parameter to "true"
         And we set the "show_participant_status" parameter to "true"
         And we set the "url" parameter to "https://test:oGbWK-tdbSB-bsRoC-jTjAB-3k6Bi@quelltext.ocloud.de:443/remote.php/dav/calendars/test/public/#can_add_email_attendee=true"
         And we set the "tab" parameter to "day"
        When we look at 2025-03-18
         And we click on the event "test event for sign up"
         And we click on the div "Sign Up"
         And we write "niccokunzmann+test-signup@gmail.com" into "signup-email"
         And we click the button "Sign Up"
         And we wait for the loader to disappear
         And we click on the event "test event for sign up"
        When we click on the summary "Participants"
        Then the link "niccokunzmann+test-signup@gmail.com" opens "mailto:niccokunzmann+test-signup@gmail.com"

