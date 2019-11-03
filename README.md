Open Web Calendar
=================

[![Build Status](https://travis-ci.org/niccokunzmann/open-web-calendar.svg?branch=master)](https://travis-ci.org/niccokunzmann/open-web-calendar)
**[Try it out][web]**

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

[web]: https://openwebcalendar.herokuapp.com/

Related Work
------------

- [calender_merger](https://github.com/niccokunzmann/calender_merger) for merging several ICAL files into one
- [ical-filter](https://github.com/thoka/ical-filter) for filtering events in an ICAL file and providing the selection as file
- [Wordpress all in one event calendar](https://wordpress.org/plugins/all-in-one-event-calendar/)
- [My Mailbox Calendar](https://github.com/niccokunzmann/my-mailbox-calendar#readme)

[app.json]: app.json
