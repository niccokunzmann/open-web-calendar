# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""
This test the algorithm written
in the api.md file.
"""

import pytest
from werkzeug.datastructures import MultiDict

from open_web_calendar.app import (
    cache_url,
    get_default_specification,
    get_specification,
)


def test_specification_equals_default_specification_by_default():
    assert get_specification(query=MultiDict({})) == get_default_specification()


def test_specification_overrides_attributes_from_default_specification():
    assert get_default_specification()["css"] == ""
    assert get_specification(query=MultiDict({"css": "test"}))["css"] == "test"


with_url = pytest.mark.parametrize(
    "url",
    [
        "https://tets.io/aksdkkj.json",
        "https://alskdj.asd.de/asld/asdasd.yml",
    ],
)


@with_url
def test_specification_prefers_url_over_default(url):
    cache_url(url, '{"css": "123"}')
    assert (
        get_specification(query=MultiDict({"specification_url": url}))["css"] == "123"
    )


@with_url
def test_url_parameters_are_more_important_than_specification_url(url):
    cache_url(url, '{"test": "123"}')
    assert (
        get_specification(query=MultiDict({"specification_url": url, "test": "test"}))[
            "test"
        ]
        == "test"
    )


@with_url
def test_specification_can_be_loaded_from_yml_files(url):
    cache_url(url, 'test: "123"')
    assert (
        get_specification(query=MultiDict({"specification_url": url}))["test"] == "123"
    )


@pytest.mark.parametrize(
    ("string", "expected_bool"),
    [
        ("true", True),
        ("True", True),
        ("false", False),
        ("False", False),
    ],
)
def test_false_and_true(string, expected_bool):
    """Check that True and False work."""
    value = get_specification(query=MultiDict({"param": string}))["param"]
    assert bool(value) == bool(expected_bool)
    assert (not value) == (not expected_bool)


def test_boolean_values_of_parameters():
    """Some parameters have boolean values."""
    spec = get_specification(
        query=MultiDict({"clean_html_style": "false", "clean_html_links": "True"})
    )
    assert spec["clean_html_embedded"] is True, "default"
    assert spec["clean_html_style"] is False
    assert spec["clean_html_links"] is True
