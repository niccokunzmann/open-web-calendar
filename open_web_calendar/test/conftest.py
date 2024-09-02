# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

# constants
HERE = Path(__file__).parent
CALENDAR_DIRECTORY = HERE / ".." / "features" / "calendars"

# relative imports
sys.path.append(HERE.absolute() / ".." / "..")
sys.path.append(HERE.absolute())
from open_web_calendar.app import DEFAULT_SPECIFICATION, cache_url  # noqa: E402

DEFAULT_SPECIFICATION["url"] = []


@pytest.fixture(autouse=True)
def _no_requests(monkeypatch):
    """Prevent requests from sending out requests

    See https://docs.pytest.org/en/latest/monkeypatch.html#example-preventing-requests-from-remote-operations
    """

    def test_cannot_call_outside(*args, **kw):
        raise RuntimeError(
            "Tests are not allowed to make requests to the"
            " Internet. You can use cache_url() to mock that."
        )

    monkeypatch.setattr(requests.sessions.Session, "request", test_cannot_call_outside)


@pytest.fixture
def mock():
    return Mock()


@pytest.fixture
def app():
    """Create the app.

    See https://flask.palletsprojects.com/en/2.2.x/testing/
    """
    from open_web_calendar.app import app

    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    return app

    # clean up / reset resources here


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


calendar_files = {}
for file in CALENDAR_DIRECTORY.iterdir():
    with file.open() as f:
        calendar_files[file] = f.read()


@pytest.fixture
def calendar_urls():
    """Mapping the calendar name without .ics to the cached url.

    The files are located in the CALENDAR_FOLDER.
    """
    mapping = {}
    for file, content in calendar_files.items():
        url = "http://test.examples.local/" + file.name
        cache_url(url, content)
        mapping[file.name] = url
        if file.suffix.lower() == ".ics":
            mapping[file.stem] = url
    return mapping


@pytest.fixture
def calendar_content():
    """Mapping the calendar name without .ics to the calendar content.

    The files are located in the CALENDAR_FOLDER.
    """
    mapping = {}
    for file, content in calendar_files.items():
        if file.suffix.lower() == ".ics":
            mapping[file.stem] = content
    return mapping
