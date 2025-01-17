# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Test choosing the map for the location and geo links."""

from flask.testing import FlaskClient


def test_event_in_mountain_view(client: FlaskClient, calendar_urls):
    """The event has a location with geo."""
    events = client.get(
        f"/calendar.events.json?url={calendar_urls['issue-23-location-berlin']}&from=2025-01-15&to=2025-01-17"
    ).json
    event = events[0]
    assert (
        event["location"]["text"]
        == "Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika"
    )
    url: str = event["location"]["url"]
    assert "37.386013" in url
    assert "-122.082932" in url
    assert url.startswith("https://www.openstreetmap")


def test_event_in_berlin_with_altrep(client: FlaskClient, calendar_urls):
    """The event has a location with altrep."""
    events = client.get(
        f"/calendar.events.json?url={calendar_urls['issue-23-location-berlin']}&from=2025-01-12&to=2025-01-15"
    ).json
    event = events[0]
    print(event["location"])
    assert event["location"]["text"] == "Berlin"
    url: str = event["location"]["url"]
    assert (
        url == "https://www.openstreetmap.org/relation/62422"
    ), "should be the same url as in altrep"


def test_event_in_berlin_text_only(client: FlaskClient, calendar_urls):
    """The event has a location text only."""
    events = client.get(
        f"/calendar.events.json?url={calendar_urls['issue-23-location-berlin']}&from=2025-01-10&to=2025-01-12"
    ).json
    event = events[0]
    print(event["location"])
    assert event["location"]["text"] == "Berlin"
    url: str = event["location"]["url"]
    assert "Berlin" in url


def test_replace_geo_url(client: FlaskClient, calendar_urls):
    """Replace the geo url."""
    events = client.get(
        f"/calendar.events.json?url={calendar_urls['issue-23-location-berlin']}&from=2025-01-15&to=2025-01-17&event_url_geo=x{{lat}}y{{lon}}z{{zoom}}"
    ).json
    event = events[0]
    assert (
        event["location"]["text"]
        == "Mountain View, Santa Clara County, Kalifornien, Vereinigte Staaten von Amerika"
    )
    url: str = event["location"]["url"]
    assert url == "x37.386013y-122.082932z16"
