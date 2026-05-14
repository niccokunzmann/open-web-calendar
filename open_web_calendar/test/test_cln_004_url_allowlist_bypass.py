# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

r"""clean_html_host_whitelist must not be honoured.

Addresses pentest finding CLN-004 ("lxml_html_clean fails to enforce the
embedded URL allowlist"). lxml_html_clean's host_whitelist parameter
validates URLs via urllib.parse.urlsplit(...).hostname, which strips `\`
from the authority while browsers don't. A URL like
`http://evil.com:\@allowed.com` would pass an allowlist of `allowed.com`
while the browser fetches `evil.com`. Upstream partially mitigated this
for <iframe>/<embed> via an authority-mismatch check, but the parameter
still gives users a false sense of security for other tags.

The pentest report recommends OWC disallow the parameter; clean_html now
drops `clean_html_host_whitelist` from the spec on the way into the
cleaner so the misleading semantics can't be re-introduced via any spec
source (query string, specification_url, env var, default spec).
"""

from open_web_calendar.clean_html import clean_html


def test_host_whitelist_param_is_dropped_from_spec():
    """An allowlisted iframe must NOT survive cleanup."""
    spec = {"clean_html_host_whitelist": ["allowed.com"]}
    html = '<iframe src="http://allowed.com/safe"></iframe>'
    out = clean_html(html, spec)
    assert "iframe" not in out
    assert "allowed.com" not in out


def test_host_whitelist_bypass_payload_is_blocked():
    """The pentest PoC URL must never survive cleanup."""
    spec = {"clean_html_host_whitelist": ["allowed.com"]}
    html = '<iframe src="http://evil.com:\\@allowed.com"></iframe>'
    out = clean_html(html, spec)
    assert "iframe" not in out
    assert "allowed.com" not in out
    assert "evil.com" not in out


def test_host_whitelist_is_silently_ignored():
    """Adding clean_html_host_whitelist must not change the cleaning result."""
    html = '<a href="http://evil.com:\\@allowed.com">x</a>'
    with_param = clean_html(html, {"clean_html_host_whitelist": ["allowed.com"]})
    without_param = clean_html(html, {})
    assert with_param == without_param
