# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""We want to be able to subscribe from sites that provide ICS links indirectly.

See https://github.com/niccokunzmann/open-web-calendar/issues/309
"""


def test_request_from_alternate_link(client, calendar_urls):
    """If we request from an alternate link, we should see the events from the calendar.

    The HTML page links to the ics file.
    """
    calendar_text = client.get(
        f"/calendar.ics?url={calendar_urls['one-day-event']}"
    ).text
    html_text = client.get(
        f"/calendar.ics?url={calendar_urls['one-day-event.html']}"
    ).text
    assert (
        calendar_text == html_text
    ), "Whether alternate link or direct, the content should be the same."
