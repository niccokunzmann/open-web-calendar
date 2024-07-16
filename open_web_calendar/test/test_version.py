# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""
Test the version of the Open Web Calendar.
"""

import sys

import pytest


@pytest.mark.parametrize("no_version_file", [True, False])
def test_version_can_be_imported(monkeypatch, no_version_file):
    """Import the version"""
    if no_version_file:
        monkeypatch.delitem(sys.modules, "open_web_calendar")
        monkeypatch.setitem(sys.modules, "open_web_calendar.version", None)
    import open_web_calendar

    assert open_web_calendar.version_tuple == open_web_calendar.__version_tuple__
    assert isinstance(open_web_calendar.__version_tuple__, tuple)
    assert isinstance(open_web_calendar.__version__, str)
