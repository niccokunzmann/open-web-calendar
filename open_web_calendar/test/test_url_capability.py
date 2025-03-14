# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""
Test that we can configure urls.

"""

import pytest

from open_web_calendar.url import URLCapability


def test_parse_from_url():
    """Test parsing from a url."""
    cap = URLCapability.from_url("https://secret.url/we/configure#value=none")
    assert not cap.can_add_email_attendee()
    assert cap.get("value") == "none"
    assert not cap.get("asd")


def test_parse_from_string():
    cap = URLCapability.from_string("asd=cfx")
    assert cap.get("cfx") == ""
    assert cap.get("asd") == "cfx"


def test_add_to_url_empty():
    cap = URLCapability()
    assert cap.restrict("https:asd.com/asd") == "https:asd.com/asd#"


def add_to_url_set():
    cap = URLCapability.from_string("q=123")
    assert cap.restrict("https:asd.com/asd") == "https:asd.com/asd#q=123"


def test_replacing():
    cap = URLCapability.from_string("q=123")
    assert cap.restrict("https:asd.com/asd#q=555&a=233") == "https:asd.com/asd#q=123"


def test_special_case_empty():
    cap = URLCapability.from_string("a=")
    assert cap.get("a") in ("", None)


def test_special_case_double():
    cap = URLCapability.from_string("a=1&a=2")
    assert cap.get("a") == "1"


@pytest.mark.parametrize(
    ("string", "value"),
    [
        ("", False),
        ("can_add_email_attendee=tru", False),
        ("can_add_email_attendee=False", False),
        ("can_add_email_attendee=True", True),
        ("can_add_email_attendee=true", True),
        ("can_add_email_attendee=TRUE", True),
    ],
)
def test_email_attendee(string, value):
    cap = URLCapability.from_string(string)
    assert cap.can_add_email_attendee() == value
