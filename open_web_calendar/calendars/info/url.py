# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Extract calendar information from a URL."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from open_web_calendar.calendars.info.interface import CalendarInfoInterface


class URLInfo(CalendarInfoInterface):
    """Information from an icalendar url."""

    def __init__(self, url):
        """Create a new URL info."""
        self._url = urlparse(url)

    @property
    def calendar_name(self) -> str | None:
        """Return the name of the calendar."""
        path = Path(self._url.path)
        return path.stem or self._url.hostname


__all__ = ["URLInfo"]
