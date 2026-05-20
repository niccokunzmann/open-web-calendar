---
# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Write and run browser tests for the Open Web Calendar."
---

# Browser Tests

Bug fixes that affect the user-facing interface usually ship with a regression test.
We use [Behave] with Selenium to drive a real browser against a live Flask app.
The suite lives in `open_web_calendar/features/`.

Browser tests are the top layer of the test pyramid.
[Unit tests](unit-tests.md) cover pure functions and
[integration tests](integration-tests.md) cover HTTP routes through the
Flask test client. Reach for a browser test when the behavior under test
is rendering, clicks, or layout.

If you have not run the browser tests before, start with the
[browser testing section](index.md#browser-testing) in the setup guide.
It covers `tox -e web`, picking a browser, and changing the window size.

## Where things live

- `open_web_calendar/features/*.feature`: the Gherkin scenarios.
- `open_web_calendar/features/calendars/`: the `.ics` fixtures the scenarios
  load. A small HTTP server in `environment.py` serves these to the browser.
- `open_web_calendar/features/steps/browser_steps.py`: the reusable
  `@given`/`@when`/`@then` step library. Check it before writing a new step.
- `open_web_calendar/features/environment.py`: the setup that boots the
  Flask app, the Selenium driver, and the fixture HTTP server.

## Run one feature

```sh
tox -e web -- open_web_calendar/features/issue-679-caldav-sign-up.feature
```

You can pass any Behave options after the `--`. For example, run a single
scenario by line number:

```sh
tox -e web -- open_web_calendar/features/issue-679-caldav-sign-up.feature:10
```

## Add a feature for a bug

Name the file after the issue it covers: `issue-<number>-<short-slug>.feature`.
Most regression tests follow this pattern, so the regression for issue 1234
becomes `issue-1234-short-description.feature`. Topic-named features
(`burger-menu.feature`, `categories.feature`, etc.) also exist for behavior
that is not tied to one bug.

A small feature looks like this:

```gherkin
Feature: We do not show the sign-up button on regular events.

    Scenario: Usually, I cannot see the signup button.
        Given we add the calendar "issue-23-location-berlin"
         When we look at 2025-01-10
          And we click on the event "Event in Berlin!"
         Then we cannot see the text "Sign Up"
```

The `Given we add the calendar "..."` step takes the fixture name without
the `.ics` extension. The fixture HTTP server picks it up automatically.

## Add a fixture calendar

Drop the `.ics` file into `open_web_calendar/features/calendars/` and
reference its stem from the scenario. No registration step needed.

Keep fixtures small. One event is enough for most tests.
If the bug involves a specific date, pin the event to that date and
use `When we look at <date>` to make the scenario deterministic.

## Add a step

Before writing a new step, search [browser_steps.py] for an existing one
that covers the assertion.

If none fits, add a function to `browser_steps.py` decorated with `@given`,
`@when`, or `@then`. Keep the wording natural so other scenarios can reuse it.

## When a test fails

See [Browser Testing](index.md#browser-testing) for where screenshots land
and how to jump from a failed step back to its source line.

## Recording API responses

Some scenarios talk to a real CalDAV server like Nextcloud. The browser
tests cannot reach one, so the calls are recorded once and replayed on
each run. The [responses] library does the replay. Recordings live as
YAML files under `open_web_calendar/test/responses/`.

Recordings freeze the API in time on purpose. A test should not break
because Nextcloud shipped a new release overnight. The cost: when the
external API really does change, the recording has to be re-captured
against the live server.

### Replay a recording in a feature

In a scenario, load a recording before any step that triggers an HTTP
request:

```gherkin
Scenario: A user signs up for an event.
    Given we load the api recording "issue-680-sign-up-for-event"
      And we add the calendar "issue-679-sign-up-for-event"
     When we look at 2025-03-17
      ...
```

The argument is the recording stem. The `.yml` extension is implied. The
recording stops at the end of the scenario.

### Record a new interaction

Start the dev server in recording mode:

```sh
tox -e dev
```

The dev server records by default. Every outbound HTTP request is captured
and written to `open_web_calendar/test/responses/dev.yml` once a second.

Drive the interaction you want to capture: open `index.html`, fill the
calendar URL, click through the configuration page. Stop the server when
you are done.

Rename `dev.yml` to a meaningful stem, like
`issue-1234-event-signup.yml`, and keep it under
`open_web_calendar/test/responses/`. Reference it from your feature with
`Given we load the api recording "issue-1234-event-signup"`.

### Replay a recording locally

Pass the recording name to the dev module to run the calendar against a
saved recording instead of the live network:

```sh
python -m open_web_calendar.test issue-680-sign-up-for-event
```

The server still listens on <http://localhost:5000>. Every external HTTP
call is served from the YAML file. Handy for iterating on a scenario
before turning it into a feature.

### When to record fresh

Re-record when:

- The external API changes shape (a Nextcloud release, say).
- You add a scenario that exercises an interaction not in any existing
  recording.
- A scenario fails with an `OrderedRegistry` mismatch and the new request
  order is intentional.

Keep recordings small. One scenario per recording is the norm.

[responses]: https://github.com/getsentry/responses

[Behave]: https://behave.readthedocs.io/
[browser_steps.py]: https://github.com/niccokunzmann/open-web-calendar/blob/HEAD/open_web_calendar/features/steps/browser_steps.py
