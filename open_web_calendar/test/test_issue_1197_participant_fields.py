# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""The participants of an event have an "is_organizer" field.

See https://github.com/niccokunzmann/open-web-calendar/issues/1197
"""

CALENDAR = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:participants
DTSTART:20250913T090000Z
DTEND:20250913T100000Z
SUMMARY:Meeting
ORGANIZER;CN=The Boss:mailto:boss@example.com
ATTENDEE;CN=Worker:mailto:worker@example.com
END:VEVENT
END:VCALENDAR"""


def test_participants_have_is_organizer(client, cache_url):
    """The organizer flag is spelled is_organizer."""
    url = "http://test.examples.local/participants.ics"
    cache_url(url, CALENDAR)
    response = client.get(
        f"/calendar.events.json?url={url}&timezone=UTC&from=2025-09-10&to=2025-09-20"
    )
    assert response.status_code == 200
    participants = response.json[0]["participants"]
    by_email = {p["email"]: p for p in participants}
    assert by_email["boss@example.com"]["is_organizer"] is True
    assert by_email["worker@example.com"]["is_organizer"] is False
    for participant in participants:
        assert "is_oragnizer" not in participant
