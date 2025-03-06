# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""This adds mocking of API requests to the Open Web Calendar."""

from __future__ import annotations

from pathlib import Path
from threading import Timer

from responses import (
    RequestsMock,
    _recorder,
)
from responses.registries import OrderedRegistry

HERE = Path(__file__).parent
RESPONSES = HERE / "responses"
HEADER = """# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""


class Recorder:
    """Record requests."""

    def __init__(self, name: str):
        """Record requests in a file."""
        self._name = name
        self._last_saved_registered = []

    @property
    def _recorder(self):
        """The recorder we use."""
        return _recorder.recorder

    def start(self):
        """Start recording requests to the API.

        Previous recordings will be deleted.
        """
        self._recorder.reset()
        self._recorder.start()

    def save(self):
        """Save all recordings."""
        registered = self._recorder.get_registry().registered[:]
        if registered == self._last_saved_registered:
            return
        file_name = RESPONSES / f"{self._name}.yml"
        self._recorder.dump_to_file(file_path=file_name, registered=registered)
        file_name.write_text(
            HEADER + file_name.read_text().replace("content-encoding: gzip", "")
        )
        self._last_saved_registered = registered

    def stop(self):
        """Stop recording."""
        self._recorder.stop()

    @classmethod
    def development(cls) -> Recorder:
        """The recording used in the development setting."""
        dev = cls("dev")
        dev.start()
        dev.save_periodically()
        return dev

    def save_periodically(self, interval_in_seconds: float = 1):
        """Save the content preriodically to disk."""
        self.save()
        Timer(interval_in_seconds, self.save_periodically).start()


class Recording:
    """Replay a priviously recorded API."""

    def __init__(self):
        """Allow loading recorded API requests."""
        self.rsps = RequestsMock(registry=OrderedRegistry)

    def load(self, name: str):
        """Load a recording and start serving it."""
        self.stop()
        path = RESPONSES / f"{name}.yml"
        # see https://github.com/getsentry/responses?tab=readme-ov-file#replay-responses-populate-registry-from-files
        self.rsps._add_from_file(file_path=path)
        self.rsps.start()

    def stop(self):
        """Stop using the test API."""
        self.rsps.stop(allow_assert=False)
        self.rsps.reset()


__all__ = ["Recorder", "Recording"]
