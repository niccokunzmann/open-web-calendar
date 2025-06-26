# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Get information about a calendar from its ICS representation."""

from __future__ import annotations

from icalendar import Calendar

from open_web_calendar.calendars.info.interface import CalendarInfoInterface


class IcalInfo(CalendarInfoInterface):
    """Information from an icalendar file."""

    def __init__(self, calendar: Calendar | None = None):
        self._calendar = calendar if calendar is not None else Calendar()

    @property
    def calendar_name(self) -> str | None:
        """Return the name of the calendar."""
        return self._calendar.calendar_name

    @property
    def calendar_description(self) -> str | None:
        """Return the description of the calendar."""
        return self._calendar.description

    @property
    def calendar_color(self) -> str | None:
        """Return the color of the calendar."""
        return self._calendar.color

    @property
    def calendar_categories(self) -> list[str]:
        """Return the categories of the calendar."""
        return self._calendar.categories


__all__ = ["IcalInfo"]
