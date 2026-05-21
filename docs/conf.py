# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

import datetime
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "_ext"))

from _links import LINK_URLS

project = "Open Web Calendar"
copyright = (  # noqa: A001
    f"{datetime.date.today().year}, "  # noqa: DTZ011
    "Nicco Kunzmann and Open Web Calendar Contributors"
)
author = "Nicco Kunzmann and Open Web Calendar Contributors"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_issues",
    "sphinx_sitemap",
    "sphinxext.opengraph",
    "notfound.extension",
    "owc_source_replace",
    "owc_canonical",
    "owc_rss",
]

source_suffix = {".md": "markdown"}
root_doc = "index"
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "snippets",
    "assets/templates",
    "assets/calendars",
]
templates_path = ["_templates"]

myst_enable_extensions = [
    "attrs_inline",
    "attrs_block",
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 4

# Pygments' CSS lexer rejects the backslash-escaped selectors generated
# from rfc-822 email-style UIDs. Acceptable; the block still renders.
suppress_warnings = ["misc.highlighting_failure"]

# Substitutions cannot be used in `[text]({{var}})` link targets; those
# tokens are expanded by owc_source_replace before MyST parses.
myst_substitutions = {f"link_{k}": v for k, v in LINK_URLS.items()}

language = "en"
locale_dirs = ["locale"]
gettext_compact = False
gettext_uuid = False
gettext_location = False

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_extra_path = ["assets"]
html_logo = "assets/img/logo/owc.svg"
html_favicon = "assets/img/logo/owc.svg"
html_title = "Open Web Calendar"
html_baseurl = "https://open-web-calendar.quelltext.eu/"
html_css_files = ["css/custom.css"]

html_theme_options = {
    "icon_links": [
        {
            "name": "Website",
            "url": "https://open-web-calendar.hosted.quelltext.eu",
            "icon": "fa-solid fa-globe",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/niccokunzmann/open-web-calendar/",
            "icon": "fa-brands fa-square-github",
        },
        {
            "name": "Weblate",
            "url": "https://hosted.weblate.org/engage/open-web-calendar/",
            "icon": "fa-solid fa-language",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/open-web-calendar/",
            "icon": "fa-brands fa-python",
        },
        {
            "name": "Docker",
            "url": "https://hub.docker.com/r/niccokunzmann/open-web-calendar",
            "icon": "fa-brands fa-docker",
        },
        {
            "name": "Mastodon",
            "url": "https://toot.wales/tags/OpenWebCalendar",
            "icon": "fa-brands fa-mastodon",
        },
    ],
    "use_edit_page_button": True,
    "show_nav_level": 1,
    "show_toc_level": 2,
    "navigation_with_keys": True,
    "footer_start": ["copyright"],
    "footer_end": ["theme-version"],
    "article_footer_items": ["comments.html"],
}

html_context = {
    "github_user": "niccokunzmann",
    "github_repo": "open-web-calendar",
    "github_version": "master",
    "doc_path": "docs",
    "languages": yaml.safe_load(
        (HERE / "_languages.yml").read_text(encoding="utf-8")
    )["languages"],
}

issues_github_path = "niccokunzmann/open-web-calendar"

sitemap_url_scheme = "{lang}{link}"

ogp_site_url = "https://open-web-calendar.quelltext.eu/"
ogp_image = "https://open-web-calendar.quelltext.eu/assets/img/logo/owc.svg"

linkcheck_retries = 2
linkcheck_timeout = 15
linkcheck_anchors = True
linkcheck_ignore = [
    r"http://localhost.*",
    r"https?://127\.0\.0\.1.*",
    r"https?://192\.168\.\d+\.\d+.*",
    r"https?://[^/]*\.onion/.*",
    r"https?://heroku\.com/.*",
    r"https?://polar\.sh/niccokunzmann/open-web-calendar",
    r"https?://antroposofiachile\.net/.*",
    r"https?://(www\.)?squid-cache\.org/.*",
    r"https?://(www\.)?cloudron\.io/.*",
    r"https?://(www\.)?ngi\.eu.*",
    r".*\.canonical$",
]
