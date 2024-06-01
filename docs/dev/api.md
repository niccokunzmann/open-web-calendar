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
- `/calendar.events.json` - FLEXIBLE - get the events as JSON  
    Please note that you CAN use this but you cannot be sure that the
    JSON schema remains the same. If you want that, add tests.

Additional parameters are required for `/calendar.events.json`:

- `timezone=UTC` - the timezone that you need to display the events in
- `from=YYYY-MM-DD` - the start of the period in which events happen (inclusive)
- `to=YYYY-MM-DD` - the end of the period in which events happen (exclusive)

## Parameters

All configuration parameters are described sufficiently in the [default_specification].
That is the reference.
E.g. if you find the parameter `title` in the [default_specification],
you have several options:

=== "Query Parameter"

    Change the title in a query parameter:

    ```sh
    /index.html?title=calendar
    ```

=== "YAML"

    Change the title in a YAML specification:

    ```YAML
    title: calendar
    ```

=== "JSON"

    Change the title in a JSON specification:

    ```json
    {
      "title": "calendar"
    }
    ```


## Adding Parameters

If you add a new parameter as a developer,

- Add the parameter with a default value to the [default_specification]
- Add an implementation, depending on its use in the `app.py` or the templates
  of the JavaScript files.
  The specification is already available in all of them to use.
- Add tests in [features/configure-the-calendar.feature]({{link.code}}/features/configure-the-calendar.feature) to check that the calendar responds to the feature.
- Add tests in [features/edit-the-calendar.feature]({{link.code}}/features/edit-the-calendar.feature) to make sure that the parameter can be used when a calendar is edited.

## Compiling the Specification

You can change the calendar behavior and looks with parameters.
These are the places to specify parameters:

1. **Query parameters**  
    All parameters to the calendar url are put into the specification.
    The query parameters have the highest precedence.  
    Examples:

    ```txt
    index.html?language=de
    calendar.html?title=CALENDAR
    ```

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
    They must not be hard-coded in the source code. All of them are there.
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

[default_specification]: {{link.code}}/default_specification.yml

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
