# Python Package

![](https://img.shields.io/pypi/v/open-web-calendar.svg) ![](https://img.shields.io/pypi/pyversions/open-web-calendar.svg)

The Open Web Calendar is available as a Python package on [PyPI](https://pypi.org/project/open-web-calendar/).
If you have Python 3 installed, run this to install the package:

```shell
pip install open-web-calendar
```

After installation, run the Open Web Calendar using [Gunicorn](https://pypi.org/project/gunicorn/):

```shell
gunicorn open_web_calendar:app
```

You should now see the server running at [http://127.0.0.1:8000](http://127.0.0.1:8000).

For more configuration options, see here:

- [Gunicorn](https://pypi.org/project/gunicorn/)
- [Configuration](../configure)
