# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test the escaping of content that should be embedded more raw.

This concerns
- JavaScript https://github.com/niccokunzmann/open-web-calendar/issues/632
- CSS https://github.com/niccokunzmann/open-web-calendar/issues/396
"""

from urllib.parse import quote

import pytest


@pytest.mark.parametrize(
    ("raw"),
    [
        "alert('hello')",
        'alert("hello")',
        "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~",
        "console.log(specification);",
    ],
)
@pytest.mark.parametrize("included", [False, True])
@pytest.mark.parametrize("param", ["css", "javascript"])
def test_some_content_needs_to_be_embedded_fully(raw, param, included, client):
    """Check that this content is included."""
    html = client.get(
        "/calendar.html?" + (f"{param}={quote(raw)}" if included else "")
    ).text
    print(html)
    assert (raw in html) == included


@pytest.mark.parametrize(
    ("param", "raw", "expected"),
    [
        (
            "javascript",
            "</script>",
            "</scr\\ipt>",
        ),  # see https://stackoverflow.com/a/23983448
    ],
)
@pytest.mark.parametrize("included", [False, True])
def test_escape_certain_content(client, param, raw, expected, included):
    """Check that content gets replaced."""
    html = client.get(
        "/calendar.html?" + (f"{param}={quote(raw)}" if included else "")
    ).text
    print(html)
    assert (expected in html) == included
