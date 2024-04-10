
<!-- Page level macros, see https://mkdocs-macros-plugin.readthedocs.io/en/latest/pages/#page-level-macros -->

{% macro calendar_iframe(spec, width="100%") -%}
<iframe class="open-web-calendar"
    style="background:url('https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/static/img/loaders/circular-loader.gif') center center no-repeat;"
    src="{{link.web}}/calendar.html?specification_url={{link.templates}}/{{spec}}"
    sandbox="allow-scripts allow-same-origin allow-top-navigation"
    allowTransparency="true" scrolling="no"
    frameborder="0" height="600px" width="{{width}}"></iframe>
[Edit the calendar]({{link.web}}/index.html?specification_url={{link.templates}}/{{spec}})
{%- endmacro %}


# Templates

We have prepared a variety of different styles so you can edit them to your needs.
For each style, you can click on the `?` question mark in the corner
and edit the calendar.


## Mobile One Day Calendar Feed

Here is an example of a one day view of a Christmas day:

{{calendar_iframe("christmas-day.json", "300px")}}
