# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Browser fixture setup and teardown

see https://behave.readthedocs.io/en/stable/practical_tips.html#selenium-example
"""

import http.server
import multiprocessing
import random
import socketserver
import subprocess
import sys
from pathlib import Path

from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from werkzeug import run_simple

HERE = Path(__file__)
sys.path.append(HERE / "..")
from app import app  # noqa: E402

CALENDAR_FOLDER = HERE / "calendars"


def locate_command(command: str):
    """Locate a command on the command line or return ''."""
    code, output = subprocess.getstatusoutput(f"which {command}")  # noqa: S605
    if code == 0:
        return output.strip()
    return ""


@fixture
def browser_firefox(context):
    # run firefox in headless mode
    # see https://stackoverflow.com/a/47642457/1320237
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    # specify firefox executible and gecko drivers
    # see https://stackoverflow.com/a/76852633
    # see https://stackoverflow.com/a/71766991/1320237
    # specify the path to your geckodriver
    geckodriver_path = Path("/snap/bin/geckodriver")
    # Set the language for the tests
    opts.set_preference("intl.accept_languages", "en-US, en")
    # construct the arguments
    kw = {"options": opts}
    if geckodriver_path.exists():
        kw["service"] = Service(executable_path=geckodriver_path)
    browser = Firefox(**kw)
    context.browser = browser
    browser.set_page_load_timeout(10)
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()


@fixture
def browser_chrome(context):
    # see https://behave.readthedocs.io/en/stable/tutorial.html#environmental-controls
    # for an example
    # lots of options come from https://stackoverflow.com/a/52340526/1320237
    options = webdriver.ChromeOptions()
    options.add_argument(
        "--headless"
    )  # from https://stackoverflow.com/q/56637973/1320237
    options.add_argument(
        "start-maximized"
    )  # https://stackoverflow.com/a/26283818/1689770
    options.add_argument(
        "enable-automation"
    )  # https://stackoverflow.com/a/43840128/1689770
    options.add_argument("--no-sandbox")  # https://stackoverflow.com/a/50725918/1689770
    options.add_argument(
        "--disable-dev-shm-usage"
    )  # https://stackoverflow.com/a/50725918/1689770
    options.add_argument(
        "--disable-browser-side-navigation"
    )  # https://stackoverflow.com/a/49123152/1689770
    options.add_argument(
        "--disable-gpu"
    )  # https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc

    # executable_path from https://stackoverflow.com/a/76550727/1320237
    path = locate_command("chromium.chromedriver") or locate_command("chromedriver")
    service = Service(executable_path=path)
    context.browser = webdriver.Chrome(service=service, options=options)
    yield context.browser
    context.browser.quit()


@fixture
def browser_safari(context):
    context.browser = webdriver.Safari()
    yield context.browser
    context.browser.quit()


browsers = {
    "firefox": browser_firefox,
    "chrome": browser_chrome,
    "safari": browser_safari,
}


@fixture
def set_window_size(context):
    """Set the window size of the browser."""
    # see https://stackoverflow.com/a/55878622/1320237
    if "window" in context.config.userdata:
        width, height = context.config.userdata["window"].split("x")
        context.browser.set_window_size(int(width), int(height))


def serve_calendar_files(host, port, directory=CALENDAR_FOLDER):
    """Serve the calendar files so they can be requested.

    see https://stackoverflow.com/a/52531444/1320237
    """

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    try:
        with socketserver.TCPServer((host, port), Handler) as httpd:
            print("serving calendars at port", port)
            httpd.serve_forever()
    except OSError as e:
        print("\n", e)


def get_free_port(start=10000, end=60000):
    """Return a free port number."""
    return random.randint(start, end)  # noqa: S311


@fixture
def app_server(context):
    """Start the flask app in a server."""
    app_port = get_free_port()
    # from https://werkzeug.palletsprojects.com/en/2.1.x/serving/#shutting-down-the-server
    # see also https://stackoverflow.com/questions/72824420/how-to-shutdown-flask-server
    p = multiprocessing.Process(target=run_simple, args=("localhost", app_port, app))
    p.start()
    context.index_page = f"http://localhost:{app_port}/"
    yield
    p.terminate()


@fixture
def calendars_server(context):
    """Start the flask app in a server."""
    calendar_port = 8001
    # from https://werkzeug.palletsprojects.com/en/2.1.x/serving/#shutting-down-the-server
    # see also https://stackoverflow.com/questions/72824420/how-to-shutdown-flask-server
    p = multiprocessing.Process(
        target=serve_calendar_files, args=("localhost", calendar_port)
    )
    p.start()
    context.calendars_url = f"http://localhost:{calendar_port}/"
    yield
    p.terminate()


def before_all(context):
    browser = browsers[context.config.userdata["browser"]]
    use_fixture(browser, context)
    use_fixture(set_window_size, context)
    use_fixture(app_server, context)
    use_fixture(calendars_server, context)


def before_scenario(context, scenario):
    """Reset the calendar for each scenario."""
    context.specification = {"url": []}
