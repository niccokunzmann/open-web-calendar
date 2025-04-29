# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Error handling for Open Web Calendar."""
from __future__ import annotations

import sys
import traceback
from typing import TYPE_CHECKING

from flask import jsonify, request

from open_web_calendar.config import environment as config

if TYPE_CHECKING:
    from types import TracebackType


def http_status_code_for_error(error: Exception) -> int:
    """Return the status code from an exception or 500."""
    return getattr(error, "http_status_code", 500)


def json_error(err: BaseException | None = None, tb: TracebackType | None = None):
    """Return the active exception as json."""
    if err is None:
        _, err, tb = sys.exc_info()
    if tb is None:
        tb = err.__traceback__
    status_code = http_status_code_for_error(err)
    traceback.print_exception(type(err), err, tb)
    message = str(err) if config.debug else None
    error = type(err).__name__
    return jsonify(
        {
            "message": message,
            "description": message,
            "url": request.url,
            "traceback": traceback.format_exception(type(err), err, tb)
            if config.debug
            else None,
            "error": error,
            "text": error,
            "code": status_code,
        }
    ), status_code


__all__ = ["http_status_code_for_error", "json_error"]
