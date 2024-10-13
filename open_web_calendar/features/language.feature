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
