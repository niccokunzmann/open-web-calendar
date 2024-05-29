#!/bin/bash
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

#
# We want to make sure that weblate can use the documentation translation files.
#

if grep -rF "`echo -e \"\x02\"`" translations/ || grep -rF "`echo -e \"\x02\"`" translations/; then
  echo "Weblate could not parse the translation files while updating the translations."
  exit 1
fi
