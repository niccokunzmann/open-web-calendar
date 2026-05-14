# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Handle calendars from ICS links."""

from __future__ import annotations

from typing import TYPE_CHECKING

import icalendar
import recurring_ical_events

from open_web_calendar.calendars.base import Calendars
from open_web_calendar.calendars.errors import InvalidCalendars
from open_web_calendar.config import environment as config
from open_web_calendar.error import ResponseTooLarge

if TYPE_CHECKING:
    from datetime import datetime


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
        # Sum across all parsed calendars so an attacker can't bypass the cap
        # by concatenating multiple VCALENDAR blocks in one response.
        total_source = sum(len(calendar.walk("VEVENT")) for calendar in self._calendars)
        ResponseTooLarge.check(
            "Source events",
            total_source,
            "max_source_events",
            config.max_source_events,
        )
        events = []
        for calendar in self._calendars:
            events.extend(recurring_ical_events.of(calendar).between(start, end))
        return events

    def get_icalendars(self) -> list[icalendar.Calendar]:
        return self._calendars[:]


__all__ = ["ICSCalendars"]
