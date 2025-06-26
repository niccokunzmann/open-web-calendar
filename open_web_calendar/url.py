# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""This contains URL specific customizations and parameters."""

from __future__ import annotations

from urllib.parse import parse_qs, urlencode, urlparse


class URLCapability:
    """The capabilities of a URL.

    This is saved in the hash behind the URL.
    This hash is discarded for all requests to servers.
    As such, we can safe configuration data in it.
    """

    @classmethod
    def from_url(cls, url: str):
        """Get the capabilities from a URL."""
        parsed = urlparse(url)
        return cls.from_string(parsed.fragment)

    @classmethod
    def from_string(cls, parameters: str):
        """Get the capabilities from a URL."""
        return cls({k: v[0] for k, v in parse_qs(parameters).items()})

    def __init__(self, values: dict[str, str] | None = None):
        """Create a capability based on a hash."""
        self._values = {} if values is None else values.copy()

    def to_string(self) -> str:
        """As a string."""
        return urlencode(self._values)

    def get(self, name: str, default: str = "") -> str:
        """Get a value."""
        return self._values.get(name, default)

    def get_false(self, name: str) -> bool:
        """Return if this is true or false, default false."""
        return self.get(name).lower() == "true"

    def can_add_email_attendee(self) -> bool:
        return self.get_false("can_add_email_attendee")

    def __repr__(self):
        """repr(self)"""
        return f"{self.__class__.__name__}({self._values!r})"

    def restrict(self, url: str) -> str:
        """Return the URL with the restictions set by me."""
        plain_url = url.split("#", 1)[0]
        return plain_url + "#" + self.to_string()


__all__ = ["URLCapability"]
