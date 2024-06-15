# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test adding JavaScript to the calendar.

This allows people to
- add DHTMLX scheduler customizations
- configure the scheduler themselves
"""

from urllib.parse import quote

import pytest


@pytest.mark.parametrize(
    ("query", "tags"),
    [
        (
            "?javascript_url=https://tippi.js/embed.js",
            ['<script src="https://tippi.js/embed.js"'],
        ),
        (
            "?javascript_url=/feature1.js&javascript_url=/feature2.js",
            ['<script src="/feature1.js"', '<script src="/feature2.js"'],
        ),
    ],
)
def test_embed_js_link(client, query, tags):
    """Check that the JS links are used."""
    response = client.get(f"/calendar.html{query}")
    for html in tags:
        assert html in response.text


@pytest.mark.parametrize(
    ("js", "html"),
    [
        ("console.log(specification);", "console.log(specification);"),
        ("<html>&", "&lt;html&gt;&amp;"),
    ],
)
def test_embed_js_directly(client, js, html):
    """Check direct JS embedding."""
    response = client.get(f"/calendar.html?javascript={quote(js)}")
    print(response.text)
    assert f'<script type="text/javascript">{html}</script>' in response.text


@pytest.mark.parametrize(
    ("query", "urls"),
    [
        ("?css_url=https://tippi.js/embed.css", ["https://tippi.js/embed.css"]),
        (
            "?css_url=/feature1.css&css_url=/feature2.css",
            ["/feature1.css", "/feature2.css"],
        ),
    ],
)
def test_embed_css_link(client, query, urls):
    """Check that the CSS links are used."""
    response = client.get(f"/calendar.html{query}")
    for url in urls:
        assert (
            f'<link href="{url}" rel="stylesheet" type="text/css" charset="utf-8">'
            in response.text
        )
