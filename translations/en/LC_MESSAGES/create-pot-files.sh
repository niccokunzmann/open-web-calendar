#!/bin/sh
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

set -e
cd "`dirname \"$0\"`"

for file in `find . -name '*.po' -exec echo {} \;` ; do
  pot="${file}t"
  cp "$file" "$pot"
done
