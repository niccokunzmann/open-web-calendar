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
      And we click on the event "Link with URLs"
     Then the link "Berlin" targets "<target>"

    Examples:
      | target |
      | _top   |
      | _blank |

  Scenario Outline: Links in the description should have the configured target.
    Given we add the calendar "issue-287-links-1"
      And we set the "target" parameter to "<config_target>"
     When we look at 2022-11-26
      And we click on the event "Holiday Craft Frenzy"
     Then the link "https://www.WalsworthCC.org/events/holiday-craft-frenzy" targets "<link_target>"

    Examples:
      | config_target | link_target |
      | _top          | _top        |
      | _blank        | _blank      |
      | iframe1       | iframe1     |

  Scenario: Links in the description should have the default target if no target is given.
    Given we add the calendar "issue-287-links-1"
     When we look at 2022-11-26
      And we click on the event "Holiday Craft Frenzy"
     Then the link "https://www.WalsworthCC.org/events/holiday-craft-frenzy" targets "_top"

  Scenario Outline: Links in the description replace the given target.
    Given we add the calendar "issue-287-links-1"
      And we set the "target" parameter to "<config_target>"
       And we set the "tab" parameter to "week"
     When we look at 2022-09-02
      And we click on the event "Grocery Grab 2"
     Then the link "https://www.DowntownMarceline.org/2022-grocery-grab" targets "<link_target>"
      And the link "https://www.DowntownMarceline.org/2022-grocery-grab" opens "https://www.google.com/url?q=https://www.DowntownMarceline.org/2022-grocery-grab&sa=D&source=calendar&ust=1662339011708338&usg=AOvVaw3IdHYp4Zpxv9ePQloSCoy6"

    Examples:
      | config_target | link_target |
      | _top          | _top        |
      | _blank        | _blank      |
      | iframe1       | iframe1     |

  Scenario Outline: HTML links with a description different to the URL also change the target if they are in the description.
    Given we add the calendar "issue-287-links-2"
      And we set the "target" parameter to "<target>"
     When we look at 2024-03-06
      And we click on the event "March 6, 1888 - City of Marceline is incorporated"
     Then the link "www.MarcelineHistory.org" targets "<target>"
      And the link "www.MarcelineHistory.org" opens "https://www.marcelinehistory.org/"

    Examples:
      | target |
      | _self  |
      | _blank |
