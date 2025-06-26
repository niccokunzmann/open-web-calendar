# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Encryption for endpoints and data.

See https://cryptography.io/en/latest/fernet/
"""

from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from typing import Any

import bcrypt
from cryptography.fernet import Fernet, MultiFernet

PREFIX = "fernet://"


class InvalidKey(ValueError):
    """This key cannot be used for encryption."""


class NoKeyProvided(InvalidKey):
    """No key was provided to do any cryptographic operation."""


class InvalidPassword(ValueError):
    """The passwords provided do not allow sharing this data."""

    http_status_code = 403


def get_password_hash(password: str) -> str:
    """Return a hash with password and salt."""
    # https://stackoverflow.com/a/13001189/1320237
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, pw_hash: str) -> bool:
    """Check if the password matches the hash."""
    return bcrypt.checkpw(password.encode(), pw_hash.encode())


class DecryptedData:
    """Data that has been decrypted."""

    def __init__(self, data: dict):
        """The data that is decrypted."""
        self._data = data

    def __getitem__(self, name: str) -> Any:
        return self._data[name]

    @property
    def url(self) -> str | None:
        return self._data.get("url")

    def expose(self, passwords: list[str]) -> dict:
        """Expose the data to the user.

        Raises InvalidPassword if no password is correct.
        """
        for password in passwords:
            for pw_hash in self._data.get("hashes", []):
                if check_password(password, pw_hash):
                    return self._data
        raise InvalidPassword("None of the passwords provided allow sharing this data.")


class BaseStore(ABC):
    """Sharing basic functionality."""

    @staticmethod
    def generate_key() -> str:
        """Generate a key to be used."""
        return Fernet.generate_key().decode("utf-8")

    @classmethod
    def from_environment(cls) -> FernetStore | EmptyFernetStore:
        """Create a new Fernet store from environment variables.

        We load the keys from the OWC_ENCRYPTION_KEYS environment variable.
        """
        keys = os.environ.get("OWC_ENCRYPTION_KEYS", "").split(",")
        return EmptyFernetStore() if keys == [""] else FernetStore(keys)

    @staticmethod
    def is_encrypted(data: str) -> bool:
        """Wether this data is encrypted."""
        return data.startswith(PREFIX)

    def expose(self, data: str, passwords: list[str]) -> dict:
        """Expose the data to the user."""
        decrypted = self.decrypt(data)
        return decrypted.expose(passwords)

    @classmethod
    def can_encrypt(cls) -> bool:
        return False

    @classmethod
    def can_decrypt(cls) -> bool:
        """Wether we can decrypt data."""
        return cls.can_encrypt()

    @abstractmethod
    def encrypt(self, data: dict) -> str:
        """Encrypt data."""

    @abstractmethod
    def decrypt(self, data: str) -> DecryptedData:
        """Decrypt the data."""


class EmptyFernetStore(BaseStore):
    def encrypt(self, data: dict) -> str:
        """We cannot encrypt anything."""
        raise NoKeyProvided("No key was provided to do any cryptographic operation.")

    def decrypt(self, data: str) -> DecryptedData:
        """We cannot decrypt anything."""
        raise NoKeyProvided("No key was provided to do any cryptographic operation.")


class FernetStore(BaseStore):
    """Allow encrypting and decrypting values."""

    @staticmethod
    def can_encrypt() -> bool:
        return True

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


__all__ = ["DecryptedData", "EmptyFernetStore", "FernetStore", "InvalidKey"]
