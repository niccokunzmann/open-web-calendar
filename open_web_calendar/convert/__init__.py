# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Strategies for converting content between different formats."""

from .events import ConvertToEvents
from .ics import ConvertToICS

__all__ = [
    "ConvertToEvents",
    "ConvertToICS",
]
