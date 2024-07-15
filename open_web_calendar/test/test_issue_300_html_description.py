# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Use the HTML description where given.

See https://github.com/niccokunzmann/open-web-calendar/issues/300

Calendars:
- description is HTML: issue-287-links-1.ics
- description parameter is HTML: event-with-html-markup.ics
- alt description attribtue is HTML: food.ics

"""

from icalendar import Calendar, Event

from open_web_calendar.app import ConvertToDhtmlx


def event_with_uid(calendar_content: str, uid: str) -> Event:
    """Return the first event with the UID."""
    calendar = Calendar.from_ical(calendar_content)
    events = [event for event in calendar.walk("VEVENT") if event["UID"] == uid]
    assert events
    return events[0]


def test_description_is_html(calendar_content):
    """The description of the event is already in HTML."""
    event = event_with_uid(
        calendar_content["issue-287-links-1"], "1jkma74p98bj79c760660arc07@google.com"
    )
    description = ConvertToDhtmlx({"timezone": "Europe/London"}).get_event_description(
        event
    )
    assert '<a href="https://bethanymarceline.com/"' in description


def test_description_is_parameter(calendar_content):
    """The description of the event is already in HTML."""
    event = event_with_uid(
        calendar_content["event-with-html-markup"],
        "683642b3-9b25-4177-8b46-ec2f65e64020",
    )
    description = ConvertToDhtmlx({"timezone": "Europe/London"}).get_event_description(
        event
    )
    assert "<h1>\n Know This Heading!\n</h1>" in description


def test_alt_attribute(calendar_content):
    """The HTML description is in an alt attribute."""
    event = event_with_uid(calendar_content["food"], "2851")
    description = ConvertToDhtmlx({"timezone": "Europe/London"}).get_event_description(
        event
    )
    assert "Cauliflower\n  <br>" in description
