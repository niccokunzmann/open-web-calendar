# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Base interface to calendars."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from open_web_calendar.calendars.ics import ICSCalendars

if TYPE_CHECKING:
    from datetime import datetime

    import icalendar


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


__all__ = ["Calendars"]
