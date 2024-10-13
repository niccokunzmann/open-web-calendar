---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "The Open Web Calendar can be installed as a Python package from PyPI."
---
# Python Package

![](https://img.shields.io/pypi/v/open-web-calendar.svg) ![](https://img.shields.io/pypi/pyversions/open-web-calendar.svg)

The Open Web Calendar is available as a Python package on [PyPI]({{link.pypi}}).
If you have [Python 3](https://www.python.org/) installed, run this to install the package:

```shell
pip install open-web-calendar
```

After installation, run the Open Web Calendar using [Gunicorn]:

```shell
gunicorn open_web_calendar:app
```

You should now see the server running at [http://127.0.0.1:8000](http://127.0.0.1:8000).

For more configuration options, see here:

- [Gunicorn Command Line Arguments](https://docs.gunicorn.org/en/stable/run.html#commonly-used-arguments) and `gunicorn --help`.
- [Configuration](../configure)
- [Gunicorn]

[Gunicorn]: https://docs.gunicorn.org/
