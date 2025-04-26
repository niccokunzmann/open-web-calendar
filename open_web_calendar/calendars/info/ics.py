# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

from typing import Optional

from icalendar import Calendar

from open_web_calendar.calendars.info.interface import CalendarInfoInterface


class IcalInfo(CalendarInfoInterface):
    """Information from an icalendar file."""

    def __init__(self, calendar: Optional[Calendar] = None):
        self._calendar = calendar if calendar is not None else Calendar()

    @property
    def calendar_name(self) -> str | None:
        """Return the name of the calendar."""
        return self._calendar.get("NAME")

    @property
    def calendar_description(self) -> str | None:
        """Return the description of the calendar."""
        return self._calendar.get("DESCRIPTION")

    @property
    def calendar_color(self) -> str | None:
        """Return the color of the calendar."""
        return self._calendar.get("COLOR")

    @property
    def calendar_categories(self) -> list[str]:
        """Return the categories of the calendar."""
        cats = self._calendar.get("CATEGORIES")
        return cats.cats if cats is not None else []


__all__ = ["IcalInfo"]
