# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Clean HTML content of events.

This is important to mitigate attacks from ICS sources.
See https://stackoverflow.com/questions/3073881/clean-up-html-in-python
"""

import re
import warnings

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from lxml.html.clean import Cleaner

CLEAN_HTML_SPECIFICATION_PREFIX = "clean_html_"
DEFAULT_SPEC = {
    "page_structure": True,
    "remove_tags": ("body", "div"),
}
HTML_TAG_MATCH = re.compile("<[^>]*>")


def clean_html(bad_html: str, spec: dict) -> str:
    """Clean up the HTML.

    For the content of the spec parameter, see
    - the default_specification.yml file, clean_html_* attributes
    - https://lxml.de/api/lxml.html.clean.Cleaner-class.html
    """
    with warnings.catch_warnings():
        # ignore that input might be short
        # see https://stackoverflow.com/a/17654868/1320237
        warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
        tree = BeautifulSoup(bad_html, "html.parser")
    bad_html = tree.prettify()
    kw = DEFAULT_SPEC.copy()
    kw.update(
        {
            name[len(CLEAN_HTML_SPECIFICATION_PREFIX) :]: value
            for name, value in spec.items()
            if name.startswith(CLEAN_HTML_SPECIFICATION_PREFIX)
        }
    )
    cleaner = Cleaner(**kw)
    result = cleaner.clean_html(f"<div>{bad_html}</div>").strip()
    if result.startswith("<div>"):
        result = result[5:-6]
    return result


def remove_html(html: str) -> str:
    """Remove all HTML from the html string and only return the text."""
    return HTML_TAG_MATCH.sub("", html)


__all__ = ["clean_html", "remove_html"]
