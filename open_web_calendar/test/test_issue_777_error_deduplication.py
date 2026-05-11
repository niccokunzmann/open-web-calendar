# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Errors are deduplicated in user output but always logged.

See https://github.com/niccokunzmann/open-web-calendar/issues/777
"""

import pytest

from open_web_calendar.convert.calendar import ConvertToCalendars
from open_web_calendar.convert.events import ConvertToEvents
from open_web_calendar.convert.ics import ConvertToICS


def boom(url):
    raise ValueError("nope")


def get_errors(strategy):
    if isinstance(strategy, ConvertToCalendars):
        return strategy.errors
    if isinstance(strategy, ConvertToEvents):
        return [c for c in strategy.components if c.get("type") == "error"]
    return [
        c
        for c in strategy.components
        if any(str(e.get("UID", "")).startswith("error") for e in c.walk("VEVENT"))
    ]


@pytest.fixture(params=[ConvertToCalendars, ConvertToEvents, ConvertToICS])
def strategy_cls(request):
    return request.param


SPEC = {
    "url": [],
    "title": "t",
    "source_code": "x",
    "timezone": "UTC",
    "timeshift": 0,
}


def test_same_url_failing_twice_records_one_error(strategy_cls, capfd):
    spec = SPEC | {"url": ["http://x.example/a", "http://x.example/a"]}
    strategy = strategy_cls(spec, get_text_from_url=boom)
    strategy.retrieve_calendars()
    assert len(get_errors(strategy)) == 1
    assert capfd.readouterr().err.count("ValueError") >= 2


def test_two_urls_failing_identically_record_two_errors(strategy_cls):
    spec = SPEC | {"url": ["http://a.example/x", "http://b.example/y"]}
    strategy = strategy_cls(spec, get_text_from_url=boom)
    strategy.retrieve_calendars()
    assert len(get_errors(strategy)) == 2
