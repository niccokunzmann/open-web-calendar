# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Encryption for endpoints and data.

See https://cryptography.io/en/latest/fernet/
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional

from cryptography.fernet import Fernet, MultiFernet

PREFIX = "fernet://"


class InvalidKey(ValueError):
    """This key cannot be used for encryption."""


class DecryptedData:
    """Data that has been decrypted."""

    def __init__(self, data: dict):
        """The data that is decrypted."""
        self._data = data

    def __getitem__(self, name: str) -> Any:
        return self._data[name]

    @property
    def url(self) -> Optional[str]:
        return self._data.get("url")


class EmptyFernetStore:
    @staticmethod
    def encrypt(*args, **kw) -> str:  # noqa: ARG004
        raise InvalidKey("Cannot encrypt, no key provided.")

    @staticmethod
    def decrypt(*args, **kw) -> str:  # noqa: ARG004
        raise InvalidKey("Cannot encrypt, no key provided.")

    @staticmethod
    def can_encrypt() -> bool:
        return False


class FernetStore:
    """Allow encrypting and decrypting values."""

    @staticmethod
    def can_encrypt() -> bool:
        return True

    @classmethod
    def from_environment(cls) -> FernetStore | EmptyFernetStore:
        """Create a new Fernet store from environment variables.

        We load the keys from the OWC_ENCRYPTION_KEYS environment variable.
        """
        keys = os.environ.get("OWC_ENCRYPTION_KEYS", "").split(",")
        return EmptyFernetStore() if keys == [""] else cls(keys)

    def __init__(self, keys: list[str]):
        """Create a new Fernet store to encrypt and decrypt values."""
        self._keys = keys[:]
        fernets = []
        for i, key in enumerate(keys):
            try:
                fernet = Fernet(key.encode("UTF-8"))
            except ValueError as e:
                raise InvalidKey(f"Key {i} is invalid.") from e
            fernets.append(fernet)
        if not fernets:
            raise InvalidKey("We need at least one key.")
        self._fernet = MultiFernet(fernets)

    @property
    def keys(self) -> list[str]:
        """The keys in use."""
        return self._keys[:]

    def encrypt(self, data: dict) -> str:
        """Encrypt the data."""
        string = json.dumps(data)
        return PREFIX + self._fernet.encrypt(string.encode("UTF-8")).decode("UTF-8")

    def decrypt(self, data: str) -> DecryptedData:
        """Decrypt the data."""
        if not self.is_encrypted(data):
            raise ValueError("Data is not encrypted.")
        token = data[len(PREFIX) :].encode("UTF-8")
        string = self._fernet.decrypt(token).decode("UTF-8")
        data = json.loads(string)
        return DecryptedData(data)

    @staticmethod
    def is_encrypted(data: str) -> bool:
        """Wether this data is encrypted."""
        return data.startswith(PREFIX)

    @staticmethod
    def generate_key() -> str:
        """Generate a key to be used."""
        return Fernet.generate_key().decode("utf-8")


__all__ = ["DecryptedData", "FernetStore", "InvalidKey"]
