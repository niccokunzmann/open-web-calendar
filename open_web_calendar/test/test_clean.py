# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test cleaning the HTML input."""

from pprint import pprint

import pytest

from open_web_calendar.clean_html import clean_html, html_to_text, remove_html


@pytest.mark.parametrize(
    ("html", "spec", "expected_output"),
    [
        ("<script>js</script>a", {"clean_html_scripts": True}, "a"),
        ("<malicious>", {"clean_html_remove_unknown_tags": True}, ""),
    ],
)
def test_clean_html_from_spec(html, spec, expected_output):
    """Specify how to clean the HTML content."""
    output = clean_html(html, spec=spec).replace("\n", "")
    assert output == expected_output


def test_remove_html():
    """Remove all HTML tags - we do not expect them in the summary."""
    assert remove_html("<asd>aaa</asd>bbb") == "aaabbb"
    assert remove_html("><<<>") == ">"


def test_html_to_text_keeps_readable_breaks():
    """Extract text from HTML while preserving meaningful line breaks."""
    html = "<p>Breakfast<br>Eggs and toast</p><p>Lunch</p>"
    assert html_to_text(html) == "Breakfast\nEggs and toast\nLunch"


def test_html_to_text_keeps_inline_text_together():
    """Inline formatting should not add noisy line breaks."""
    assert html_to_text("A <strong>bold</strong> day") == "A bold day"


def test_nice_id_for_event(client, calendar_urls):
    """Make sure that we have nice IDs without HTML in them."""
    response = client.get(
        f"/calendar.events.json?url={calendar_urls['one-event']}&timezone=Europe/London&from=2019-03-04&to=2019-03-05"
    )
    event = response.json[0]
    pprint(event)
    assert " " not in event["id"]
    assert ":" not in event["id"]
