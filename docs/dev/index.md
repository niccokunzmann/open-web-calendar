---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Learn how to develop the Open Web Calendar."
---

# Setup & Tests

This section guides you through everything you need to know to develop the
software: build it and make changes.

## First-time Contributors

Contributions from people new to the Open Web Calendar are welcome.
A few things worth knowing before you start:

- You are free to pick up any open issue. Comment on it to say you are
  starting, and open a draft pull request when you have something to show.
- Open the PR early. It saves other people from duplicating your effort and
  gives reviewers a chance to weigh in before you go too far.
- Ask questions if the scope is unclear. Better to clarify on the issue
  than to rebuild after a review.
- The [`good first issue`](https://github.com/niccokunzmann/open-web-calendar/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
  label is a good place to start if you are looking for something small.

If you use AI to help write a pull request, follow the
[PCE AI policy](https://pycal.org/ai-policy/). The short version: take
responsibility for what you submit, disclose the model and how you used it
in your commit messages, and be ready to discuss the code.

## Clone the Repository

```sh
git clone https://github.com/niccokunzmann/open-web-calendar
cd open-web-calendar
```

## Code Quality

We use [ruff] to improve the code quality.
Please install [pre-commit] before committing.
It will ensure that the code is formatted and linted as expected using [ruff].

```sh
pre-commit install
```

To format the code before commit without the pre-commit hook, run this:

```shell
tox -e ruff
```

[ruff]: https://docs.astral.sh/ruff/
[pre-commit]:  https://pre-commit.com/

## Running Tests

To run the tests, we use `tox`.
`tox` tests all different Python versions which we want to
be compatible to.

```sh
pip install -r requirements/dev.in
```

Run all tests:

```sh
tox
```

Run a specific Python version:

```sh
tox -e py310
```

## Browser Testing

We use selenium to test the app in different browsers.
By default, Firefox is used.
You can test the features like this:

```sh
tox -e web
```

If you like to change the browser, use

```sh
tox -e web -- -D browser=firefox
tox -e web -- -D browser=chrome
```

You can also change the layout of the window to test the responsive design:

```sh
tox -e web -- -D window=375x812 # iPhone11 size
```

When a browser test fails, the runner saves a screenshot of the page so you can
see what the browser actually saw at the moment of failure.
The screenshots land in the `screenshots/` folder at the project root,
named after the feature and the line that failed
(for example, `issue-679-caldav-sign-up@line-7.png`).
The runner prints the full path as `Capturing screenshot to <path>` so you
can open it directly from the terminal.

Behave's own output lists each step with its source location as `<file>:<line>`.
Most modern terminals (VS Code, iTerm2, Windows Terminal) turn these into
clickable links that jump to the failing step in the source.

For details on writing browser tests, see the
[browser testing guide](testing.md).

### Debug Mode

To run the app locally with debug mode on, use:

```sh
tox -e dev
```

This starts the Flask dev server on <http://localhost:5000> with `APP_DEBUG=true`
and a test encryption key. The full list of environment variables it sets is
in `tox.ini` under `[testenv:dev]`.

## Documentation

You can build the documentation with `tox`, too.
It is located in the `docs` directory.

```sh
# For all languages
tox -e docs                          # writes to docs/_build/html

# Quick testing, English and German only
tox -e docs-quick                    # writes docs/_build/html-en and html-de

# Regenerate translation templates and update PO files
tox -e docs-i18n

# Check external links
tox -e docs-linkcheck
```

We are using [Sphinx] with the [MyST parser] for Markdown and the
[pydata-sphinx-theme] for styling. Translations live under `docs/locale/`
and are managed by [sphinx-intl] (driven by Weblate on
[hosted.weblate.org](https://hosted.weblate.org/engage/open-web-calendar/)).

[Sphinx]: https://www.sphinx-doc.org/
[MyST parser]: https://myst-parser.readthedocs.io/
[pydata-sphinx-theme]: https://pydata-sphinx-theme.readthedocs.io/
[sphinx-intl]: https://sphinx-intl.readthedocs.io/

## Troubleshooting

A few things that tend to trip people up:

- **Browser tests can't find Firefox.** Install Firefox locally, or pass
  `-D browser=chrome` (you need a real Chrome install for that too). Selenium
  drives the browser of your choice; we don't ship one.
- **Docs build fails on Windows with a missing `assets/img/logo` directory.**
  `docs/assets/img/logo` is a git symlink that Windows checks out as a plain
  file unless symlinks are enabled. Replace it with a directory junction
  locally (`mklink /J docs\assets\img\logo open_web_calendar\static\img\logo`)
  and `git update-index --skip-worktree` to ignore the change.
- **`tox -e reuse` flags missing SPDX headers.** Every new source file needs
  the SPDX header at the top (copyright line + license identifier). Copy it
  from any existing file of the same type.
- **`tox -e docs-i18n` writes changes to `.po` files under `docs/locale/`.**
  Those are translation templates regenerated from your source edits. They
  get synced separately by the maintainers' translation workflow, so don't
  commit them as part of an unrelated PR.
