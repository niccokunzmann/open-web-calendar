# SPDX-FileCopyrightText: 2026 Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

from open_web_calendar.app import get_default_specification


def test_index_page_exposes_home_navigation_data(client):
    """The configuration page should expose data for a home navigation link."""
    response = client.get("/index.html")

    assert response.status_code == 200
    assert '"home": "Home"' in response.text
    assert f'const homepageUrl = "{get_default_specification()["homepage"]}";' in (
        response.text
    )
