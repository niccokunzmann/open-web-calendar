# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Caldav interface to retrieve calendars."""

from __future__ import annotations

import re
from datetime import date
from typing import TYPE_CHECKING

import caldav
from icalendar import vCalAddress

from open_web_calendar.calendars.base import Calendars
from open_web_calendar.url import URLCapability

if TYPE_CHECKING:
    from datetime import datetime

    import icalendar


def convert_to_date(dt: date) -> date:
    """Converts a date or datetime to a date"""
    return date(dt.year, dt.month, dt.day)


def validate_email(email):
    """valiedate the email.

    See https://grabaro.com/blog/understanding-and-implementing-regex-for-email-verification/
    """
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(regex, email))


class CalDAVCalendars(Calendars):
    """Return calendars from caldav."""

    @classmethod
    def from_url(cls, url: str):
        """Create an interface to calendars from a caldav URL.

        We should have a caldav URL here with username and password.

        Example:

            "https://username:password@nexcloud.mydomain.com/remote.php/dav/calendars/test/test_shared_by_other/"
        """
        capabilities = URLCapability.from_url(url)
        client = caldav.DAVClient(url=url)
        calendar = caldav.Calendar(client, url=url)
        return cls(calendar, capabilities)

    def __init__(
        self, calendar: caldav.Calendar, capability: URLCapability | None = None
    ):
        """Create a new CalDAV interface for one calendar."""
        self._calendar = calendar
        self._capability = URLCapability() if capability is None else capability

    def get_events_between(
        self, start: datetime, end: datetime
    ) -> list[icalendar.Event]:
        """Return a list of events that occur between start and end."""
        events: list[caldav.Event] = self._calendar.search(
            expand=True, comp_class=caldav.Event, start=start, end=end
        )
        result = []
        for caldav_event in events:
            result.extend(caldav_event.icalendar_instance.events)
        can_add_attendees = "true" if self.can_add_attendees() else "false"
        for event in result:
            event["X-OWC-CAN-ADD-ATTENDEE"] = can_add_attendees
        return result

    def get_icalendars(self) -> list[icalendar.Calendar]:
        """Return a list of ICS calendars."""
        events: list[caldav.Event] = self._calendar.events()
        return [event.icalendar_instance for event in events]

    def can_add_attendees(self) -> bool:
        """Wether we can add attendees in general."""
        return self._capability.can_add_email_attendee()

    def add_attendee_to_event(self, event: icalendar.Event, name: str, email: str):
        """Add an attendee to the event, checking that it is possible."""
        if not self.can_add_attendees():
            raise ValueError(
                "Adding attendees is not allowed. Set #can_add_email_attendee=true"
            )
        if not validate_email(email):
            raise ValueError(f"Invalid email address {email}")
        if len(name) > 100:
            raise ValueError("Name too long.")
        query_start = event.start
        query_end = query_start
        events = self.get_events_between(query_start, query_end)
        if event not in events:
            raise ValueError(
                f"The event \n{event.to_ical().decode()}\n"
                f"was not found among {len(events)} events."
            )
        uid = event["UID"]
        caldav_event = next(
            e for e in self._calendar.events() if e.icalendar_component["UID"] == uid
        )
        sequence = max(
            e.get("SEQUENCE", 0) for e in caldav_event.icalendar_instance.events
        )

        # An organizer is required or else we will not send emails.
        principal = self._calendar.client.principal()
        organizer = principal.get_vcal_address()
        event["ORGANIZER"] = organizer

        # we add the attendee
        attendee = vCalAddress("MAILTO:" + email)
        attendee.params["cn"] = name
        attendee.params["ROLE"] = "REQ-PARTICIPANT"
        attendee.params["CUTYPE"] = "INDIVIDUAL"
        attendee.params["PARTSTAT"] = "NEEDS-ACTION"
        attendee.params["RSVP"] = "TRUE"
        attendee.params["SENT-BY"] = str(organizer)
        event.add("attendee", attendee, encode=0)
        if event.get("STATUS") == "TENTATIVE":
            event["STATUS"] = "CONFIRMED"
        # event["SUMMARY"] += "✓"  # debug
        event["SEQUENCE"] = sequence + 1  # set as latest event
        if (
            "RECURRENCE-ID" not in event
            and len(caldav_event.icalendar_instance.events) == 1
        ):
            # we have to replace the event as it is not recurring
            for older_event in caldav_event.icalendar_instance.events:
                caldav_event.icalendar_instance.subcomponents.remove(older_event)
        caldav_event.icalendar_instance.add_component(event)
        caldav_event.save()


__all__ = ["CalDAVCalendars"]
