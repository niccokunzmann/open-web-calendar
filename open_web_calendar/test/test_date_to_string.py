# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

import datetime

import pytest
from pytz import timezone, utc

from open_web_calendar.app import ConvertToDhtmlx

berlin = timezone("Europe/Berlin")
eastern = timezone("US/Eastern")

UTC = "UTC"
BERLIN = "Europe/Berlin"
EASTERN = "US/Eastern"


@pytest.mark.parametrize(
    ("date", "tz", "expected"),
    [
        # test date object without time zone
        (datetime.date(2019, 3, 23), UTC, "2019-03-23 00:00"),
        (datetime.date(2019, 3, 23), BERLIN, "2019-03-23 00:00"),
        (datetime.date(2019, 3, 23), EASTERN, "2019-03-23 00:00"),
        # test datetime object without time zone
        (datetime.datetime(2019, 6, 2, 20), UTC, "2019-06-02 20:00"),
        (datetime.datetime(2019, 4, 20, 10, 10), BERLIN, "2019-04-20 10:10"),
        (datetime.datetime(2019, 12, 1, 0, 13, 23), EASTERN, "2019-12-01 00:13"),
        # test datetime object with time zone
        (berlin.localize(datetime.datetime(2019, 6, 2, 20)), UTC, "2019-06-02 18:00"),
        (
            berlin.localize(datetime.datetime(2019, 4, 20, 10, 10)),
            BERLIN,
            "2019-04-20 10:10",
        ),
        (
            berlin.localize(datetime.datetime(2019, 12, 1, 0, 13, 23)),
            EASTERN,
            "2019-11-30 18:13",
        ),
        (utc.localize(datetime.datetime(2019, 6, 2, 20)), UTC, "2019-06-02 20:00"),
        (
            utc.localize(datetime.datetime(2019, 4, 20, 10, 10)),
            BERLIN,
            "2019-04-20 12:10",
        ),
        (
            utc.localize(datetime.datetime(2019, 12, 1, 0, 13, 23)),
            EASTERN,
            "2019-11-30 19:13",
        ),
    ],
)
def test_date_to_string_conversion(date, tz, expected):
    """Convert dates and datetime objects for the events.json"""
    string = ConvertToDhtmlx({"timezone": tz}).date_to_string(date)
    print(date)
    assert string == expected
