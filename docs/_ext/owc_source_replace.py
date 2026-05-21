# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

from typing import TYPE_CHECKING

from _links import LINK_URLS

if TYPE_CHECKING:
    from sphinx.application import Sphinx

# Expanded before MyST parses because `myst_substitutions` does not
# support `{{var}}` inside `[text]({{var}})` link targets.
LINK_REPLACEMENTS = {f"{{{{link.{k}}}}}": v for k, v in LINK_URLS.items()}


def on_source_read(app, docname, source):
    text = source[0]
    for token, replacement in LINK_REPLACEMENTS.items():
        text = text.replace(token, replacement)
        spaced = token.replace("{{", "{{ ").replace("}}", " }}")
        text = text.replace(spaced, replacement)
    source[0] = text


def setup(app: Sphinx):
    app.connect("source-read", on_source_read)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": "1.0",
    }
