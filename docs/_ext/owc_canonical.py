# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx

# The suffix tells the documentation link checker to skip canonical URLs.
CANONICAL_EXT = ".canonical"


def append_canonical_suffix(app, pagename, templatename, context, doctree):
    pageurl = context.get("pageurl")
    if pageurl:
        context["pageurl"] = pageurl + CANONICAL_EXT


def setup(app: Sphinx):
    app.connect("html-page-context", append_canonical_suffix)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": "1.0",
    }
