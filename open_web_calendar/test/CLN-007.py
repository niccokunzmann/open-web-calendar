import pathlib

calendar = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//SabreDAV//SabreDAV//EN
CALSCALE:GREGORIAN
"""



for i in range(1000):
 calendar += """
BEGIN:VEVENT
CREATED:20190303T111937Z
DTSTAMP:20190303T111937Z
LAST-MODIFIED:20190303T111937Z
UID:{}
SUMMARY:every day
RRULE:FREQ=DAILY
DTSTART:20190304T080000Z
DTEND:20190304T083000Z
END:VEVENT
""".format(i)


calendar += """
END:VCALENDAR
"""


path = pathlib.Path(__file__).parent.parent / "features" / "calendars" / "CLN-007.ics"
path.write_text(calendar)
