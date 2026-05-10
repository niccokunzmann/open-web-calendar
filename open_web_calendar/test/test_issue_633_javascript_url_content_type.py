# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Make sure javascript_url scripts execute even when the remote server
returns a non-JavaScript Content-Type (e.g. text/plain from a GitHub gist).

See https://github.com/niccokunzmann/open-web-calendar/issues/633
"""

import re


def test_javascript_url_is_served_with_javascript_content_type(client, cache_url):
    """A remote script served as text/plain must reach the browser as
    text/javascript so nosniff browsers will execute it."""
    js_url = "http://example.com/script.js"
    js_content = "console.log('hi from a gist');"
    cache_url(js_url, js_content)

    page = client.get(f"/calendar.html?javascript_url={js_url}").text
    sources = re.findall(r'<script\s+src="([^"]+)"', page)

    served_contents = []
    for src in sources:
        if src.startswith(("http://", "https://")):
            continue  # remote scripts must not be referenced directly
        response = client.get(src)
        if response.headers.get("Content-Type", "").startswith("text/javascript"):
            served_contents.append(response.data.decode("utf-8"))

    assert any(js_content in body for body in served_contents)
