# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""OWC_ENABLE_JS gates user-supplied JavaScript.

See https://github.com/niccokunzmann/open-web-calendar/issues/563

When the env var is set to `false`, the `javascript` and `javascript_url`
spec keys are silently dropped from query strings and from the body
fetched via `specification_url`. JavaScript set in
`default_specification.yml` or the `OWC_SPECIFICATION` env var still
works (admin-trusted). The `/js/proxy` route returns 403 so direct
attempts also fail.

The default is `true` for backward compatibility with OWC's standard
"own subdomain" deployment model.
"""

import os

from werkzeug.datastructures import MultiDict

from open_web_calendar.app import DEFAULT_SPECIFICATION, get_specification


def test_default_enables_js_from_query():
    """Default env: javascript query param is honoured."""
    spec = get_specification(query=MultiDict({"javascript": "alert(1)"}))
    assert spec["javascript"] == "alert(1)"


def test_default_enables_js_url_from_query():
    """Default env: javascript_url query param is honoured."""
    spec = get_specification(query=MultiDict({"javascript_url": "/feature.js"}))
    assert spec["javascript_url"] == ["/feature.js"]


def test_disable_drops_js_from_query(monkeypatch):
    """OWC_ENABLE_JS=false: javascript query param is silently dropped."""
    monkeypatch.setitem(os.environ, "OWC_ENABLE_JS", "false")
    spec = get_specification(query=MultiDict({"javascript": "alert(1)"}))
    assert spec["javascript"] == ""


def test_disable_drops_js_url_from_query(monkeypatch):
    """OWC_ENABLE_JS=false: javascript_url query param is silently dropped."""
    monkeypatch.setitem(os.environ, "OWC_ENABLE_JS", "false")
    spec = get_specification(query=MultiDict({"javascript_url": "/x.js"}))
    assert spec["javascript_url"] == []


def test_disable_drops_js_from_specification_url(monkeypatch, cache_url):
    """OWC_ENABLE_JS=false: javascript in a fetched specification_url is dropped."""
    monkeypatch.setitem(os.environ, "OWC_ENABLE_JS", "false")
    spec_url = "https://example.com/spec.yml"
    cache_url(spec_url, 'javascript: "alert(1)"\njavascript_url: ["/x.js"]\n')
    spec = get_specification(query=MultiDict({"specification_url": spec_url}))
    assert spec["javascript"] == ""
    assert spec["javascript_url"] == []


def test_disable_keeps_admin_supplied_js_from_app_default(monkeypatch):
    """OWC_ENABLE_JS=false: JS from the in-app DEFAULT_SPECIFICATION still works."""
    monkeypatch.setitem(os.environ, "OWC_ENABLE_JS", "false")
    monkeypatch.setitem(DEFAULT_SPECIFICATION, "javascript", "console.log('admin')")
    spec = get_specification(query=MultiDict({}))
    assert spec["javascript"] == "console.log('admin')"


def test_disable_returns_403_from_js_proxy(client, monkeypatch):
    """OWC_ENABLE_JS=false: /js/proxy returns 403."""
    monkeypatch.setitem(os.environ, "OWC_ENABLE_JS", "false")
    response = client.get("/js/proxy?url=http://example.com/x.js")
    assert response.status_code == 403


def test_default_allows_js_proxy(client, cache_url):
    """Default env: /js/proxy serves the script."""
    js_url = "http://example.com/x.js"
    cache_url(js_url, "console.log('ok');")
    response = client.get(f"/js/proxy?url={js_url}")
    assert response.status_code == 200
    assert b"console.log('ok');" in response.data


def test_disable_does_not_affect_css(monkeypatch):
    """OWC_ENABLE_JS=false: css and css_url query params still work."""
    monkeypatch.setitem(os.environ, "OWC_ENABLE_JS", "false")
    spec = get_specification(
        query=MultiDict({"css": "body{color:red}", "css_url": "/style.css"})
    )
    assert spec["css"] == "body{color:red}"
    assert spec["css_url"] == ["/style.css"]
