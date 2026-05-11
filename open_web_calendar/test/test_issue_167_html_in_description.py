# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""DESCRIPTION served in /calendar.ics is plain text per RFC 5545.

Sources may put HTML directly in DESCRIPTION (Google Calendar) or in ALTREP /
X-ALT-DESC parameters. OWC normalises this so subscribers like Thunderbird see
clean text while X-ALT-DESC carries the HTML for clients that want it.

See https://github.com/niccokunzmann/open-web-calendar/issues/167
"""

from icalendar_compatibility import Description


def event_by_uid(cal, uid):
    return next(e for e in cal.events if str(e.get("UID", "")) == uid)


def test_html_in_description_is_stripped(merged):
    """Every DESCRIPTION in the merged output must be plain text."""
    cal = merged(["issue-287-links-1"])
    for event in cal.events:
        desc = str(event.get("DESCRIPTION", ""))
        assert not Description.this_could_be_html(desc), (
            f"HTML leaked into DESCRIPTION: {desc!r}"
        )


def test_html_is_preserved_in_x_alt_desc(merged):
    """When the source carried HTML, X-ALT-DESC must keep it so HTML-aware
    clients still get the formatted version."""
    cal = merged(["issue-287-links-1"])
    events_with_html = [e for e in cal.events if e.get("X-ALT-DESC") is not None]
    assert events_with_html, "expected at least one event with X-ALT-DESC"
    for event in events_with_html:
        x_alt = event["X-ALT-DESC"]
        assert x_alt.params.get("FMTTYPE") == "text/html"
        assert Description.this_could_be_html(str(x_alt))


def test_plain_text_description_is_unchanged(merged):
    """A source event with plain-text DESCRIPTION keeps its text verbatim
    and gets no spurious X-ALT-DESC."""
    cal = merged(["issue-287-links-1"])
    event = event_by_uid(cal, "1lnco7mmf4p8042a098k4h968g@google.com")
    assert event.get("X-ALT-DESC") is None
    assert "www.DowntownMarceline.org" in str(event["DESCRIPTION"])


def test_altrep_html_is_normalised(merged):
    """When the source carries HTML via DESCRIPTION;ALTREP="data:text/html,...",
    DESCRIPTION ends up plain text and X-ALT-DESC carries the HTML."""
    cal = merged(["event-with-html-markup"])
    event = event_by_uid(cal, "683642b3-9b25-4177-8b46-ec2f65e64020")
    desc = str(event["DESCRIPTION"])
    assert not Description.this_could_be_html(desc)
    x_alt = event["X-ALT-DESC"]
    assert x_alt.params.get("FMTTYPE") == "text/html"
    assert Description.this_could_be_html(str(x_alt))


def test_existing_x_alt_desc_is_preserved(merged):
    """When the source already has X-ALT-DESC;FMTTYPE=text/html, the HTML
    is preserved verbatim (no overwrite)."""
    cal = merged(["food"])
    event = event_by_uid(cal, "2845")
    x_alt = event["X-ALT-DESC"]
    assert x_alt.params.get("FMTTYPE") == "text/html"
    # Source X-ALT-DESC starts with this DOCTYPE; verify it wasn't overwritten.
    assert str(x_alt).startswith("<!DOCTYPE HTML")
