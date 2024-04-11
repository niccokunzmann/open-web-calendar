
# Examples

<!-- Page level macros, see https://mkdocs-macros-plugin.readthedocs.io/en/latest/pages/#page-level-macros -->

{% macro calendar_iframe(spec, width="100%") -%}
<iframe class="open-web-calendar"
    style="background:url('https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/static/img/loaders/circular-loader.gif') center center no-repeat; border-radius: 10px;"
    src="{{link.web}}/calendar.html?specification_url={{link.templates}}/{{spec}}"
    sandbox="allow-scripts allow-same-origin allow-top-navigation"
    allowTransparency="true" scrolling="no"
    frameborder="0" height="600px" width="{{width}}"></iframe>
<a href="{{link.web}}/index.html?specification_url={{link.templates}}/{{spec}}" target="_blank">Edit the calendar</a>
{%- endmacro %}


We have prepared a variety of different styles so you can edit them to your needs.
For each style, you can click on the `?` question mark in the corner
and edit the calendar.
If you are inspired, you can also just head over and [start from scratch]({{link.web}}).

> Are you proud of your calendar? Share it here!

## Mobile One Day Calendar Feed

Here is an example of a one day view of a Christmas day:

{{calendar_iframe("christmas-day.json", "300px")}}

Modifications:

- start and end time
- fixed date
- CSS

## Recurring Events with Categories

If you are at home, planning the days with the family, events might have
different categories depending on who they are for: `work` or `personal`.
Events can be single events or occur every day.

{{calendar_iframe("family-planning.json")}}

- start and end time
- fixed date
- CSS

## Events Hosted as a Tor Hidden Service

This calendar is not styled but contains events that can be hosted behind
a firewall on a little anonymous server. [Example](https://tor.open-web-calendar.hosted.quelltext.eu/calendar.html?url=http%3A%2F%2F3nbwmxezp5hfdylggjjegrkv5ljuhguyuisgotrjksepeyc2hax2lxyd.onion%2Fone-day-event-repeat-every-day.ics
)

## Contributing Here

If you want to add another example or showcase your calendar, this is the place.
You can contact us with the link of the calendar e.g. in an [issue]({{link.issues}}).

You can **edit the page** yourself:

1. Place all required `.ics` files in the [calendars](https://github.com/niccokunzmann/open-web-calendar/tree/master/docs/assets/calendars) directory.
2. Download the specification of the calendar. And add it to the [templates](https://github.com/niccokunzmann/open-web-calendar/tree/master/docs/assets/templates) directory.
3. Edit this file and add a section.
