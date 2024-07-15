# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""This tests adding an alternative link to the ICS file.

The link can be relative or absolute.

See https://github.com/niccokunzmann/open-web-calendar/issues/308
"""

import html

import pytest

from open_web_calendar.app import cache_url


@pytest.mark.parametrize("page", ["index.html", "about.html", "calendar.html"])
@pytest.mark.parametrize(
    "query",
    [
        "a=1&b=2",
        "specification_url=https://open-web-calendar.quelltext.eu/assets/templates/free-and-busy.json",
    ],
)
def test_the_query_is_used_in_the_alternate_link(client, page, query):
    """Make sure an alternate link is present."""
    cache_url(
        "https://open-web-calendar.quelltext.eu/assets/templates/free-and-busy.json",
        "{}",
    )
    response = client.get(f"/{page}?{query}")
    # html.escape, see https://stackoverflow.com/a/5072031/1320237
    link = f'<link rel="alternate" type="text/calendar" href="/calendar.ics?{html.escape(query)}" />'
    print(response.text[:1000])
    assert link in response.text
