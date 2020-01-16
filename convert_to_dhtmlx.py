import datetime
import io
import traceback
from flask import jsonify

class ConvertToDhtmlx:
    """Convert events to dhtmlx. This conforms to a stratey pattern."""
    
    def __init__(self, specification):
        """Create a DHTMLX conversion strategy.
        
        - timeshift_minutes is the timeshift specified by the calendar
            for dates.
        """
        self.timeshift = int(specification["timeshift"])

    def date_to_string(self, date):
        """Convert a date to a string."""
        # use ISO format
        # see https://docs.dhtmlx.com/scheduler/howtostart_nodejs.html#step4implementingcrud
        # see https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat
        # see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        timezone = datetime.timezone(datetime.timedelta(minutes=-self.timeshift))
        if isinstance(date, datetime.date) and not isinstance(date, datetime.datetime):
            date = datetime.datetime(date.year, date.month, date.day, tzinfo=timezone)
        elif date.tzinfo is None:
            date = date.replace(tzinfo=timezone)
        date = date.astimezone(datetime.timezone.utc)
        return date.strftime("%Y-%m-%d %H:%M")


    def convert_ical_event(self, calendar_event):
        start = calendar_event["DTSTART"].dt
        end = calendar_event.get("DTEND", calendar_event["DTSTART"]).dt
        geo = calendar_event.get("GEO", None)
        if geo:
            geo = {"lon": geo.longitude, "lat": geo.latitude}
        name = calendar_event.get("SUMMARY", "")
        sequence = str(calendar_event.get("SEQUENCE", 0))
        uid = calendar_event["UID"]
        start_date = self.date_to_string(start)
        return {
            "start_date": start_date,
            "end_date": self.date_to_string(end),
            "start_date_iso": start.isoformat(),
            "end_date_iso": end.isoformat(),
            "start_date_iso_0": start.isoformat(),
            "end_date_iso_0": end.isoformat(),
            "text":  name,
            "description": calendar_event.get("DESCRIPTION", ""),
            "location": calendar_event.get("LOCATION", None),
            "geo": geo,
            "uid": uid,
            "ical": calendar_event.to_ical().decode("UTF-8"),
            "sequence": sequence,
            "recurrence": None,
            "url": calendar_event.get("URL"),
            "id": (uid, start_date),
            "type": "event"
        }

    def error(self, ty, error, tb, url=None):
        """Create an error which can be used by the dhtmlx scheduler."""
        now = datetime.datetime.now();
        now_iso = now.isoformat()
        now_s = self.date_to_string(now)
        tb_s = io.StringIO()
        traceback.print_exception(ty, error, tb, file=tb_s)
        return {
            "start_date": now_s,
            "end_date": now_s,
            "start_date_iso": now_iso,
            "end_date_iso": now_iso,
            "start_date_iso_0": now_iso,
            "end_date_iso_0": now_iso,
            "text":  type(error).__name__,
            "description": str(error),
            "traceback": tb_s.getvalue(),
            "location": None,
            "geo": None,
            "uid": "error",
            "ical": "",
            "sequence": 0,
            "recurrence": None,
            "url": url,
            "id": id(error),
            "type": "error"
        }
    
    def merge(self, events):
        return jsonify(events)

