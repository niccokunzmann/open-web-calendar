# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations


class CalendarInfoInterface:
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

    @property
    def css_classes(self) -> list[str]:
        """Return the CSS classes of the calendar."""
        result = []
        if self.calendar_index is not None:
            result.append(f"CALENDAR-INDEX-{self.calendar_index}")
        for category in self.calendar_categories:
            result.append(f"CATEGORY-{category}")
        return result


__all__ = ["CalendarInfoInterface"]
