Feature: If we add calendars that do not work, we would like to see an error message.

    Scenario: When we load a broken calendar, we .
       Given we add the calendar "broken-calendar.html"
        When we look at 2019-03-04
        When we click the link "!"
        When we click on a link containing "broken-calendar.html"
        Then we can see the text "You should clean your HTML."

    Scenario: A calendar that does not exist but has a 404 page.
       Given we add the calendar "non-existing-calendar.js"
        When we look at 2019-03-04
        When we click the link "!"
        When we click on a link containing "non-existing-calendar.js"
        Then we can see the text "File not found."

    Scenario: A calendar to a URL that does not exist.
       Given we add the calendar "https://non-existing-calendar.js"
        When we look at 2019-03-04
        When we click the link "!"
        Then the link "https://non-existing-calendar.js" opens "https://non-existing-calendar.js/"

    Scenario: HTML of error messages is cleaned.
       Given we add the calendar "malicious-calendar.html"
        When we look at 2019-03-04
        When we click the link "!"
        Then we cannot see the text "Hacked!"
        Then we can see the text "<script>"

    Scenario: We cannot use file:// links.
       Given we add the calendar "file:///home/user/Documents/file.odt"
        When we look at 2019-03-04
        When we click the link "!"
        Then we can see the text "InvalidSchema"
