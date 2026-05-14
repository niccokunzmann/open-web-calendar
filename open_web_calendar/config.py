# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Open Web Calendar configuration.

This is inbetween the app and the parameters and environment variables.
Use open_web_calendar.config.environment as default.
"""

from __future__ import annotations

import os
import tempfile
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Any

import requests
import requests_cache

if TYPE_CHECKING:
    from collections.abc import Callable

MB = 1024 * 1024


def config_property(func: Callable) -> property:
    """Configuration properties.

    This equips the properties with a default value.
    You can override the value if you wish to.
    """
    attr = f"_{func.__name__}"

    @property
    @wraps(func)
    def wrapper(config):
        if hasattr(config, attr):
            return getattr(config, attr)
        return func(config)

    @wrapper.setter
    def wrapper(config, value):
        setattr(config, attr, value)

    return wrapper


class Config:
    """The configuration of the Open Web Calendar.

    See https://open-web-calendar.quelltext.eu/host/configure/

    You can set all the properties as environment variables and override them.

        >>> c = Config({})
        >>> c.port
        5000
        >>> c.port = 8080
        >>> c.port
        8080
    """

    def __init__(self, source: dict[str, str]):
        """Create a new configuration."""
        self._source = source

    @config_property
    def requests_timeout(self) -> int | None:
        """The timeout for requests of source files from the web in seconds.

        Set to 0 to use requests' default timeout.

        Variable: SOURCE_TIMEOUT
        Default: 60
        """
        result = int(self._source.get("SOURCE_TIMEOUT", "60"))
        if result <= 0:
            return None
        return result

    @config_property
    def port(self) -> int:
        """The port of the application.

        Variable: PORT
        Default: 5000
        """
        return int(self._source.get("PORT", "5000"))

    @config_property
    def debug(self) -> bool:
        """The debug mode of the application.

        Variable: DEBUG
        Default: False
        """
        return self._source.get("APP_DEBUG", "").lower() == "true"

    @config_property
    def enable_js(self) -> bool:
        """Whether user-supplied JavaScript is allowed.

        Variable: OWC_ENABLE_JS
        Default: True
        """
        return self._source.get("OWC_ENABLE_JS", "true").lower() != "false"

    @config_property
    def max_source_events(self) -> int:
        """Maximum VEVENTs accepted from a single ICS payload.

        The cap sums across all VCALENDAR blocks in one fetched ICS response,
        so an attacker can't bypass it by concatenating multiple calendars.

        Variable: OWC_MAX_SOURCE_EVENTS
        Default: 1000
        """
        return int(self._source.get("OWC_MAX_SOURCE_EVENTS", "1000"))

    @config_property
    def max_response_events(self) -> int:
        """Maximum expanded events in a /calendar.events.json response.

        Variable: OWC_MAX_RESPONSE_EVENTS
        Default: 10000

        Defense-in-depth only: the check fires after recurring_ical_events
        has already expanded all occurrences, so the CPU work of expansion
        is not avoided. Real pagination is a future change. Operators with
        CPU pressure should also lower max_source_events.
        """
        return int(self._source.get("OWC_MAX_RESPONSE_EVENTS", "10000"))

    @config_property
    def max_response_bytes(self) -> int:
        """Maximum byte size of a /calendar.events.json response body.

        Variable: OWC_MAX_RESPONSE_MB
        Default: 10 (MB)

        The check runs after the full JSON has been serialized in memory,
        so an extreme response transiently allocates the full size before
        rejection. Real streaming serialization is a future change.
        """
        return int(float(self._source.get("OWC_MAX_RESPONSE_MB", "10")) * MB)

    @config_property
    def cache_expire_after(self) -> int:
        """The cache expiration timeout in seconds.

        Variable: CACHE_REQUESTED_URLS_FOR_SECONDS
        Default: 600 (10 minutes)
        """
        return int(self._source.get("CACHE_REQUESTED_URLS_FOR_SECONDS", "600"))

    @config_property
    def use_requests_cache(self) -> bool:
        """Whether we have a cache."""
        return (
            self.cache_expire_after > 0
            and self.cache_max_bytes != 0
            and self.cache_max_file_bytes > 0
        )

    @config_property
    def cache_max_file_bytes(self) -> int:
        """The maximum size of a cached file in bytes.

        Variable: CACHE_FILE_SIZE
        Default: 10
        """
        return int(float(self._source.get("CACHE_FILE_SIZE", "10")) * MB)

    @config_property
    def cache_block_bytes(self) -> int:
        """The block size on the file system in bytes."""
        return 4096

    @config_property
    def cache_max_bytes(self) -> int:
        """The maximum size of the cache in bytes.

        Variable: CACHE_SIZE
        Default: 200 (MB)
        """
        value = self._source.get("CACHE_SIZE", "200")
        if value.lower() == "unlimited":
            return -1
        return int(float(value) * MB)

    @config_property
    def allowed_hosts(self) -> list[str]:
        """The allowed hosts.

        Variable: ALLOWED_HOSTS
        Default: []
        """
        result = self._source.get("ALLOWED_HOSTS", "").split(",")
        if result == [""]:
            return []
        return result

    @config_property
    def requests(self) -> requests.Session:
        """The requests session."""
        if self.use_requests_cache:
            return requests_cache.CachedSession(**self.session_params)
        return requests.Session()

    @config_property
    def session_params(self) -> dict[str, Any]:
        """The parameters for requests caching's session."""
        if not self.use_requests_cache:
            return {}
        cache_params = {
            "cache_name": self.cache_path,
            "expire_after": self.cache_expire_after,
            "backend": "filesystem",
        }
        if self.cache_max_bytes > 0:
            cache_params["maximum_cache_bytes"] = self.cache_max_bytes
            cache_params["maximum_file_bytes"] = self.cache_max_file_bytes
            cache_params["block_bytes"] = self.cache_block_bytes
        return cache_params

    @config_property
    def cache_path(self) -> str:
        """The path of the cache.

        Variable: CACHE_DIRECTORY
        Default: a temporary directory
        """
        configured_path = self._source.get("CACHE_DIRECTORY", tempfile.gettempdir())
        cache_path = Path(configured_path) / "open-web-calendar-cache"
        cache_path.mkdir(parents=True, exist_ok=True)
        return str(cache_path)


environment = Config(os.environ)

__all__ = ["Config", "environment"]
