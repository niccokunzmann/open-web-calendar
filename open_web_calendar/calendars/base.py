# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Base interface to calendars."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from open_web_calendar.calendars.info.dict import DictInfo
from open_web_calendar.calendars.info.ics import IcalInfo
from open_web_calendar.calendars.info.list import ListInfo

if TYPE_CHECKING:
    from datetime import datetime

    import icalendar

    from open_web_calendar.calendars.info.interface import CalendarInfoInterface


class Calendars(ABC):
    """Base class for calendars.

    We handle multiple calendars behind a URL in one go.
    """

    @classmethod
    def empty(cls) -> Calendars:
        """There are no calendars."""
        from open_web_calendar.calendars.ics import (  # noqa: PLC0415, RUF100
            ICSCalendars,
        )

        return ICSCalendars()

    @abstractmethod
    def get_events_between(
        self, start: datetime, end: datetime
    ) -> list[icalendar.Event]:
        """Return a list of events that occur between start and end."""

    @abstractmethod
    def get_icalendars(self) -> list[icalendar.Calendar]:
        """Return a list of ICS calendars."""

    def get_infos(self) -> list[CalendarInfoInterface]:
        """Return information about the calendars."""
        return [
            ListInfo([DictInfo(calendar_index_in_file=i), IcalInfo(c)])
            for i, c in enumerate(self.get_icalendars())
        ]


__all__ = ["Calendars"]
