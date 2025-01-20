Feature: The calendar is translated into different languages. We want to
         Be able to choose languages.

    Scenario Outline: I would like to use the configuration page in different languages.
      Given we are on the configuration page
       Then we cannot see the text "<word>"
       When we click on a link containing "<language>"
       Then we can see the text "<word>"

      Examples:
        | word        | language |
        | calendrier  | French   |
        | Kalender    | Deutsch  |
        | calendarios | Español  |

    Scenario Outline: When I set the language parameter, the calendar changes its language.
      Given we add the calendar "event-with-html-markup"
        And we set the "language" parameter to "<language>"
       When we look at 2024-04-14
       Then we can see the text "<word>"

      Examples:
        | word   | language |
        | MONTH  | en       |
        | MONAT  | de       |
        | ДЕНЬ   | ru       |
