#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""This file is an interface file for comptibility.

Originally, open_web_calendar/app.py was in this place.
To provide the same interface, this file was created.
"""

from open_web_calendar import app, main

__all__ = ["app", "main"]

if __name__ == "__main__":
    main()
