# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Utility functions."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote, urlparse

if TYPE_CHECKING:
    from caldav import URL


def set_url_username_password(
    url: str | URL, username: str | None, password: str | None
) -> str:
    """Create a URL with username and password."""
    # see https://stackoverflow.com/a/75060902/1320237
    if username is None or password is None:
        return unset_url_username_password(url)
    _username = quote(username)
    _password = quote(password)
    _url = urlparse(str(url))
    _netloc = _url.netloc.split("@")[-1]
    _url = _url._replace(netloc=f"{_username}:{_password}@{_netloc}")
    return _url.geturl()


def unset_url_username_password(url: str | URL) -> str:
    """Remove username and password."""
    # see https://stackoverflow.com/a/75060902/1320237
    _url = urlparse(str(url))
    _netloc = _url.netloc.split("@")[-1]
    _url = _url._replace(netloc=_netloc)
    return _url.geturl()


__all__ = ["set_url_username_password"]
