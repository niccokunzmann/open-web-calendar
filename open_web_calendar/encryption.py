# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Encryption for endpoints and data.

See https://cryptography.io/en/latest/fernet/
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any, Optional

from cryptography.fernet import Fernet, MultiFernet

PREFIX = "fernet://"


class InvalidKey(ValueError):
    """This key cannot be used for encryption."""


class InvalidPassword(ValueError):
    """The passwords provided do not allow sharing this data."""

    http_status_code = 403


def get_salt() -> str:
    """Return a salt for hashing."""
    return os.urandom(16).hex()


def get_password_hash(password: str, salt: Optional[str] = None):
    """Return a hash with password and salt."""
    if salt is None:
        salt = get_salt()
    return hashlib.sha3_512(password.encode() + salt.encode()).hexdigest(), salt


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

    def expose(self, passwords: list[str]) -> dict:
        """Expose the data to the user.

        Raises InvalidPassword if no password is correct.
        """
        for password in passwords:
            for hash_, salt in self._data.get("hashes", []):
                if hash_ == get_password_hash(password, salt)[0]:
                    return self._data
        raise InvalidPassword("None of the passwords provided allow sharing this data.")


class EmptyFernetStore:
    @staticmethod
    def encrypt(*args, **kw) -> str:  # noqa: ARG004
        raise InvalidKey("Cannot encrypt, no key provided.")

    @staticmethod
    def decrypt(*args, **kw) -> str:  # noqa: ARG004
        raise InvalidKey("Cannot decrypt, no key provided.")

    @staticmethod
    def expose(*args, **kw) -> str:  # noqa: ARG004
        raise InvalidKey("Cannot decrypt, no key provided.")

    @staticmethod
    def can_encrypt() -> bool:
        return False

    @staticmethod
    def is_encrypted(data: str) -> bool:
        """Wether this data is encrypted."""
        return data.startswith(PREFIX)


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
        if "password" in data:
            data.setdefault("hashes", [])
            data["hashes"].append(get_password_hash(data["password"]))
            del data["password"]
        string = json.dumps(data)
        return PREFIX + self._fernet.encrypt(string.encode("UTF-8")).decode("UTF-8")

    def decrypt(self, data: str) -> DecryptedData:
        """Decrypt the data.

        This value is for accessing data, not for sharing it.
        Use expose() if you want to give this to a user.
        """
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

    def expose(self, data: str, passwords: list[str]) -> dict:
        """Expose the data to the user."""
        decrypted = self.decrypt(data)
        return decrypted.expose(passwords)


__all__ = ["DecryptedData", "EmptyFernetStore", "FernetStore", "InvalidKey"]
