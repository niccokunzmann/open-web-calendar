#!/usr/bin/env python3
from flask import Flask, render_template, make_response, request, jsonify, \
    redirect, send_from_directory
from flask_caching import Cache
import json
import os
import tempfile
import requests
import icalendar
import datetime
from dateutil.rrule import rrulestr
from pprint import pprint
import yaml
import traceback
import io
import sys
from convert_to_dhtmlx import ConvertToDhtmlx
from convert_to_ics import ConvertToICS
import pytz
import translate

# configuration
DEBUG = os.environ.get("APP_DEBUG", "true").lower() == "true"
PORT = int(os.environ.get("PORT", "5000"))
CACHE_REQUESTED_URLS_FOR_SECONDS = int(os.environ.get("CACHE_REQUESTED_URLS_FOR_SECONDS", 600))

# constants
HERE = os.path.dirname(__file__) or "."
DEFAULT_SPECIFICATION_PATH = os.path.join(HERE, "default_specification.yml")
TEMPLATE_FOLDER_NAME = "templates"
TEMPLATE_FOLDER = os.path.join(HERE, TEMPLATE_FOLDER_NAME)
CALENDARS_TEMPLATE_FOLDER_NAME = "calendars"
CALENDAR_TEMPLATE_FOLDER = os.path.join(TEMPLATE_FOLDER, CALENDARS_TEMPLATE_FOLDER_NAME)
STATIC_FOLDER_NAME = "static"
STATIC_FOLDER_PATH = os.path.join(HERE, STATIC_FOLDER_NAME)
DHTMLX_LANGUAGES_FILE = os.path.join(STATIC_FOLDER_PATH, "js", "dhtmlx", "locale", "languages.json")

# specification
PARAM_SPECIFICATION_URL = "specification_url"

# globals
app = Flask(__name__, template_folder="templates")
# Check Configuring Flask-Cache section for more details
CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': tempfile.mktemp(prefix="cache-")}
cache = Cache(app, config=CACHE_CONFIG)

# caching

__URL_CACHE = {}
def cache_url(url, text):
    """Cache the value of a url."""
    __URL_CACHE[url] = text
    try:
        get_text_from_url(url)
    finally:
        del __URL_CACHE[url]


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

# configuration

def get_configuration():
    """Return the configuration for the browser"""
    config = {
        "default_specification": get_default_specification(), 
        "timezones": pytz.all_timezones, # see https://stackoverflow.com/a/13867319
        "dhtmlx": {
            "languages": translate.dhtmlx_languages()
        },
        "index": {
            "languages": translate.languages_for_the_index_file()
        }
    }
    return config

def set_JS_headers(response):
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = '*'
    # see https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowHeaderFromPreflight
    response.headers['Access-Control-Allow-Headers'] = request.headers.get("Access-Control-Request-Headers")
    response.headers['Content-Type'] = 'text/calendar'
    return response

def set_js_headers(func):
    """Set the response headers for a valid CORS request."""
    def with_js_response(*args, **kw):
        return set_JS_headers(func(*args, **kw))
    return with_js_response

@cache.memoize(
    CACHE_REQUESTED_URLS_FOR_SECONDS,
    forced_update=lambda: bool(__URL_CACHE))
def get_text_from_url(url):
    """Return the text from a url.

    The result is cached CACHE_REQUESTED_URLS_FOR_SECONDS.
    """
    if __URL_CACHE:
        return __URL_CACHE[url]
    return requests.get(url).content

def get_default_specification():
    """Return the default specification."""
    with open(DEFAULT_SPECIFICATION_PATH, encoding="UTF-8") as file:
        return yaml.safe_load(file)

def get_specification(query=None):
    """Build the calendar specification."""
    if query is None:
        query = request.args
    specification = get_default_specification()
    # get a request parameter, see https://stackoverflow.com/a/11774434
    url = query.get(PARAM_SPECIFICATION_URL, None)
    if url:
        url_specification_response = get_text_from_url(url)
        try:
            url_specification_values = json.loads(url_specification_response)
        except json.JSONDecodeError:
            url_specification_values = yaml.safe_load(url_specification_response)
        specification.update(url_specification_values)
    for parameter in query:
        # get a list of arguments
        # see http://werkzeug.pocoo.org/docs/0.14/datastructures/#werkzeug.datastructures.MultiDict
        value = query.getlist(parameter, None)
        if len(value) == 1:
            value = value[0]
        specification[parameter] = value
    return specification


def get_query_string():
    return "?" + request.query_string.decode()

def render_app_template(template, specification):
    translation_file = os.path.splitext(template)[0]
    return render_template(template,
        specification=specification,
        configuration = get_configuration(),
        json=json,
        get_query_string=get_query_string,
        html=lambda id: translate.html(specification["language"], translation_file, id)
    )

@app.route("/calendar.<type>", methods=['GET', 'OPTIONS'])
# use query string in cache, see https://stackoverflow.com/a/47181782/1320237
#@cache.cached(timeout=CACHE_TIMEOUT, query_string=True)
def get_calendar(type):
    """Return a calendar."""
    specification = get_specification()
    if type == "spec":
        return jsonify(specification)
    if type == "events.json":
        strategy = ConvertToDhtmlx(specification, get_text_from_url)
        strategy.retrieve_calendars()
        return strategy.merge()    
    if type == "ics":
        strategy = ConvertToICS(specification, get_text_from_url)
        strategy.retrieve_calendars()
        return strategy.merge()
    if type == "html":
        template_name = specification["template"]
        all_template_names = os.listdir(CALENDAR_TEMPLATE_FOLDER)
        assert template_name in all_template_names, "Template names must be file names like \"{}\", not \"{}\".".format("\", \"".join(all_template_names), template_name)
        template = CALENDARS_TEMPLATE_FOLDER_NAME + "/" + template_name
        return render_app_template(template, specification)
    raise ValueError("Cannot use extension {}. Please see the documentation or report an error.".format(type))

for folder_name in os.listdir(STATIC_FOLDER_PATH):
    folder_path = os.path.join(STATIC_FOLDER_PATH, folder_name)
    if not os.path.isdir(folder_path):
        continue
    @app.route('/' + folder_name + '/<path:path>', endpoint="static/" + folder_name)
    def send_static(path, folder_name=folder_name):
        return send_from_directory('static/' + folder_name, path)

@app.route("/")
@app.route("/index.html")
def serve_index():
    specification = get_specification()
    return render_app_template("index.html", specification)

@app.route("/about.html")
def serve_about():
    specification = get_specification()
    return render_app_template("about.html", specification)

@app.route("/configuration.js")
def serve_configuration():
    return "/* generated */\nconst configuration = {};".format(json.dumps(get_configuration()))

@app.route("/locale_<lang>.js")
def serve_locale(lang):
    return render_template("locale.js", locale=json.dumps(translate.dhtmlx(lang), indent="  "))

@app.errorhandler(500)
def unhandledException(error):
    """Called when an error occurs.

    See https://stackoverflow.com/q/14993318
    """
    file = io.StringIO()
    traceback.print_exception(type(error), error, error.__traceback__, file=file)
    return """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <html>
        <head>
            <title>500 Internal Server Error</title>
        </head>
        <body>
            <h1>Internal Server Error</h1>
            <p>The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the application.</p>
            <pre>\r\n{traceback}
            </pre>
        </body>
    </html>
    """.format(traceback=file.getvalue()), 500 # return error code from https://stackoverflow.com/a/7824605

# make serializable for multiprocessing
#app.__reduce__ = lambda: __name__ + ".app"

if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
