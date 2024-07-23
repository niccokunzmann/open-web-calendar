# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
from __future__ import annotations

import io
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
from urllib.parse import urljoin

import requests
from icalendar import Calendar
from lxml import etree


def get_text_from_url(url):
    """Return the text from a url."""
    return requests.get(url, timeout=10).text


INDEX_TYPE = tuple[int, int]


class CalendarInfo:
    """Provide an easy API for calendar information."""

    def __init__(self, index: INDEX_TYPE, url: str, calendar: Calendar):
        """Create a new calendar info."""
        self._calendar = calendar
        self._index = index
        self._url = url

    @property
    def name(self) -> str:
        """The name of the calendar."""
        name = self._calendar.get("name", self._calendar.get("x-wr-calname"))
        if name is not None:
            return name
        return self._url.rsplit("/", 1)[-1].rsplit(".", 1)[0]

    @property
    def description(self) -> str:
        """The name of the calendar."""
        return self._calendar.get("description", self._calendar.get("x-wr-caldesc", ""))

    @property
    def calendar(self) -> Calendar:
        """My calendar."""
        return self._calendar

    @property
    def index(self) -> INDEX_TYPE:
        """The index of the calendar url.

        Since one URL can have several calendars, this is multiple indices."""
        return self._index

    @property
    def event_css_classes(self) -> list[str]:
        """The css classes for all events in this calendar."""
        return [
            f"CALENDAR-INDEX-{self.index[0]}",
            f"CALENDAR-INDEX-{self.index[0]}-{self.index[1]}",
        ]

    @property
    def id(self) -> str:
        """Return this calendar information as JSON."""
        return f"{self.index[0]}-{self.index[1]}"

    def to_json(self) -> dict[str, any]:
        """Return a JSON compatible version of this information."""
        return {
            "id": self.id,
            "type": "calendar",
            "url-index": self.index[0],
            "calendar-index": self.index[0],
            "name": self.name,
            "description": self.description,
            "url": self._url,
            "event-css-classes": self.event_css_classes,
        }


class ConversionStrategy:
    """Base class for conversions."""

    # TODO: add as parameters
    MAXIMUM_THREADS = 100

    def __init__(self, specification, get_text_from_url=get_text_from_url):
        self.specification = specification
        self.lock = RLock()
        self.components = []
        self.get_text_from_url = get_text_from_url
        self.created()

    def created(self):
        """Template method for subclasses."""

    def error(self, ty, err, tb, url):
        tb_s = io.StringIO()
        traceback.print_exception(ty, err, tb, file=tb_s)
        return self.convert_error(err, url, tb_s.getvalue())

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

    def get_calendars_from_url(self, url: str):
        """Return a lis of calendars from a URL."""
        if url.startswith("webcal://"):
            url = url.replace("webcal://", "http://", 1)
        calendar_text = self.get_text_from_url(url)
        try:
            return Calendar.from_ical(calendar_text, multiple=True)
        except ValueError:
            # ValueError: Content line could not be parsed into parts:
            # find the alt link
            # see https://stackoverflow.com/a/11466033/1320237
            htmlparser = etree.HTMLParser()
            tree = etree.XML(calendar_text, htmlparser)
            links = tree.xpath('//link[@rel = "alternate" and @type = "text/calendar"]')
            result = []
            for link in links:
                href = link.get("href")
                new_url = urljoin(url, href)
                calendar_text = self.get_text_from_url(new_url)
                result += Calendar.from_ical(calendar_text, multiple=True)
            if result == []:
                # We did not find any link to any calendar from this source.
                raise
            return result

    def retrieve_calendar(self, index_url):
        """Retrieve a calendar from a url"""
        try:
            index, url = index_url
            calendars = self.get_calendars_from_url(url)
            for i, calendar in enumerate(calendars):
                self.collect_components_from(CalendarInfo((index, i), url, calendar))
        except:
            ty, err, tb = sys.exc_info()
            self.add_component(self.error(ty, err, tb, url))

    def add_component(self, component):
        """Add a component to the result."""
        with self.lock:
            self.components.append(component)

    def collect_components_from(self, calendar_info: CalendarInfo):
        """Collect all the compenents from the calendar."""
        raise NotImplementedError("to be implemented in subclasses")

    def merge(self):
        """Return the flask Response for the merged calendars."""
        raise NotImplementedError("to be implemented in subclasses")

    def convert_error(self, err: Exception, url: str, traceback: str):
        """Convert an error."""
        raise NotImplementedError("to be implemented in subclasses")


__all__ = ["ConversionStrategy", "get_text_from_url", "CalendarInfo", "INDEX_TYPE"]
