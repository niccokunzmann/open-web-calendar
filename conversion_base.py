from concurrent.futures import ThreadPoolExecutor
from threading import RLock
import requests
import sys
import traceback
import io
from icalendar import Calendar

def get_text_from_url(url):
    """Return the text from a url."""
    return requests.get(url).text


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
        assert len(urls) <= self.MAXIMUM_THREADS, "You can only merge {} urls. If you like more, open an issue.".format(MAXIMUM_THREADS)
        with ThreadPoolExecutor(max_workers=self.MAXIMUM_THREADS) as e:
            for e in e.map(self.retrieve_calendar, urls):
                pass # no error should pass silently; import this
    
    def retrieve_calendar(self, url):
        """Retrieve a calendar from a url"""
        try:
            calendar_text = self.get_text_from_url(url)
            calendars = Calendar.from_ical(calendar_text, multiple=True)
            self.collect_components_from(calendars)
        except:
            ty, err, tb = sys.exc_info()
            with self.lock:
                self.components.append(self.error(ty, err, tb, url))
     
    def collect_components_from(self, calendars):
        """Collect all the compenents from the calendar."""
        raise NotImplementedError("to be implemented in subclasses")
    
    def collect_calendar_information(self, calendars):
        """Collect additional information from the calendars."""
    
    def merge(self):
        """Return the flask Response for the merged calendars."""
        raise NotImplementedError("to be implemented in subclasses")
        

