# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""
Test the caching functionality which will be used by subsequent tests.

"""

import pytest
import requests

from open_web_calendar.app import get_text_from_url


def test_tests_can_cache_values(cache_url):
    cache_url("http://asd.asd", "test123")
    assert get_text_from_url("http://asd.asd") == b"test123"


def test_caching_twice_works(cache_url):
    cache_url("http://asd.asd", "test123")
    cache_url("http://asd.asd", "asd")
    assert get_text_from_url("http://asd.asd") == b"asd"


def test_requests_are_forbidden():
    with pytest.raises(requests.ConnectionError):
        requests.get("https://duckduckgo.com", timeout=20)
