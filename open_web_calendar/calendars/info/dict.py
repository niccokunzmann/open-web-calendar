# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

from typing import Optional

from open_web_calendar.calendars.info.interface import CalendarInfoInterface


class DictInfo(CalendarInfoInterface):
    """Calendar information stored in a dictionary."""

    def __init__(
        self, info: Optional[dict[str, str | list[str] | int | None]] = None, **kwargs
    ):
        self._info = {}
        self.set(info)
        self.set(kwargs)

    @property
    def calendar_name(self) -> str | None:
        """Return the name of the calendar."""
        return self._info.get("calendar_name")

    @property
    def calendar_url(self) -> str | None:
        """Return the URL of the calendar."""
        return self._info.get("calendar_url")

    @property
    def calendar_index(self) -> int | None:
        """Return the index of the URL of the calendar."""
        return self._info.get("calendar_index")

    @property
    def calendar_description(self) -> str | None:
        """Return the description of the calendar."""
        return self._info.get("calendar_description")

    @property
    def calendar_color(self) -> str | None:
        """Return the color of the calendar."""
        return self._info.get("calendar_color")

    @property
    def calendar_categories(self) -> list[str]:
        """Return the categories of the calendar."""
        return self._info.get("calendar_categories", [])

    def set(
        self, values: Optional[dict[str, str | list[str] | int | None]] = None, **kwargs
    ):
        """Set values."""
        if values:
            self._info.update(values)
        if kwargs:
            self._info.update(kwargs)


__all__ = ["DictInfo"]
