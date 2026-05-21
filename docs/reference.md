---
# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Every spec key in the Open Web Calendar, what it does, what it accepts, and what it defaults to."
---

# Specification Reference

This page lists every spec key, grouped by purpose.
Every key has a default in [default_specification.yml].
Override any of them in a query parameter, a `specification_url` file,
or the `OWC_SPECIFICATION` env var on the server.
For the order of precedence, see [Specification Inheritance](dev/specification-inheritance.md).

[default_specification.yml]: {{link.code}}/open_web_calendar/default_specification.yml

## Content Sources

### `url`

The calendar feed URL or a list of URLs.
Each URL points to an ICS file or a CalDAV endpoint.
When more than one URL is given, all events are merged into a single view.

Type: string or list of strings.
Default: a sample Germany holidays calendar.

```yaml
url:
  - https://example.com/team.ics
  - https://example.com/personal.ics
```

### `specification_url`

A URL whose body is fetched and layered on top of the defaults.
The body must be valid YAML or JSON.

Type: string.
Default: not set.

See [Specification Inheritance](dev/specification-inheritance.md) for how this
combines with other layers.

## Display

### `title`

The HTML page title.

Type: string. Default: `"Open Web Calendar"`.

### `favicon`

URL to the favicon. Absolute URLs and absolute paths under the same origin
are both allowed.

Type: string. Default: `"/static/img/logo/owc.svg"`.

### `description`

A short paragraph shown in the menu. Falls back to the project description
when empty.

Type: string. Default: empty.

### `date`

The starting date of the calendar view in `YYYY-MM-DD` format. Empty means
today.

Type: string. Default: empty.

### `tab`

The view selected when the calendar opens.

Type: string. Default: `"month"`. Values: `"month"`, `"week"`, `"day"`,
`"agenda"`.

### `tabs`

The list of views the user can switch between.

Type: list of strings. Default: `["month", "week", "day"]`.

### `agenda_months`

The number of months the agenda view spans. Useful for academic calendars
or project timelines.

Type: integer. Default: `1`.

### `month_event_multiline`

When `true`, events in the month view wrap onto multiple lines instead of
truncating. Useful for tall narrow dashboards.

Type: boolean. Default: `false`.

### `inline_description`

When `true`, event descriptions are rendered under the title in the agenda
view. Useful when descriptions hold important content, like a school lunch
menu.

Type: boolean. Default: `false`.

### `start_of_week`

The first day of the week.

Type: string. Default: `"mo"`. Values: `"mo"` (Monday), `"su"` (Sunday),
`"work"` (Monday to Friday only).

### `starting_hour`

The first hour of the day visible in day and week views.

Type: string. Default: `"0"`.

### `ending_hour`

The last hour of the day visible in day and week views.

Type: string. Default: `"24"`.

### `hour_division`

The vertical resolution of day and week views.

Type: string. Default: `"1"`. Values: `"1"` (one hour), `"2"` (30 minutes),
`"4"` (15 minutes), `"6"` (10 minutes).

### `hour_format`

