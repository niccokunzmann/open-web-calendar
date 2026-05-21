#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from pathlib import Path
from subprocess import check_call

HERE = Path(__file__).parent


for po_file in HERE.glob("**/*.po"):
    # add encoding
    content = po_file.read_text()
    print(po_file)  # noqa: T201
    if not any(
        line.startswith(('"Content-Type:', 'msgstr "Content-Type:'))
        for line in content.splitlines()
    ):
        content = content.replace(
            'msgstr ""', 'msgstr ""\n"Content-Type: text/plain; charset=UTF-8\\n"', 1
        )
        print("\t added header")  # noqa: T201
    content = content.replace(
        '"Content-Type": "text/plain; charset=UTF-8\\n"\n', ""
    )  # fix old edit
    po_file.write_text(content)
    # make content uniq
    check_call(["msguniq", "-o", po_file, po_file])  # noqa: S603, S607
