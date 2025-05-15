# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Convert the source links according to the specification to a list of calendars."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from open_web_calendar.calendars.info.dict import DictInfo
from open_web_calendar.calendars.info.list import ListInfo
from open_web_calendar.calendars.info.url import URLInfo
from open_web_calendar.convert.base import ConversionStrategy
from open_web_calendar.error import convert_error_message_to_json

if TYPE_CHECKING:
    from open_web_calendar.calendars.base import Calendars


class ConvertToCalendars(ConversionStrategy):
    """Create a list of metadata for all the calendars.

    The result should be like this:
    {
        "calendars": [
            {
                url_index: int,
                calendar_index: int,
                name: str,
                description: str,
                color: str,
                categories: [str, ...],
                css-classes: [str, ...], # the first 2 classes identify the events
            }
        ],
        errors: [
            {
                ...  # json_error
            }
        ]
    }
    """

    def created(self):
        """I was just created with a spec."""
        self.calendars: list[dict[str, Any]] = []
        self.errors = []

    def get_default_info_for_url(self, index: int):
        """Return default information for the calendar."""
        urls: list[str] = self.specification.get("url", [])
        if index >= len(urls):
            return DictInfo()
        return URLInfo(urls[index])

    def collect_components_from(self, index: int, calendars: Calendars):
        """Collect all calendars in use."""
        default = self.get_default_info_for_url(index)
        for calendar_info in calendars.get_infos():
            info = ListInfo([calendar_info, default])
            self.calendars.append(
                {
                    "url_index": index,
                    "calendar_index": info.calendar_index_in_file,
                    "id": f"calendar-{index}-{info.calendar_index_in_file}",
                    "name": self.clean_html(info.calendar_name or ""),
                    "description": self.clean_html(info.calendar_description or ""),
                    "color": self.clean_html(info.calendar_color or ""),
                    "categories": [
                        self.clean_html(category)
                        for category in info.calendar_categories
                    ],
                    "css-classes": [self.clean_html(f"CALENDAR-INDEX-{index}")]
                    + [self.clean_html(category) for category in info.css_classes],
                }
            )

    def clean_html(self, html):
        """Clean the HTML for JSON content."""
        return super().clean_html(html).strip()

    def merge(self):
        """Merge all retrieved calendars."""
        return self.jsonify({"calendars": self.calendars, "errors": self.errors})

    def convert_error(self, error: str, url: str, tb_s: str):
        """Tell the client more about the error."""
        self.errors.append(
            convert_error_message_to_json(
                f"Error in {type(self).__name__}",
                error,
                url,
                tb_s,
            )
        )


__all__ = ["ConvertToCalendars"]
