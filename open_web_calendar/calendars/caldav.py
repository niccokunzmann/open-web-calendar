# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Caldav interface to retrieve calendars."""

from __future__ import annotations

from typing import TYPE_CHECKING

import caldav

from open_web_calendar.calendars.base import Calendars

if TYPE_CHECKING:
    from datetime import datetime

    import icalendar


class CalDAVCalendars(Calendars):
    """Return calendars from caldav."""

    @classmethod
    def from_url(cls, url: str):
        """Create an interface to calendars from a caldav URL.

        We should have a caldav URL here with username and password.

        Example:

            "https://username:password@nexcloud.mydomain.com/remote.php/dav/calendars/test/test_shared_by_other/"
        """
        client = caldav.DAVClient(url=url)
        calendar = caldav.Calendar(client, url=url)
        return cls(calendar)

    def __init__(self, calendar: caldav.Calendar):
        """Create a new CalDAV interface for one calendar."""
        self._calendar = calendar

    def get_events_between(
        self, start: datetime, end: datetime
    ) -> list[icalendar.Event]:
        """Return a list of events that occur between start and end."""
        events: list[caldav.Event] = self._calendar.search(
            expand=True, comp_class=caldav.Event, start=start, end=end
        )
        result = []
        for caldav_event in events:
            result.extend(caldav_event.icalendar_instance.walk("VEVENT"))
        return result

    def get_icalendars(self) -> list[icalendar.Calendar]:
        """Return a list of ICS calendars."""
        events: list[caldav.Event] = self._calendar.events()
        return [event.icalendar_instance for event in events]


__all__ = ["CalDAVCalendars"]
