# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Events should know which calendar they are in.

See https://github.com/niccokunzmann/open-web-calendar/issues/406

See https://datatracker.ietf.org/doc/html/rfc7986#section-5.1
And X-WR-CALNAME is in use, too.
"""

import pytest
from icalendar import Calendar

from open_web_calendar.conversion_base import CalendarInfo


@pytest.mark.parametrize(
    ("file", "name"),
    [
        ("calendar-name-rfc-7986", "RFC 7986 compatible calendar"),
        ("calendar-x-wr-calname", "old calendar description"),
        ("food", "food"),
    ],
)
def test_calendar_name_is_known(calendar_content, file, name):
    """Check that we can extract the calendar name."""
    cal = CalendarInfo(
        (0,0), f"https://localhost/{file}.ics", Calendar.from_ical(calendar_content[file])
    )
    assert cal.name == name


@pytest.mark.parametrize(
    ("file", "description"),
    [
        ("calendar-name-rfc-7986", "This is a later version with attributes"),
        ("calendar-x-wr-calname", " This calendar uses non-standard descriptions"),
        ("food", ""),
    ],
)
def test_calendar_description(calendar_content, file, description):
    """Check that we can extract the calendar name."""
    cal = CalendarInfo(
        (0,0), f"https://localhost/{file}.ics", Calendar.from_ical(calendar_content[file])
    )
    assert cal.description == description


@pytest.mark.parametrize(
    ("calendar_file", "attribute", "value"),
    [
        ("calendar-name-rfc-7986", "description", "This is a later version with attributes"),
        ("calendar-name-rfc-7986", "id", "0-0"),
        ("food", "id", "0-0"),
        ("calendar-x-wr-calname", "id", "0-0"),
        ("calendar-x-wr-calname", "name", "old calendar description"),
        ("calendar-x-wr-calname", "url-index", 0),
    ]
)
def test_calendar_information(client, calendar_urls, calendar_file,attribute,value):
    """Test the the information yielded from the calendars is correct."""
    result = client.get(f"/calendar.json?url={calendar_urls[calendar_file]}").json
    print(result)
    assert len(result["calendars"]) == 1
    cal = result["calendars"]["0-0"]
    assert cal[attribute] == value, f"attribute {attribute} expected to be {value} but found {cal[attribute]}"


@pytest.mark.parametrize("index",
                         [(0,0), (0, 3), (3, 1)])
def test_event_classes(index, calendar_content):
    ci = CalendarInfo(
        index, f"https://localhost/file.ics", Calendar.from_ical(calendar_content["food"])
    )
    assert f"CALENDAR-INDEX-{index[0]}" in ci.event_css_classes
    assert f"CALENDAR-INDEX-{index[0]}-{index[1]}" in ci.event_css_classes


@pytest.mark.parametrize("url",
                         ["http://localhost:8001/nanan.ics", 
                          "https://abc.com/cal.ics"])
def test_event_classes(url):
    ci = CalendarInfo(
        (1,1), url, Calendar()
    )
    assert ci.to_json()["url"] == url


# TODO: test what happens if a URL does not work.