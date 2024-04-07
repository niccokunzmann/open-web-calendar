Feature: Content can be crafted to add scripts and such to the calendar. We want to block those.

    Scenario: We load a valid calendar with bad HTML.
       Given we add the calendar "malicious"
        When we look at 2019-03-04
        Then we cannot find an XPATH "//maliciouscalname"
        Then we cannot find an XPATH "//maliciouscolor"
        Then we cannot find an XPATH "//maliciousuid"
        Then we cannot find an XPATH "//malicioussummary"
        Then we cannot find an XPATH "//maliciousdescription"
        When we click on the event ">event!"
        Then we cannot find an XPATH "//maliciousdescription"
        Then we cannot find an XPATH "//maliciouslocation"
        Then we cannot find an XPATH "//maliciouscategory"
