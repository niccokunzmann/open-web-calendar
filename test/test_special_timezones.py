# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test that special time zones are also handeled correctly.

See https://github.com/niccokunzmann/open-web-calendar/issues/190
"""

import pytest


@pytest.mark.parametrize(
    ("timezone", "event_start", "timeshift"),
    [
        ("", "2019-03-04 07:00", 0),  # UTC
        ("", "2019-03-04 04:00", 180),  # UTC-3
        ("Etc/GMT 3", "2019-03-04 04:00", 180),
        ("Etc/GMT 5", "2019-03-04 02:00", 300),
        ("undefined", "2019-03-04 06:00", 60),
        ("undefined", "2019-03-04 07:00", 0),
        ("UTC", "2019-03-04 07:00", 180),  # timeshift ignored, proper timezone
        (
            "Europe/London",
            "2019-03-04 07:00",
            -240,
        ),  # timeshift ignored, proper timezone
        ("Europe/Berlin", "2019-03-04 08:00", 0),  # timeshift ignored, proper timezone
    ],
)
def test_that_timezones_do_not_create_an_error(
    timezone, client, event_start, calendar_urls, timeshift
):
    """These time zones are a bit special, not 1:1 Python.

    This is why we use the timeshift given.
    """
    response = client.get(
        f"/calendar.events.json?url={calendar_urls['one-event']}&timezone={timezone}&timeshift={timeshift}&from=2019-03-04&to=2019-03-05"
    )
    assert response.status_code == 200
    assert len(response.json) == 1
    event = response.json[0]
    assert event["start_date"] == event_start, f"Timezone differs in offset: {timezone}"
