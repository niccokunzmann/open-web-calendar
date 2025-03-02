# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test encrypting and decrypting values.


"""

import os

import pytest
from flask.testing import FlaskClient

from open_web_calendar.app import get_configuration
from open_web_calendar.conversion_base import ConversionStrategy
from open_web_calendar.encryption import (
    DecryptedData,
    EmptyFernetStore,
    FernetStore,
    InvalidKey,
)


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"test": 1, "url": "https://asd.asd"},
        {"nose": 1, "url": "https://asd.asd/2"},
    ],
)
def test_we_can_encrypt_json(data, store: FernetStore):
    """Test that we can encrypt and decrypt values."""
    encrypted = store.encrypt(data)
    assert isinstance(encrypted, str)
    decrypted = store.decrypt(encrypted)
    assert not isinstance(decrypted, dict)
    for key, value in data.items():
        assert decrypted[key] == value


def test_generate_key():
    """Generate a key."""
    key = FernetStore.generate_key()
    assert isinstance(key, str)
    store = FernetStore([key])
    assert store.keys == [key]


@pytest.mark.parametrize(
    "keys",
    [
        [],
        ["invalid key"],
        [FernetStore.generate_key(), "invalid key"],
        [FernetStore.generate_key() + "asd", "invalid key"],
    ],
)
def test_invalid_key(keys):
    """Test invalid keys."""
    with pytest.raises(InvalidKey):
        FernetStore(keys)


def test_encrypt_with_one_key_and_decrypt_with_more():
    """Test rotating keys."""
    key = FernetStore.generate_key()
    store = FernetStore([key])
    data = {"test": 1, "url": "https://asd.asd"}
    encrypted = store.encrypt(data)
    store = FernetStore([FernetStore.generate_key(), key])
    decrypted = store.decrypt(encrypted)
    for key, value in data.items():
        assert decrypted[key] == value


def test_url_attribute():
    """Test the URL attribute."""
    d = DecryptedData({"url": "https://asd.asd"})
    assert d.url == "https://asd.asd"


def test_url_attribute_absent():
    """Test the URL attribute."""
    d = DecryptedData({"urla": "https://asd.asd"})
    assert d.url is None


def test_encrypted_values_start_with_fernet(store: FernetStore):
    """The data should be clearly distinguishable."""
    data = {"test": 1, "url": "https://asd.asd"}
    encrypted = store.encrypt(data)
    assert encrypted.startswith("fernet://")
    assert store.is_encrypted(encrypted)


@pytest.mark.parametrize("data", [{"test": 1, "url": "https://asd.asd"}, {}])
def test_encrypt_values_with_a_url(client: FlaskClient, store: FernetStore, data: dict):
    """Check that we can encrypt and decrypt values.

    We should use POST, see https://stackoverflow.com/a/13021883/1320237
    """
    response = client.post("/encrypt", json=data)
    token = response.json["token"]
    assert store.is_encrypted(token)
    decrypted = store.decrypt(token)
    assert decrypted._data == data


def test_can_encrypt_in_configuration(client):
    """Check that the configuration allows encyption."""
    configuration = get_configuration()
    assert configuration["encryption"] is True


def test_encryption_not_possible(monkeypatch):
    """If we have no keys."""
    monkeypatch.setattr(FernetStore, "from_environment", lambda: EmptyFernetStore())
    configuration = get_configuration()
    assert configuration["encryption"] is False


def test_cannot_load_encrytption_from_environment(monkeypatch):
    """Check that there are no keys."""
    monkeypatch.delitem(os.environ, "OWC_ENCRYPTION_KEYS", raising=False)
    store = FernetStore.from_environment()
    assert not store.can_encrypt()


KEY1 = "AHDLqMWyyMLTw87kkcIG_-pD6Dl_4ZWw-GKdNIkVKFc="
KEY2 = "S8UirFfeKg83-qtmt4mr3xYRvSC6osUAP4R8wQJ-72I="


@pytest.mark.parametrize(
    "keys",
    [
        [KEY1, KEY2],
        [KEY1],
    ],
)
def test_load_encrytption_from_environment(monkeypatch, keys):
    """Check that there are keys."""
    monkeypatch.setitem(os.environ, "OWC_ENCRYPTION_KEYS", ",".join(keys))
    store = FernetStore.from_environment()
    assert store.can_encrypt()
    assert store.keys == keys


def test_collect_calendar_from_encrypted_url(store, client, mock):
    """Check that we can collect a calendar from an encrypted url."""
    cb = ConversionStrategy({}, mock, store)
    mock.return_value = ""
    url = store.encrypt({"url": "http://url.to/a/calendar.ics"})
    cb.get_calendars_from_url(url)
    mock.assert_called_once_with("http://url.to/a/calendar.ics")


def test_no_url_included(store, client, mock):
    """The encrypted data has no url, so we have no calendar."""
    cb = ConversionStrategy({}, mock, store)
    mock.return_value = ""
    url = store.encrypt({})
    result = cb.get_calendars_from_url(url)
    assert result == []
    mock.assert_not_called()
