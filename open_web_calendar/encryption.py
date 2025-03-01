# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Encryption for endpoints and data."""
from __future__ import annotations

import json
from typing import Any

from cryptography.fernet import Fernet, MultiFernet


class InvalidKey(ValueError):
    """This key cannot be used for encryption."""


class DecryptedData:
    """Data that has been decrypted."""

    def __init__(self, data:dict):
        """The data that is decrypted."""
        self._data = data

    def __getitem__(self, name: str) -> Any:
        return self._data[name]

class FernetStore:
    """Allow encrypting and decrypting values."""

    def __init__(self, keys:list[str]):
        """Create a new """
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
        return self._fernet.encrypt(string.encode("UTF-8")).decode("UTF-8")

    def decrypt(self, data:str) -> DecryptedData:
        """Decrypt the data."""
        string = self._fernet.decrypt(data.encode("UTF-8")).decode("UTF-8")
        data = json.loads(string)
        return DecryptedData(data)

    @staticmethod
    def generate_key() -> str:
        """Generate a key to be used."""
        return Fernet.generate_key().decode("utf-8")


__all__ = ["DecryptedData", "FernetStore", "InvalidKey"]
