Feature: The calendar about page has a link to edit an existing calendar.
         This link leads to the configuration page where all the configured
         values are filled into the fields.

    Scenario Outline: I can see URLs filled into the configuration page.
      Given we set the "<parameter>" parameter to <value>
        And we are on the configuration page
       Then "<parameter>" is specified as <value>

      Examples:
        | parameter | value                               |
        | url       | ["http://url.com","https://url.de"] |
        | url       | ["url1","url2","url3","url4"]       |
        | url       | "http://url.com"                    |
        | language  | "de"                                |
        | language  | "es"                                |
        | title     | "New Cal!"                          |
