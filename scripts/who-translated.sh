#!/bin/bash

# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

TRANSLATION_MATCH="Translated using Weblate"

# These translators are sorted by number of commits
translators="`git log --grep="" --pretty="%ae" | sort | uniq -c | sort -n | awk '{print $2}' | tac`"
#git log --grep="$TRANSLATION_MATCH" --pretty="%ae" | sort | uniq -c | sort -n



echo "| Translator | Language | Commits |"
echo "| ---------- | -------- | ------- |"
for translator in $translators; do
    if echo "$translator" | grep -q "weblate.org"; then
        continue
    fi
    name="`git log --grep="$TRANSLATION_MATCH" --author="$translator" --pretty="%an <%ae>" | head -n 1`"
    if [ -z "$name" ]; then
        continue
    fi
    language="`git log --grep="$TRANSLATION_MATCH" --author="$translator" --pretty="%B" \
        | grep -Po "$TRANSLATION_MATCH *\(\K[^)]*" | sort | uniq -c | sort -n | tail -n 1 | awk '{print $2 " | " $1}'
        `"
    if [ -z "$language" ]; then
        continue
    fi
    echo "| $name | $language |"
done
