# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Run the open web calendar in development mode and serve files.

python -m open_web_calendar.test

"""

import atexit
import http
import socketserver
import threading
from pathlib import Path

from open_web_calendar.app import main

HERE = Path(__file__).parent.absolute()
CALENDAR_FOLDER = HERE.parent / "features" / "calendars"
PORT = 8001
HOST = "localhost"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CALENDAR_FOLDER, **kwargs)


try:
    httpd = socketserver.TCPServer((HOST, PORT), Handler)
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

main()
