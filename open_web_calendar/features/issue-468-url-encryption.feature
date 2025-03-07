Feature: In order to protect credentials, I want to encrypt URls.

    Scenario: If encryption is not enabled, I do not want to see related features.
        Given we load the api recording "with-no-content"
          And we configure the urls
         Then we cannot see the text "Decrypt URLs"
          And we cannot see the text "We recommend encrypting"

    Scenario: If encryption is enabled, I want to be able to encrypt URLs.
        Given we load the api recording "with-no-content"
          And we enable encryption
          And we configure the urls
         Then we can see the text "We recommend encrypting"
          And we can see the text "Decrypt URLs"
         

    Scenario: When I encrypt a URL, I get visual feedback.
        Given we load the api recording "with-no-content"
          And we add the calendar "gancio.antroposofiachile.net.ics"
          And we enable encryption
          And we configure the urls
         Then we cannot see the text "Encrypted"
         When we click on the first button "Encrypt URL"
         Then we can see the text "Encrypted"

    Scenario: I cannot encrypt an encrypted URL.
        Given we load the api recording "with-no-content"
          And we enable encryption
          And we configure the urls
         Then we cannot see the text "Encrypted"
         When we write "fernet://gAAAAABnxNJ-uR0tW9UumJLvRB8UYNRxFstIdXu6Mwr2JiEsK98dq_1-oVv6AtRV3pfl67bDehGrrMimbGqHhYL74bZe_VP9Wxu8ouwa0Hhf2G6UJ6z3Sdvyl5xLMiZx7ItzST-yZU7e" into "add-url-url"
         When we click the button "Add"
         Then we can see the text "Encrypted"

    Scenario: I can view the encrypted URL's content.
        Given we load the api recording "with-no-content"
          And we enable encryption
          And we set the "url" parameter to "fernet://gAAAAABnxNJ-uR0tW9UumJLvRB8UYNRxFstIdXu6Mwr2JiEsK98dq_1-oVv6AtRV3pfl67bDehGrrMimbGqHhYL74bZe_VP9Wxu8ouwa0Hhf2G6UJ6z3Sdvyl5xLMiZx7ItzST-yZU7e"
         When we look at 2019-03-04
         Then we can see the text "test1"
        
    Scenario: I want to be able to see the password
        Given we load the api recording "with-no-content"
          And we enable encryption
          And we configure the urls
         When we write "myP4ssphraz3" into "encryption-password"
          And we click on the button with id "toggle-password-visibility"
         Then we can see the password

    Scenario: I cannot see the password by default.
        Given we load the api recording "with-no-content"
          And we enable encryption
          And we configure the urls
         When we write "myP4ssphraz3" into "encryption-password"
         Then we cannot see the password

    Scenario: The encryption password is randomly generated if not entered.
        Given we load the api recording "with-no-content"
          And we enable encryption
          And we configure the urls
         Then "" is not written in "encryption-password"
    
    Scenario: When I reload the page, I do not want to see my password.
        Given we load the api recording "with-no-content"
          And we enable encryption
          And we configure the urls
         When we write "myP4ssphraz3" into "encryption-password"
         Then "myP4ssphraz3" is written in "encryption-password"
         When we reload the page
         Then "myP4ssphraz3" is not written in "encryption-password"

    Scenario: I want to use a password to decrypt the url.
        Given we load the api recording "with-no-content"
          And we enable encryption
          And we set the "url" parameter to "fernet://gAAAAABnxeBLuaiwUtEojjmamNedri09-39WgQ8D7VdlNE336pQRDJZIEdok7rCfZDsaZ4lCtk_2SsZ8ug-UYRUaHUwamEEShssL9zf8HAXfSCuo1yfLWvIFrJEVnhNLwcX849Rjxiz-xG6bnf9ZcG6tOxRFs9QtdrGl5e31M8MyhhwdK0UTKolImmoq6cgJ7KKz2e0gbBBvcojthmzqGq0anmEFwMnbaatPO4AdFm8_rjXXFPi_ULp5ZvyofWwNKUh8Op5xy0oajC1-Izg_OJcixKZPoyNAVw=="
          And we configure the urls
         When we write "0xquba6f" into "encryption-password"
          And we click the button "Decrypt URLs"
        Then "url" is specified as "https://www.calendarlabs.com/ical-calendar/ics/46/Germany_Holidays.ics"

    Scenario: I cannot decrypt with the wrong password.
        Given we load the api recording "with-no-content"
          And  we enable encryption
          And we set the "url" parameter to "fernet://gAAAAABnxZUaid25bXTHwqEPuQY0Hflx36PPYuM5DnPSzEw75xL_DfU3Mp1rlLQWJDXhruBI7tqRwX9hY1J-dFQSFBUKkXm1MFIHIc5WJ8R_HXdQEC3ty2Bwk48O_CZgkF9gX-qdmHwLHcxsePN-3-JJ_t9r9bVQ5rrh09sg_eANLjJpqQiI9YLP_u2eo2WAEK-aGkOy-MmwNzk0QeRkgfxs10yJVpcjFudO4Mxizq2Nyy8664xpXc3VV52M_KMDBtmiTHEYQdCrHwsXLVqc8vUtjnfHl_vsb_w3dSe0ZNC44VxkxwN60OcKX8jtBUc5WXyMK3yu7FOLoJ69VzorhPYjt7t9phvTsv3Ghd-wzvWxPy17hPfsJGihSkUVHkQg2f4Hdq_-NzoZvb-JCaTnILRNsZtSrOa8nTpMY6BUA_boj1JR3RUZn4E="
          And we configure the urls
         When we write "wrong password" into "encryption-password"
          And we click the button "Decrypt URLs"
        Then "url" is specified as "fernet://gAAAAABnxZUaid25bXTHwqEPuQY0Hflx36PPYuM5DnPSzEw75xL_DfU3Mp1rlLQWJDXhruBI7tqRwX9hY1J-dFQSFBUKkXm1MFIHIc5WJ8R_HXdQEC3ty2Bwk48O_CZgkF9gX-qdmHwLHcxsePN-3-JJ_t9r9bVQ5rrh09sg_eANLjJpqQiI9YLP_u2eo2WAEK-aGkOy-MmwNzk0QeRkgfxs10yJVpcjFudO4Mxizq2Nyy8664xpXc3VV52M_KMDBtmiTHEYQdCrHwsXLVqc8vUtjnfHl_vsb_w3dSe0ZNC44VxkxwN60OcKX8jtBUc5WXyMK3yu7FOLoJ69VzorhPYjt7t9phvTsv3Ghd-wzvWxPy17hPfsJGihSkUVHkQg2f4Hdq_-NzoZvb-JCaTnILRNsZtSrOa8nTpMY6BUA_boj1JR3RUZn4E="
