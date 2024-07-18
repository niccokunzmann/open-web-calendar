# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Check that we can open webcal links.

webcal:// usually means http.
"""

from open_web_calendar.conversion_base import ConversionStrategy


def test_webcal_is_replaced(mock):
    """Check that when we use webcal://, we actually use http"""
    cb = ConversionStrategy({}, mock)
    mock.return_value = ""
    cb.get_calendars_from_url("webcal://url.to/a/calendar.ics")
    mock.assert_called_once_with("http://url.to/a/calendar.ics")
