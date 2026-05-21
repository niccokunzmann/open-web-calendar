# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

import datetime
import re
from email.utils import format_datetime
from pathlib import Path
from typing import TYPE_CHECKING
from xml.sax.saxutils import escape

if TYPE_CHECKING:
    from sphinx.application import Sphinx

DATE_PREFIX = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-")
H1 = re.compile(r"^#\s+(.+)$", re.MULTILINE)
PARA = re.compile(r"^\n+([^#\n][^\n]+(?:\n[^#\n][^\n]+)*)$", re.MULTILINE)


def _parse_post(path: Path) -> dict[str, str | datetime.datetime]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5 :]

    match = DATE_PREFIX.match(path.stem)
    if match:
        date = datetime.datetime(
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            tzinfo=datetime.timezone.utc,
        )
    else:
        date = datetime.datetime.fromtimestamp(
            path.stat().st_mtime, tz=datetime.timezone.utc
        )

    title_match = H1.search(text)
    title = title_match.group(1).strip() if title_match else path.stem

    description = ""
    if title_match:
        after_title = text[title_match.end() :]
        para_match = PARA.search(after_title)
        if para_match:
            description = para_match.group(1).strip()

    return {
        "title": title,
        "date": date,
        "description": description,
        "slug": path.stem,
    }


def _render_feed(posts: list[dict], site_url: str, language: str) -> str:
    posts_sorted = sorted(posts, key=lambda p: p["date"], reverse=True)
    items = []
    for post in posts_sorted:
        link = f"{site_url}news/{post['slug']}/"
        items.append(
            "    <item>\n"
            f"      <title>{escape(post['title'])}</title>\n"
            f"      <link>{escape(link)}</link>\n"
            f'      <guid isPermaLink="true">{escape(link)}</guid>\n'
            f"      <pubDate>{format_datetime(post['date'])}</pubDate>\n"
            f"      <description>{escape(post['description'])}</description>\n"
            "    </item>"
        )
    items_xml = "\n".join(items)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n'
        "  <channel>\n"
        "    <title>Open Web Calendar</title>\n"
        f"    <link>{escape(site_url)}</link>\n"
        "    <description>News about the Open Web Calendar.</description>\n"
        f"    <language>{escape(language)}</language>\n"
        f"{items_xml}\n"
        "  </channel>\n"
        "</rss>\n"
    )


def on_build_finished(app, exception):
    if exception is not None:
        return
    if app.builder.name != "html":
        return

    news_dir = Path(app.srcdir) / "news"
    posts = [_parse_post(p) for p in news_dir.glob("*.md")]
    if not posts:
        return

    site_url = app.config.html_baseurl.rstrip("/") + "/"
    feed = _render_feed(posts, site_url, app.config.language)

    out_path = Path(app.outdir) / "feed.xml"
    out_path.write_text(feed, encoding="utf-8")


def setup(app: Sphinx):
    app.connect("build-finished", on_build_finished)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": "1.0",
    }
