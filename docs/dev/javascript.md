---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "The calendar can be customized with JavaScript."
---

# JavaScript Customization

The Open Web Calendar can be modified with JavaScript.
For this, two [parameters] are available:

- `javascript=...` for adding JavaScript to the calendar.
- `javascript_url=...` for loading JavaScript from a URL.

[parameters]: ../api

Anything that is added to the `javascript` parameter is executed after the calendar has been loaded.
Thus, you can access the calendar and choose change its configuration.

## Useful Variables

When executing JavaScript, the stable variables and functions are listed below.
More functions and variables are available but if they are not documented here, they can change.

### `onCalendarInitialized`

The `onCalendarInitialized()` function is called after the calendar is fully configured.
You can override the configuration of the calendar at this point.
After this is called, the events are loaded into the calendar.
The content of this function can be modified with the JavaScript parameter `javascript=...`.

### `scheduler`

The `scheduler` variable contains the [DHTMLX Scheduler] object.
Here are some links to the API documentation:

- [DHTMLX Scheduler]
- [Properties](https://docs.dhtmlx.com/scheduler/api__refs__scheduler_props.html)
- [Sizes](https://docs.dhtmlx.com/scheduler/api__scheduler_xy_other.html)

### `specification`

The `specification` variable contains the full specification of the calendar with all [parameters] including your own and those defined for all calendars.

See also:

- [parameters]

[DHTMLX Scheduler]: https://docs.dhtmlx.com/scheduler/api__refs__scheduler.html
