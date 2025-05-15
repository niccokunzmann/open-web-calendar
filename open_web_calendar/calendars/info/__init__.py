# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Information about calendars."""

from .dict import DictInfo
from .ics import IcalInfo
from .interface import CalendarInfoInterface
from .list import ListInfo
from .url import URLInfo

__all__ = ["CalendarInfoInterface", "DictInfo", "IcalInfo", "ListInfo", "URLInfo"]
