---
# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Write and run integration tests for the Open Web Calendar."
---

# Integration Tests

Integration tests exercise the Flask app through its HTTP routes.
They sit between the pure-function [unit tests](unit-tests.md) and the
full [browser tests](testing.md).
The runner is `pytest`, and they live alongside the unit tests in
`open_web_calendar/test/`.

The line between a unit test and an integration test is the `client`
fixture. A test that imports a helper and asserts on its return value
is a unit test. A test that issues `client.get("/calendar.events.json")`
and asserts on the response is an integration test.

If you have not run the tests before, the
[running tests section](index.md#running-tests) in the setup guide
covers `tox` and how to target one Python version.

## Run one test

```sh
tox -e py -- open_web_calendar/test/test_headers.py
```

Pass any `pytest` option after the `--`. To run a single test:

```sh
tox -e py -- open_web_calendar/test/test_headers.py::test_ics
```

## A small integration test

```python
def test_json_result(client):
    """Check the JSON response headers."""
    response = client.get("/calendar.events.json")
    assert response.access_control_allow_origin == "*"
    assert response.content_type.startswith("application/json")
```

`client` is the Flask test client. It bypasses the network and calls
the app's WSGI handler directly, so the test does not need a running
server.

## Fixtures you will use

The shared fixtures are defined in
[`open_web_calendar/test/conftest.py`][conftest]. The ones that matter
for integration tests:

- `client`: the Flask test client.
- `cache_url(url, content)`: register a fake HTTP response. Every
  outbound HTTP call goes through this mock; without a `cache_url`
  entry, the request fails.
- `calendar_urls`: a mapping from each `.ics` fixture in
  `open_web_calendar/features/calendars/` to a cached URL. Look up a
  fixture by its file stem.
- `calendar_content`: the same mapping, but returning the raw `.ics`
  text instead of a URL.
- `merged(urls, specification)`: fetches `/calendar.ics` with the
  given fixtures and spec parameters and returns the parsed
  `icalendar.Calendar`. Most ICS-pipeline regression tests use this.
- `production`: turns off debug mode for the duration of the test.
  Use it when the behavior under test depends on debug being off, such
  as the error 500 page.

## When to write an integration test

Reach for one when the bug or feature touches:

- An HTTP route (`/calendar.html`, `/calendar.events.json`, `/calendar.ics`).
- Response headers (CORS, content type, caching).
- The full request-to-response pipeline: spec assembly, source
  fetching, conversion, serialization.
- Anything where you need to assert on what a client actually receives.

If the bug is in a pure helper function, a [unit test](unit-tests.md)
is enough. If the bug is in rendering, clicks, or layout, write a
[browser test](testing.md) instead.

## Mocking external HTTP

Every HTTP request the app makes during a test is mocked. The default
is "no network." If your test exercises a code path that fetches an ICS
or talks to CalDAV, register the response first:

```python
def test_my_route(client, cache_url):
    cache_url(
        "https://example.com/calendar.ics",
        "BEGIN:VCALENDAR\n...END:VCALENDAR\n",
    )
    response = client.get(
        "/calendar.events.json?url=https://example.com/calendar.ics"
    )
    assert response.status_code == 200
```

For a CalDAV or Nextcloud-style multi-request interaction, recordings
are the right tool. See
[Recording API responses](testing.md#recording-api-responses).

[conftest]: https://github.com/niccokunzmann/open-web-calendar/blob/HEAD/open_web_calendar/test/conftest.py
