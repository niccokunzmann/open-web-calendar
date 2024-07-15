#!/bin/sh

# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

gunicorn -w "$WORKERS" -b "0.0.0.0:$PORT" open_web_calendar.app:app
