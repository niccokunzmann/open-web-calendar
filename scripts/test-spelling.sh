#!/bin/bash

# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

set -e

cd "`dirname \"$0\"`"

(
  cd ..
  if grep -rqI calend''er; then
    grep -rI calend''er
    echo "ERROR: wrong spelling"
    exit 1
  fi
)