The format string for hour labels.
See the [DHTMLX format reference](https://docs.dhtmlx.com/scheduler/settings_format.html).

Type: string. Default: `"%H:%i"` (24-hour). Other useful values: `"%G:%i"`
(24-hour without leading zero), `"%g:%i %a"` (12-hour with am/pm).

### `timezone`

The IANA timezone the events are displayed in. Empty means the viewer's
local timezone.

Type: string. Default: empty.

### `language`

The default calendar language. The list of valid codes is in the
[translations directory]({{link.code}}/open_web_calendar/translations/).

Type: string. Default: `"en"`.

### `prefer_browser_language`

When `true`, the calendar uses the browser's language when one of the
supported languages matches. Falls back to the `language` key otherwise.

Type: boolean. Default: `false`.

### `target`

Where links open.

Type: string. Default: `"_top"`. Values: `"_top"` (replace the embedding
page), `"_blank"` (new tab), `"_self"` (replace the calendar), `"_parent"`
(the parent frame).

### `compact_layout_width`

The viewport width in pixels at which the calendar switches to a compact
layout so all controls still fit.

Type: integer. Default: `600`.

### `loader`

The URL of an animated image shown while events are loading.

Type: string. Default: `"/img/loaders/circular-loader.gif"`.

## Skin and Styling

### `skin`

The DHTMLX skin used for the calendar.

Type: string. Default: `"material"`. Values: `"material"`,
`"contrast-black"`, `"terrace"`, `"contrast-white"`, `"flat"`, `"dark"`.

### `css`

Inline CSS injected into the calendar page.

Type: string. Default: empty.

### `css_url`

A list of URLs to external stylesheets loaded into the calendar page.

Type: list of strings. Default: empty.

For class names you can target, see [CSS Classes](dev/css-classes.md).
For theme color variables, see
[Custom Theme Colors](host/configure.md#custom-theme-colors).

### `style-event-status-tentative`

When `true`, events with `STATUS:TENTATIVE` are rendered in italic.

Type: boolean. Default: `false`.

### `style-event-status-confirmed`

When `true`, events with `STATUS:CONFIRMED` are rendered in bold, and all
other events lose their default bold weight.

Type: boolean. Default: `false`.

### `style-event-status-cancelled`

When `true`, events with `STATUS:CANCELLED` are rendered with a
strikethrough.

Type: boolean. Default: `false`.

## Controls and Menu

### `controls`

The list of header controls the user can see and use.

Type: list of strings. Default: `["next", "previous", "today", "date"]`.
Values: `"next"`, `"previous"`, `"today"`, `"date"`, `"menu"`.

### `menu_shows_title`

When `true`, the calendar title appears in the burger menu.

Type: boolean. Default: `true`.

### `menu_shows_description`

When `true`, the calendar description appears in the burger menu.

Type: boolean. Default: `true`.

### `menu_shows_calendar_names`

When `true`, the burger menu lists the name of every URL in `url`.

Type: boolean. Default: `true`.

### `menu_shows_calendar_descriptions`

When `true`, the burger menu lists the description of every URL in `url`.

Type: boolean. Default: `false`.

### `menu_shows_calendar_visibility_toggle`

When `true`, each entry in the burger menu has a checkbox to hide that
calendar from the view.

Type: boolean. Default: `false`.

### `event_popup_add_to_calendar`

When `true`, the event popup shows an "Add to my Calendar" button that
downloads the event as `.ics`.

Type: boolean. Default: `true`.

## Plugins

### `plugin_event_details`

When `true`, clicking an event opens the popup with the event details.

Type: boolean. Default: `true`.

### `plugin_event_tooltip`

When `true`, hovering an event shows a tooltip with the event summary.
The tooltip is suppressed on touch devices regardless of this setting.

Type: boolean. Default: `true`.

## Participants

### `show_organizers`

When `true`, the event popup lists the event organizer.
See [RFC 5545 ORGANIZER](https://www.rfc-editor.org/rfc/rfc5545.html#page-113).

Type: boolean. Default: `false`.

### `show_attendees`

When `true`, the event popup lists the event attendees.
See [RFC 5545 ATTENDEE](https://www.rfc-editor.org/rfc/rfc5545.html#page-108).

Type: boolean. Default: `false`.

### `show_participant_status`

When `true`, the participant entry includes the participation status
(`ACCEPTED`, `DECLINED`, `TENTATIVE`, `NEEDS-ACTION`).
Requires `show_organizers` or `show_attendees`.

Type: boolean. Default: `false`.

### `show_participant_type`

When `true`, the participant entry includes the participant type
(`INDIVIDUAL`, `GROUP`, `RESOURCE`, `ROOM`).
Requires `show_organizers` or `show_attendees`.

Type: boolean. Default: `false`.

### `show_participant_role`

When `true`, the participant entry includes the role (`CHAIR`,
`REQ-PARTICIPANT`, `OPT-PARTICIPANT`, `NON-PARTICIPANT`).
Requires `show_organizers` or `show_attendees`.

Type: boolean. Default: `false`.

## Maps

### `event_url_location`

The template URL that the event's `LOCATION` text expands into.
Must contain `{location}` and can contain `{zoom}`.

Type: string. Default: `"https://www.openstreetmap.org/search?query={location}"`.

### `event_url_geo`

The template URL that the event's `GEO` property (latitude and longitude)
expands into.
Must contain `{lat}` and `{lon}` and can contain `{zoom}`.

Type: string. Default: `"https://www.openstreetmap.org/#map={zoom}/{lat}/{lon}"`.

See the [icalendar-compatibility map spec](https://icalendar-compatibility.readthedocs.io/en/latest/usage.html#custom-map-spec)
for the underlying library.

## JavaScript

### `javascript`

Inline JavaScript injected into the calendar page.

Type: string. Default: empty.

!!! warning

    JavaScript from untrusted sources is dropped when the server runs with
    `OWC_ENABLE_JS=false`. See [Security Model](host/security-model.md).

### `javascript_url`

A list of URLs to external JavaScript files loaded into the calendar page.
Absolute URLs are routed through `/js/proxy` to enforce the correct
content type.

Type: list of strings. Default: empty.

## HTML Cleaning

Event descriptions and inline HTML are cleaned through `lxml` before
rendering. The strict defaults below ship with the project. Loosening any
of them can make your instance vulnerable to script injection from
malicious calendars.

| Key | Default | What it does |
| --- | --- | --- |
| `clean_html_page_structure` | `true` | Remove `<head>`, `<body>`, `<html>` tags |
| `clean_html_meta` | `true` | Remove `<meta>` tags |
| `clean_html_embedded` | `true` | Remove `<embed>`, `<object>`, `<applet>` |
| `clean_html_links` | `true` | Remove `<link>` and `@import` references |
| `clean_html_style` | `true` | Remove `<style>` blocks |
| `clean_html_processing_instructions` | `true` | Remove `<?...?>` processing instructions |
| `clean_html_inline_style` | `true` | Remove inline `style="..."` attributes |
| `clean_html_scripts` | `true` | Remove `<script>` tags |
| `clean_html_javascript` | `true` | Remove `javascript:` URLs |
| `clean_html_comments` | `true` | Remove HTML comments |
| `clean_html_frames` | `true` | Remove `<frame>` and `<iframe>` |
| `clean_html_forms` | `true` | Remove `<form>` and form controls |
| `clean_html_annoying_tags` | `true` | Remove `<blink>`, `<marquee>`, etc. |
| `clean_html_remove_unknown_tags` | `true` | Remove tags lxml does not know |
| `clean_html_safe_attrs_only` | `true` | Strip every attribute not in `clean_html_safe_attrs` |
| `clean_html_safe_attrs` | see below | The whitelist used by `clean_html_safe_attrs_only` |
| `clean_html_remove_tags` | `[body, head, html]` | Tags whose content survives but the tag itself is removed |

Default `clean_html_safe_attrs`: `src`, `color`, `href`, `title`, `class`,
`name`, `id`.

See the [lxml Cleaner documentation](https://lxml.de/api/lxml.html.clean.Cleaner-class.html)
for the underlying library.

## Project Identification

### `source_code`

The URL where users can find the project source. Required by the GPL when
you modify the project.

Type: string. Default: `"https://github.com/niccokunzmann/open-web-calendar/"`.

### `version`

The version string shown next to the source code link. Empty falls back to
the installed package version.

Type: string. Default: empty.

### `contributing`

The URL of the contribution guide shown in the about page.

Type: string. Default: `"https://open-web-calendar.quelltext.eu/contributing/"`.

### `translate`

The URL of the translation platform shown in the about page.

Type: string. Default: `"https://hosted.weblate.org/engage/open-web-calendar/"`.

### `privacy_policy`

The URL of the privacy policy linked from the about page.

Type: string. Default: `"https://open-web-calendar.quelltext.eu/host/privacy-policy/"`.

## Internal

Set by the project. You will not need to touch these.

### `template`

The Jinja template that renders the calendar page.

Type: string. Default: `"dhtmlx.html"`.

### `timeshift`

Set by the DHTMLX scheduler at render time.

Type: integer. Default: `0`.

See also:

- [API](dev/api.md)
- [Specification Inheritance](dev/specification-inheritance.md)
- [Server Configuration](host/configure.md)
- [CSS Classes](dev/css-classes.md)
