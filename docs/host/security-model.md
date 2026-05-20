---
# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "How the Open Web Calendar defends against malicious input, and what an operator must do to deploy it safely."
---

# Security Model

The Open Web Calendar has two layers of defense.
The project ships the first. The operator owns the second.
Both layers matter.

## Layer One: Input Handling

Everything that arrives at the server is untrusted: calendar URLs, query
parameters, the body fetched via `specification_url`, and the contents
of any `.ics` file the calendar downloads.
The project handles this layer.

Event description HTML runs through `lxml` before it reaches the browser.
The `clean_html_*` spec keys control the rules, and the defaults are
strict.
The error 500 page escapes exception details, so a crashing request
cannot reflect HTML or JavaScript back through the response.

Recurring events are capped twice: before expansion via
`OWC_MAX_SOURCE_EVENTS`, and after expansion via
`OWC_MAX_RESPONSE_EVENTS` and `OWC_MAX_RESPONSE_MB`.
A small ICS with a malicious `RRULE` cannot inflate into a denial of
service.

The encryption module uses Fernet with bcrypt for URL secrets.

Security reports go through [private advisories][advisories] so a fix
can land before the report is public.
If you find something in this layer, please follow the
[Security Policy](../../SECURITY).

[advisories]: https://github.com/niccokunzmann/open-web-calendar/security/advisories

## Layer Two: Safe Deployment

This layer is about where you run the calendar.

The Open Web Calendar loads user-supplied JavaScript through the
`javascript` and `javascript_url` spec keys.
That is on purpose. Users extend the calendar without forking the
project.
It is also the source of the main deployment risk.

In one sentence: an attacker who can hand someone a calendar URL with a
`javascript` payload can run arbitrary JavaScript in whatever origin
serves the calendar.

On a dedicated subdomain, this is fine.
The script runs only in the calendar's own origin, and there is nothing
interesting there.
On a shared origin, the script runs alongside whatever else is on that
origin. It can read cookies, read local storage, and call APIs.

### Safe by Default

The calendar is safe with no extra work when it runs on:

- A dedicated domain such as `calendar.example.com`.
- A dedicated subdomain with no shared cookies. `SameSite` defaults do
  not cross subdomains, but it is worth a check on the other services.
- A separate origin entirely, such as the hosted instance at
  [open-web-calendar.hosted.quelltext.eu]({{ link.web }}).

[open-web-calendar.hosted.quelltext.eu]: {{ link.web }}

### Shared Origin

Action is needed when the calendar shares an origin with another
service, in either of these shapes:

- **Same domain, different sub-path.** `example.com/calendar/` alongside
  `example.com/app/`. Cookies and storage are shared.
- **Same domain, root path.** Same risk; just no sub-path.

Set [`OWC_ENABLE_JS=false`](../configure#owc_enable_js) on the calendar
server.
The configuration guide covers the exact behavior.

Then add a strict `Content-Security-Policy` header through your reverse
proxy.
`OWC_ENABLE_JS=false` keeps OWC from injecting attacker JS, but it does
not isolate the response from the parent origin on its own.
A minimal CSP that disables inline scripts and limits sources to the
calendar's own origin:

```text
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;
```

Adjust `style-src` and `img-src` to match the calendars and images you
need to display.

### Sub-Path Hosting Checklist

When the calendar must live at a sub-path:

1. Set `OWC_ENABLE_JS=false`.
2. Add a strict `Content-Security-Policy` header.
3. Set `ALLOWED_HOSTS` to your domain. Requests with a `Host` header
   that does not match are rejected before any route runs.
4. Put SSRF protection in front of the calendar. See
   [SSRF Protection with a Proxy Server](../configure#ssrf-protection-with-a-proxy-server).
5. Review the [`clean_html_*` defaults](/assets/default_specification.yml).
   Tighter is safer.

## What the Project Will Not Do

A few choices that are unlikely to change.

JavaScript stays a first-class spec key.
Killing it project-wide would break legitimate uses.
`OWC_ENABLE_JS` is the per-instance switch for the operators who need it
off.

The server does not run untrusted code.
Every script from a spec key runs in the browser only.

No logging of calendar contents or IP addresses by default.
See the [Privacy Policy](../privacy-policy) for what the hosted instance
records.

See also:

- [Security Policy](../../SECURITY)
- [Server Configuration](../configure)
- [Privacy Policy](../privacy-policy)
