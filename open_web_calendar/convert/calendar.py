# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Convert the source links according to the specification to a list of calendars."""

from typing import Any

from flask import jsonify

from open_web_calendar.calendars.base import Calendars
from open_web_calendar.convert.base import ConversionStrategy


class ConvertToCalendars(ConversionStrategy):
    """Create a list of metadata for all the calendars.

    The result should be like this:
    [
        {
            # for each url
            index: int,  # sorted by index
            url: str,
            errors: []  # would usually be 0/1 error
            calendars: [  # can be empty on error
                {
                    # for each possible calendar
                    index: int,  # sorted by index in the file. We expect one calendar per file
                    color: color # influenced by the url and the color attribute
                    categories: ["cat", ...],
                    css-classes: ["css-class", ...],
                    name: str  # also influenced by the url config
                    description: str # also influenced by the url config
                }
            ]
        }, ...
    ]
    """

    def created(self):
        """I was just created with a spec."""
        self.calendars: list[dict[str, Any]] = []

    def collect_components_from(self, index: int, calendars: Calendars):
        """Collect all calendars in use."""
        for i, calendar in enumerate(calendars.get_icalendars()):
            self.calendars.append(
                {
                    "index": index,
                    "innerIndex": i,  # a file can contain several calendars
                    "url": self.specification["url"][index],
                }
            )

    def merge(self):
        """Merge all retrieved calendars."""
        return jsonify(self.calendars)


__all__ = ["ConvertToCalendars"]
