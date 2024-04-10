# API

The calendar has an API that allows customizing it.
This API uses HTTP GET and refers to the query parameters.

## Endpoints

The basic parameters are the same at these endpoints:

- `/index.html` - edit the calendar
- `/about.html` - view the about page
- `/calendar.html` - view the calendar
- `/calendar.spec` - download the specification
- `/calendar.ics` - subscribe to the ics file
- `/calendar.events.json` - get the events as JSON

## Parameters

All parameters are described sufficiently in the [default_specification].
That is the reference.
E.g. if you find the parameter `title` in the [default_specification],
you have several options:

- Change it as query parameter

        `/index.html?title=calendar`

- Add it to your own specification as YML:

        title: calendar

- Add it to your own specification as JSON:

        {
          "title": "calendar"
        }


## Adding Parameters

If you add a new parameter,

- Add it with a default value to the [default_specification]
- Add an implementation, depending on its use in the `app.py` or the templates
  of the JavaScript files.
  The specification is already available in all of them to use.

## Specification Resolution

You can change the calendar behavior and looks with parameters.
These are the places to specify parameters:

1. **Query parameters**  
    All parameters to the calendar url are put into the specification.
    The query parameters have the highest precedence.  
    Examples:

        index.html?language=de
        calendar.html?title=CALENDAR

2. **specification_url**  
    If you specify this query parameter, the editor configuration is loaded from
    this url, too.
    Query parameters are still more important than what is written
    in this file.
    The source format can be YAML or JSON.
    Examples:

        calendar.html?specification_url=https://github.com/niccokunzmann/open-web-calendar/raw/master/default_specification.yml

3. **[default_specification]**  
    This file contains the default parameters.
    They must not be hardcoded in the source code. They are there.
    Query parameters and the `specification_url` override these values.

## Specification in the Calendar

[app.py](https://github.com/niccokunzmann/open-web-calendar/blob/85a72dab4561e250aec69b5ad7c3de074eefa1e8/app.py#L81) compiles the specification from the given parameters in `get_specification()`.
In the [template](https://github.com/niccokunzmann/open-web-calendar/blob/85a72dab4561e250aec69b5ad7c3de074eefa1e8/templates/calendars/dhtmlx.html#L23) you can access the specification through the `specification` variable.
The specification is available to JavaScript as the `specification` variable.

## Specification in the Index Page

The default specification is available before the calendar is built via JavaScript in the
`configuration.default_specification` variable.
There is a [getSpecification()](https://github.com/niccokunzmann/open-web-calendar/blob/85a72dab4561e250aec69b5ad7c3de074eefa1e8/static/js/index.js#L93) function which created the
specification from the inputs.
Generally, the `specification` variable should be used.

[default_specification]: https://github.com/niccokunzmann/open-web-calendar/blob/master/default_specification.yml
