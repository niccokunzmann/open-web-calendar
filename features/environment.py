"""Browser fixture setup and teardown

see https://behave.readthedocs.io/en/stable/practical_tips.html#selenium-example
"""
import  sys
import os

HERE = os.path.dirname(__file__ or ".")
sys.path.append(os.path.join(HERE, ".."))

from behave import fixture, use_fixture
from selenium.webdriver import Firefox, FirefoxProfile
from selenium import webdriver
from app import app
from werkzeug import run_simple
import multiprocessing
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service
import tempfile
from selenium.webdriver.common.by import By
import shutil
from behave.log_capture import capture
import http.server
import socketserver
from selenium.webdriver.chrome.service import Service


@fixture
def browser_firefox(context):
    # run firefox in headless mode
    # see https://stackoverflow.com/a/47642457/1320237
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    # specify firefox executible and gecko drivers
    # see https://stackoverflow.com/a/76852633
    # see https://stackoverflow.com/a/71766991/1320237
    geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
    # Set the language for the tests
    opts.set_preference('intl.accept_languages', 'en-US, en')
    # construct the arguments
    kw = dict(options=opts)
    if os.path.exists(geckodriver_path):
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
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless") # from https://stackoverflow.com/q/56637973/1320237
    # executable_path from https://stackoverflow.com/a/76550727/1320237
    service = Service(executable_path='/snap/bin/chromium.chromedriver')
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

def serve_calendar_files(host, port, directory=os.path.join(HERE, "calendars")):
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
    import random
    port = random.randint(start, end)
    return port


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
    p = multiprocessing.Process(target=serve_calendar_files, args=("localhost", calendar_port))
    p.start()
    context.calendars_url = f"http://localhost:{calendar_port}/"
    yield
    p.terminate()


def before_all(context):
    browser = browsers[context.config.userdata["browser"]]
    use_fixture(browser, context)
    use_fixture(app_server, context)
    use_fixture(calendars_server, context)


def before_scenario(context, scenario):
    """Reset the calendar for each scenario."""
    context.specification = {
        "url": []
    }
