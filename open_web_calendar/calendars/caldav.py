# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Caldav interface to retrieve calendars."""

from __future__ import annotations

from urllib.parse import ParseResult, urlparse

import caldav

from open_web_calendar.calendars.base import Calendars
from open_web_calendar.util import unset_url_username_password


class CalDAVCalendars(Calendars):
    """Return calendars from caldav."""

    @classmethod
    def from_url(cls, url: str):
        """Create an interface to calendars from a caldav URL.

        We should have a caldav URL here with username and password.

        Example:

            "https://username:password@nexcloud.mydomain.com/remote.php/dav/calendars/test/test_shared_by_other/"
        """
        parsed: ParseResult = urlparse(url)
        calendar_url = unset_url_username_password(url)
        with caldav.DAVClient(
            url=calendar_url, username=parsed.username, password=parsed.password
        ) as client:
            calendar = caldav.Calendar(client, url=calendar_url)
            return cls(calendar)

    def __init__(self, calendar: caldav.Calendar):
        """Create a new CalDAV interface for one calendar."""
        self._calendar = calendar


__all__ = ["CalDAVCalendars"]
