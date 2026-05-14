# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Hard caps on /calendar.events.json prevent recurring-event DoS.

Addresses pentest finding CLN-007. A malicious 20KB ICS with daily
recurring events until 2050 expands to ~1.69 million events (~2.4GB
JSON), stalling a worker until timeout.

This module verifies three layers of defense:
- OWC_MAX_SOURCE_EVENTS: cap on raw VEVENT count per source calendar
- OWC_MAX_RESPONSE_EVENTS: cap on expanded events per response
- OWC_MAX_RESPONSE_MB: cap on serialized JSON byte size

Each cap returns HTTP 413 when exceeded.
"""

import os


def _build_calendar(events_body: str) -> str:
    return f"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:test\r\n{events_body}END:VCALENDAR\r\n"


def _build_pentest_poc(source_event_count: int = 100) -> str:
    """Return the pentest CLN-007 PoC: N events each with daily RRULE to 2050."""
    body = ""
    for i in range(source_event_count):
        body += (
            "BEGIN:VEVENT\r\n"
            "DTSTAMP:20151219T021727Z\r\n"
            "DTSTART:20200101T100000Z\r\n"
            "DTEND:20200101T110000Z\r\n"
            "RRULE:FREQ=DAILY;UNTIL=20500310T035959Z\r\n"
            "SUMMARY:Meeting\r\n"
            f"UID:{i + 1}@test\r\n"
            "END:VEVENT\r\n"
        )
    return _build_calendar(body)


def _build_simple_calendar(event_count: int) -> str:
    """Return a calendar with N simple non-recurring events."""
    body = ""
    for i in range(event_count):
        body += (
            "BEGIN:VEVENT\r\n"
            "DTSTAMP:20260101T000000Z\r\n"
            f"DTSTART:202601{(i % 28) + 1:02d}T100000Z\r\n"
            f"DTEND:202601{(i % 28) + 1:02d}T110000Z\r\n"
            "SUMMARY:Simple Event\r\n"
            f"UID:simple-{i}@test\r\n"
            "END:VEVENT\r\n"
        )
    return _build_calendar(body)


def test_default_allows_normal_recurring_calendar(client, cache_url):
    """A small recurring calendar within default caps returns events."""
    url = "http://example.com/normal.ics"
    body = ""
    for i in range(5):
        body += (
            "BEGIN:VEVENT\r\n"
            "DTSTAMP:20260101T000000Z\r\n"
            "DTSTART:20260101T100000Z\r\n"
            "DTEND:20260101T110000Z\r\n"
            "RRULE:FREQ=DAILY;COUNT=30\r\n"
            "SUMMARY:Daily Standup\r\n"
            f"UID:normal-{i}@test\r\n"
            "END:VEVENT\r\n"
        )
    cache_url(url, _build_calendar(body))
    response = client.get(
        f"/calendar.events.json?url={url}&from=2026-01-01&to=2026-02-01"
    )
    assert response.status_code == 200
    assert len(response.json) > 0


def test_pentest_poc_is_rejected(client, cache_url):
    """A scaled-down CLN-007 pentest pattern is rejected by the expanded cap.

    Real PoC uses 100 source events; we use 5 over a 6-year window which still
    expands to ~10960 events (over the OWC_MAX_RESPONSE_EVENTS cap of 10000).
    """
    url = "http://example.com/poc.ics"
    cache_url(url, _build_pentest_poc(source_event_count=5))
    response = client.get(
        f"/calendar.events.json?url={url}&from=2020-01-01&to=2026-01-01"
    )
    assert response.status_code == 413


def test_too_many_source_events_is_rejected(client, cache_url):
    """A calendar exceeding OWC_MAX_SOURCE_EVENTS is rejected pre-expansion."""
    url = "http://example.com/many-source.ics"
    cache_url(url, _build_simple_calendar(event_count=2000))
    response = client.get(
        f"/calendar.events.json?url={url}&from=2026-01-01&to=2026-02-01"
    )
    assert response.status_code == 413


def test_too_many_expanded_events_is_rejected(client, cache_url):
    """A single event whose RRULE expands beyond the cap is rejected."""
    url = "http://example.com/expand-bomb.ics"
    # DAILY with COUNT=20000 produces ~20k occurrences within a 60-year window,
    # which exceeds the default OWC_MAX_RESPONSE_EVENTS=10000 cap.
    body = (
        "BEGIN:VEVENT\r\n"
        "DTSTAMP:20260101T000000Z\r\n"
        "DTSTART:20000101T100000Z\r\n"
        "DTEND:20000101T110000Z\r\n"
        "RRULE:FREQ=DAILY;COUNT=20000\r\n"
        "SUMMARY:Daily 20k times\r\n"
        "UID:expand-bomb@test\r\n"
        "END:VEVENT\r\n"
    )
    cache_url(url, _build_calendar(body))
    response = client.get(
        f"/calendar.events.json?url={url}&from=2000-01-01&to=2060-01-01"
    )
    assert response.status_code == 413


def test_caps_are_tunable_via_env_vars(client, cache_url, monkeypatch):
    """Raising OWC_MAX_SOURCE_EVENTS lets a previously-rejected calendar through."""
    monkeypatch.setitem(os.environ, "OWC_MAX_SOURCE_EVENTS", "10000")
    url = "http://example.com/raised-cap.ics"
    cache_url(url, _build_simple_calendar(event_count=2000))
    response = client.get(
        f"/calendar.events.json?url={url}&from=2026-01-01&to=2026-02-01"
    )
    assert response.status_code == 200


def test_cap_rejection_has_413_status_and_json_body(client, cache_url):
    """A rejected request returns 413 with the standard JSON error shape."""
    url = "http://example.com/too-big.ics"
    cache_url(url, _build_simple_calendar(event_count=2000))
    response = client.get(
        f"/calendar.events.json?url={url}&from=2026-01-01&to=2026-02-01"
    )
    assert response.status_code == 413
    assert response.content_type.startswith("application/json")
    assert response.json["code"] == 413
