---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "The API of the Open Web Calendar allows more customization than the configuration page."
---

# API

Generally, the Open Web Calendar is there to be used without restriction.
You can use this API to customize the calendar on the fly.

This section can be of use if one of these applies:

- You are a web developer who wants to embed the Open Web Calendar.
- You want to exploit the full flexibility, not just what is exposed
    on the configuration page.
- You want to use JavaScript to dynamically generate the calendar design and options.
- You want to extend the functionality of the Open Web Calendar.
- You want to use the Open Web Calendar as a proxy to request JSON events for your self-made event feed.

## Endpoints

The basic parameters are the same at these endpoints:

- `/index.html` - edit the calendar
- `/about.html` - view the about page
- `/calendar.html` - view the calendar
- `/calendar.spec` - download the specification
- `/calendar.ics` - subscribe to the ics file
- `/calendar.json` - information about the calendar and the content as JSON
- `/calendar.events.json` - FLEXIBLE - get the events as JSON  
    Please note that you CAN use this but you cannot be sure that the
    JSON schema remains the same. If you want that, add tests.

Additional parameters are required for `/calendar.events.json`:

- `timezone=UTC` - the timezone that you need to display the events in
- `from=YYYY-MM-DD` - the start of the period in which events happen (inclusive)
- `to=YYYY-MM-DD` - the end of the period in which events happen (exclusive)

### ICS Output Format

The merged feed at `/calendar.ics` follows
[RFC 5545](https://www.rfc-editor.org/rfc/rfc5545.html). One detail to
flag:

`DESCRIPTION` properties that contain HTML are split. The plain-text
version stays in `DESCRIPTION` (per RFC 5545), and the original HTML
moves to a parallel `X-ALT-DESC;FMTTYPE=text/html` property. Clients that
understand `X-ALT-DESC` (Outlook, some Apple Calendar versions) render
the HTML. Older clients fall back to the plain-text description.

The HTML in `X-ALT-DESC` goes through the same `clean_html_*` rules as
the rest of the calendar, so it is safe to render.

## Parameters

All configuration parameters are described sufficiently in the [default_specification].
That is the reference.
E.g. if you find the parameter `title` in the [default_specification],
you have several options:

::::{tab-set}

:::{tab-item} Query Parameter
Change the title in a query parameter:

```sh
/index.html?title=calendar
```
:::

:::{tab-item} YAML
Change the title in a YAML specification:

```yaml
title: calendar
```
:::

:::{tab-item} JSON
Change the title in a JSON specification:

```json
{
  "title": "calendar"
}
```
:::

::::

## Compiling the Specification

You can change the calendar behavior and looks with parameters.
If the same parameter is specified in different places, the earlier place listed below has the highest precedence.
These are the places to specify parameters:

For a worked example and a diagram of how the layers combine, see
[Specification Inheritance](specification-inheritance.md).

### Query parameters

All parameters to the calendar url are put into the specification.
The query parameters have the highest precedence.

Examples:

    index.html?language=de
    calendar.html?title=CALENDAR

### specification_url

If you specify this query parameter, the editor configuration is loaded from this url, too.
Query parameters are still more important than what is written in this file.
The source format can be YAML or JSON.

Examples:

    calendar.html?specification_url=https://github.com/niccokunzmann/open-web-calendar/raw/master/open_web_calendar/default_specification.yml

### open_web_calendar.app.DEFAULT_SPECIFICATION

This is intended for developers and Python-internal.

```python
from open_web_calendar.app import DEFAULT_SPECIFICATION
DEFAULT_SPECIFICATION['title'] = 'calendar'
```

### OWC_SPECIFICATION

This is an optional environment variable.
Please read more about it in the [Server Configuration](../host/configure.md#owc_specification).

### [default_specification]

This file contains the default parameters.
They must not be hard-coded in the source code.
All parameters are listed and documented there so this file can be used for reference.
Do not modify this file, instead use the `OWC_SPECIFICATION` environment variable.

## Adding Parameters

If you add a new parameter as a developer:

- Add the parameter with a default value to the [default_specification]
- Add an implementation, depending on its use in the `app.py` or the templates
  of the JavaScript files.
  The specification is already available in all of them to use.
- Add tests in [features/configure-the-calendar.feature] to check that the calendar responds to the feature.
- Add tests in [features/edit-the-calendar.feature] to make sure that the parameter can be used when a calendar is edited.

[features/configure-the-calendar.feature]: {{link.code}}/open_web_calendar/features/configure-the-calendar.feature
[features/edit-the-calendar.feature]: {{link.code}}/open_web_calendar/features/edit-the-calendar.feature


## Specification in the Calendar

[app.py][app.py-link] compiles the specification from the given parameters in `get_specification()`.
In the [template][dhtmlx-link] you can access the specification through the `specification` variable.
The specification is available to JavaScript as the `specification` variable.

See also:

- [JavaScript Customization](javascript.md)


[app.py-link]: {{link.code}}/open_web_calendar/app.py
[dhtmlx-link]: {{link.code}}/open_web_calendar/templates/calendars/dhtmlx.html

## Specification in the Index Page

The default specification is available before the calendar is built via JavaScript in the
`configuration.default_specification` variable.
There is a [getSpecification()] function which created the
specification from the inputs.
Generally, the `specification` variable should be used.

[default_specification]: {{link.code}}/open_web_calendar/default_specification.yml
[getSpecification()]: {{link.code}}/open_web_calendar/static/js/index.js

## Architecture

Below, you can find a picture of the architecture.

![architecture](/assets/img/architecture.svg)

The base of a calendar is the specification, given in the various forms.
This specification influences all the steps.

After the specification is compiled, the calendar (ics) files are downloaded from
the locations on the Internet.

From the calendar files, the events are generated.

Then, different views are chosen to display the events.

In the end, these lead to HTML and style changes of the calendar website.

In the real application, these steps are bit bit mixed up and unordered or omitted but this explains simply the basic, initial idea behind the event processing.
