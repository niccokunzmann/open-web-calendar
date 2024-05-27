#!/bin/bash
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only


cd "`dirname \"$0\"`"
cd ..

if ! which linkchecker > /dev/null; then
  pip3 install linkchecker
fi
if ! which tox > /dev/null; then
  pip3 install tox
fi

tox -e docs -- build || exit 2
python3 -m http.server -d site 63728 &
docs_PID="$!"

sleep 1

linkchecker \
  -o text \
  -F html \
  --ignore-url='.canonical$|http://localhost:5000|//[^/]*\.onion/|/security/code-scanning/|//(www\.)?ngi\.eu|/translations/.*\.md\.po$' \
  --check-extern \
  --user-agent 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0' \
  --threads 50 \
  http://127.0.0.1:63728/
result="$?"

kill "$docs_PID"
wait
exit $?
