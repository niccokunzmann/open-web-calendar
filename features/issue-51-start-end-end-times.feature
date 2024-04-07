Feature: The start and end times of the events should be simple and non-confusing.
         This is the case for one-day, multi-day and timed events in the calendar and the details.

    Scenario: I view a single day event and I do not see the time.
      Given we add the calendar "malicious"
       When we look at 2019-03-04
       When we click on the event ">event!"
       Then we cannot see the text "0:0"

#    Scenario: Check the 31st March 2024 in Germany works.
