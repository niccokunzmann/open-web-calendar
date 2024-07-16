# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

from .app import app, main

try:
    from .version import __version__, __version_tuple__, version, version_tuple
except ModuleNotFoundError:
    __version__ = version = "0.0dev0"
    __version_tuple__ = version_tuple = (0, 0, "dev0")

__all__ = [
    "main",
    "app",
    "__version__",
    "version",
    "__version_tuple__",
    "version_tuple",
]
