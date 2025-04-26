# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test the calendars endpoint.

See https://github.com/niccokunzmann/open-web-calendar/issues/762
"""

import json
import pytest
from icalendar import Calendar

from open_web_calendar.calendars.ics import ICSCalendars
from open_web_calendar.calendars.info import (
    CalendarInfoInterface,
    DictInfo,
    IcalInfo,
    ListInfo,
)
from open_web_calendar.convert.calendar import ConvertToCalendars


@pytest.fixture(params=["My Calendar", "Company Calendar"])
def title(request) -> str:
    return request.param


@pytest.fixture(params=[0, 1, 10])
def index(request) -> int:
    return request.param


STR_ATTR = ["calendar_name", "calendar_url", "calendar_description", "calendar_color"]


@pytest.fixture(params=STR_ATTR)
def str_attr(request) -> str:
    return request.param


INT_ATTR = ["calendar_index"]


@pytest.fixture(params=INT_ATTR)
def int_attr(request) -> str:
    return request.param


LIST_ATTR = ["calendar_categories"]


@pytest.fixture(params=LIST_ATTR)
def list_attr(request) -> str:
    return request.param


param_cls = pytest.mark.parametrize("cls", [ListInfo, DictInfo, IcalInfo])


@pytest.fixture(params=[ListInfo, DictInfo])
def empty_info(request) -> CalendarInfoInterface:
    return request.param()


@pytest.mark.parametrize("attr", INT_ATTR + STR_ATTR)
def test_empty_means_none(attr, empty_info):
    """None is the default"""
    assert getattr(empty_info, attr) is None


def test_categories_are_empty(empty_info, list_attr):
    """Categories are a list always."""
    assert getattr(empty_info, list_attr) == []


def test_get_str_attr_from_dict(str_attr, title):
    """Just get the attribute."""
    assert getattr(DictInfo({str_attr: title}), str_attr) == title


def test_get_int_attr_from_dict(int_attr, index):
    """Just get the attribute."""
    assert getattr(DictInfo({int_attr: index}), int_attr) == index


def test_get_list_attr_from_dict(list_attr, title):
    """Just get the attribute."""
    assert getattr(DictInfo({list_attr: [title]}), list_attr) == [title]


def test_get_first_str_in_list(str_attr, title):
    """The first one is in use."""
    assert (
        getattr(
            ListInfo([DictInfo({str_attr: title}), DictInfo({str_attr: "lalalaa"})]),
            str_attr,
        )
        == title
    )


def test_skip_if_first_str_is_empty(str_attr, title):
    """The first one is in use."""
    assert (
        getattr(ListInfo([DictInfo(), DictInfo({str_attr: title})]), str_attr) == title
    )


def test_get_first_int_in_list(int_attr, index):
    """The first one is in use."""
    assert (
        getattr(
            ListInfo([DictInfo({int_attr: index}), DictInfo({int_attr: 20})]), int_attr
        )
        == index
    )


def test_skip_if_first_int_is_empty(int_attr, index):
    """The first one is in use."""
    assert (
        getattr(ListInfo([DictInfo(), DictInfo({int_attr: index})]), int_attr) == index
    )


def test_categories_in_use(title):
    """Categories get added up."""
    assert ListInfo([DictInfo(calendar_categories=[title])]).calendar_categories == [
        title
    ]


def test_categories_added(title):
    """Categories get added up."""
    assert ListInfo(
        [DictInfo(calendar_categories=[title]), DictInfo(calendar_categories=["cat"])]
    ).calendar_categories == [title, "cat"]


@pytest.fixture(params=[[], [DictInfo()], [DictInfo(calendar_categories=["cat1"])]])
def list_info(request):
    """Different categories listed."""
    return ListInfo(request.param)


def test_empty_css():
    """The categories include the index."""
    assert ListInfo().css_classes == []


def test_css_uses_index(list_info: ListInfo, index):
    """The categories include the index."""
    list_info.set(calendar_index=index)
    assert f"CALENDAR-INDEX-{index}" in list_info.css_classes


def test_css_uses_categories(list_info: ListInfo, title):
    """The categories include the index."""
    list_info.set(calendar_categories=[title])
    assert f"CATEGORY-{title}" in list_info.css_classes


def test_get_name_from_calendar(title):
    """Get the RFC 7986 name."""
    calendar = Calendar(NAME=title)
    print(calendar.to_ical().decode())
    assert IcalInfo(calendar).calendar_name == title


def test_get_description_from_calendar(title):
    """Get the RFC 7986 description."""
    calendar = Calendar(DESCRIPTION=title)
    assert IcalInfo(calendar).calendar_description == title


def test_get_color(title):
    """Get the RFC 7986 color."""
    calendar = Calendar(COLOR=title)
    assert IcalInfo(calendar).calendar_color == title


def test_get_categories(title):
    """Get the RFC 7986 categories."""
    calendar = Calendar()
    calendar.add("CATEGORIES", title)
    assert IcalInfo(calendar).calendar_categories == [title]


@pytest.fixture
def ics_calendars():
    return ICSCalendars.from_text(
        """
