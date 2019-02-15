Open Web Calendar
=================

[Try it out][web]

There are several commercial solutions which allow embedding of calendar into
my website. I only have a link to an ICS file and want to show a nice-looking
calenar on my site which gives me the control over who knows the people who
visit the site.

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

[web]: https://open-web-calendar.herokuapp.com

