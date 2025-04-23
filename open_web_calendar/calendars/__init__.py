# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""A unified interface to calendars from different sources."""

from .base import Calendars
from .caldav import CalDAVCalendars
from .errors import InvalidCalendars
from .ics import ICSCalendars

__all__ = [
    "CalDAVCalendars",
    "Calendars",
    "ICSCalendars",
    "InvalidCalendars",
]
