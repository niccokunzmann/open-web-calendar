# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Convert the source links according to the specification to an ICS file."""

import datetime
import re

from flask import Response
from icalendar import Calendar, Event, Timezone
from icalendar.prop import vDDDTypes
from icalendar_compatibility import Description
from mergecal import merge_calendars

from open_web_calendar.calendars.base import Calendars
from open_web_calendar.clean_html import remove_html

from .base import ConversionStrategy


class ConvertToICS(ConversionStrategy):
    """Convert events to ICS. This conforms to a strategy pattern."""

    html_description_property = "X-ALT-DESC"

    def clean_ics_html(self, html: str) -> str:
        """Clean and compact HTML before storing it in an ICS property."""
        cleaned_html = " ".join(self.clean_html(html).split())
        return re.sub(r">\s+<", "><", cleaned_html)

    def created(self):
        self.title = self.specification["title"]
        self.timezones = set()  # ids

    def is_event(self, component):
        """Whether a component is an event."""
        return isinstance(component, Event)

    def is_timezone(self, component):
        """Whether a component is an event."""
        return isinstance(component, Timezone)

    def collect_components_from(self, calendar_index: int, calendars: Calendars):
        with self.lock:
            self.components.extend(calendars.get_icalendars())

    def clean_html_descriptions(self, calendar: Calendar):
        """Clean HTML descriptions before serializing the ICS response."""
        for event in calendar.walk("VEVENT"):
            description = event.get(self.html_description_property)
            if description is None:
                continue
            descriptions = (
                description if isinstance(description, list) else [description]
            )
            cleaned_descriptions = []
            for value in descriptions:
                parameters = value.params.copy() if hasattr(value, "params") else {}
                cleaned_descriptions.append(
                    (self.clean_ics_html(str(value)), parameters)
                )
            del event[self.html_description_property]
            for value, parameters in cleaned_descriptions:
                event.add(self.html_description_property, value, parameters=parameters)

    def convert_error(self, error: str, url: str, tb_s: str):
        """Create an error event that appears in the ICS output."""
        event = Event()
        event["DTSTART"] = event["DTEND"] = vDDDTypes(datetime.datetime.now())
        event["SUMMARY"] = error
        event["DESCRIPTION"] = tb_s
        event["URL"] = url
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
        # Replace the event and only allow one event
        only_event = self.specification.get("set_event")
        if only_event:
            for event in calendar.events:
                calendar.subcomponents.remove(event)
            calendar.add_component(Event.from_ical(only_event))
        else:
            for event in calendar.events:
                description = Description(event)
                html = description.html
                if not html:
                    continue
                event["DESCRIPTION"] = description.text or remove_html(html)
                if "X-ALT-DESC" not in event:
                    event.add("X-ALT-DESC", html, parameters={"FMTTYPE": "text/html"})
        self.clean_html_descriptions(calendar)
        return Response(calendar.to_ical(), mimetype="text/calendar")


__all__ = ["ConvertToICS"]
