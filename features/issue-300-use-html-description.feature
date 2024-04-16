Feature: I would like to use the HTML style of the event if given.

  Scenario Outline: When I attach a URL to an event, this url is also opening in the target location.
    Given we add the calendar "event-with-html-markup"
      And we set the "target" parameter to "<config_target>"
     When we look at 2024-04-14
      And we click on the event "Link with URLs"
     Then the link "http://open-web-web-calendar.quelltext.eu/" targets "<link_target>"
      And the link "http://open-web-web-calendar.quelltext.eu/" opens "http://open-web-web-calendar.quelltext.eu/"

    Examples:
      | config_target | link_target |
      |               | _top        |
      | _self         | _self       |
      | _blank        | _blank      |
