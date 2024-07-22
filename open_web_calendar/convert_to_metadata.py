# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

from flask import jsonify

from .conversion_base import CalendarInfo, ConversionStrategy


class ConvertToMetadata(ConversionStrategy):
    """Convert the specification into metadata information about the calendars given."""

    def created(self):
        """This instance is created."""
        self.components = {"calendars": {}, "errors": {}}

    def collect_components_from(self, calendar_info: CalendarInfo):
        self.add_component(calendar_info.to_json())

    def add_component(self, component: dict):
        with self.lock:
            kind = f"{component['type']}s"
            self.components[kind][component["id"]] = component

    def convert_error(self, err: Exception, url: str, traceback: str):
        """Convert an error."""
        return {
            "type": "error",
            "id": url,
            "url": url,
            "traceback": traceback,
            "error": str(err),
        }

    def merge(self):
        """Return the response."""
        return jsonify(self.components)


__all__ = ["ConvertToMetadata"]
