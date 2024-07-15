# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test the headers of responses."""

import pytest

CAL_JSON = "/calendar.events.json"
CAL_ICS = "/calendar.ics"


def test_json_result(client):
    """Check the JS headers."""
    response = client.get(CAL_JSON)
    assert response.access_control_allow_origin == "*"
    assert response.content_type.startswith("application/json")


def test_ics(client):
    """Check the JS headers."""
    response = client.get(CAL_ICS)
    print(dir(response))
    assert response.access_control_allow_origin == "*"
    assert response.content_type.startswith("text/calendar")


@pytest.mark.parametrize("endpoint", [CAL_ICS, CAL_JSON])
@pytest.mark.parametrize("h", ["", "asd asd2"])
def test_allow_headers(endpoint, client, h):
    """Check the allowed headers"""
    response = client.get(CAL_ICS, headers={"Access-Control-Request-Headers": h})
    print(response.text)
    assert response.headers.get("Access-Control-Allow-Headers") == h


@pytest.mark.parametrize("endpoint", [CAL_ICS, CAL_JSON])
def test_return_code(client, endpoint):
    """Check the return code"""
    result = client.get(endpoint)
    print(result, dir(result))
    assert result.status_code == 200
