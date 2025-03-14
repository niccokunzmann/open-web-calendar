Feature: We enable people to sign up to events.

    Scenario: Usually, I cannot see the signup button.

    Scenario: The calendar allows signing up to certain events.
       Given we set the "show_attendees" parameter to "true"
         And we set the "show_organizers" parameter to "true"
         And we set the "show_participant_role" parameter to "true"
         And we set the "show_participant_status" parameter to "true"
         And we set the "url" parameter to "https://test:oGbWK-tdbSB-bsRoC-jTjAB-3k6Bi@quelltext.ocloud.de/remote.php/dav/calendars/test/public/#can_add_email_attendee=true"
         And we set the "tab" parameter to "day"
        When we look at 2025-03-18
         And we click on the event "test event for sign up"
         And we click on the div "SIGN UP"
         And we write "niccokunzmann+test-signup@gmail.com" into "signup-email"
         And we clock the button "Sign Up"
         And we click on the event "test event for sign up"
         And we click on "Participants"
        Then the link "niccokunzmann+test-signup@gmail.com" opens "mailto:niccokunzmann+test-signup@gmail.com"

