# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Errors."""


class InvalidCalendars(ValueError):
    """The content or URL provided cannot be used as calendars."""


__all__ = [
    "InvalidCalendars",
]
