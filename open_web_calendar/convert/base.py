# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""The base interface to convert calendars to different outputs."""

from __future__ import annotations

import io
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
from typing import Any
from urllib.parse import urljoin

import requests
from flask import Response, jsonify
from lxml import etree

from open_web_calendar.calendars import (
    CalDAVCalendars,
    Calendars,
    ICSCalendars,
    InvalidCalendars,
)
from open_web_calendar.clean_html import clean_html
from open_web_calendar.encryption import EmptyFernetStore, FernetStore


def get_text_from_url(url):
    """Return the text from a url."""
    return requests.get(url, timeout=10).text


class ConversionStrategy:
    """Base class for conversions.

    You can customize how calendars are retrived and if encryption is used.
    """

    # TODO: add as parameters
    MAXIMUM_THREADS = 100

    def __init__(
        self,
        specification: dict[str, Any],
        get_text_from_url=get_text_from_url,
        encryption: EmptyFernetStore | FernetStore | None = None,
        debug: bool = False,  # noqa: FBT001
    ):
        self.specification = specification
        self.encryption = EmptyFernetStore() if encryption is None else encryption
        self.lock = RLock()
        self.components = []
        self.get_text_from_url = get_text_from_url
        self.debug = debug
        self.created()

    def created(self):
        """Template method for subclasses."""

    def error(self, ty, err, tb, url):
        tb_s = io.StringIO()
        traceback.print_exception(ty, err, tb, file=tb_s)
        return self.convert_error(
            str(err) if self.debug else type(err).__name__,
            url,
            tb_s.getvalue() if self.debug else "",
        )

    def convert_error(self, error: str, url: str, tb_s: str):
        """Tell the client more about the error."""
        raise NotImplementedError("To be implemented in subclasses")

    def retrieve_calendars(self):
        """Retrieve the calendars from different sources."""
        urls = self.specification["url"]
        if isinstance(urls, str):
            urls = [urls]
        assert len(urls) <= self.MAXIMUM_THREADS, (
            f"You can only merge {self.MAXIMUM_THREADS} urls."
            " If you like more, open an issue."
        )
        with ThreadPoolExecutor(max_workers=self.MAXIMUM_THREADS) as e:
            for _e in e.map(self.retrieve_calendar, enumerate(urls)):
                pass  # no error should pass silently; import this

    def get_calendars_from_url(self, url: str) -> Calendars:
        """Return a lis of calendars from a URL."""
        if self.encryption.is_encrypted(url):
            url = self.encryption.decrypt(url).url
            if url is None:
                return Calendars.empty()
        if url.startswith("webcal://"):
            url = url.replace("webcal://", "http://", 1)
        calendar_text = self.get_text_from_url(url)
        try:
            return ICSCalendars.from_text(calendar_text)
        except InvalidCalendars:
            # ValueError: Content line could not be parsed into parts:
            # find the alt link
            # see https://stackoverflow.com/a/11466033/1320237
            htmlparser = etree.HTMLParser()
            tree = etree.XML(calendar_text, htmlparser)
            links = tree.xpath('//link[@rel = "alternate" and @type = "text/calendar"]')
            result = ICSCalendars()
            for link in links:  # we expect one link
                href = link.get("href")
                new_url = urljoin(url, href)
                calendar_text = self.get_text_from_url(new_url)
                result.add_from_text(calendar_text)
            if not result:
                # We did not find any link to any calendar from this source.
                # We could have a CalDAV calendar.
                result = CalDAVCalendars.from_url(url)
                if not result:
                    raise
            return result

    def retrieve_calendar(self, index_url: tuple[int, str]):
        """Retrieve a calendar from a url"""
        try:
            index, url = index_url
            calendars = self.get_calendars_from_url(url)
            self.collect_components_from(index, calendars)
        except:
            ty, err, tb = sys.exc_info()
            with self.lock:
                self.components.append(self.error(ty, err, tb, url))

    def collect_components_from(self, index: int, calendars: Calendars):
        """Collect all the compenents from the calendar."""
        raise NotImplementedError("to be implemented in subclasses")

    def merge(self):
        """Return the flask Response for the merged calendars."""
        raise NotImplementedError("to be implemented in subclasses")

    def clean_html(self, html: str) -> str:
        """Return the cleaned HTML."""
        return clean_html(html, self.specification)

    def jsonify(self, data: Any) -> Response:
        return jsonify(data)


__all__ = ["ConversionStrategy", "get_text_from_url"]
