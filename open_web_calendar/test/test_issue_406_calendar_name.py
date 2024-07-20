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
        0, f"https://localhost/{file}.ics", Calendar.from_ical(calendar_content[file])
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
        0, f"https://localhost/{file}.ics", Calendar.from_ical(calendar_content[file])
    )
    assert cal.description == description
