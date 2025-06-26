# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Combine several information sources about calendars."""

from __future__ import annotations

import functools
import operator

from open_web_calendar.calendars.info.dict import DictInfo
from open_web_calendar.calendars.info.interface import CalendarInfoInterface


class ListInfo(CalendarInfoInterface):
    """Information about a calendar stored in a list."""

    def __init__(self, infos: list[CalendarInfoInterface] | None = None):
        """Compose information about the calendar from different information sources."""
        self._mine = DictInfo()
        self._infos = [self._mine] + (infos or [])

    def set(
        self, values: dict[str, str | list[str] | int | None] | None = None, **kwargs
    ):
        """Set values."""
        self._mine.set(values)
        self._mine.set(kwargs)

    @property
    def calendar_name(self) -> str | None:
        """Return the name of the calendar."""
        return next(
            (
                info.calendar_name
                for info in self._infos
                if info.calendar_name is not None
            ),
            None,
        )

    @property
    def calendar_url(self) -> str | None:
        """Return the URL of the calendar."""
        return next(
            (
                info.calendar_url
                for info in self._infos
                if info.calendar_url is not None
            ),
            None,
        )

    @property
    def calendar_index_in_file(self) -> int | None:
        """Return the index of the URL of the calendar."""
        return next(
            (
                info.calendar_index_in_file
                for info in self._infos
                if info.calendar_index_in_file is not None
            ),
            None,
        )

    @property
    def calendar_description(self) -> str | None:
        """Return the description of the calendar."""
        return next(
            (
                info.calendar_description
                for info in self._infos
                if info.calendar_description is not None
            ),
            None,
        )

    @property
    def calendar_color(self) -> str | None:
        """Return the color of the calendar."""
        return next(
            (
                info.calendar_color
                for info in self._infos
                if info.calendar_color is not None
            ),
            None,
        )

    @property
    def calendar_categories(self) -> list[str]:
        """Return the categories of the calendar."""
        return functools.reduce(
            operator.iadd, (info.calendar_categories for info in self._infos), []
        )


__all__ = ["ListInfo"]
