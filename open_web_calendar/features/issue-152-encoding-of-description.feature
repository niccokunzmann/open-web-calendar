Feature: The calendar should be correctly encoded.

    Scenario: make sure the name is decoded properly
       Given we add the calendar "issue_152_broken_characters"
        When we look at 2023-02-27
        Then we see that event "S2R47971-0@lantiv.com-2023-02-27-10-15" has the text "10:15 2-1, 2-2, 2-3, 2-4, 2-5, 2-6, 2-7, 2-8, 2-9, 2-10, 2-11, 2-12, p1 Kostiju trupa, Anatomija s organogenezom domaćih životinja II"
