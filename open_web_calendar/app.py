#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

import io
import json
import os
import tempfile
import traceback
from pathlib import Path

import pytz
import requests
import yaml
from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
    render_template,
    request,
    send_from_directory,
)
from flask_allowed_hosts import AllowedHosts
from flask_caching import Cache

from . import translate, version
from .convert_to_dhtmlx import ConvertToDhtmlx
from .convert_to_ics import ConvertToICS

# configuration
DEBUG = os.environ.get("APP_DEBUG", "true").lower() == "true"
PORT = int(os.environ.get("PORT", "5000"))
CACHE_REQUESTED_URLS_FOR_SECONDS = int(
    os.environ.get("CACHE_REQUESTED_URLS_FOR_SECONDS", 600)
)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
if ALLOWED_HOSTS == [""]:  # noqa: SIM300, RUF100
    ALLOWED_HOSTS = []
REQUESTS_TIMEOUT = int(os.environ.get("SOURCE_TIMEOUT", "60"))

# constants
HERE = Path(__file__).parent
DEFAULT_SPECIFICATION_PATH = HERE / "default_specification.yml"
TEMPLATE_FOLDER_NAME = "templates"
TEMPLATE_FOLDER = HERE / TEMPLATE_FOLDER_NAME
CALENDARS_TEMPLATE_FOLDER_NAME = "calendars"
CALENDAR_TEMPLATE_FOLDER = TEMPLATE_FOLDER / CALENDARS_TEMPLATE_FOLDER_NAME
STATIC_FOLDER_NAME = "static"
STATIC_FOLDER_PATH = HERE / STATIC_FOLDER_NAME
DEFAULT_REQUEST_HEADERS = {
    "user-agent": "open-web-calendar",
}

# specification
PARAM_SPECIFICATION_URL = "specification_url"

# globals
app = Flask(__name__, template_folder="templates")
# Check Configuring Flask-Cache section for more details
CACHE_CONFIG = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": tempfile.mkdtemp(prefix="owc-cache-"),
}
cache = Cache(app, config=CACHE_CONFIG)

# caching

__URL_CACHE = {}


# limiting access
def host_not_allowed():
    return render_template(
        "403.html",
        hostname=request.host.split(":")[0],
        allowed_hosts=", ".join(ALLOWED_HOSTS),
    ), 403


allowed_hosts = AllowedHosts(
    app, allowed_hosts=ALLOWED_HOSTS, on_denied=host_not_allowed
)

# This is an in-app override of the default_specification.yml
DEFAULT_SPECIFICATION = {}


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
    """Return the configuration for the browser."""
    return {
        "default_specification": get_default_specification(),
        "version": version.version,
        "version-list": version.version_tuple,
        "timezones": pytz.all_timezones,  # see https://stackoverflow.com/a/13867319
        "dhtmlx": {"languages": translate.dhtmlx_languages()},
        "index": {"languages": translate.languages_for_the_index_file()},
    }


def set_js_headers(response):
    response = make_response(response)
    response.headers["Access-Control-Allow-Origin"] = "*"
    # see https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowHeaderFromPreflight
    response.headers["Access-Control-Allow-Headers"] = request.headers.get(
        "Access-Control-Request-Headers"
    )
    if "Content-Type" not in response.headers:
        response.headers["Content-Type"] = "text/calendar"
    return response


def make_js_file_response(content: str) -> Response:
    """Modify the response to set the content type for .js files."""
    response = make_response(content)
    set_js_headers(response)
    response.headers["Content-Type"] = "text/javascript"
    return response


@cache.memoize(
    CACHE_REQUESTED_URLS_FOR_SECONDS, forced_update=lambda: bool(__URL_CACHE)
)
def get_text_from_url(url):
    """Return the text from a url.

    The result is cached CACHE_REQUESTED_URLS_FOR_SECONDS.
    """
    if __URL_CACHE:
        return __URL_CACHE[url]
    return requests.get(
        url, headers=DEFAULT_REQUEST_HEADERS, timeout=REQUESTS_TIMEOUT
    ).content


def get_default_specification():
    """Return the default specification."""
    with DEFAULT_SPECIFICATION_PATH.open(encoding="UTF-8") as file:
        spec = yaml.safe_load(file)
        spec.update(DEFAULT_SPECIFICATION)
        return spec


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
        # see https://web.archive.org/web/20230325034825/https://werkzeug.palletsprojects.com/en/0.14.x/datastructures/
        value = query.getlist(parameter)
        # convert values
        for i in range(len(value)):
            if value[i] in ("false", "False"):
                value[i] = False
            elif value[i] in ("true", "True"):
                value[i] = True
        if len(value) == 1 and not isinstance(specification.get(parameter), list):
            value = value[0]
        specification[parameter] = value

    return specification


