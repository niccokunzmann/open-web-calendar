# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""
Test the version of the Open Web Calendar.
"""

import sys

import pytest

import open_web_calendar


@pytest.mark.parametrize("no_version_file", [True, False])
def test_version_can_be_imported(monkeypatch, no_version_file):
    """Import the version"""
    if no_version_file:
        monkeypatch.delitem(sys.modules, "open_web_calendar")
        monkeypatch.setitem(sys.modules, "open_web_calendar._version", None)
    import open_web_calendar

    assert open_web_calendar.version_tuple == open_web_calendar.__version_tuple__
    assert isinstance(open_web_calendar.__version_tuple__, tuple)
    assert isinstance(open_web_calendar.__version__, str)


@pytest.mark.parametrize("page", ["about.html", "index.html"])
def test_version_in_footer(page, client):
    """Check that we can see the version on the website."""
    response = client.get(f"/{page}")
    assert open_web_calendar.__version__ in response.text
