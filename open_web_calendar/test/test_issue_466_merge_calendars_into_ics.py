# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test the merging of calendars into .ics files."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from icalendar import Calendar


@pytest.mark.parametrize(
    ("attr", "expected_value", "spec"),
    [
        ("VERSION", "2.0", {}),
        ("PRODID", "open-web-calendar", {}),
        ("CALSCALE", "GREGORIAN", {}),
        ("X-WR-CALNAME", "My Calendar", {"title": "My Calendar"}),
        ("X-WR-CALNAME", "Company Calendar", {"title": "Company Calendar"}),
        ("X-PROD-SOURCE", "http://my-code", {"source_code": "http://my-code"}),
        ("X-PROD-SOURCE", "XXX", {"source_code": "XXX"}),
    ]
)
def test_default_parameters(attr, expected_value, spec, merged):
    """Check that the parameters are set in the merged calendar."""
    cal : Calendar = merged([], spec)
    assert cal[attr] == expected_value


def test_empty_calendar_has_no_events(merged):
    """No events in an empty calendar."""
    assert merged().events == []


def test_get_events_from_one_calendar(merged):
    """All events should be in the calendar."""
    cal : Calendar = merged(["food.ics"])
    assert len(cal.events) == 132


def test_get_events_from_two_calendars(merged):
    """All events should be in the calendar."""
    cal : Calendar = merged(["food.ics", "one-event.ics"])
    assert len(cal.events) == 133


def test_timezone_is_included(merged):
    """The timezone should be included."""
    cal : Calendar = merged(["one-event.ics"])
    assert len(cal.timezones) == 1
    assert cal.timezones[0].tz_name == "Europe/Berlin"
