import datetime
from flask import jsonify
from conversion_base import ConversionStrategy
import recurring_ical_events
from pprint import pprint


class ConvertToDhtmlx(ConversionStrategy):
    """Convert events to dhtmlx. This conforms to a stratey pattern.
    
    - timeshift_minutes is the timeshift specified by the calendar
        for dates.
    """
    
    def created(self):
        self.timeshift = int(self.specification["timeshift"])

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
        uid = calendar_event.get("UID", "") # issue 69: UID is helpful for debugging but not required
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
            "type": "event",
            "color": calendar_event.get("COLOR", calendar_event.get("X-APPLE-CALENDAR-COLOR", ""))
        }

    def convert_error(self, error, url, tb_s):
        """Create an error which can be used by the dhtmlx scheduler."""
        now = datetime.datetime.now();
        now_iso = now.isoformat()
        now_s = self.date_to_string(now)
        return {
            "start_date": now_s,
            "end_date": now_s,
            "start_date_iso": now_iso,
            "end_date_iso": now_iso,
            "start_date_iso_0": now_iso,
            "end_date_iso_0": now_iso,
            "text":  type(error).__name__,
            "description": str(error),
            "traceback": tb_s,
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
    
    def merge(self):
        pprint(self.components)
        return jsonify(self.components)
        
    def collect_components_from(self, calendars):
        today = datetime.datetime.utcnow()
        one_year_ahead = today.replace(year=today.year + 1)
        one_year_before = today.replace(year=today.year - 1)
        for calendar in calendars:
            events = recurring_ical_events.of(calendar).between(one_year_before, one_year_ahead)
            with self.lock:
                for event in events:
                    json_event = self.convert_ical_event(event)
                    self.components.append(json_event)
                


