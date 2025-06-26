# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Error handling for Open Web Calendar."""

from __future__ import annotations

import sys
import traceback
from typing import TYPE_CHECKING

from flask import Response, jsonify, request

from open_web_calendar.config import environment as config

if TYPE_CHECKING:
    from types import TracebackType


def http_status_code_for_error(error: Exception) -> int:
    """Return the status code from an exception or 500."""
    return getattr(error, "http_status_code", 500)


def json_error(
    err: BaseException | None = None, tb: TracebackType | None = None
) -> Response:
    """Return the active exception as json."""
    if err is None:
        _, err, tb = sys.exc_info()
    if tb is None:
        tb = err.__traceback__
    status_code = http_status_code_for_error(err)
    traceback.print_exception(type(err), err, tb)
    return jsonify(
        convert_error_message_to_json(
            type(err).__name__,
            str(err),
            request.url,
            "\n".join(traceback.format_exception(type(err), err, tb)),
            status_code,
        )
    ), status_code


def convert_error_message_to_json(
    error_type: str, message: str, url: str, traceback: str, status_code: int = 500
) -> dict[str, str | None]:
    """Create a JSON error message for an error.

    Args:
        error (str): The error message.
        url (str): The URL of the error.
        traceback (str): The traceback of the error.
        status_code (int): The status code of the error.

    Returns:
        dict: The JSON error message.

    This uses the debug flag in the config to determine if the traceback
    should be included in the error message.
    """
    return {
        "message": message if config.debug else error_type,
        "description": message if config.debug else error_type,
        "url": url,  # the url is public anyway and not sensitive
        "traceback": traceback if config.debug else "",
        "error": error_type,
        "text": error_type,
        "code": status_code,
    }


__all__ = ["convert_error_message_to_json", "http_status_code_for_error", "json_error"]
