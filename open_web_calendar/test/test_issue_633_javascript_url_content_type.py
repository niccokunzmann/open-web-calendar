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

    assert not any(src.startswith(("http://", "https://")) for src in sources), (
        f"remote script src must be proxied, got: {sources}"
    )

    served_as_js = False
    for src in sources:
        r = client.get(src)
        is_js = r.headers.get("Content-Type", "").startswith("text/javascript")
        if is_js and js_content in r.data.decode("utf-8"):
            served_as_js = True
            break
    assert served_as_js, f"no script source served {js_content!r} as text/javascript"
