Feature: The calendar about page has a link to edit an existing calendar.
         This link leads to the configuration page where all the configured
         values are filled into the fields.

    Scenario Outline: I can see URLs filled into the configuration page.
      Given we set the "<parameter>" parameter to <value>
        And we are on the configuration page
       Then "<parameter>" is specified as <value>

      Examples:
        | parameter     | value                               |
        | url           | ["http://url.com","https://url.de"] |
        | url           | ["url1","url2","url3","url4"]       |
        | url           | "http://url.com"                    |
        | language      | "de"                                |
        | language      | "es"                                |
        | title         | "New Cal!"                          |
        | date          | "2024-02-14"                        |
        | date          | "2023-12-24"                        |
        | ending_hour   | "19"                                |
        | starting_hour | "12"                                |
        | timezone      | "Asia/Kuala_Lumpur"                 |
        | timezone      | "America/Dawson"                    |
        | tab           | "agenda"                            |
        | tab           | "week"                              |
        | loader        | ""                                  |
        | loader        | "https://my-custom-loader.uk/l.gif" |
        | start_of_week | "su"                                |
        | start_of_week | "work"                              |
        | tabs          | ["week","day"]                      |
        | tabs          | ["month","agenda"]                  |
        | controls      | ["next","previous","today"]         |
        | controls      | ["date"]                            |
        | skin          | "dhtmlxscheduler_flat.css"          |
        | hour_division | "2"                                 |
        | hour_format   | "%G:%i"                             |
        | hour_format   | "%g:%i%a"                           |
        | target        | "_blank"                            |
        | target        | "_self"                             |
