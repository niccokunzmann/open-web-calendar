# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""If the Open Web Calendar is started in tests in a different process.

This allows communication and configuration.
"""

from __future__ import annotations

import multiprocessing
import multiprocessing.connection
import os
import sys
import threading
from functools import wraps
from io import StringIO

from open_web_calendar.test.api_mocking import Recording

recording = Recording()


def _raise(err):
    raise err


def _return(result):
    return result


def remote_call(func):
    """Turn a function into a remote call."""

    @wraps(func)
    def wrapper(self: RPCPipe | None, *args, **kw):
        if self is None:
            return func(*args, **kw)
        return self.call(wrapper, None, *args, **kw)

    return wrapper


OUTPUT = StringIO()


class RPCPipe:
    """Send calls to the other process."""

    def __init__(self):
        """Create a new RPCPipe."""
        self.connection, other_connection = multiprocessing.Pipe()
        self.for_other_process = self.ProcessingPipe(other_connection)

    class ProcessingPipe:
        def __init__(self, connection: multiprocessing.connection.Connection):
            self.connection = connection

        def start(self):
            """Serve calls."""
            thread = threading.Thread(target=self.loop)
            thread.start()

        def loop(self):
            """React in a loop"""
            while True:
                func, args, kw = self.connection.recv()
                try:
                    result = func(*args, **kw)
                except:
                    self.connection.send((_raise, (sys.exc_info()[1],), {}))
                else:
                    self.connection.send((_return, (result,), {}))

    def call(self, function, *args, **kw):
        """Call a function in the other process."""
        self.connection.send((function, args, kw))
        func, args, kw = self.connection.recv()
        return func(*args, **kw)

    @remote_call
    def start_recorded_api(name: str):  # noqa: N805
        recording.load(name)

    @remote_call
    def stop_recorded_api():
        recording.stop()

    @remote_call
    def enable_encryption():
        os.environ["OWC_ENCRYPTION_KEYS"] = (
            "cxXiQ8n7ZkgdiAZ-GX2lkANZKbZDaqqq1vdyS7eGsFw="
        )

    @remote_call
    def disable_encryption():
        del os.environ["OWC_ENCRYPTION_KEYS"]

    @remote_call
    def capture_stdout():
        global OUTPUT  # noqa: PLW0603
        sys.stderr = sys.stdout = OUTPUT = StringIO()

    @remote_call
    def get_output() -> str:
        return OUTPUT.getvalue()


__all__ = ["RPCPipe"]
