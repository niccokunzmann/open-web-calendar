#!/bin/bash
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

set -e
shopt -s globstar
cd "`dirname \"$0\"`"

translated_documentation_languages="en"

for lang in `ls ../translations`; do
  for file in index.md.po contributing.md.po ; do
    po="../translations/$lang/LC_MESSAGES/$file"
    msgstr_count="`grep -F 'msgstr' \"$po\" | wc -l`"
    empty_msgstr_count="`grep -F 'msgstr ""' \"$po\" | wc -l`"
    # add to count because of auto-generated messages: X-Generator
    min_messages=$(( empty_msgstr_count + 1 ))
    if test "$msgstr_count" -gt  "$min_messages" ; then
      echo -e "$lang\t has a translation in `basename \"$po\"`\t$po ($msgstr_count, $min_messages)"
      if [[ "$translated_documentation_languages" != *"$lang"* ]]; then
        translated_documentation_languages="$translated_documentation_languages $lang"
      fi
    fi
  done
done

echo "The documentation is translated into: $translated_documentation_languages"

for lang in $translated_documentation_languages; do
  if grep -qE "^ *- $lang\$" ../mkdocs.yml; then
    echo "mdpo.language present: $lang"
  else
    echo "Adding mdpo.language: $lang"
    sed -i "s/# add mdpo.languages above/        - $lang\n# add mdpo.languages above/" ../mkdocs.yml
  fi
done

for lang in $translated_documentation_languages; do
  if grep -qE "^ *lang: $lang\$" ../mkdocs.yml; then
    echo "extra.alternate present: $lang"
  else
    name="`grep -F 'language:' ../translations/$lang/calendar.yml | tail -c +11`"
    if [ -z "$name" ]; then
      echo "ERROR: Did not find a name for $lang. Add it manually."
      continue
    fi
    echo "Adding extra.alternate: $lang as $name"
    sed -i "s/# add extra.alternate languages above/    - name: $name\n      link: $lang\n      lang: $lang\n# add extra.alternate languages above/" ../mkdocs.yml
  fi
done
