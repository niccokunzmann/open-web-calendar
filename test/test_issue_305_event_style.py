"""This tests that events receive the right styling.

See https://github.com/niccokunzmann/open-web-calendar/issues/305
"""
import pytest
from app import ConvertToDhtmlx
from collections import namedtuple

CATEGORY = namedtuple("CATEGORY", ["cats"])

@pytest.mark.parametrize(
    "event,expected_classes",
    [
        ({"UID": "test123"}, ["UID-test123"]),
        ({"CATEGORIES": CATEGORY(["CAT1"])}, ["CATEGORY-CAT1"]),
        ({"TRANSP": "OPAQUE"}, ["TRANSP-OPAQUE"]),
        ({"TRANSP": "TRANSPARENT"}, ["TRANSP-TRANSPARENT"]),
    ]
)
def test_get_event_classes(event, expected_classes):
    """Check that event classes are correctly extracted."""
    dhx = ConvertToDhtmlx({"timezone":"Europe/London"})
    classes = dhx.get_event_classes(event)
    assert classes == expected_classes


@pytest.mark.parametrize(
    "calendar,start,stop,uid,classes",
    [
        ("event-with-categories", "2023-03-04", "2023-03-05", "UYDQSG9TH4DE0WM3QFL2J", ["event", "UID-UYDQSG9TH4DE0WM3QFL2J", "CATEGORY-APPOINTMENT", "CATEGORY-EDUCATION", 'CALENDAR-0']),
        ("issue-135-free-busy", "2022-11-18", "2022-11-23", "83E6A2ED-D816-4E6F-94B5-251A101C6E36", ["UID-83E6A2ED-D816-4E6F-94B5-251A101C6E36", "STATUS-CONFIRMED", "TRANSP-OPAQUE"])
    ]
)
def test_classes_of_events(client, calendar, start, stop, uid, classes, calendar_urls):
    """Make sure that events have certain classes in them."""
    response = client.get(f"/calendar.events.json?url={calendar_urls[calendar]}&timezone=UTC&timeshift=0&from={start}&to={stop}")
    events = [event for event in response.json if event["uid"] == uid]
    assert len(events) >= 1
    for event in events:
        print(classes)
        print(event["css-classes"])
        assert set(classes) <= set(event["css-classes"])
