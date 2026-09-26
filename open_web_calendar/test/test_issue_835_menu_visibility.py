# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""The menu should not be rendered when it is disabled.

See https://github.com/niccokunzmann/open-web-calendar/issues/835
"""


def test_menu_is_not_rendered_without_the_control(client):
    """Without "menu" in controls, no menu elements are in the page."""
    response = client.get("/calendar.html?controls=next")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'id="menu__toggle"' not in html
    assert 'id="menu-meta-data"' not in html


def test_menu_is_rendered_with_the_control(client):
    """With "menu" in controls, the menu elements are in the page."""
    response = client.get("/calendar.html?controls=menu")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'id="menu__toggle"' in html
    assert 'id="menu-meta-data"' in html


def test_menu_is_not_rendered_by_default(client):
    """The default specification does not include the menu."""
    response = client.get("/calendar.html")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'id="menu__toggle"' not in html
