# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

"""Browser fixture setup and teardown

see https://behave.readthedocs.io/en/stable/practical_tips.html#selenium-example
"""

import copy
import http.server
import multiprocessing
import random
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path

import requests
from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from werkzeug import run_simple

HERE = Path(__file__).parent.absolute()
sys.path.append(HERE / "..")
from open_web_calendar.app import DEFAULT_SPECIFICATION, app  # noqa: E402

CALENDAR_FOLDER = HERE / "calendars"
# timeout in seconds
WAIT = 10


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
    wait_for_http_server(context.index_page, on_error=p.terminate)
    yield
    p.terminate()


def wait_for_http_server(url, on_error=lambda: None):
    """Make sure the HTTP server is up and running."""
    print(f"HTTP SERVER: Waiting for {url} to start ... ", end="")
    timeout = time.time() + WAIT
    ty = err = tb = None
    while time.time() < timeout:
        try:
            requests.get(url, timeout=WAIT)
            ty = err = tb = None
            break
        except:
            ty, err, tb = sys.exc_info()
            time.sleep(0.01)
    if err is not None:
        print("FAIL")
        on_error()
        raise err.with_traceback(tb)
    print("OK")


@fixture
def calendars_server(context):
    """Serve the calendar files so they can be requested.

    see https://stackoverflow.com/a/52531444/1320237
    """
    # reuse address
    # see https://zaiste.net/posts/python_simplehttpserver_not_closing_port/
    socketserver.TCPServer.allow_reuse_address = True
    port = 8001
    host = "localhost"
    context.calendars_url = f"http://{host}:{port}/"

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=CALENDAR_FOLDER, **kwargs)

    try:
        httpd = socketserver.TCPServer((host, port), Handler)
    except OSError as e:
        if e.errno == 98:
            # OSError: [Errno 98] Address already in use
            wait_for_http_server(context.calendars_url)
            yield
            return
        else:
            raise
    # from https://werkzeug.palletsprojects.com/en/2.1.x/serving/#shutting-down-the-server
    # see also https://stackoverflow.com/questions/72824420/how-to-shutdown-flask-server
    t = threading.Thread(target=httpd.serve_forever)
    t.start()

    def final():
        httpd.server_close()
        httpd.shutdown()

    wait_for_http_server(context.calendars_url, on_error=final)
    yield
    final()


def before_all(context):
    browser = browsers[context.config.userdata["browser"]]
    use_fixture(browser, context)
    use_fixture(set_window_size, context)
    use_fixture(app_server, context)
    use_fixture(calendars_server, context)


# Set the default timezone of the browser
# If we would like to set another timezone in the tests, we can write:
#    Given we set the "teimzone" parameter to "Asia/Singapore"
DEFAULT_SPECIFICATION.update(
    {
        "url": [],
        "timezone": "Europe/Moscow",
        "date": "1605-11-05",
    }
)


def before_scenario(context, scenario):
    """Reset the calendar for each scenario.

    Empty url and set the timezone and other parameters.
    """
    context.specification = copy.deepcopy(DEFAULT_SPECIFICATION)
