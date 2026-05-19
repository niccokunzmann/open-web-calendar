# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""A plain-text DESCRIPTION is preserved in the event popup.

See https://github.com/niccokunzmann/open-web-calendar/issues/443

The DHTMLX v7 popup was reported to drop the event description.
The proximate cause is that ``get_event_description`` only returned
``Description(event).html``, which is empty when the description is
plain text (no HTML tags, no ALTREP, no X-ALT-DESC).
"""

from icalendar import Calendar, Event

from open_web_calendar.app import ConvertToEvents


def event_with_uid(calendar_content: str, uid: str) -> Event:
    """Return the first event with the UID."""
    calendar = Calendar.from_ical(calendar_content)
    events = [event for event in calendar.walk("VEVENT") if event["UID"] == uid]
    assert events
    return events[0]


def test_plain_text_description_is_preserved(calendar_content):
    """A plain-text DESCRIPTION must round-trip into the event JSON."""
    event = event_with_uid(
        calendar_content["issue-287-links-1"], "1lnco7mmf4p8042a098k4h968g@google.com"
    )
    description = ConvertToEvents({"timezone": "Europe/London"}).get_event_description(
        event
    )
    assert "Stroll down the original Main Street USA" in description


def test_plain_text_description_with_url_is_preserved(calendar_content):
    """Plain text containing URLs must not be mistaken for HTML and dropped."""
    event = event_with_uid(
        calendar_content["issue-287-links-1"], "2mq8bka1v6opsra23c1na99bcr@google.com"
    )
    description = ConvertToEvents({"timezone": "Europe/London"}).get_event_description(
        event
    )
    assert "See attached flyer for details." in description
