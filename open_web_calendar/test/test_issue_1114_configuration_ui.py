# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only


def test_index_page_exposes_event_details_controls(client):
    """The configuration UI exposes the existing event detail plugins."""
    response = client.get("/index.html")

    assert response.status_code == 200
    assert 'id="configure-event-details"' in response.text
    assert 'id="plugin_event_details"' in response.text
    assert 'id="plugin_event_tooltip"' in response.text
