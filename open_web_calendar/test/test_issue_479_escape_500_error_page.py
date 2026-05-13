# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""The 500 error page must HTML-escape interpolated values.

See https://github.com/niccokunzmann/open-web-calendar/issues/479
Addresses pentest finding NF-006 ("Potential XSS in error 500 handling").

The pentest report says:

    Once fixed, it could become an XSS vector, as the content of the
    stack trace and ValueError is embedded in the returned HTML without
    sanitization. An attacker could deliberately trigger an error and
    use the controllable parts of the stack trace or ValueError to
    inject HTML into the response.

These tests cover both:
- the route-level path (a real 500 dispatched through Flask's error handler)
- the unit-level handler call (the handler escapes regardless of dispatch)
"""

import pytest

from open_web_calendar.app import unhandled_exception
from open_web_calendar.config import environment


@pytest.fixture()
def debug():
    """Force debug mode on so the traceback is rendered."""
    original = environment.debug
    environment.debug = True
    yield
    environment.debug = original


@pytest.fixture()
def errors_propagate_to_handler(app):
    """Flask's TESTING=True re-raises uncaught exceptions instead of
    dispatching them to error handlers. These tests need the real handler."""
    original_testing = app.testing
    original_propagate = app.config.get("PROPAGATE_EXCEPTIONS")
    app.testing = False
    app.config["PROPAGATE_EXCEPTIONS"] = False
    yield
    app.testing = original_testing
    app.config["PROPAGATE_EXCEPTIONS"] = original_propagate


def test_500_in_production_has_no_traceback(
    client, production, errors_propagate_to_handler
):
    """In production, the 500 page must not leak traceback or internals."""
    response = client.get("/calendar.notavalidext")
    assert response.status_code == 500
    body = response.data.decode("utf-8")
    assert "Traceback" not in body
    assert "<pre>" not in body
    assert "open_web_calendar" not in body


def test_500_in_debug_includes_traceback(client, debug, errors_propagate_to_handler):
    """In debug, the 500 page must show the traceback (fixes #479's reporter ask)."""
    response = client.get("/calendar.notavalidext")
    assert response.status_code == 500
    body = response.data.decode("utf-8")
    assert "Traceback" in body
    assert "ValueError" in body


def test_500_in_debug_escapes_script_tag_in_exception_message(
    client, debug, errors_propagate_to_handler
):
    """An attacker-controlled <script> tag in the ValueError message must
    appear HTML-escaped in the 500 response (NF-006)."""
    response = client.get("/calendar.%3Cscript%3Ealert(1)%3C/script%3E")
    assert response.status_code == 500
    body = response.data.decode("utf-8")
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in body


def _raise_xss_payload():
    """Raise an exception whose message carries an XSS payload."""
    raise ValueError("<img src=x onerror=alert(1)>")


def test_500_escapes_via_direct_handler_call(app, debug):
    """Defense-in-depth: the handler escapes regardless of routing."""
    with app.test_request_context("/"):
        try:
            _raise_xss_payload()
        except ValueError as exc:
            response_body, status = unhandled_exception(exc)
    assert status == 500
    assert "<img src=x onerror=alert(1)>" not in response_body
    assert "&lt;img src=x onerror=alert(1)&gt;" in response_body


def test_500_response_is_html(client, errors_propagate_to_handler):
    """The 500 response advertises HTML content type."""
    response = client.get("/calendar.notavalidext")
    assert response.status_code == 500
    assert response.content_type.startswith("text/html")
