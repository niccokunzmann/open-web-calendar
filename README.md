Open Web Calendar
=================

[![Build Status](https://travis-ci.org/niccokunzmann/open-web-calendar.svg?branch=master)](https://travis-ci.org/niccokunzmann/open-web-calendar)
[![Support on Open Collective](https://img.shields.io/opencollective/all/open-web-calendar?label=support%20on%20open%20collective)](https://opencollective.com/open-web-calendar/)
**[Try&nbsp;it&nbsp;out][web]**
[![build and publish the Docker image](https://github.com/niccokunzmann/open-web-calendar/actions/workflows/docker-image.yml/badge.svg)](https://github.com/niccokunzmann/open-web-calendar/actions/workflows/docker-image.yml)

Python: 3.7, 3.8, 3.9, 3.10

There are several commercial solutions which allow embedding of calendars into my website.
I only have a link to an ICS file and want to show a nice-looking calendar on my site.
Browser-only calendars usually have the problem that many ICS files can not be
accessed (such as ownCloud/nextCloud in my case).
I also want to be in control over who knows the people who
visit the site and not pass everything to Google.
This is a solution in my case which I share with the world.
You are free to use it or deploy your own, modify or share it.
It works offline and in company networks, too.

Features
- Embedded calendar
- Choice of time zone
- ICS link, best multiple
- month/week as a view
- name, time of event, link?
- showing the time span
- styling of choice (icon, color, font, ...)

## Deployment

You can deploy the app using Heroku.
There is a free plan.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Heroku uses [gunicorn](http://flask.pocoo.org/docs/dev/deploying/wsgi-standalone/#gunicorn)
to run the server, see the [Procfile](Procfile).

### Docker
#### Docker build
To build the container yourself type the command `docker build . -t <container-name>` with `<container-name>` being the name that you want for your container

#### Using pre build dockerhub image with docker-compose
<TODO: Docker compose file>

To deploy the open-web-calendar with docker-compose, do the following steps:
1. Copy the `docker-compose.yml` file to the directory from where you want to run the container
2. If needed change port mapping and environment variables
3. Type `docker-compose up -d` to start the container
4. The container will be pulled automatically from dockerhub and then starts

#### Update prebuild image with docker-compose
If you want to update your image with the latest version from dockerhub type `docker-compose pull`

Note: You need to start the container after pulling again in order for the update to apply (`docker-compose up -d`)

Research
--------

- https://serverfault.com/questions/142598/open-source-web-application-for-viewing-ics-calendars
- https://stackoverflow.com/questions/300849/html-viewer-for-ics-ical-files
- https://phpicalendar.net
  - https://sourceforge.net/projects/phpicalendar/
- https://icalendar.readthedocs.io/
- https://github.com/rianjs/ical.net
- https://stackoverflow.com/questions/4671764/is-there-a-javascript-calendar-that-takes-an-ical-link-as-input-to-display-event
- https://www.webgui.org/content-managers-guide-wiki/calendar
- https://www.quora.com/What-calendars-can-I-embed-in-my-website-that-arent-Google-Calendar

Hosts
- https://www.chronoflocalendar.com/
- with API: http://www.instantcal.com/api.html
- Wordpress: https://de.wordpress.org/plugins/all-in-one-event-calendar/

Sources/Libs
- https://stackoverflow.com/questions/9072802/is-there-an-open-source-javascript-calendar-that-supports-built-in-event-detail#9072985

Search Terms
------------

calendar ics service, ics calendar to html, open source calendar view ical,
python Ical, calendar viewer website for ics, open source calendar website,
embed calendar into website

Software Components
-------------------

- Python3 and the packages in requirements.txt
  - [Flask](http://flask.pocoo.org/)
- [DHTMLX scheduler](https://docs.dhtmlx.com/scheduler/)
- [python-recurring-ical-events](https://github.com/niccokunzmann/python-recurring-ical-events)


Development
-----------

1. Optional: Install virtualenv and Python3 and create a virtual environment.
    ```
    virtualenv -p python3 ENV
    source ENV/bin/activate
    ```
2. Install the packages.
    ```
    pip install -r requirements.txt
    ```
3. Start the app.
    ```
    python3 app.py
    ```

For the configuration of the app through environment variables,
see the [app.json] file.

## Running Tests

To run the tests, we use `tox`.
`tox` tests all different Python versions which we want to 
be compatible to.

```
pip install tox
```

Run all tests:

```
tox
```

Run a specific Python version:

```
tox -e py39
```

[web]: https://openwebcalendar.herokuapp.com/

### Updating Dependencies

We use `pip-compile` to guarantee a
tested deployment by fixing all
the dependencies to a specific
version.

You can update the packages to the latest version:

```
rm requirements.txt test-requirements.txt
pip install --upgrade pip-tools -r requirements.in -r test-requirements.in
pip-compile -o requirements.txt requirements.in
pip-compile -o test-requirements.txt test-requirements.in
```

And run the tests:
```
pytest
```

Changelog
---------

- v1.0
  - Create the changelog.
  - Add support for colors from ICS calendars, see [Issue #52](https://github.com/niccokunzmann/open-web-calendar/issues/52) and [Pull Request 88](https://github.com/niccokunzmann/open-web-calendar/pull/88).

Related Work
------------

- [docker-ics-view](https://github.com/11notes/docker-ics-view) and [its Docker image](https://hub.docker.com/r/11notes/ics-view) - a fork of this project with further improvements
- [calender_merger](https://github.com/niccokunzmann/calender_merger) for merging several ICAL files into one
- [ical-filter](https://github.com/thoka/ical-filter) for filtering events in an ICAL file and providing the selection as file
- [Wordpress all in one event calendar](https://wordpress.org/plugins/all-in-one-event-calendar/)
- [My Mailbox Calendar](https://github.com/niccokunzmann/my-mailbox-calendar#readme)

[app.json]: app.json
