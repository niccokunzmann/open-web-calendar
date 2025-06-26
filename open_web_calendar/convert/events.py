# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Convert the source links according to the specification to a list of events."""

from __future__ import annotations

import datetime
import zoneinfo
from html import escape
from typing import TYPE_CHECKING, Any
from urllib.parse import unquote

from dateutil.parser import parse as parse_date
from flask import jsonify
from icalendar_compatibility import Description, Location, LocationSpec

from .base import ConversionStrategy

if TYPE_CHECKING:
    from icalendar import Event, vCalAddress

    from open_web_calendar.calendars.base import Calendars


def is_date(date):
    """Whether the date is a datetime.date and not a datetime.datetime"""
    return isinstance(date, datetime.date) and not isinstance(date, datetime.datetime)


class ConvertToEvents(ConversionStrategy):
    """Convert events to dhtmlx. This conforms to a stratey pattern.

    - timeshift_minutes is the timeshift specified by the calendar
        for dates.
    """

    def created(self):
        """Set attribtues when created."""
        try:
            self.timezone = zoneinfo.ZoneInfo(self.specification["timezone"])
        except (zoneinfo.ZoneInfoNotFoundError, ValueError):
            # same as pytz.FixedOffset(-int(self.specification["timeshift"]))
            td = datetime.timedelta(minutes=-int(self.specification["timeshift"]))
            self.timezone = datetime.timezone(td)
        self.today = today = (
            parse_date(self.specification["date"]).replace(tzinfo=self.timezone)
            if self.specification.get("date")
            else datetime.datetime.now(self.timezone)
        )
        self.to_date = (
            parse_date(self.specification["to"]).replace(tzinfo=self.timezone)
            if self.specification.get("to")
            else today.replace(year=today.year + 1)
        )
        self.from_date = (
            parse_date(self.specification["from"]).replace(tzinfo=self.timezone)
            if self.specification.get("from")
            else today.replace(year=today.year - 1)
        )

    def date_to_string(self, date):
        """Convert a date to a string."""
        # use ISO format
        # see https://docs.dhtmlx.com/scheduler/howtostart_nodejs.html#step4implementingcrud
        # see https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat
        # see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        if is_date(date):
            date = datetime.datetime(
                date.year, date.month, date.day, tzinfo=self.timezone
            )
        elif date.tzinfo is None:
            date = date.replace(tzinfo=self.timezone)
        # convert to other timezone, see https://stackoverflow.com/a/54376154
        viewed_date = date.astimezone(self.timezone)
        return viewed_date.strftime("%Y-%m-%d %H:%M")

    @property
    def location_spec(self) -> LocationSpec:
        return LocationSpec(
            geo_url=self.specification.get("event_url_geo", ""),
            text_url=self.specification.get("event_url_location", ""),
        )

    @classmethod
    def get_participants(cls, event: Event) -> dict[str, Any]:
        """Return the participants of the event."""
        participants = []
        organizer = event.get("ORGANIZER")
        if organizer is not None:
            participants.append(
                cls.create_participant_from(
                    organizer, role="ORGANIZER", is_oragnizer=True
                )
            )
        attendees = event.get("ATTENDEE", [])
        if not isinstance(attendees, list):
            attendees = [attendees]
        for attendee in attendees:
            participants.append(cls.create_participant_from(attendee))
        return participants

    @classmethod
    def create_participant_from(
        cls,
        address: vCalAddress,
        role: str = "REQ-PARTICIPANT",
        is_oragnizer: bool = False,  # noqa: FBT001
    ) -> dict[str, Any]:
        """Create a participant with default values."""
        participant = {}
        participant["type"] = pt = address.params.get("CUTYPE", "INDIVIDUAL")
        participant["email"] = email = unquote(
            address[7:] if address.lower().startswith("mailto:") else str(address)
        )
        participant["name"] = address.params.get("CN", email)
        participant["status"] = status = address.params.get("PARTSTAT", "NEEDS-ACTION")
        participant["role"] = pr = address.params.get("ROLE", role)
        participant["css"] = [
            "PARTICIPANT",
            f"PARTICIPANT-{pt}",
            f"PARTICIPANT-{pr}",
            f"PARTICIPANT-{status}",
        ]
        participant["is_oragnizer"] = is_oragnizer
        return participant

    def convert_ical_event(self, calendar_index, calendar_event: Event):
        start = calendar_event.start
        end = calendar_event.end
        if is_date(start) and is_date(end) and start == end:
            end = start + datetime.timedelta(days=1)
        location = Location(calendar_event, self.location_spec)
        name = calendar_event.get("SUMMARY", "")
        sequence = calendar_event.sequence
        uid = calendar_event.uid
        start_date = self.date_to_string(start)
        location_map: dict[str, str] | None = {
            "text": location.text,
            "url": location.url,
        }
        if not location_map["text"] and not location_map["url"]:
            location_map = None
        return {
            "start_date": start_date,
            "end_date": self.date_to_string(end),
            "start_date_iso": start.isoformat(),
            "end_date_iso": end.isoformat(),
            "start_date_iso_0": start.isoformat(),
            "end_date_iso_0": end.isoformat(),
            "text": name,
            "description": self.get_event_description(calendar_event),
            "location": location_map,
            "uid": uid,
            "ical": calendar_event.to_ical().decode("UTF-8"),
            "sequence": sequence,
            "recurrence": None,
            "url": calendar_event.get("URL"),
            "id": uid + "-" + start_date.replace(" ", "-").replace(":", "-"),
            "type": "event",
            "color": calendar_event.color,
            "categories": self.get_event_categories(calendar_event),
            "css-classes": ["event"]
            + self.get_event_classes(calendar_event)
            + [f"CALENDAR-INDEX-{calendar_index}"],
            "participants": self.get_participants(calendar_event),
            "owc": {
                attr: value
                for attr, value in calendar_event.items()
                if attr.lower().startswith("x-owc")
            },
            "calendar-index": calendar_index,
        }

    def convert_error(self, error: str, url: str, tb_s: str):
        """Create an error which can be used by the dhtmlx scheduler."""
        # always add the error within the requested time range
        now = self.from_date
        now_iso = now.isoformat()
        now_s = self.date_to_string(now)
        return {
            "start_date": now_s,
            "end_date": now_s,
            "start_date_iso": now_iso,
            "end_date_iso": now_iso,
            "start_date_iso_0": now_iso,
            "end_date_iso_0": now_iso,
            "text": escape(error.split(":")[0]),
            "description": self.clean_html(escape(error)),
            "traceback": self.clean_html(escape(tb_s)),
            "location": None,
            "geo": None,
            "uid": "error",
            "categories": [],
            "ical": "",
            "sequence": 0,
            "recurrence": None,
            "url": url,
            "id": id(error),
            "type": "error",
            "css-classes": ["error"],
        }

    def get_event_description(self, event: Event):
        """Return a formatted description of the event.

        HTML is cleaned.
        """
        description = Description(event).html
        return self.clean_html(description)

    def merge(self):
        return jsonify(self.components)

    def collect_components_from(self, calendar_index: int, calendars: Calendars):
        # see https://stackoverflow.com/a/16115575/1320237
        events = calendars.get_events_between(self.from_date, self.to_date)
        with self.lock:
            for event in events:
                json_event = self.convert_ical_event(calendar_index, event)
                self.components.append(json_event)

    def get_event_classes(self, event) -> list[str]:
        """Return the CSS classes that should be used for the event styles."""
        classes = []
        for attr in ["UID", "TRANSP", "STATUS", "CLASS", "PRIORITY"]:
            value = event.get(attr)
            if value is not None:
                classes.append(f"{attr}-{value}")
        if event.get("CLASS") not in [None, "PUBLIC", "CONFIDENTIAL", "PRIVATE"]:
            classes.append("CLASS-PRIVATE")  # unrecognized is private
        for category in self.get_event_categories(event):
            classes.append(f"CATEGORY-{category}")
        return classes

    def get_event_categories(self, event: Event) -> list[str]:
        """Return the categories of the event."""
        return event.categories


__all__ = ["ConvertToEvents"]
