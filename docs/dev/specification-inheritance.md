---
# SPDX-FileCopyrightText: 2026 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "How the calendar specification is built from defaults, environment variables, and request parameters."
---

# Specification Inheritance

The specification is a dictionary that controls everything about a calendar.
The server builds it fresh for each request, layering values from several
sources. Later sources win over earlier ones.

The specification is also the project's stable contract.
The same specification should always produce the same kind of calendar.
DHTMLX scheduler updates and bug fixes can shift the look, but spec keys
do not get renamed or removed.
Hundreds of sites embed calendars that depend on this.

## The Layers

There are five layers. Higher up means higher precedence:

```text
                       ┌──────────────────────────┐
                       │ 1. Query parameters      │ highest
                       ├──────────────────────────┤
                       │ 2. specification_url     │
                       ├──────────────────────────┤
                       │ 3. DEFAULT_SPECIFICATION │ (Python)
                       ├──────────────────────────┤
                       │ 4. OWC_SPECIFICATION     │ (env var)
                       ├──────────────────────────┤
                       │ 5. default_specification.yml │ lowest
                       └──────────────────────────┘
```

The merge starts at layer 5 and works up.
A key set at layer 1 wins, no matter what the lower layers say.
A key set nowhere falls through to the default in
[default_specification.yml]({{link.code}}/open_web_calendar/default_specification.yml).

### 5. default_specification.yml

The base layer. Every spec key has a documented default here.
Operators should not edit this file. Use `OWC_SPECIFICATION` instead.

### 4. OWC_SPECIFICATION

An optional environment variable. Set it to a path or to an inline YAML
or JSON string to change defaults for every calendar your instance
serves.

See [OWC_SPECIFICATION in the configuration guide](../../host/configure#owc_specification).

### 3. open_web_calendar.app.DEFAULT_SPECIFICATION

A Python dict on the `open_web_calendar.app` module.
It is meant for code that runs inside the same Python process: custom
hosting code, test setup, that kind of thing.
Most operators never touch it.

### 2. specification_url

A query parameter that points at a YAML or JSON file.
The body of that file is layered on top of the defaults before query
parameters apply.

This is how a small embed URL can carry a big configuration.
Put the long config in a file and link to it with
`?specification_url=…`.

### 1. Query parameters

The top layer. Every value in the query string becomes a key in the
specification.
This is also the only layer a regular embed user can edit, through the
configuration page.

## A Worked Example

Say `default_specification.yml` ships with `title: "Open Web Calendar"`.

The operator starts the server like this:

```sh
OWC_SPECIFICATION='{"title": "Acme Calendar"}' gunicorn open_web_calendar:app
```

Every calendar now starts with `title: "Acme Calendar"`.

A user embeds the calendar with
`?specification_url=https://acme.example/owc.yml`.
The file there contains:

```yaml
title: "Acme Sports Schedule"
language: "de"
```

`title` is now `"Acme Sports Schedule"` and `language` is `"de"`.

The user shares a link with `?title=Friday Match` appended.
Query parameters apply last, so the final specification is:

- `title: "Friday Match"` (from query param)
- `language: "de"` (from `specification_url`)
- everything else from defaults

## Trusted vs Untrusted Layers

Three layers are trusted. The operator who deploys the server sets
them: `default_specification.yml`, `OWC_SPECIFICATION`, and
`DEFAULT_SPECIFICATION`.

Two layers are untrusted. Anyone who can hand someone a calendar URL can
set them: `specification_url` and query parameters.

This matters for spec keys that load code, like `javascript` and
`javascript_url`.
When `OWC_ENABLE_JS=false`, those keys are silently dropped from the
untrusted layers and still work from the trusted ones.

See [Security Model](../../host/security-model) for why this split matters,
and [`get_specification()` in `app.py`]({{link.code}}/open_web_calendar/app.py)
for the implementation.

## Where Each Layer Lives

| Layer | Trust | Set by | Edited at |
| ----- | ----- | ------ | --------- |
| Query parameters | untrusted | the embedder or the viewer | the embed URL |
| `specification_url` | untrusted | the embedder | a file on the web |
| `DEFAULT_SPECIFICATION` | trusted | a developer | Python code |
| `OWC_SPECIFICATION` | trusted | the operator | an env var or file |
| `default_specification.yml` | trusted | the project | the source tree |

See also:

- [API](api)
- [Server Configuration](../../host/configure)
