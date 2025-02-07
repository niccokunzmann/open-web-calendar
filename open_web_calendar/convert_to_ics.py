# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

import datetime

from flask import Response
from icalendar import Calendar, Event, Timezone
from icalendar.prop import vDDDTypes
from mergecal import merge_calendars

from .conversion_base import ConversionStrategy


class ConvertToICS(ConversionStrategy):
    """Convert events to dhtmlx. This conforms to a stratey pattern."""

    def created(self):
        self.title = self.specification["title"]
        self.timezones = set()  # ids

    def is_event(self, component):
        """Whether a component is an event."""
        return isinstance(component, Event)

    def is_timezone(self, component):
        """Whether a component is an event."""
        return isinstance(component, Timezone)

    def collect_components_from(self, calendar_index, calendars):
        with self.lock:
            self.components.extend(calendars)

    def convert_error(self, error, url, tb_s):
        """Create an error which can be used by the dhtmlx scheduler."""
        event = Event()
        event["DTSTART"] = event["DTEND"] = vDDDTypes(datetime.datetime.now())
        event["SUMMARY"] = type(error).__name__
        event["DESCRIPTION"] = str(error) + "\n\n" + tb_s
        event["UID"] = "error" + str(id(error))
        if url:
            event["URL"] = url
        calendar = Calendar()
        calendar.add_component(event)
        return calendar

    def merge(self):
        calendar = merge_calendars(self.components + [Calendar()])
        calendar["VERSION"] = "2.0"
        calendar["PRODID"] = "open-web-calendar"
        calendar["CALSCALE"] = "GREGORIAN"
        calendar["METHOD"] = "PUBLISH"
        calendar["X-WR-CALNAME"] = self.title
        calendar["NAME"] = self.title
        calendar["X-PROD-SOURCE"] = self.specification["source_code"]
        return Response(calendar.to_ical(), mimetype="text/calendar")
