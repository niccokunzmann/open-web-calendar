# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Set the canonical URL of pages

See https://www.mkdocs.org/user-guide/configuration/#hooks
See https://github.com/squidfunk/mkdocs-material/discussions/6730#discussioncomment-8339285

This makes the links easily detectable by the link checker.
"""

CANONICAL_EXT = ".canonical"


def on_page_markdown(markdown, *, page, config, files):
    if not page.canonical_url.endswith(CANONICAL_EXT):
        page.canonical_url = page.canonical_url + CANONICAL_EXT
