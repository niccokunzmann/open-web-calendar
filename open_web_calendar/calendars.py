# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""A unified interface to calendars from different sources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from urllib.parse import ParseResult, urlparse

import caldav
import icalendar
import recurring_ical_events

from open_web_calendar.util import unset_url_username_password

if TYPE_CHECKING:
    from datetime import datetime


class InvalidCalendars(ValueError):
    """The content or URL provided cannot be used as calendars."""


class Calendars(ABC):
    """Base class for calendars.

    We handle multiple calendars behind a URL in one go.
    """

    @classmethod
    def empty(cls) -> Calendars:
        """There are no calendars."""
        return ICSCalendars()

    @abstractmethod
    def get_events_between(
        self, start: datetime, end: datetime
    ) -> list[icalendar.Event]:
        """Return a list of events that occur between start and end."""

    @abstractmethod
    def get_icalendars(self) -> list[icalendar.Calendar]:
        """Return a list of ICS calendars."""


class ICSCalendars(Calendars):
    """Wrapper to handle ICS calendars."""

    @classmethod
    def from_text(cls, text: str):
        """Create ICS calendars from the text of a calendar file."""
        result = cls()
        result.add_from_text(text)
        return result

    def __init__(self):
        """Handle ICS calendars in a unified way."""
        self._calendars: list[icalendar.Calendar] = []

    def add_from_text(self, text: str):
        """Add ICS calendars from text."""
        try:
            self._calendars.extend(icalendar.Calendar.from_ical(text, multiple=True))
        except ValueError as e:
            raise InvalidCalendars(
                "The content of this URL is not an ICS calendar."
            ) from e

    def __bool__(self):
        """If we have any content."""
        return bool(self._calendars)

    def get_events_between(
        self, start: datetime, end: datetime
    ) -> list[icalendar.Event]:
        events = []
        for calendar in self._calendars:
            events.extend(recurring_ical_events.of(calendar).between(start, end))
        return events

    def get_icalendars(self) -> list[icalendar.Calendar]:
        return self._calendars[:]


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


__all__ = [
    "CalDAVCalendars",
    "Calendars",
    "ICSCalendars",
    "InvalidCalendars",
]
