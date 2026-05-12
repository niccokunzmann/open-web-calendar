---
# SPDX-FileCopyrightText: 2026 Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Write and run Behave browser tests for the Open Web Calendar."
---

# Behave Tests

The browser tests use [Behave](https://behave.readthedocs.io/) with Selenium.
They exercise the built Open Web Calendar in a real browser and live in
`open_web_calendar/features/`.

## Feature Files

Each `*.feature` file describes one user-facing behavior with Gherkin steps.
Prefer adding scenarios near related behavior, for example:

- `configure-the-calendar.feature` for configuration parameters.
- `edit-the-calendar.feature` for the configuration UI.
- Issue-specific files such as `issue-206-subscribe-to-ics.feature` for
  regressions.

The shared step implementations live in
`open_web_calendar/features/steps/browser_steps.py`. Reuse existing steps before
adding new ones, because many common actions are already available: adding a
calendar fixture, setting specification parameters, opening a date, clicking
links or buttons, checking text, checking links, downloading `.ics` files, and
loading API recordings.

## Calendar Fixtures

Calendar input files live in `open_web_calendar/features/calendars/`. Put small
`.ics` fixtures there when a scenario needs stable calendar data. Refer to a
fixture with:

```gherkin
Given we add the calendar "one-event"
```

The step appends `.ics` when the fixture name has no extension. Download
expectations created by tests are stored under
`open_web_calendar/features/downloads_by_tests/` and can be compared with the
checked fixtures in `open_web_calendar/features/downloads/`.

## Running Tests

Run all browser features with:

```sh
tox -e web
```

Run one feature file while iterating:

```sh
tox -e web -- open_web_calendar/features/issue-206-subscribe-to-ics.feature
```

Run a specific scenario by line number:

```sh
tox -e web -- open_web_calendar/features/configure-the-calendar.feature:42
```

Use a specific browser or window size with Behave `-D` options:

```sh
tox -e web -- -D browser=firefox
tox -e web -- -D browser=chrome
tox -e web -- -D window=375x812
```

When a step fails, the test environment records a screenshot in `screenshots/`
and prints the path together with captured server output.

## Adding Steps

Only add a new Python step when a scenario cannot be expressed with the shared
steps. Keep new steps small and user-focused, and put browser-specific logic in
`browser_steps.py` so future feature files can reuse it.

