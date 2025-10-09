# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""
Open Web Calendar - Embed calendars into your website

Documentation: https://open-web-calendar.quelltext.eu/
Contributing: https://open-web-calendar.quelltext.eu/contributing/
Development: https://open-web-calendar.quelltext.eu/dev/
"""

from .app import app, main
from .version import __version__, __version_tuple__, version, version_tuple

__all__ = [
    "__version__",
    "__version_tuple__",
    "app",
    "main",
    "version",
    "version_tuple",
]
