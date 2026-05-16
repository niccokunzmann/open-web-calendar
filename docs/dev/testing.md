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

[Behave]: https://behave.readthedocs.io/
[browser_steps.py]: https://github.com/niccokunzmann/open-web-calendar/blob/main/open_web_calendar/features/steps/browser_steps.py
