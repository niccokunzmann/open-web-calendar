# SPDX-FileCopyrightText: 2026 Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

from open_web_calendar.app import get_default_specification


def test_translate_link_is_shown_once_in_language_section(client):
    """The language section should not repeat the translate link."""
    response = client.get("/index.html#configure-languages")

    assert response.status_code == 200
    translate_url = get_default_specification()["translate"]
    assert response.text.count(f'href="{translate_url}"') == 1
