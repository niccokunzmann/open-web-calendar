Feature: I would like to choose which tabs to display.

  Scenario: I see the default tabs.
    Given we add the calendar "one-event"
     When we look at 2024-01-18
     Then we can see the text "DAY"
     Then we can see the text "WEEK"
     Then we can see the text "MONTH"
     Then we can see the text "January 2024"
     Then we cannot see the text "AGENDA"

  Scenario: I see all possible tabs.
    Given we add the calendar "one-event"
      And we set the "tabs" parameter to ["month","week","day","agenda"]
     When we look at 2024-01-18
     Then we can see the text "DAY"
     Then we can see the text "WEEK"
     Then we can see the text "MONTH"
     Then we can see the text "AGENDA"

  Scenario: I do not allow any controls.
    Given we add the calendar "one-event"
      And we set the "controls" parameter to ""
     When we look at 2024-01-18
     Then we cannot see a dhx_cal_prev_button
     Then we cannot see a dhx_cal_today_button
     Then we cannot see a dhx_cal_next_button

  Scenario: I can use the default controls.
    Given we add the calendar "one-event"
     When we look at 2024-01-18
     Then we can see a dhx_cal_prev_button
     Then we can see a dhx_cal_today_button
     Then we can see a dhx_cal_next_button

  Scenario: I do not see any tabs.
    Given we add the calendar "one-event"
      And we set the "tabs" parameter to ""
     When we look at 2024-01-18
#     Then we cannot see the text "DAY"  # included in TODAY
     Then we cannot see the text "WEEK"
     Then we cannot see the text "MONTH"
     Then we cannot see the text "AGENDA"

  Scenario: I can disable the TODAY button but still see the DAY button.
    Given we add the calendar "one-event"
      And we set the "controls" parameter to ""
     When we look at 2024-01-18
     Then we can see the text "DAY"
