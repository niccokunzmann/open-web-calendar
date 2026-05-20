---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: false
title: Customize Your Own Online Calendar Display
description: "See the features or try the Open Web Calendar yourself!"
---

![]({{link.img}}/logo/github-social-preview.svg)

A highly flexible calendar display for your website.

Give a calendar your personal touch within minutes!

- **[Try it out now!]({{link.web}})**
- [See Examples](templates)

## Getting Started

Pick the path that matches what you have.

### I have an ICS URL

1. Open the [configuration page]({{link.web}}).
2. Paste the ICS URL into the calendar URL input near the top of the
   page.
3. Adjust the title, language, and starting tab.
4. Copy the embed snippet at the bottom of the page into your website.

The hosted instance at <{{link.web}}> is free to use.
To run your own, see [Self-Hosting](host/self).

### I have CalDAV

The Open Web Calendar talks to CalDAV servers like Nextcloud.
The setup is the same as an ICS URL; just point at the CalDAV endpoint
instead.

For a CalDAV calendar where viewers sign up to events, see the
[CalDAV Sign Up tutorial](news/2025-03-17-caldav-nextcloud-sign-up).

### I want to customize the appearance

Three ways, in order of effort:

- **Quick changes** in the configuration page: title, colors, hours,
  controls.
- **Theme colors** through `--owc-*` CSS variables in your `css` spec
  key. See [Custom Theme Colors](host/configure#custom-theme-colors).
- **Full control** by writing CSS that targets the auto-generated
  event classes. See [CSS Classes](dev/css-classes).

For the full list of spec keys, see the
[Specification Reference](reference).

### I want to host my own instance

Start with [Self-Hosting](host/self) and
[Server Configuration](host/configure).

If the calendar will share a domain with another service, read the
[Security Model](host/security-model) before you go live.

## Features

| Features |  |
| --- | --- |
| Instant Event Syncing | <center>✔</center> |
| Embed with an HTML snippet | <center>✔</center> |
| Desktop and Mobile | <center>✔</center> |
| Multi-Language Support | <center>✔</center> |
| Fixed and Automatic Timezone | <center>✔</center> |
| Easy Editing | <center>✔</center> |
| Designs To Choose  | <center>✔</center> |
| Multiple Calendar Sources | <center>✔</center> |
| Style per Calendar, Category and more | <center>✔</center> |
| Custom CSS | <center>✔</center> |
| Day, Week, Month, Agenda | <center>✔</center> |
| Work Week | <center>✔</center> |
| Custom Date & Time Range | <center>✔</center> |
| Custom Title & Icon | <center>✔</center> |
| Click on Event Location | <center>✔</center> |
| Styled Event Descriptions | <center>✔</center> |
| FOSS - No Vendor Lock-In | <center>✔</center> |
| [Hosted]({{link.web}}) and [Self-Hosted](host/self) | <center>✔</center> |
| Subscribe Link | <center>✔</center> |
| Community and Paid Support | <center>✔</center> |
| [Developer API](dev/api) | <center>✔</center> |
