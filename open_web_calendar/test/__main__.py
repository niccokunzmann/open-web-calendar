# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Run the open web calendar in development mode and serve files.

python -m open_web_calendar.test

"""

import atexit
import http
import http.client as http_client
import logging
import socketserver
import sys
import threading
from pathlib import Path

from open_web_calendar.app import main

from .api_mocking import Recorder, Recording

HERE = Path(__file__).parent.absolute()
CALENDAR_FOLDER = HERE.parent / "features" / "calendars"
PORT = 8001
HOST = "0.0.0.0"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CALENDAR_FOLDER, **kwargs)


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


try:
    httpd = ReusableTCPServer((HOST, PORT), Handler)
except OSError as e:
    print(f"Could not start the HTTP server. Assuming it is runnning... {e}")
else:
    print(f"Started calendar server at http://{HOST}:{PORT}/")
    # from https://werkzeug.palletsprojects.com/en/2.1.x/serving/#shutting-down-the-server
    # see also https://stackoverflow.com/questions/72824420/how-to-shutdown-flask-server
    t = threading.Thread(target=httpd.serve_forever)
    t.start()

    def final():
        httpd.server_close()
        httpd.shutdown()

    atexit.register(final)

names = sys.argv[1:]
if names:
    print(f"Loading recorded API {names[0]}")
    Recording().load(names[0])
else:
    print("Recording interaction.")
    Recorder.development()


# from https://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application
# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger()
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
logging.getLogger("caldav").setLevel(logging.DEBUG)

main()
