---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Play with a variety of Calendars for your own project."
---

# Examples

<!-- Page level macros, see https://mkdocs-macros-plugin.readthedocs.io/en/latest/pages/#page-level-macros -->

{% macro calendar_iframe(spec, width="100%", params="", id="") -%}

<iframe class="open-web-calendar" id="{{id}}"
    style="background:url('/assets/img/circular-loader.gif') center center no-repeat; border-radius: 10px;"
    src="{{link.web}}/calendar.html?specification_url={{link.templates}}/{{spec}}&{{params}}"
    sandbox="allow-scripts allow-same-origin allow-top-navigation"
    allowTransparency="true" scrolling="no"
    frameborder="0" height="600px" width="{{width}}"></iframe>

{%- endmacro %}

{% macro calendar_example(spec, width="100%", params="", id="", html="") -%}

=== "Calendar"

    {{ calendar_iframe(spec, width, params, id) }}

=== "Specification"


    ```json
    --8<-- "{{ spec }}"
    ```

=== "HTML"

    ```html
    {{ calendar_iframe(spec, width, params, id) }}
    {% if html != "" %}
    --8<-- "{{ html }}"
    {% endif %}
    ```

<a href="{{link.web}}/index.html?specification_url={{link.templates}}/{{spec}}" target="_blank">Edit the calendar</a>
{%- endmacro %}


We have prepared a variety of different styles so you can edit them to your needs.
For each style, you can edit the calendar and shape is as you need it.
If you are inspired, you can also just head over and [start from scratch]({{link.web}}).

> Are you proud of your calendar? Share it here!

## Multiple Calendars

You can embed several calendars into one view. In this example, we show
different rooms in an office.

{{calendar_example("rooms.json")}}

This is also useful if you have multiple calendar sources - be it
different places, clubs, applications or organizations.

Modifications:

- CSS
- hours
- tab

## Mobile One Day Calendar Feed

Here is an example of a one day view of a Christmas day:

{{calendar_example("christmas-day.json", "300px")}}

Modifications:

- start and end time
- fixed date
- CSS

## Recurring Events with Categories

If you are at home, planning the days with the family, events might have
different categories depending on who they are for: `work` or `personal`.
Events can be single events or occur every day.

{{calendar_example("family-planning.json")}}

Modifications:

- start and end time
- fixed date
- CSS

## Events Hosted as a Tor Hidden Service

This calendar is not styled but contains events that can be hosted behind
a firewall on a little anonymous server. [Example](https://tor.open-web-calendar.hosted.quelltext.eu/calendar.html?url=http%3A%2F%2F3nbwmxezp5hfdylggjjegrkv5ljuhguyuisgotrjksepeyc2hax2lxyd.onion%2Fone-day-event-repeat-every-day.ics
)

Modifications:

- [proxy parameters](../host/configure#ssrf-protection-with-a-proxy-server)

## Choose Timezones

For an international calendar, you can allow choosing the time zone that the
events are displayed in.

--8<-- "choose-timezone.html"

{{calendar_example("timezone-example.json", id="owcTimezoneExample", html="choose-timezone.html")}}

Modifications:

- JavaScript
- timezone

## Free and Busy

You can change the design based on whether you are free or busy.

This calendar has changed CSS so that the background is green and the
events are either orange or red.

{{calendar_example("free-and-busy.json")}}


Modifications:

- CSS

## Contribute Examples!

If you want to add another example or showcase your calendar, this is the place.
You can **contact us** with the link of the calendar e.g. in an [issue]({{link.issues}}).

You can **edit the page** yourself:

1. Place all required `.ics` files in the [calendars](https://github.com/niccokunzmann/open-web-calendar/tree/master/docs/assets/calendars) directory.
2. Download the specification of the calendar. And add it to the [templates](https://github.com/niccokunzmann/open-web-calendar/tree/master/docs/assets/templates) directory.
3. Edit this file and add a section.
