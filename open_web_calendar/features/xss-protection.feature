Feature: Calendars and URLs can contain JavaScript content and HTML. We want to make sure that XSS attacks are not possible.

    Scenario: I set an invalid URL to JavaScript
        Given we open the url from issue 563
         Then we cannot see the text "hacked"
  
    Scenario: I can set JavaScript links in URLs.
        Given we set the "url" parameter to "javascript:document.body.innerText='hacked'"
          When we look at 2025-01-24
          And we click on the link "!"
          And we click on the first link "javascript:document.body.innerText='hacked'"
         Then we can see the text "javascript:"