BEGIN:VCALENDAR
NAME:My Calendar
END:VCALENDAR
BEGIN:VCALENDAR
DESCRIPTION:My Calendar Description
END:VCALENDAR
BEGIN:VCALENDAR
COLOR:black
END:VCALENDAR
BEGIN:VCALENDAR
CATEGORIES:NOSE,WHOLS
END:VCALENDAR
"""
)

def test_get_calendar_indices(ics_calendars:ICSCalendars):
    """We want to have it easy with the index."""
    assert [info.calendar_index for info in ics_calendars.get_infos()] == [0, 1, 2, 3]


def test_get_calendar_names(ics_calendars:ICSCalendars):
    """We want to have it easy with the index."""
    assert [info.calendar_name for info in ics_calendars.get_infos()] == [
        "My Calendar",
        None,
        None,
        None,
    ]

def test_get_calendar_descriptions(ics_calendars:ICSCalendars):
    """We want to have it easy with the index."""
    assert [info.calendar_description for info in ics_calendars.get_infos()] == [
        None,
        "My Calendar Description",
        None,
        None,
    ]

def test_get_calendar_colors(ics_calendars:ICSCalendars):
    """We want to have it easy with the index."""
    assert [info.calendar_color for info in ics_calendars.get_infos()] == [
        None,
        None,
        "black",
        None,
    ]

def test_get_calendar_categories(ics_calendars:ICSCalendars):
    """We want to have it easy with the index."""
    assert [info.calendar_categories for info in ics_calendars.get_infos()] == [
        [],
        [],
        [],
        ["NOSE", "WHOLS"],
    ]


class CleanedHTML(str):
    clean = True


@pytest.fixture
def merged(ics_calendars, index, monkeypatch) -> dict:
    """Convert a calendar and return the JSON."""
    cals = ConvertToCalendars({})
    monkeypatch.setattr(cals, "jsonify", lambda data: data)
    monkeypatch.setattr(cals, "clean_html", CleanedHTML)
    cals.collect_components_from(index, ics_calendars)
    return cals.merge()


def test_json_has_no_errors(merged):
    """Usually, there are no errors."""
    assert merged["errors"] == []

def test_we_have_several_calendars(merged):
    """We have several calendars."""
    assert len(merged["calendars"]) == 4

def test_index_merged(merged, index):
    """The index is in the right place."""
    for i, calendar in enumerate(merged["calendars"]):
        assert calendar["url_index"] == index
        assert calendar["calendar_index"] == i


def test_color_is_clean(merged):
    """Color is clean."""
    colors = [calendar["color"] for calendar in merged["calendars"]]
    assert all(color.clean for color in colors)
    assert colors == ["", "", "black", ""]

def test_name_is_clean(merged):
    """Color is clean."""
    names = [calendar["name"] for calendar in merged["calendars"]]
    assert all(name.clean for name in names)
    assert names == ["My Calendar", "", "", ""]

def test_desccription_is_clean(merged):
    """Color is clean."""
    desccriptions = [calendar["description"] for calendar in merged["calendars"]]
    assert all(desccription.clean for desccription in desccriptions)
    assert desccriptions == ["", "My Calendar Description", "", ""]


def test_categories_is_clean(merged):
    """Color is clean."""
    categories = [calendar["categories"] for calendar in merged["calendars"]]
    assert all(category.clean for cats in categories for category in cats)
    assert categories == [[], [], [], ["NOSE", "WHOLS"]]


def test_css_is_clean(merged):
    """Color is clean."""
    css_list = [calendar["css-classes"] for calendar in merged["calendars"]]
    assert all(cls.clean for cats in css_list for cls in cats)
    assert css_list == [["CALENDAR-INDEX-0"], ["CALENDAR-INDEX-1"], ["CALENDAR-INDEX-2"], ["CALENDAR-INDEX-3", "CATEGORY-NOSE", "CATEGORY-WHOLS"]]
