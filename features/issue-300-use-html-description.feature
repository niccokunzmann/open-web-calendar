Feature: I would like to use the HTML style of the event if given.

  Scenario Outline: The links of HTML styled event descriptions change the target.
    Given we add the calendar "event-with-html-markup"
      And we set the "target" parameter to "<target>"
     When we look at 2024-04-14
      And we click on the event "Link with URLs"
     Then the link "Examples" targets "<target>"
      And the link "Examples" opens "https://open-web-calendar.quelltext.eu/templates/"

    Examples:
      | target |
      | _self  |
      | _blank |
