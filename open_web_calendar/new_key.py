# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Generate a new key and offer encryption setup help."""

from open_web_calendar.encryption import BaseStore

store = BaseStore.from_environment()
if store.can_encrypt():
    print("✅ Encryption is set up. You are ready to go!")  # noqa: T201
else:
    print("❌ Encryption is not set up. Please provide a key.")  # noqa: T201
    print("You can use the one generated below.")  # noqa: T201
    print()  # noqa: T201
    print(f"    OWC_ENCRYPTION_KEYS='{store.generate_key()}'")  # noqa: T201
