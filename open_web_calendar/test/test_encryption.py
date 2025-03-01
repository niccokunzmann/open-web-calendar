# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Test encrypting and decrypting values."""
import pytest
from open_web_calendar.encryption import FernetStore, InvalidKey


@pytest.mark.parametrize(
    "data", 
    [
        {},
        {"test": 1, "url": "https://asd.asd"},
        {"nose": 1, "url": "https://asd.asd/2"},
    ]
)
def test_we_can_encrypt_json(data, store):
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
    "keys", [
        [],
        ["invalid key"],
        [FernetStore.generate_key(), "invalid key"],
        [FernetStore.generate_key() + "asd", "invalid key"],
    ]
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
