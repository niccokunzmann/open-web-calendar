# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""X-ALT-DESC HTML in /calendar.ics output must be sanitized.

See https://github.com/niccokunzmann/open-web-calendar/issues/1187

Two paths produce X-ALT-DESC HTML in the merged ICS feed:

1. DESCRIPTION HTML promoted to X-ALT-DESC by the #167 fix (PR #1185)
2. X-ALT-DESC carried verbatim from a source event

Both paths previously copied HTML through without sanitization, so a
malicious source calendar could ship `<script>` or event-handler
payloads to every subscriber of the merged feed.
"""

from icalendar_compatibility import Description


def event_by_uid(cal, uid):
    return next(e for e in cal.events if str(e.get("UID", "")) == uid)


def test_promoted_x_alt_desc_is_sanitized(merged):
    """HTML promoted from DESCRIPTION to X-ALT-DESC must be cleaned."""
    cal = merged(["issue-1187-xss-promoted"])
    event = event_by_uid(cal, "issue-1187-promoted@example.com")
    x_alt = str(event["X-ALT-DESC"])
    assert "<script>" not in x_alt
    assert "alert(" not in x_alt
    assert "onerror" not in x_alt
    assert Description.this_could_be_html(x_alt)


def test_source_x_alt_desc_is_sanitized(merged):
    """X-ALT-DESC carried over from the source event must be cleaned."""
    cal = merged(["issue-1187-xss-x-alt-desc"])
    event = event_by_uid(cal, "issue-1187-x-alt-desc@example.com")
    x_alt = str(event["X-ALT-DESC"])
    assert "<script>" not in x_alt
    assert "alert(" not in x_alt
    assert "onerror" not in x_alt
    assert Description.this_could_be_html(x_alt)
