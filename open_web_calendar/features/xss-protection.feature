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
    
    Scenario: The calendar provides JS in an event URL and we replace it with #
        Given we add the calendar "xss-event-js-url"
         When we look at 2025-01-24
          And we click on the event "the event url has a JS link"
         Then the link "🔗 the event url has a JS link" opens nothing

    Scenario: The calendar provides JS in an event LOCATION and we replace it with #
        Given we add the calendar "xss-event-js-url"
         When we look at 2025-01-25
          And we click on the event "the event location has a JS link"
         Then the link "javascript execute" opens nothing