def get_query_string():
    return "?" + request.query_string.decode()


def render_app_template(template, specification):
    translation_file = Path(template).stem
    language = specification["language"]
    if specification["prefer_browser_language"]:
        # see https://stackoverflow.com/a/30441752/1320237
        # see https://tedboy.github.io/flask/generated/generated/werkzeug.LanguageAccept.html
        language = request.accept_languages.best_match(
            translate.LANGUAGE_CODES, language
        )
    return render_template(
        template,
        specification=specification,
        configuration=get_configuration(),
        json=json,
        get_query_string=get_query_string,
        html=lambda tid, **template_replacements: translate.html(
            language, translation_file, tid, **template_replacements
        ),
        language=language,
    )


@app.route("/calendar.<ext>", methods=["GET", "OPTIONS"])
@allowed_hosts.limit()
# use query string in cache, see https://stackoverflow.com/a/47181782/1320237
# @cache.cached(timeout=CACHE_TIMEOUT, query_string=True)
def get_calendar(ext):
    """Return a calendar."""
    specification = get_specification()
    if ext == "spec":
        return jsonify(specification)
    if ext == "events.json":
        strategy = ConvertToDhtmlx(specification, get_text_from_url)
        strategy.retrieve_calendars()
        return set_js_headers(strategy.merge())
    if ext == "ics":
        strategy = ConvertToICS(specification, get_text_from_url)
        strategy.retrieve_calendars()
        return set_js_headers(strategy.merge())
    if ext == "html":
        template_name = specification["template"]
        all_template_names = os.listdir(CALENDAR_TEMPLATE_FOLDER)
        assert (
            template_name in all_template_names
        ), 'Template names must be file names like "{}", not "{}".'.format(
            '", "'.join(all_template_names), template_name
        )
        template = CALENDARS_TEMPLATE_FOLDER_NAME + "/" + template_name
        return render_app_template(template, specification)
    raise ValueError(
        f"Cannot use extension {ext}. Please see the documentation or report an error."
    )


for folder_path in STATIC_FOLDER_PATH.iterdir():
    if not folder_path.is_dir():
        continue

    @app.route(
        "/" + folder_path.name + "/<path:path>", endpoint="static/" + folder_path.name
    )
    def send_static(path, folder_name=folder_path.name):
        return send_from_directory("static/" + folder_name, path)


@app.route("/")
@app.route("/index.html")
@allowed_hosts.limit()
def serve_index():
    specification = get_specification()
    return render_app_template("index.html", specification)


@app.route("/about.html")
@allowed_hosts.limit()
def serve_about():
    specification = get_specification()
    return render_app_template("about.html", specification)


@app.route("/configuration.js")
@allowed_hosts.limit()
def serve_configuration():
    return make_js_file_response(
        f"/* generated */\nconst configuration = {json.dumps(get_configuration())};"
    )


@app.route("/locale_<lang>.js")
@allowed_hosts.limit()
def serve_locale(lang):
    """Serve the locale translations for the web frontend DHTMLX."""
    return make_js_file_response(
        render_template(
            "locale.js", locale=json.dumps(translate.dhtmlx(lang), indent="  ")
        )
    )


@app.errorhandler(500)
def unhandled_exception(error):
    """Called when an error occurs.

    See https://stackoverflow.com/q/14993318
    """
    file = io.StringIO()
    traceback.print_exception(type(error), error, error.__traceback__, file=file)
    return (
        f"""
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <html>
        <head>
            <title>500 Internal Server Error</title>
        </head>
        <body>
            <h1>Internal Server Error</h1>
            <p>
                The server encountered an internal error and was unable to
                complete your request.  Either the server is overloaded or
                there is an error in the application.
            </p>
            <pre>\r\n{file.getvalue()}
            </pre>
        </body>
    </html>
    """,
        500,
    )  # return error code from https://stackoverflow.com/a/7824605


# make serializable for multiprocessing
# app.__reduce__ = lambda: __name__ + ".app"


def main():
    """Run the Open Web Calendar"""
    print("""If you want to run the Open Web Calendar in production,
please use this command:

    gunicorn open_web_calendar:app
    """)  # noqa: T201

    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)


__all__ = [
    "main",
    "app",
    "DEFAULT_SPECIFICATION",
    "cache_url",
    "get_text_from_url",
    "get_default_specification",
    "get_specification",
    "DEFAULT_REQUEST_HEADERS",
]

if __name__ == "__main__":
    main()
