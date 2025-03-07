Feature: I want to be able to load CalDAV calendars.

    Scenario: I view a calendar with a CalDAV URL
      Given we set the "url" parameter to "https://test:oGbWK-tdbSB-bsRoC-jTjAB-3k6Bi@quelltext.ocloud.de/remote.php/dav/calendars/test/public/"
        And we load the api recording "issue-189-caldav-test-calendar"
       When we look at 2025-03-05
       Then we can see the event "Weekly Event"
        And we can see the event "another weekly event"

    Scenario: I want to insert a CalDAV URL and choose the calendar.
      Given we load the api recording "issue-189-choose-calendars"
        And we configure the urls
       When we write "https://test:oGbWK-tdbSB-bsRoC-jTjAB-3k6Bi@quelltext.ocloud.de/remote.php/dav/calendars/" into "add-url-url"
        And we choose "public" in "add-url-calendars"
        And we click the button "Add"
       Then "url" is specified as "https://test:oGbWK-tdbSB-bsRoC-jTjAB-3k6Bi@quelltext.ocloud.de:443/remote.php/dav/calendars/test/public/"
