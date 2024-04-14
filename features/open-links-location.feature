Feature: I would like to choose where links open.

  Scenario: I want to open links on the calendar page in a new tab.
    Given we add the calendar "event-with-html-markup"
      And we set the "target" parameter to "_blank"
     When we look at 2024-04-14
     Then the link "?" targets "_blank"

  Scenario Outline: I want to configure how to open the link to the map.
    Given we add the calendar "event-with-html-markup"
      And we set the "target" parameter to "<target>"
     When we look at 2024-04-14
     Then the link "Berlin" targets "<target>"

    Examples:
      | target |
      | _top   |
      | _blank |

  Scenario Outline: Links in the description should have the configured target.
    Given we add the calendar "issue-287-links-1"
      And we set the "target" parameter to "<target>"
     When we look at 2022-11-26
     Then the link "https://www.WalsworthCC.org/events/holiday-craft-frenzy" targets "<target>"

    Examples:
      | config_target | link_target |
      |               | _top        |
      | _blank        | _blank      |
      | iframe1       | iframe1     |

  Scenario Outline: Links in the description replace the given target.
    Given we add the calendar "issue-287-links-1"
      And we set the "target" parameter to "<target>"
     When we look at 2022-09-02
     Then the link "https://www.DowntownMarceline.org/2022-grocery-grab" targets "<target>"
      And the link "https://www.DowntownMarceline.org/2022-grocery-grab" opens "https://www.google.com/url?q=https://www.DowntownMarceline.org/2022-grocery-grab&amp;sa=D&amp;source=calendar&amp;ust=1662339011708338&amp;usg=AOvVaw3IdHYp4Zpxv9ePQloSCoy6"

    Examples:
      | config_target | link_target |
      |               | _top        |
      | _blank        | _blank      |
      | iframe1       | iframe1     |

  Scenario Outline: HTML links with a description different to the URL also change the target if they are in the description.
    Given we add the calendar "issue-287-links-2"
      And we set the "target" parameter to "<target>"
     When we look at 2024-03-01
     Then the link "www.MarcelineHistory.org" targets "<target>"
      And the link "www.MarcelineHistory.org" opens "www.MarcelineHistory.org"

    Examples:
      | config_target | link_target |
      | _self         | _self       |
      | _blank        | _blank      |

  Scenario Outline: When I attach a URL to an event, this url is also opening in the target location.
    Given we add the calendar "event-with-html-markup"
      And we set the "target" parameter to "<config_target>"
     When we look at 2024-04-14
     Then the link "http://open-web-web-calendar.quelltext.eu/" targets "<link_target>"
      And the link "http://open-web-web-calendar.quelltext.eu/" opens "http://open-web-web-calendar.quelltext.eu/"

    Examples:
      | config_target | link_target |
      |               | _top        |
      | _self         | _self       |
      | _blank        | _blank      |
