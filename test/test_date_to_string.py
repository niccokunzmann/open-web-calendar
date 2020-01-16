import pytest
import datetime
from app import ConvertToDhtmlx
from pytz import timezone, utc

berlin = timezone("Europe/Berlin")
eastern = timezone('US/Eastern')

@pytest.mark.parametrize("date,timeshift_minutes,expected", [
    # test date object without time zone
    (datetime.date(2019, 3, 23),    0, "2019-03-23 00:00"),
    (datetime.date(2019, 3, 23), -120, "2019-03-22 22:00"),
    (datetime.date(2019, 3, 23),  120, "2019-03-23 02:00"),
    # test datetime object without time zone
    (datetime.datetime(2019,  6,  2, 20),           0, "2019-06-02 20:00"),
    (datetime.datetime(2019,  4, 20, 10, 10),    -120, "2019-04-20 08:10"),
    (datetime.datetime(2019, 12,  1,  0, 13, 23), 120, "2019-12-01 02:13"),
    # test datetime object with time zone
    (berlin.localize(datetime.datetime(2019,  6,  2, 20)),           0, "2019-06-02 18:00"),
    (berlin.localize(datetime.datetime(2019,  4, 20, 10, 10)),    -120, "2019-04-20 08:10"),
    (berlin.localize(datetime.datetime(2019, 12,  1,  0, 13, 23)), 120, "2019-11-30 23:13"),
    (utc.localize(datetime.datetime(2019,  6,  2, 20)),           0, "2019-06-02 20:00"),
    (utc.localize(datetime.datetime(2019,  4, 20, 10, 10)),    -120, "2019-04-20 10:10"),
    (utc.localize(datetime.datetime(2019, 12,  1,  0, 13, 23)), 120, "2019-12-01 00:13"),
])
def test_date_to_string_conversion(date, timeshift_minutes, expected):
    """Convert dates and datetime objects for the events.json"""
    string = ConvertToDhtmlx({"timeshift":timeshift_minutes}).date_to_string(date)
    print(date)
    assert string == expected



