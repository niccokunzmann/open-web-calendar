"""Tests for Issue 241.

See https://github.com/niccokunzmann/open-web-calendar/issues/241

We expect application/javascript.
https://stackoverflow.com/a/189877/1320237
"""
import pytest


@pytest.mark.parametrize(
    "js_url",
    [
        "/configuration.js",
        "/js/index.js",
        "/locale_de.js",
        "/locale_nb_NO.js",
    ]
)
def test_mime_type_of_configuration_js(client, js_url):
    """Check the Content-Type header.
    """
    response = client.get(js_url)
    assert "application/javascript" in response.content_type
