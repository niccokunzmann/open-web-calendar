import datetime
from icalendar import Event, Calendar
from icalendar.prop import vDDDTypes
from flask import Response
import io
import traceback

class ConvertToICS:
    """Convert events to dhtmlx. This conforms to a stratey pattern."""
    
    def __init__(self, specification):
        """Create an ICS conversion strategy."""
        self.title = specification["title"]

    def convert_ical_event(self, calendar_event):
        return calendar_event

    def error(self, ty, error, tb, url=None):
        """Create an error which can be used by the dhtmlx scheduler."""
        tb_s = io.StringIO()
        traceback.print_exception(ty, error, tb, file=tb_s)
        event = Event()
        event["DTSTART"] = event["DTEND"] = vDDDTypes(datetime.datetime.now())
        event["SUMMARY"] = type(error).__name__
        event["DESCRIPTION"] = str(error) + "\n\n" + tb_s.getvalue()
        event["UID"] = "error" + str(id(error))
        if url:
            event["URL"] = url
        return event
    
    def create_calendar(self):
        calendar = Calendar()
        calendar["VERSION"] = "2.0"
        calendar["PRODID"] = "open-web-calendar"
        calendar["CALSCALE"] = "GREGORIAN"
        calendar["METHOD"] = "PUBLISH"
        calendar["X-WR-CALNAME"] = self.title
        calendar["X-PROD-SOURCE"] = "https://github.com/niccokunzmann/open-web-calendar/"
        return calendar
    
    def merge(self, events):
        calendar = self.create_calendar()
        for event in events:
            calendar.add_component(event)
        return Response(calendar.to_ical(), mimetype="text/calendar")

