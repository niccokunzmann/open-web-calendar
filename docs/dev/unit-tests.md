---
# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Write and run unit tests for the Open Web Calendar."
---

# Unit Tests

The unit tests live in `open_web_calendar/test/` and run with `pytest`
through `tox`. They cover the pieces below the HTTP layer: parsing,
merging, the configuration object, encryption, and so on.

If you have not run the tests before, the
[running tests section](index.md#running-tests) in the setup guide
covers `tox` and how to target one Python version.

## Run one test

```sh
tox -e py -- open_web_calendar/test/test_specification.py
```

Pass any `pytest` option after the `--`. To run a single test:

```sh
tox -e py -- open_web_calendar/test/test_specification.py::test_specification_equals_default_specification_by_default
```

## Fixtures you will use

The shared fixtures are defined in
[`open_web_calendar/test/conftest.py`][conftest]. The ones you will reach
for most often:

- `client`: the Flask test client.
- `cache_url(url, content)`: register a fake HTTP response so your test
  does not need the network. All outbound HTTP is mocked by default, so
  any URL the code fetches needs a `cache_url` entry first.
- `calendar_urls`: a mapping from each `.ics` fixture in
  `open_web_calendar/features/calendars/` to a cached URL. Look up a
  fixture by its file stem.
- `calendar_content`: the same mapping, but returning the raw `.ics`
  text instead of a URL.
- `merged(urls, specification)`: fetches `/calendar.ics` with the given
  fixtures and spec parameters and returns the parsed `icalendar.Calendar`.
- `production`: flips off debug mode for the duration of the test.

## Add a regression test for a bug

Name the file after the issue: `test_issue_<number>_<short_slug>.py`.
Most regression tests in `open_web_calendar/test/` follow this pattern.
Topic-named tests (`test_clean.py`, `test_config.py`, etc.) also exist
for behavior that is not tied to one bug.

A small regression test looks like this:

```python
def test_issue_NNN_specific_behavior(merged):
    cal = merged(
        urls=["one-event"],
        specification={"timezone": "UTC"},
    )
    events = list(cal.walk("VEVENT"))
    assert len(events) == 1
```

For features that are easier to verify in a real browser
(rendering, clicks, layout), write a [browser test](testing.md) instead.

[conftest]: https://github.com/niccokunzmann/open-web-calendar/blob/HEAD/open_web_calendar/test/conftest.py
