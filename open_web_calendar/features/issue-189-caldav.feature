Feature: I want to be able to load CalDAV calendars.

    Scenario: I view a calendar with a CalDAV URL
      Given we set the "url" parameter to "https://test:oGbWK-tdbSB-bsRoC-jTjAB-3k6Bi@quelltext.ocloud.de/remote.php/dav/calendars/test/public/"
        And we load the api recording "issue-189-caldav-test-calendar"
       When we look at 2025-03-05
       Then we can see the event "Weekly Event"
        And we can see the event "another weekly event"
