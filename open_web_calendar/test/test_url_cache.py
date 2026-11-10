# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""
Test the caching functionality which will be used by subsequent tests.

"""

from unittest.mock import Mock

import pytest
import requests

from open_web_calendar.app import get_text_from_url
from open_web_calendar.convert.base import ConversionStrategy


def test_tests_can_cache_values(cache_url):
    cache_url("http://asd.asd", "test123")
    assert get_text_from_url("http://asd.asd") == b"test123"


def test_caching_twice_works(cache_url):
    cache_url("http://asd.asd", "test123")
    cache_url("http://asd.asd", "asd")
    assert get_text_from_url("http://asd.asd") == b"asd"


def test_default_fetch_preserves_utf8_ics_content(monkeypatch):
    expected_summary = "🏊 Sea swimming ≤3"
    content = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Open Web Calendar//Test\r\n"
        "BEGIN:VEVENT\r\n"
        "UID:utf8-test\r\n"
        "DTSTAMP:20261110T100000Z\r\n"
        "DTSTART:20261110T110000Z\r\n"
        "DTEND:20261110T120000Z\r\n"
        f"SUMMARY:{expected_summary}\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    ).encode()
    response = Mock(content=content, text=content.decode("latin-1"))
    monkeypatch.setattr(
        "open_web_calendar.convert.base.requests.get",
        lambda _url, **_kwargs: response,
    )

    calendars = ConversionStrategy({}).get_calendars_from_url(
        "https://calendar.example.com/utf8.ics"
    )

    assert str(calendars.get_icalendars()[0].events[0]["SUMMARY"]) == expected_summary


def test_requests_are_forbidden():
    with pytest.raises(requests.ConnectionError):
        requests.get("https://duckduckgo.com", timeout=20)
