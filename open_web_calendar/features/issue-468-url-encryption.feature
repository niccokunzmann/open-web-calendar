Feature: In order to protect credentials, I want to encrypt URls.

    Scenario: If encryption is not enabled, I do not want to see related features.
        Given we are on the configuration page
         Then we cannot see the text "✅ Encrypted"
         Then we cannot see the text "Encrypt URL"

    Scenario: If encryption is enabled, I want to be able to encrypt URLs.
        Given we enable encryption
          And we are on the configuration page
         Then we can see the text "Encrypt URL"

    Scenario: When I encrypt a URL, I get visual feedback.
        Given we add the calendar "gancio.antroposofiachile.net.ics"
          And we enable encryption
          And we are on the configuration page
         Then we cannot see the text "✅ Encrypted"
         When we click on the first button "Encrypt URL"
         Then we can see the text "✅ Encrypted"

    Scenario: I cannot encrypt an empty URL.
        Given we enable encryption
          And we are on the configuration page
         Then we cannot see the text "✅ Encrypted"
         When we click on the button "Encrypt URL"
         Then we cannot see the text "✅ Encrypted"

    Scenario: I can view the encrypted URL's content.
        Given we enable encryption
          And we set the "url" parameter to "fernet://gAAAAABnxNJ-uR0tW9UumJLvRB8UYNRxFstIdXu6Mwr2JiEsK98dq_1-oVv6AtRV3pfl67bDehGrrMimbGqHhYL74bZe_VP9Wxu8ouwa0Hhf2G6UJ6z3Sdvyl5xLMiZx7ItzST-yZU7e"
         When we look at 2019-03-04
         Then we can see the text "test1"
         