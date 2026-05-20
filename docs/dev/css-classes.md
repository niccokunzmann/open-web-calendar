---
# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Reference for the CSS classes that every event in the Open Web Calendar carries, and examples of how to style them."
---

# Auto-Generated CSS Classes

Every event on the page carries CSS classes that say where it came from
and what it is.
Target them from the `css` spec key or a stylesheet loaded via
`css_url`, and you can restyle events without forking the project.

The classes are generated in
[`ConvertToEvents.get_event_classes()`]({{link.code}}/open_web_calendar/convert/events.py).

## The Classes

Every event has the `event` class plus a `CALENDAR-INDEX-{n}` class.
The other classes appear only when the corresponding `VEVENT` property is
set in the source `.ics` file.

| Class                       | Source                              | Example values                         |
| --------------------------- | ----------------------------------- | -------------------------------------- |
| `event`                     | always present                      | (none)                                 |
| `CALENDAR-INDEX-{n}`        | the position of the source URL      | `CALENDAR-INDEX-0`, `CALENDAR-INDEX-1` |
| `UID-{uid}`                 | the event's `UID` property          | `UID-abc123@example.com`               |
| `TRANSP-{value}`            | the `TRANSP` property               | `TRANSP-OPAQUE`, `TRANSP-TRANSPARENT`  |
| `STATUS-{value}`            | the `STATUS` property               | `STATUS-CONFIRMED`, `STATUS-TENTATIVE`, `STATUS-CANCELLED` |
| `CLASS-{value}`             | the `CLASS` property                | `CLASS-PUBLIC`, `CLASS-PRIVATE`, `CLASS-CONFIDENTIAL` |
| `PRIORITY-{0-9}`            | the `PRIORITY` property             | `PRIORITY-1`, `PRIORITY-9`             |
| `CATEGORY-{category}`       | one class per `CATEGORIES` entry    | `CATEGORY-work`, `CATEGORY-personal`   |

!!! note

    If `CLASS` is set to a value other than `PUBLIC`, `CONFIDENTIAL`, or
    `PRIVATE`, the event keeps its `CLASS-{original}` class and also
    picks up `CLASS-PRIVATE`. Unknown values are treated as private; the
    extra class is a defense-in-depth fallback.

## Built-In Styles

Three classes have spec-level toggles in the [default_specification].
Turning them on ships the styling for you:

- `style-event-status-tentative` adds `font-style: italic` to
  `STATUS-TENTATIVE`.
- `style-event-status-confirmed` adds `font-weight: bold` to
  `STATUS-CONFIRMED`.
- `style-event-status-cancelled` adds `text-decoration: line-through` to
  `STATUS-CANCELLED`.

For anything else, target the classes below directly through `css` or
`css_url`.

## Examples

### Color a Single Calendar

If you have three calendars in `url`, target `CALENDAR-INDEX-0`,
`CALENDAR-INDEX-1`, and `CALENDAR-INDEX-2`:

```css
.CALENDAR-INDEX-0 { background-color: #b3d4fc; }
.CALENDAR-INDEX-1 { background-color: #fce4b3; }
.CALENDAR-INDEX-2 { background-color: #c3f0c2; }
```

### Hide Cancelled Events

Combine the spec-level toggle with a stronger rule:

```css
.STATUS-CANCELLED { display: none; }
```

### Style by Category

Target the `CATEGORY-{name}` class.
The category name comes verbatim from the `CATEGORIES` property of the
event.

```css
.CATEGORY-meeting { border-left: 4px solid #ff9800; }
.CATEGORY-deadline { background-color: #ffe0e0; }
```

### Mark a Specific Event

Use the `UID-{uid}` class to target a single event.
This is more durable than targeting a position; UIDs do not change when
the calendar reloads.

```css
.UID-team-standup\@example\.com { font-weight: bold; }
```

The `@` and `.` characters need to be escaped with a backslash in CSS
selectors.

### Combine Classes

The classes stack. You can scope a rule to a particular calendar and a
particular status:

```css
.CALENDAR-INDEX-0.STATUS-TENTATIVE { opacity: 0.6; }
```

See also:

- [`css` and `css_url`](../../host/configure#configuring-the-default-calendar)
- [Custom Theme Colors](../../host/configure#custom-theme-colors)
- [API](api)

[default_specification]: {{link.code}}/open_web_calendar/default_specification.yml
