# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test the merging of calendars into .ics files."""

from datetime import datetime, timedelta

import pytest
from icalendar import Calendar, Event, Timezone


@pytest.mark.parametrize(
    ("attr", "expected_value", "spec"),
    [
        ("VERSION", "2.0", {}),
        ("PRODID", "open-web-calendar", {}),
        ("CALSCALE", "GREGORIAN", {}),
        ("X-WR-CALNAME", "My Calendar", {"title": "My Calendar"}),
        ("X-WR-CALNAME", "Company Calendar", {"title": "Company Calendar"}),
        ("NAME", "My Calendar", {"title": "My Calendar"}),
        ("NAME", "Company Calendar", {"title": "Company Calendar"}),
        ("X-PROD-SOURCE", "http://my-code", {"source_code": "http://my-code"}),
        ("X-PROD-SOURCE", "XXX", {"source_code": "XXX"}),
    ],
)
def test_default_parameters(attr, expected_value, spec, merged):
    """Check that the parameters are set in the merged calendar."""
    cal: Calendar = merged([], spec)
    assert cal[attr] == expected_value


def test_empty_calendar_has_no_events(merged):
    """No events in an empty calendar."""
    assert merged().events == []


def test_get_events_from_one_calendar(merged):
    """All events should be in the calendar."""
    cal: Calendar = merged(["food.ics"])
    assert len(cal.events) == 132


def test_get_events_from_two_calendars(merged):
    """All events should be in the calendar."""
    cal: Calendar = merged(["food.ics", "one-event.ics"])
    assert len(cal.events) == 133


def test_timezone_is_included(merged):
    """The timezone should be included."""
    cal: Calendar = merged(["one-event.ics"])
    assert len(cal.timezones) == 1
    assert cal.timezones[0].tz_name == "Europe/Berlin"


@pytest.fixture
def download_event(client, cache_url):
    """Follow the events endpoint through to the single-event download."""

    def download(start, end, calendar_properties="", year=2025):
        url = "https://example.test/download.ics"
        cache_url(
            url,
            "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:download-test\r\n"
            f"{calendar_properties}BEGIN:VEVENT\r\nUID:download-test\r\n"
            f"{start}\r\n{end}\r\nSUMMARY:Download test\r\n"
            "END:VEVENT\r\nEND:VCALENDAR\r\n",
        )
        response = client.get(
            "/calendar.events.json",
            query_string={
                "url": url,
                "from": f"{year}-01-01",
                "to": f"{year + 1}-01-01",
                "timezone": "UTC",
            },
        )
        assert response.status_code == 200
        [event] = response.json
        response = client.get(
            "/calendar.ics", query_string={"url": url, "set_event": event["ical"]}
        )
        assert response.status_code == 200
        calendar = Calendar.from_ical(response.data)
        assert len(calendar.events) == 1
        assert calendar.events[0] == Event.from_ical(event["ical"])
        return calendar

    return download


@pytest.mark.parametrize(
    ("year", "month", "hours"),
    [(2025, 1, 1), (2025, 6, 2), (1960, 6, 1), (2050, 6, 2)],
)
def test_download_generates_missing_timezone(download_event, year, month, hours):
    """An importer can recover the offset without its own timezone database."""
    calendar = download_event(
        f"DTSTART;TZID=Europe/Berlin:{year}{month:02d}01T120000",
        f"DTEND;TZID=Europe/Berlin:{year}{month:02d}01T130000",
        year=year,
    )
    assert len(calendar.timezones) == 1
    [timezone] = calendar.timezones
    assert timezone.tz_name == "Europe/Berlin"
    imported_zone = timezone.to_tz(lookup_tzid=False)
    assert datetime(year, month, 1, 12, tzinfo=imported_zone).utcoffset() == timedelta(
        hours=hours
    )


def test_download_includes_both_endpoint_timezones(client):
    event = (
        "BEGIN:VEVENT\r\nUID:two-zones\r\n"
        "DTSTART;TZID=Europe/Berlin:20250601T120000\r\n"
        "DTEND;TZID=Europe/London:20250601T130000\r\nEND:VEVENT\r\n"
    )
    response = client.get("/calendar.ics", query_string={"set_event": event})
    assert response.status_code == 200
    calendar = Calendar.from_ical(response.data)
    assert calendar.events == [Event.from_ical(event)]
    assert {zone.tz_name for zone in calendar.timezones} == {
        "Europe/Berlin",
        "Europe/London",
    }


def test_download_preserves_source_timezone(client, calendar_urls, calendar_content):
    source = Calendar.from_ical(calendar_content["one-event"])
    response = client.get(
        "/calendar.ics",
        query_string={
            "url": calendar_urls["one-event"],
            "set_event": source.events[0].to_ical().decode(),
        },
    )
    assert response.status_code == 200
    calendar = Calendar.from_ical(response.data)
    assert len(calendar.events) == 1
    assert calendar.timezones == source.timezones


def test_download_includes_x_wr_timezone(download_event):
    calendar = download_event(
        "DTSTART:20250601T120000",
        "DTEND:20250601T130000",
        "X-WR-TIMEZONE:America/New_York\r\n",
    )
    [timezone] = calendar.timezones
    assert timezone.tz_name == "America/New_York"
    assert calendar.events[0].start.utcoffset() == timedelta(hours=-4)


@pytest.mark.parametrize(
    ("start", "end"),
    [
        ("DTSTART:20250601T120000Z", "DTEND:20250601T130000Z"),
        ("DTSTART:20250601T120000", "DTEND:20250601T130000"),
        ("DTSTART;VALUE=DATE:20250601", "DTEND;VALUE=DATE:20250602"),
    ],
)
def test_download_does_not_invent_timezone(download_event, start, end):
    assert download_event(start, end).timezones == []


def test_download_caches_generated_timezone(download_event, monkeypatch):
    calls = []
    from_tzid = Timezone.from_tzid

    def create_timezone(*args, **kwargs):
        calls.append(args[0])
        return from_tzid(*args, **kwargs)

    monkeypatch.setattr(Timezone, "from_tzid", create_timezone)
    for _ in range(2):
        calendar = download_event(
            "DTSTART;TZID=Pacific/Auckland:20250601T120000",
            "DTEND;TZID=Pacific/Auckland:20250601T130000",
        )
        assert len(calendar.timezones) == 1
    assert calls == ["Pacific/Auckland"]


def test_download_preserves_unknown_timezone(client):
    event = (
        "BEGIN:VEVENT\r\nUID:unknown-zone\r\n"
        "DTSTART;TZID=Unknown/Zone:20250601T120000\r\n"
        "DTEND;TZID=Unknown/Zone:20250601T130000\r\nEND:VEVENT\r\n"
    )
    response = client.get("/calendar.ics", query_string={"set_event": event})
    assert response.status_code == 200
    calendar = Calendar.from_ical(response.data)
    assert calendar.events == [Event.from_ical(event)]
    assert calendar.timezones == []


def test_url_property(merged):
    """Purpose:  This property may be used to convey a location where a more
    dynamic rendition of the calendar information can be found.

    https://www.rfc-editor.org/rfc/rfc7986.html#section-5.5
    """
    pytest.skip("TODO")


def test_source_property(merged):
    """Description:  This property identifies a location where a client can
    retrieve updated data for the calendar.  Clients SHOULD honor any
    specified "REFRESH-INTERVAL" value when periodically retrieving
    data.  Note that this property differs from the "URL" property in
    that "URL" is meant to provide an alternative representation of
    the calendar data rather than the original location of the data.

    https://www.rfc-editor.org/rfc/rfc7986.html#section-5.8
    """
    pytest.skip("TODO")
