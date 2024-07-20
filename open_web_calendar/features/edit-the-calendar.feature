Feature: The calendar about page has a link to edit an existing calendar.
         This link leads to the configuration page where all the configured
         values are filled into the fields.

    Scenario Outline: I can see URLs filled into the configuration page.
      Given we set the "<parameter>" parameter to <value>
        And we are on the configuration page
       Then "<parameter>" is specified as <value>

      Examples:
        | parameter               | value                               |
        | url                     | ["http://url.com","https://url.de"] |
        | url                     | ["url1","url2","url3","url4"]       |
        | url                     | "http://url.com"                    |
        | language                | "de"                                |
        | language                | "es"                                |
        | title                   | "New Cal!"                          |
        | date                    | "2024-02-14"                        |
        | date                    | "2023-12-24"                        |
        | ending_hour             | "19"                                |
        | starting_hour           | "12"                                |
        | timezone                | "Asia/Kuala_Lumpur"                 |
        | timezone                | "America/Dawson"                    |
        | tab                     | "agenda"                            |
        | tab                     | "week"                              |
        | loader                  | ""                                  |
        | loader                  | "https://my-custom-loader.uk/l.gif" |
        | start_of_week           | "su"                                |
        | start_of_week           | "work"                              |
        | tabs                    | ["week","day"]                      |
        | tabs                    | ["month","agenda"]                  |
        | controls                | ["next","previous","today"]         |
        | controls                | ["date"]                            |
        | skin                    | "flat"          |
        | hour_division           | "2"                                 |
        | hour_format             | "%G:%i"                             |
        | hour_format             | "%g:%i%a"                           |
        | target                  | "_blank"                            |
        | target                  | "_self"                             |
        | custom-value            | "nanana!"                           |
        | css                     | ".test{/*css*/}"                    |
        | prefer_browser_language | true                                |
          
  Scenario: When I visit the configuration page, the configuration is
            almost empty.
    Given we are on the configuration page
     Then "hour_division" is not specified
     Then "date" is not specified
     Then "tab" is not specified

  Scenario: We want to edit the CSS properties
      Given we set the "css" parameter to ".test"
        And we are on the configuration page
       Then ".test" is written in "css-input"
       When we write "other-css" into "css-input"
       Then "css" is specified as "other-css"

  Scenario Outline: Checkboxes are not checked by default
      Given we are on the configuration page
       Then the checkbox with id "<id>" is not checked

    Examples:
      | id                           |
      | style-event-status-tentative |
      | style-event-status-confirmed |
      | style-event-status-cancelled |

  Scenario Outline: Checkboxes get checked when the parameter is set
      Given we set the "<id>" parameter to true
        And we are on the configuration page
       Then the checkbox with id "<id>" is checked
       When we click on the input with id "<id>"
       Then "<id>" is not specified
    Examples:
      | id                           |
      | style-event-status-tentative |
      | style-event-status-confirmed |
      | style-event-status-cancelled |

  Scenario: Skin values are translated from scheduler v6 to scheduler v7
    Given we set the "skin" parameter to "dhtmlxscheduler_contrast_black.css"
      And we are on the configuration page
      Then "skin" is specified as "contrast-black"

