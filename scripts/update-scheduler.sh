#!/bin/bash

# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

set -e

cd "`dirname \"$0\"`/.."

echo "Cloning scheduler ..."
if [ -d scheduler ]; then
    cd scheduler
    git checkout master
else
    git clone https://github.com/DHTMLX/scheduler.git
    cd scheduler
fi

echo "Updating scheduler ..."
git pull
git fetch

latest_version="`git tag | sort -V | tail -n 1`"
echo "Using latest version $latest_version"
git checkout -q "$latest_version"

echo "Updating files ..."
function update_file() {
    from="$1"
    to_dir="../open_web_calendar/static/"
    name="`basename \"$from\"`"
    to="`find ../open_web_calendar/ -iname \"$name\"`"
    if [ "`echo \"$to\" | wc -l`" != 1 ]; then
        echo "Error: found $name twice! Copy it yourself!"
        echo "from: $from"
        echo "to: $to"
        return
    fi
    echo "Updating $name ..."
    cp "$from" "$to"
}

update_file codebase/dhtmlxscheduler.css
update_file codebase/dhtmlxscheduler.d.ts
update_file codebase/dhtmlxscheduler.js
update_file codebase/dhtmlxscheduler.js.map
