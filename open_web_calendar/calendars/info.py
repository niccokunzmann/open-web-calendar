# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Information about a calendar."""
from __future__ import annotations
from typing import Optional
import functools
import operator


class InfoInterface:
    """Information interface that should be provided by a calendar."""

    @property
    def calendar_name(self) -> str | None:
        """Return the name of the calendar."""
        return None

    @property
    def calendar_url(self) -> str | None:
        """Return the URL of the calendar."""
        return None

    @property
    def calendar_index(self) -> int | None:
        """Return the index of the URL of the calendar."""
        return None

    @property
    def calendar_description(self) -> str | None:
        """Return the description of the calendar."""
        return None

    @property
    def calendar_color(self) -> str | None:
        """Return the color of the calendar."""
        return None

    @property
    def calendar_categories(self) -> list[str]:
        """Return the categories of the calendar."""
        return []


class DictInfo(InfoInterface):
    """Calendar information stored in a dictionary."""

    def __init__(self, info: Optional[dict[str, str | list[str] | int | None]] = None, **kwargs):
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


    def set(self, values: Optional[dict[str, str | list[str] | int | None]] = None, **kwargs):
        """Set values."""
        if values:
            self._info.update(values)
        if kwargs:
            self._info.update(kwargs)

class ListInfo(InfoInterface):
    """Information about a calendar stored in a list."""

    def __init__(self, infos: Optional[list[InfoInterface]] = None):
        """Compose information about the calendar from different information sources."""
        self._mine = DictInfo()
        self._infos = [self._mine] + (infos or [])

    def set(self, values: Optional[dict[str, str | list[str] | int | None]] = None, **kwargs):
        """Set values."""
        self._mine.set(values)
        self._mine.set(kwargs)

    @property
    def calendar_name(self) -> str | None:
        """Return the name of the calendar."""
        return next((info.calendar_name for info in self._infos if info.calendar_name is not None), None)

    @property
    def calendar_url(self) -> str | None:
        """Return the URL of the calendar."""
        return next((info.calendar_url for info in self._infos if info.calendar_url is not None), None)

    @property
    def calendar_index(self) -> int | None:
        """Return the index of the URL of the calendar."""
        return next((info.calendar_index for info in self._infos if info.calendar_index is not None), None)

    @property
    def calendar_description(self) -> str | None:
        """Return the description of the calendar."""
        return next((info.calendar_description for info in self._infos if info.calendar_description is not None), None)

    @property
    def calendar_color(self) -> str | None:
        """Return the color of the calendar."""
        return next((info.calendar_color for info in self._infos if info.calendar_color is not None), None)

    @property
    def calendar_categories(self) -> list[str]:
        """Return the categories of the calendar."""
        return functools.reduce(operator.iadd, (info.calendar_categories for info in self._infos), [])

    @property
    def css_classes(self) -> list[str]:
        """Return the CSS classes of the calendar."""
        result = []
        if self.calendar_index is not None:
            result.append(f"CALENDAR-INDEX-{self.calendar_index}")
        for category in self.calendar_categories:
            result.append(f"CATEGORY-{category}")
        return result

___all__ = ["CalendarInfo", "InfoInterface", "DictInfo"]
