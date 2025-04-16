# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
import tempfile
from pathlib import Path

import pytest
import requests_cache

from open_web_calendar.config import Config


def config_from(**kw):
    for k, v in list(kw.items()):
        if v is None:
            kw.pop(k)
    return Config(kw)


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ("0", 0),
        ("1000", 1000),
        (None, 600),
    ],
)
def test_cache_expire_after(env, expected):
    """Check we parse this nicely."""
    config = config_from(CACHE_REQUESTED_URLS_FOR_SECONDS=env)
    assert config.cache_expire_after == expected


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ("10", 10),
        ("1000", 1000),
        (None, 5000),
    ],
)
def test_port(env, expected):
    """Check we parse this nicely."""
    config = config_from(PORT=env)
    assert config.port == expected


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ("", []),
        ("localhost", ["localhost"]),
        ("asd,123", ["asd", "123"]),
    ],
)
def test_allowed_hosts(env, expected):
    """Check we parse this nicely."""
    config = config_from(ALLOWED_HOSTS=env)
    assert config.allowed_hosts == expected


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ("0", None),
        ("1000", 1000),
        (None, 60),
    ],
)
def test_requests_timeout(env, expected):
    """Check we parse this nicely."""
    config = config_from(SOURCE_TIMEOUT=env)
    assert config.requests_timeout == expected


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ("true", True),
        ("TRUE", True),
        ("True", True),
        ("FALSE", False),
        ("False", False),
        ("false", False),
        (None, False),
    ],
)
def test_debug(env, expected):
    """Check we parse this nicely."""
    config = config_from(APP_DEBUG=env)
    assert config.debug == expected


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        (config_from(), True),  # cache by default
        (config_from(CACHE_REQUESTED_URLS_FOR_SECONDS="0"), False),
        (config_from(CACHE_REQUESTED_URLS_FOR_SECONDS="1000"), True),
        (config_from(CACHE_FILE_SIZE="0"), False),
        (config_from(CACHE_SIZE="0"), False),
        (config_from(CACHE_SIZE="1000"), True),
    ],
)
def test_when_we_have_a_cache(config: Config, expected: bool):  # noqa: FBT001
    """We might not have a cache in some cases."""
    assert config.use_requests_cache is expected


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ("10.1", int(10.1 * 1024 * 1024)),
        ("1000", 1000 * 1024 * 1024),
        (None, 200 * 1024 * 1024),
    ],
)
def test_cache_mb(env, expected):
    """Check we parse this nicely."""
    config = config_from(CACHE_SIZE=env)
    assert config.cache_max_bytes == expected


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ("0.5", 512 * 1024),
        ("11", 11 * 1024 * 1024),
        (None, 10 * 1024 * 1024),
    ],
)
def test_file_cache_mb(env, expected):
    """Check we parse this nicely."""
    config = config_from(CACHE_FILE_SIZE=env)
    assert config.cache_max_file_bytes == expected


def test_unlimited_caching():
    """Arguments for an unlimited cache."""
    config = config_from(CACHE_SIZE="unlimited")
    assert config.cache_max_bytes == -1
    assert config.use_requests_cache is True
    assert config.session_params["expire_after"] == 600
    assert config.session_params["backend"] == "filesystem"
    assert "maximum_cache_bytes" not in config.session_params
    assert "block_bytes" not in config.session_params
    assert "maximum_file_bytes" not in config.session_params
    assert isinstance(config.requests, requests_cache.CachedSession)


@pytest.mark.parametrize(
    ("cb", "fb"),
    [
        (None, None),
        ("200", "10"),
        ("100", None),
        (None, "20"),
    ],
)
def test_limited_cache(cb, fb):
    """Arguments for a limited cache."""
    config = config_from(CACHE_SIZE=cb, CACHE_FILE_SIZE=fb)
    assert config.use_requests_cache is True
    assert config.session_params["expire_after"] == 600
    assert config.session_params["backend"] == "filesystem"
    assert config.session_params["maximum_cache_bytes"] == int(cb or 200) * 1024 * 1024
    assert config.session_params["maximum_file_bytes"] == int(fb or 10) * 1024 * 1024
    assert config.session_params["block_bytes"] == 4096
    assert isinstance(config.requests, requests_cache.CachedSession)


def test_no_cache():
    """Arguments for no cache."""
    config = config_from(CACHE_REQUESTED_URLS_FOR_SECONDS="0")
    assert config.session_params == {}
    assert not isinstance(config.requests, requests_cache.CachedSession)


TMP = Path(tempfile.gettempdir())


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        (TMP / "a", TMP / "a" / "open-web-calendar-cache"),
        (TMP, TMP / "open-web-calendar-cache"),
        (None, TMP / "open-web-calendar-cache"),
    ],
)
def test_cache_path(env, expected):
    """Check we parse this nicely."""
    config = config_from(CACHE_DIRECTORY=env and str(env))
    assert config.cache_path == str(expected)


def test_override_default():
    """Override the default in Python."""
    config = config_from()
    config.port = 6000
    assert config.port == 6000


def test_override_env():
    """Override the default in Python."""
    config = config_from(APP_DEBUG="true")
    assert config.debug is True
    config.debug = False
    assert config.debug is False
