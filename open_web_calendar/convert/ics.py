# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Convert the source links according to the specification to an ICS file."""

import datetime
from copy import deepcopy
from functools import lru_cache

from flask import Response
from icalendar import Calendar, Event, Timezone
from icalendar.prop import vDDDTypes
from mergecal import merge_calendars

from open_web_calendar.calendars.base import Calendars

from .base import ConversionStrategy


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

    @staticmethod
    @lru_cache(maxsize=128)
    def get_timezone(tzid, first_date, last_date):
        """Cache generated definitions; unknown timezone IDs cannot be expanded."""
        try:
            return Timezone.from_tzid(tzid, first_date=first_date, last_date=last_date)
        except ValueError:
            return None

    def collect_components_from(self, calendar_index: int, calendars: Calendars):
        with self.lock:
            self.components.extend(calendars.get_icalendars())

    def convert_error(self, error: str, url: str, tb_s: str):
        """Create an error which can be used by the dhtmlx scheduler."""
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
        first_date = Timezone.DEFAULT_FIRST_DATE
        last_date = Timezone.DEFAULT_LAST_DATE
        for event in calendar.events:
            for name in ("DTSTART", "DTEND", "RECURRENCE-ID"):
                value = getattr(event.get(name), "dt", None)
                if isinstance(value, datetime.date):
                    first_date = min(first_date, datetime.date(value.year, 1, 1))
                    last_date = max(
                        last_date,
                        datetime.date(value.year + 1, 1, 1)
                        if value.year < datetime.MAXYEAR
                        else datetime.date.max,
                    )
        for tzid in sorted(calendar.get_missing_tzids()):
            timezone = self.get_timezone(tzid, first_date, last_date)
            if timezone is not None:
                # Keep definitions before their uses and isolate the cached value.
                calendar.subcomponents.insert(0, deepcopy(timezone))
        return Response(calendar.to_ical(), mimetype="text/calendar")


__all__ = ["ConvertToICS"]
