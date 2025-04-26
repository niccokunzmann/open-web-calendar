# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test the calendars endpoint.

See https://github.com/niccokunzmann/open-web-calendar/issues/762
"""

import pytest

from open_web_calendar.calendars.info import DictInfo, ListInfo


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


param_cls = pytest.mark.parametrize("cls", [ListInfo, DictInfo])

@pytest.mark.parametrize("attr", INT_ATTR + STR_ATTR)
@param_cls
def test_empty_means_none(attr, cls):
    """None is the default"""
    assert getattr(cls(), attr) is None

@param_cls
def test_categories_are_empty(cls, list_attr):
    """Categories are a list always."""
    assert getattr(cls(), list_attr) == []


def test_get_str_attr_from_dict(str_attr, title):
    """Just get the attribute."""
    assert getattr(DictInfo({str_attr:title}), str_attr) == title


def test_get_int_attr_from_dict(int_attr, index):
    """Just get the attribute."""
    assert getattr(DictInfo({int_attr:index}), int_attr) == index


def test_get_list_attr_from_dict(list_attr, title):
    """Just get the attribute."""
    assert getattr(DictInfo({list_attr:[title]}), list_attr) == [title]


def test_get_first_str_in_list(str_attr, title):
    """The first one is in use."""
    assert getattr(ListInfo([DictInfo({str_attr:title}), DictInfo({str_attr:"lalalaa"})]), str_attr) == title


def test_skip_if_first_str_is_empty(str_attr, title):
    """The first one is in use."""
    assert getattr(ListInfo([DictInfo(), DictInfo({str_attr:title})]), str_attr) == title


def test_get_first_int_in_list(int_attr, index):
    """The first one is in use."""
    assert getattr(ListInfo([DictInfo({int_attr:index}), DictInfo({int_attr:20})]), int_attr) == index


def test_skip_if_first_int_is_empty(int_attr, index):
    """The first one is in use."""
    assert getattr(ListInfo([DictInfo(), DictInfo({int_attr:index})]), int_attr) == index


def test_categories_in_use(title):
    """Categories get added up."""
    assert ListInfo([DictInfo(calendar_categories=[title])]).calendar_categories == [title]

def test_categories_added(title):
    """Categories get added up."""
    assert ListInfo([DictInfo(calendar_categories=[title]), DictInfo(calendar_categories=["cat"])]).calendar_categories == [title, "cat"]


@pytest.fixture(params = [[], [DictInfo()], [DictInfo(calendar_categories=["cat1"])]])
def list_info(request):
    """Different categories listed."""
    return ListInfo(request.param)


def test_empty_css():
    """The categories include the index."""
    assert ListInfo().css_classes == []


def test_css_uses_index(list_info:ListInfo, index):
    """The categories include the index."""
    list_info.set(calendar_index=index)
    assert f"CALENDAR-INDEX-{index}" in list_info.css_classes


def test_css_uses_categories(list_info:ListInfo, title):
    """The categories include the index."""
    list_info.set(calendar_categories=[title])
    assert f"CATEGORY-{title}" in list_info.css_classes
