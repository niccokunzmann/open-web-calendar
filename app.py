#!/usr/bin/python3
from flask import Flask, render_template, make_response, request, jsonify, redirect
from flask_caching import Cache
import json
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
import requests
import icalendar
import datetime

# configuration
DEBUG = os.environ.get("APP_DEBUG", "true").lower() == "true"
PORT = int(os.environ.get("PORT", "5000"))

MAXIMUM_THREADS = 100

# constants
HERE = os.path.dirname(__name__) or "."
DEFAULT_SPECIFICATION_PATH = os.path.join(HERE, "default_specification.json")
TEMPLATE_FOLDER_NAME = "templates"
TEMPLATE_FOLDER = os.path.join(HERE, TEMPLATE_FOLDER_NAME)
CALENDARS_TEMPLATE_FOLDER_NAME = "calendars"
CALENDAR_TEMPLATE_FOLDER = os.path.join(TEMPLATE_FOLDER, CALENDARS_TEMPLATE_FOLDER_NAME)
STATIC_FOLDER_NAME = "static"
STATIC_FOLDER_PATH = os.path.join(HERE, STATIC_FOLDER_NAME)

# specification
PARAM_SPECIFICATION_URL = "specification_url"

# globals
app = Flask(__name__, template_folder="templates")
# Check Configuring Flask-Cache section for more details
cache = Cache(app, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': tempfile.mktemp(prefix="cache-")})

def spec_get(url):
    if url.startswith("/"):
        assert not ".." in url
        with open(STATIC_FOLDER_PATH + url, encoding="UTF-8") as file:
            return file.read()
    return requests.get(url).text

def get_specification():
    """Build the calendar specification."""
    with open(DEFAULT_SPECIFICATION_PATH, encoding="UTF-8") as file:
        specification = json.load(file)
    # get a request parameter, see https://stackoverflow.com/a/11774434
    url = request.args.get(PARAM_SPECIFICATION_URL, None)
    if url:
        url_specification_response = spec_get(url)
        url_specification_json = json.loads(url_specification_response)
        specification.update(url_specification_json)
    specification.update(request.args)
    return specification
    
def date_to_string(date):
    """Convert a date to a string."""
    # use ISO format
    # see https://docs.dhtmlx.com/scheduler/howtostart_nodejs.html#step4implementingcrud
    # see https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat
    # see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    if hasattr(date, "astimezone"):
        date = date.astimezone(datetime.timezone.utc)
    return date.strftime("%Y-%m-%d %H:%M")

def subcomponent_is_ical_event(event):
    """Whether the calendar subcomponent is an event."""
    # TODO: this is an estimation.
    return "DESCRIPTION" in event

def retrieve_calendar(url):
    """Get the calendar entry from a url."""
    calendar_text = spec_get(url)
    calendar = icalendar.Calendar.from_ical(calendar_text)
    assert calendar.get("CALSCALE") == "GREGORIAN", "Only Gregorian calendars are supported."
    events = []
    for calendar_event in calendar.walk():
        if not subcomponent_is_ical_event(calendar_event):
            continue
        event = {
            "start_date": date_to_string(calendar_event["DTSTART"].dt),
            "end_date": date_to_string(calendar_event["DTEND"].dt),
            "text": calendar_event.get("SUMMARY", ""),
            "location": calendar_event.get("LOCATION", ""),
            "rec_type" : calendar_event.get("RRULE:FREQ", ""),
        }
        events.append(event)
    return events

def get_events(specification):
    """Return events."""
    urls = specification["url"]
    if isinstance(urls, str):
        urls = [urls]
    assert len(urls) <= MAXIMUM_THREADS, "You can only merge {} urls.".format(MAXIMUM_THREADS)
    all_events = []
    with ThreadPoolExecutor(max_workers=MAXIMUM_THREADS) as e:
        events_list = e.map(retrieve_calendar, urls)
        for events in events_list:
            all_events.extend(events)
    return events

@app.route("/calendar.<type>", methods=['GET']) 
# use query string in cache, see https://stackoverflow.com/a/47181782/1320237
#@cache.cached(timeout=CACHE_TIMEOUT, query_string=True)
def get_calendar(type):
    """Return a calendar."""
    specification = get_specification()
    if type == "spec":
        return jsonify(specification)
    if type == "events.json":
        entries = get_events(specification)
        return jsonify(entries)
    if type == "html":
        template_name = specification["template"]
        all_template_names = os.listdir(CALENDAR_TEMPLATE_FOLDER)
        assert template_name in all_template_names, "Template names must be file names like \"{}\", not \"{}\".".format("\", \"".join(all_template_names), template_name)
        return render_template(os.path.join(CALENDARS_TEMPLATE_FOLDER_NAME, template_name), 
            specification=specification,
            get_events=get_events,
            json=json,
        )
    raise ValueError("Cannot use extension {}. Please see the documentation or report an error.".format(type))

for folder_name in os.listdir(STATIC_FOLDER_PATH):
    folder_path = os.path.join(STATIC_FOLDER_PATH, folder_name)
    if not os.path.isdir(folder_path):
        continue
    @app.route('/' + folder_name + '/<path:path>')
    def send_static(path, folder_name=folder_name):
        return send_from_directory('static/' + folder_name, path)

if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
