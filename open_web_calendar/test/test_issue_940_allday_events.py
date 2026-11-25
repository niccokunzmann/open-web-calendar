# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""All-day events should be displayed on the same days in every timezone.

Events stored as datetimes which start and end at midnight are all-day
events. They used to be shifted by the timezone and spanned an extra day
in the agenda view.

See https://github.com/niccokunzmann/open-web-calendar/issues/940
See https://github.com/niccokunzmann/open-web-calendar/issues/12
"""

import pytest

ALL_DAY_UTC_CALENDAR = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:all-day-utc
DTSTART:20250913T000000Z
DTEND:20250914T000000Z
SUMMARY:One day
END:VEVENT
BEGIN:VEVENT
UID:two-days-utc
DTSTART:20250915T000000Z
DTEND:20250917T000000Z
SUMMARY:Two days
END:VEVENT
BEGIN:VEVENT
UID:timed
DTSTART:20250913T090000Z
DTEND:20250913T100000Z
SUMMARY:Timed
END:VEVENT
END:VCALENDAR"""


@pytest.fixture()
def all_day_url(cache_url):
    """Cache the calendar with the all-day events stored as UTC datetimes."""
    url = "http://test.examples.local/all-day-utc.ics"
    cache_url(url, ALL_DAY_UTC_CALENDAR)
    return url


def get_events(client, url, timezone):
    response = client.get(
        f"/calendar.events.json?url={url}&timezone={timezone}&from=2025-09-10&to=2025-09-20"
    )
    assert response.status_code == 200
    return {event["uid"]: event for event in response.json}


@pytest.mark.parametrize(
    "timezone",
    ["UTC", "Europe/Berlin", "Asia/Tokyo", "America/New_York"],
)
def test_all_day_event_keeps_its_days(client, all_day_url, timezone):
    """All-day events stored as UTC datetimes stay on their days."""
    events = get_events(client, all_day_url, timezone)
    event = events["all-day-utc"]
    assert event["start_date"] == "2025-09-13 00:00"
    assert event["end_date"] == "2025-09-14 00:00"


@pytest.mark.parametrize(
    "timezone",
    ["UTC", "Europe/Berlin", "Asia/Tokyo", "America/New_York"],
)
def test_multi_day_event_keeps_its_days(client, all_day_url, timezone):
    """Events spanning several whole days stay on their days."""
    events = get_events(client, all_day_url, timezone)
    event = events["two-days-utc"]
    assert event["start_date"] == "2025-09-15 00:00"
    assert event["end_date"] == "2025-09-17 00:00"


@pytest.mark.parametrize(
    ("timezone", "expected_start"),
    [
        ("UTC", "2025-09-13 09:00"),
        ("Europe/Berlin", "2025-09-13 11:00"),
        ("Asia/Tokyo", "2025-09-13 18:00"),
        ("America/New_York", "2025-09-13 05:00"),
    ],
)
def test_timed_events_still_shift_with_timezone(
    client, all_day_url, timezone, expected_start
):
    """Timed events are still converted to the timezone of the viewer."""
    events = get_events(client, all_day_url, timezone)
    assert events["timed"]["start_date"] == expected_start
