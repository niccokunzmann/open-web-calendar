"""Browser fixture setup and teardown

see https://behave.readthedocs.io/en/stable/practical_tips.html
"""
import  sys
import os

HERE = os.path.dirname(__file__ or ".")
sys.path.append(os.path.join(HERE, ".."))

from behave import fixture, use_fixture
from selenium.webdriver import Firefox
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


@fixture
def browser_firefox(context):
    # -- BEHAVE-FIXTURE: Similar to @contextlib.contextmanager
    # run firefox in headless mode
    # see https://stackoverflow.com/a/47642457/1320237
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    # specify firefox executible and gecko drivers
    # see https://stackoverflow.com/a/76852633
    geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
    if os.path.exists(geckodriver_path):
        driver_service = Service(executable_path=geckodriver_path)
        browser = Firefox(options=opts, service=driver_service)
    else:
        browser = Firefox(options=opts)
    context.browser = browser
    browser.set_page_load_timeout(10)
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()


def serve_calendar_files(host, port, directory=os.path.join(HERE, "calendars")):
    """Serve the calendar files so they can be requested.
    
    see https://stackoverflow.com/a/52531444/1320237
    """

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)


    with socketserver.TCPServer((host, port), Handler) as httpd:
        print("serving calendars at port", port)
        httpd.serve_forever()


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
    use_fixture(browser_firefox, context)
    use_fixture(app_server, context)
    use_fixture(calendars_server, context)


def before_scenario(context, scenario):
    """Reset the calendar for each scenario."""
    context.specification = {
        "url": []
    }

