---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "The Open Web Calendar can be installed as a Python package from PyPI."
---
# Python Package

![](https://img.shields.io/pypi/v/open-web-calendar.svg) ![](https://img.shields.io/pypi/pyversions/open-web-calendar.svg)

## Installation

The Open Web Calendar is available as a Python package on [PyPI]({{link.pypi}}).
If you have [Python 3](https://www.python.org/) installed, run this to install the package:

```shell
pip install open-web-calendar[production]
```

At this point you might get the error message

```shell
error: externally-managed-environment
```

On your productive system, it is strongly recommended to follow the instructions to create a virtual environment using 

```shell
python3 -m .venv
source .venv/bin/activate
```

followed by

```shell
pip install open-web-calendar[production]
```

This will install your open-web-calendar app in the project folder  
/home/username/venv/lib/python3.12/site-packages/open_web_calendar

## Execution
After installation, run the Open Web Calendar using [Gunicorn]:

```shell
gunicorn open_web_calendar:app
```

You should now see the server running at [http://127.0.0.1:8000](http://127.0.0.1:8000).

However, in case you have installed the WebPage you are going to use for the integration of your individual calendar on the same local machine, it must be accessible to other machines as well.  
In this case you might want to start the open_web_calendar with the dedicated IP-address of the hosting machine.

```shell
gunicorn -b 0.0.0.0 open_web_calendar:app
```

You should now see the server running at [http://192.168.178.7:8000](http://192.168.178.7:8000) not only from your local machine.

## Automatic Startup

In order to start this service automatically at startup, you are required to create a systemd service script.

```shell
sudo nano /etc/systemd/system/open_web_calendar.service
```

Copy the following text into that file and do not forget to change **username** and **usergroup** accordingly!

```shell
[Unit]
Description=Gunicorn instance for the open_web_calendar
After=network.target

[Service]
User=username
Group=usergroup
# This is where you created the virtual environment before
WorkingDirectory=/home/username/.venv
Environment="PATH=/home/username/venv/bin"
ExecStart=/home/username/.venv/bin/gunicorn -b 0.0.0.0 open_web_calendar:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Finish the installation by  
a) Reload and enable the systemd manager

```shell
sudo systemctl daemon-reload
```

b) Enable the service to start on boot

```shell
sudo systemctl enable open_web_calendar
```

c) Start the service:

```shell
sudo systemctl start open_web_calendar
```

d) Verify that the service is running without errors

```shell
sudo systemctl status open_web_calendar
```

For more configuration options, see here:

- [Gunicorn Command Line Arguments](https://docs.gunicorn.org/en/stable/run.html#commonly-used-arguments) and `gunicorn --help`.
- [Configuration](../configure)
- [Gunicorn]

[Gunicorn]: https://docs.gunicorn.org/
