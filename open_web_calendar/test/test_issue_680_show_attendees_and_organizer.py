# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Test showing the participants.

See https://github.com/niccokunzmann/open-web-calendar/issues/680
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from icalendar import vCalAddress

from open_web_calendar.convert.events import ConvertToEvents

if TYPE_CHECKING:
    from flask.testing import FlaskClient


@pytest.fixture
def event(client: FlaskClient, calendar_urls) -> dict[str, dict]:
    """Return an event with attendees."""
    events = client.get(
        f"/calendar.events.json?url={calendar_urls['issue-680-nextcloud']}&from=2025-04-05&to=2025-04-06&timezone=Europe/Zurich"
    ).json
    assert len(events) == 1
    return events[0]


@pytest.fixture
def participants(event) -> dict[str, dict]:
    """The particapants by name."""
    result = {}
    for i, participant in enumerate(event["participants"]):
        participant["index"] = i
        result[participant["name"]] = participant
    return result


def test_organizer_is_present(participants):
    """Check the details of the organizer."""
    organizer = participants["Test User"]
    assert organizer["name"] == "Test User"
    assert organizer["type"] == "INDIVIDUAL"
    assert organizer["email"] == "niccokunzmann+test.quelltext.ocloud.de@gmail.com"
    assert organizer["role"] == "ORGANIZER"
    assert organizer["index"] == 0, "the organizer should be the first always"
    assert organizer["css"] == [
        "PARTICIPANT",
        "PARTICIPANT-INDIVIDUAL",
        "PARTICIPANT-ORGANIZER",
        "PARTICIPANT-NEEDS-ACTION",
    ]


def test_attendee_nicco(participants):
    """Check the details of the first attendee."""
    attendee = participants["Nicco Kunzmann"]
    assert attendee["name"] == "Nicco Kunzmann"
    assert attendee["type"] == "INDIVIDUAL"
    assert attendee["email"] == "nicco@posteo.net"
    assert attendee["role"] == "REQ-PARTICIPANT"
    assert attendee["index"] != 0, "the organizer should be the first always"


def test_attendee_yemaya(participants):
    """Check that yemaya also has the right participant details."""
    attendee = participants["Yemaya"]
    assert attendee["name"] == "Yemaya"
    assert attendee["type"] == "GROUP"
    assert attendee["email"] == "yemaya@posteo.net"
    assert attendee["role"] == "CHAIR"
    assert attendee["index"] != 0, "the organizer should be the first always"


def test_empty_params():
    """If no params are given, this should still contain all values."""
    addr = vCalAddress("mailto:asd@asdf.com")
    attendee = ConvertToEvents.create_participant_from(addr)
    assert attendee["name"] == "asd@asdf.com"
    assert attendee["type"] == "INDIVIDUAL", "RFC 5545:  Default is INDIVIDUAL"
    assert attendee["email"] == "asd@asdf.com"
    assert attendee["role"] == "REQ-PARTICIPANT", "RFC5545: Default is REQ-PARTICIPANT"
    assert attendee["css"] == [
        "PARTICIPANT",
        "PARTICIPANT-INDIVIDUAL",
        "PARTICIPANT-REQ-PARTICIPANT",
        "PARTICIPANT-NEEDS-ACTION",
    ]


def test_participants_are_added_with_sent_by(todo):
    """When adding the participants, the principal's email is used."""
