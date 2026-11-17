# SPDX-License-Identifier: GPL-2.0-only

"""Fall back to the plain DESCRIPTION if X-ALT-DESC has no visible text.

Outlook writes an X-ALT-DESC HTML body that can be empty while DESCRIPTION
still holds the text.
"""

from icalendar import Event

from open_web_calendar.app import ConvertToEvents

EMPTY_OUTLOOK_HTML = (
    "<html><head><style><!-- p.MsoNormal {margin:0cm;} --></style></head>"
    '<body><div class=WordSection1><p class=MsoNormal><o:p>&nbsp;</o:p></p>'
    "</div></body></html>"
)


def description_of(ics_lines: str) -> str:
    event = Event.from_ical(
        "BEGIN:VEVENT\r\nSUMMARY:x\r\nDTSTART:20261021T090000Z\r\n"
        + ics_lines
        + "END:VEVENT\r\n"
    )
    return ConvertToEvents({"timezone": "Europe/London"}).get_event_description(event)


def test_empty_html_falls_back_to_plain_text():
    description = description_of(
        "DESCRIPTION:Chair: E. Spies -> U. Fendler\r\n"
        f"X-ALT-DESC;FMTTYPE=text/html:{EMPTY_OUTLOOK_HTML}\r\n"
    )
    assert "Chair: E. Spies -&gt; U. Fendler" in description
    assert "<script" not in description


def test_plain_text_is_escaped():
    description = description_of(
        "DESCRIPTION:<script>alert(1)</script>\\nsecond line\r\n"
        f"X-ALT-DESC;FMTTYPE=text/html:{EMPTY_OUTLOOK_HTML}\r\n"
    )
    assert "<script" not in description
    assert "second line" in description


def test_real_html_still_wins():
    description = description_of(
        "DESCRIPTION:plain text\r\n"
        "X-ALT-DESC;FMTTYPE=text/html:<p>real <b>html</b></p>\r\n"
    )
    assert "<b>" in description
    assert "html" in description
    assert "plain text" not in description
