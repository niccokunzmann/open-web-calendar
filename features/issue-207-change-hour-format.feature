Feature: The clock convention can be changed from the 24 hour format to the 12 hour format.

    Scenario Outline: I view the calendar in the 24h format - this is the default.
      Given we add the calendar "one-event"
        And we set the "tab" parameter to "<tab>"
       When we look at 2024-01-18
       Then we can see the text "00:00"
        And we can see the text "12:00"
        And we can see the text "23:00"
        And we cannot see the text "pm"
        And we cannot see the text "PM"

     Examples:
       | tab  |
       | day  |
       | week |

    Scenario Outline: I view the calendar in the 24h format with no 0 at the start.
      Given we add the calendar "one-event"
        And we set the "tab" parameter to "<tab>"
        And we set the "hour_format" parameter to "%G:%i"
       When we look at 2024-01-18
       Then we can see the text "0:00"
        And we can see the text "12:00"
        And we can see the text "23:00"
        And we cannot see the text "00:00"

     Examples:
       | tab  |
       | day  |
       | week |

    Scenario Outline: I view the calendar in the 12h format.
      Given we add the calendar "one-event"
        And we set the "tab" parameter to "<tab>"
        And we set the "hour_format" parameter to "%g:%i %a"
       When we look at 2024-01-18
       Then we can see the text "12:00 am"
        And we can see the text "12:00 pm"
        And we can see the text "11:00 pm"
        And we cannot see the text "13:00"

     Examples:
       | tab  |
       | day  |
       | week |
