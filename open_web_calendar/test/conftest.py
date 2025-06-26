# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Callable
from unittest.mock import Mock

import icalendar
import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

    from flask import Flask
    from flask.testing import FlaskClient
    from responses import RequestsMock

# constants
HERE = Path(__file__).parent
CALENDAR_DIRECTORY = HERE / ".." / "features" / "calendars"

# relative imports
sys.path.append(HERE.absolute() / ".." / "..")
sys.path.append(HERE.absolute())
from open_web_calendar.app import DEFAULT_SPECIFICATION  # noqa: E402
from open_web_calendar.config import environment  # noqa: E402
from open_web_calendar.encryption import FernetStore  # noqa: E402

DEFAULT_SPECIFICATION["url"] = []

environment.debug = True
environment.use_requests_cache = False


@pytest.fixture()
def production():
    environment.debug = False
    yield True
    environment.debug = True


@pytest.fixture(autouse=True)
def _use_responses(responses: RequestsMock) -> Generator[RequestsMock, None, None]:
    """Prevent requests from sending out requests

    See https://docs.pytest.org/en/latest/monkeypatch.html#example-preventing-requests-from-remote-operations
    """
    responses.reset()
    responses.assert_all_requests_are_fired = False


@pytest.fixture()
def mock():
    return Mock()


@pytest.fixture()
def app(store, monkeypatch) -> Flask:
    """Create the app.

    See https://flask.palletsprojects.com/en/2.2.x/testing/
    """
    from open_web_calendar import app  # noqa: PLC0415, RUF100

    monkeypatch.setattr(FernetStore, "from_environment", lambda: store)
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    return app


@pytest.fixture()
def cache_url(responses: RequestsMock) -> Callable[[str, str], None]:
    """Cache an additional URL."""

    def cache_url(url: str, content: str):
        print("1", responses.get_registry().registered)
        responses.remove(responses.GET, url)
        print("2", responses.get_registry().registered)
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain",  # needs to consider calendars and HTML
        )
        print("3", responses.get_registry().registered)

    return cache_url


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


calendar_files = {}
for file in CALENDAR_DIRECTORY.iterdir():
    if file.is_file():
        with file.open() as f:
            calendar_files[file] = f.read()


@pytest.fixture()
def calendar_urls(cache_url) -> dict[str, str]:
    """Mapping the calendar name without .ics to the cached url.

    The files are located in the CALENDAR_FOLDER.
    """
    mapping: dict[str, str] = {}
    for file, content in calendar_files.items():
        url = "http://test.examples.local/" + file.name
        cache_url(url, content)
        mapping[file.name] = url
        if file.suffix.lower() == ".ics":
            mapping[file.stem] = url
    return mapping


@pytest.fixture()
def calendar_content():
    """Mapping the calendar name without .ics to the calendar content.

    The files are located in the CALENDAR_FOLDER.
    """
    mapping = {}
    for file, content in calendar_files.items():
        if file.suffix.lower() == ".ics":
            mapping[file.stem] = content
    return mapping


@pytest.fixture()
def merged(
    client, calendar_urls
) -> Callable[[list[str] | None, dict[str, str] | None], icalendar.Calendar]:
    """Return a function to get a parsed calendar that is merged according to spec."""

    def _merged_calendars(
        urls: list[str] | None = None, specification: dict[str, str] | None = None
    ) -> icalendar.Calendar:
        """Return the merged ICS calendar."""
        urls = urls or []
        specification = specification or {}
        query = "?"
        for url in urls:
            query += f"url={calendar_urls[url]}&"
        for k, v in specification.items():
            query += f"{k}={v}&"
        response = client.get(f"/calendar.ics{query}")
        assert response.status_code == 200
        print(response.data.decode("utf-8"))
        return icalendar.Calendar.from_ical(response.data)

    return _merged_calendars


@pytest.fixture()
def store():
    """A test crypt store for the open web calendar."""
    return FernetStore(["n77iebivnjNTLDpmFcu6DuNFTHUnlEjCskx8oe0Xh8k="])


@pytest.fixture()
def todo() -> None:  # noqa: PT004, RUF100
    """This test should be implement later."""
    pytest.skip("This test needs implementing.")
