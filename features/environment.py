"""Browser fixture setup and teardown

see https://behave.readthedocs.io/en/latest/practical_tips.html#selenium-example
"""
import  sys
import os

HERE = os.path.dirname(__file__ or ".")
sys.path.append(os.path.join(HERE, ".."))

from behave import fixture, use_fixture
from selenium.webdriver import Firefox
from dynamic_website_reverse_proxy.app import App
from dynamic_website_reverse_proxy.config import Config
from bottle import WSGIRefServer, default_app
from wsgiref import simple_server
import threading
from selenium.webdriver import FirefoxOptions
import tempfile
from selenium.webdriver.common.by import By
import shutil
from behave.log_capture import capture


@fixture
def browser_firefox(context):
    # -- BEHAVE-FIXTURE: Similar to @contextlib.contextmanager
    # run firefox in headless mode
    # see https://stackoverflow.com/a/47642457/1320237
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    context.browser = browser = Firefox(options=opts)
    browser.set_page_load_timeout(10)
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()


@fixture
def app_client(context, port=8000):
    """Add the application.

    see https://behave.readthedocs.io/en/latest/usecase_flask.html#integration-example
    """
    class MyWSGIServer(simple_server.WSGIServer):
        """Saving all my instances so I can shut them down."""
        instance = None
        def __init__(self, *args, **kw):
            self.__class__.instance = self
            super().__init__(*args, **kw)
            
        
    with tempfile.TemporaryDirectory(prefix="dyn-tests") as td:
        context.app_config = config = Config({
            "NGINX_CONF": os.path.join(td, "nginx.conf"),
            "DOMAIN": "example.com",
            "DATABASE": os.path.join(td, "db.pickle"),
            "NETWORK": "172.16.0.0/16",
            "PORT": port,
            "DEFAULT_DOMAINS": "test.example.org->http://172.16.0.1",
            "ADMIN_PASSWORD": "12345",
            "NGINX_CONF": "",
        })
        context.app = app = App(config)
        bottle_app = default_app()
        app.serve_from(bottle_app)
        bserver = WSGIRefServer(port=port, server_class=MyWSGIServer)
        context.thread = threading.Thread(target=lambda: bserver.run(bottle_app))
        context.thread.start()
        context.index_page = f"http://localhost:{port}/"
        yield app
        MyWSGIServer.instance.shutdown()
        context.thread.join()


def before_all(context):
    use_fixture(browser_firefox, context)
    use_fixture(app_client, context)
