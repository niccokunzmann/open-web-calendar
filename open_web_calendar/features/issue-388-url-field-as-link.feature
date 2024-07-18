Feature: I would like to open links to the events.

  Scenario: When I view a calendar event that has a URL set, I can click the title and reach the page that I would like to see.
    Given we add the calendar "gancio.antroposofiachile.net.ics"
     When we look at 2024-06-01
      And we click on the event "El Significado Espiritual de las Envolturas Embrionarias a la Luz de la Antroposofía"
     Then the link "🔗 El Significado Espiritual de las Envolturas Embrionarias a la Luz de la Antroposofía" opens "https://gancio.antroposofiachile.net/event/el-significado-espiritual-de-las-envolturas-embrionarias-a-la-luz-de-la-antroposofia"

  Scenario Outline: I want links to events to open as configured, e.g. in a new tab.
    Given we add the calendar "gancio.antroposofiachile.net.ics"
      And we set the "target" parameter to "<target>"
      When we look at 2024-06-01
       And we click on the event "El Significado Espiritual de las Envolturas Embrionarias a la Luz de la Antroposofía"
      Then the link "🔗 El Significado Espiritual de las Envolturas Embrionarias a la Luz de la Antroposofía" targets "<target>"

    Examples:
      | target |
      | _top   |
      | _blank |
