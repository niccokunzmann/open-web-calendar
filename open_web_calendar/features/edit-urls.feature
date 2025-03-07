Feature: I want to be able to edit URLs when they are added.

    Scenario: I add a URL to the list.
        Given we configure the urls
         When we write "http://localhost:8001/one-event.ics" into "add-url-url"
          And we click the button "Add"
         Then the link "http://localhost:8001/one-event.ics" opens "http://localhost:8001/one-event.ics"
          And the link "http://localhost:8001/one-event.ics" targets "_blank"
        #  When we click on the first button "✎"

    Scenario: When loaded the url field is empty
        Given we configure the urls
         Then "" is written in "add-url-url"

    Scenario: I edit a URL that was added from spec
        Given we set the "url" parameter to "http://my-url.com"
        Given we configure the urls
         Then the link "http://my-url.com" opens "http://my-url.com/"
         When we click on the button "Edit"
         Then "http://my-url.com/" is written in "add-url-url"

    Scenario: I edit a URL that I just added
        Given we configure the urls
         When we write "http://localhost:8001/one-event.ics" into "add-url-url"
          And we click the button "Add"
         When we write "nothing" into "add-url-url"
          And we click the button "Edit"
         Then "http://localhost:8001/one-event.ics" is written in "add-url-url"

    Scenario: I remove a URL
        Given we set the "url" parameter to "http://my-url.com"
          And we configure the urls
         When we click the button "Remove"
         Then "url" is not specified
          And we cannot see the text "http://my-url.com"

    Scenario: I edit username and password
        Given we configure the urls
         When we write "https://test:passlala@quelltext.ocloud.de/remote.php/dav/calendars/" into "add-url-url"
          And we click on the label "This is a public url"
         Then "test" is written in "add-url-username"
          And "passlala" is written in "add-url-password"
          And "https://quelltext.ocloud.de/remote.php/dav/calendars/" is written in "add-url-url"

    Scenario: By default we edit public urls
        Given we configure the urls
         Then the checkbox with id "add-url-credentials-checkbox" is checked
         When we click on the label "This is a public url"
         Then the checkbox with id "add-url-credentials-checkbox" is not checked

    Scenario: I edit a link with username and password
        Given we set the "url" parameter to "http://name:pass@link.to/a-calendar.ics"
          And we configure the urls
         When we click on the button "Edit"
          And we click on the label "This is a public url"
         Then "name" is written in "add-url-username"
          And "pass" is written in "add-url-password"
          And "http://link.to/a-calendar.ics" is written in "add-url-url"
         
         
    Scenario: I edit a URL that is encrypted and I do not have the password
        Given we enable encryption
          And we set the "url" parameter to "fernet://invalid-fernet"
          And we configure the urls
         When we click on the button "Edit"
         Then "fernet://invalid-fernet" is written in "add-url-url"
          And the checkbox with id "add-url-credentials-checkbox" is checked

    Scenario: I edit an encrypted URL that has credentials and I can see them
        Given we enable encyption
          And we set the "url" parameter to "fernet://gAAAAABnyxiJp_fC6MWkuR4dY5O-V45NgHHouWfmNVbi5WSXE0Y_v7VOEmhYIPflbH3zTCPyki5SIRwSqLRGIsihrkp2kratbF1Zug2I89t4u70OViXHGc8oAwBEmEL-Yvj7InLI37w4CiM3SC3dihbjjzJWxJZlOS79dasTcbyDCRdf6x7-6Vb0rPlQECQRZ2WZRS1ob6BnsYV7L6M4JTAq2Tk6opgJkF8ZUbfviQMT9wzlLekxgpQ="
          And we configure the urls
          And we click the button "Edit"
         Then "userme" is written in "add-url-username"
          And "passme" is written in "add-url-password"
          And "https://test.asd/cal" is written in "add-url-url"
