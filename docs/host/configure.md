---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Configure a hosted instance."
---

# Server Configuration

If you want to change the Open Web Calendar to serve your needs, this is
well possible.
You can choose to

- Change how the default calendar looks.
- Change how the server works.

## Configuring the Default Calendar

The configuration of all calendars is rooted in the [default_specification.yml].
All those values can be changed through a copy of this file hosted on the web
through the calendar parameter `specification_url`.
Each parameter should be documented in [default_specification.yml].

If you modify the default specification, you modify **all calendars** that are hosted at your instance.
Calendars still override some values for their configuration.
Those which they do not override are affected.
Not all values are exposed to the configuration page to be changed.
Those values can still be changed in the [default_specification.yml] and the query parameters.

You might want to change the following values.

### `title`

The title of your website.

### `language`

This is the default language.
You might want to change this to serve the configuration page better to a
local audience.

### `favicon`

This is a link to the website icon.

### `source_code`

If you made changes, you are legally required to disclose them to visitors.
Please adjust the link or contribute them back to the main project.

### `contributing`

If you want to redirect to contribute to your project.

### `privacy_policy`

If you host this service yourself, you can use the default [privacy policy][privacy-policy].

If for some reason you decide to collect data i.e. in the HTTPS proxy
or log IP-addresses, then you need to create your own privacy policy.
You can link to the one of this project.

### More Values

There are loads more values that can be changed.
Please refer to the [default_specification.yml].
These values are all documented.

[default_specification.yml]: https://github.com/niccokunzmann/open-web-calendar/blob/master/open_web_calendar/default_specification.yml
[privacy-policy]: ../privacy-policy

See also:

- [API](../../dev/api)

## Configuring the Server

Environment variables only influence the running of the server.
These environment variables can be used to configure the service:

### ALLOWED_HOSTS

default empty

The clients divided by comma that are allowed to access the Open Web Calendar.
You will see this text if you try to access the service and you are not allowed:

> **Forbidden:**
> You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.*  

Examples:

- permit only the same computer: `ALLOWED_HOSTS=localhost`
- permit several hosts: `ALLOWED_HOSTS=192.168.0.1,192.168.2,api.myserver.com`
- permit everyone to access the server (default): `ALLOWED_HOSTS=` or `ALLOWED_HOSTS=*`

This functionality is provided by [flask-allowed-hosts](https://pypi.org/project/flask-allowed-hosts/).

### PORT

default `5000`, default `80` in the Docker container  

The port that the service is running on.

Examples:

- Serve on HTTP port: `PORT=80`

### WORKERS

default `4`, only for the Docker container

The number of parallel workers to handle requests.

Examples:

- Only use one worker: `WORKERS=1`

### CACHE_REQUESTED_URLS_FOR_SECONDS

default `600`

Seconds to cache the calendar files that get downloaded to reduce bandwidth and delay.

Examples:

- Refresh fast: `CACHE_REQUESTED_URLS_FOR_SECONDS=10`


### APP_DEBUG

default `true`, values `true` or `false`, always `false` in the Docker container

Set the debug flag for the app.

### Further Configuration

The Open Web Calendar uses libraries whose behavior can be further customized.

- **Flask** has **[more environment variables](https://flask.palletsprojects.com/en/3.0.x/config/)** available to configure how the application serves content.
- **Requests** is used the get the `.ics` files. You can [configure a proxy](#ssrf-protection-with-a-proxy-server).

### SSRF Protection with a Proxy Server

The Open Web Calendar can be used to access the local network behind a firewall,
see [Issue 250](https://github.com/niccokunzmann/open-web-calendar/issues/250).
This free access is intended to show calendars from everywhere.
Since `requests` is used by the Open Web Calender,
it can use a proxy as described in the
[`requests` documentation](https://requests.readthedocs.io/en/latest/user/advanced/#proxies).
The proxy can then handle the filtering.

```sh
export HTTP_PROXY="http://10.10.1.10:3128"
export HTTPS_PROXY="http://10.10.1.10:1080"
export ALL_PROXY="socks5://10.10.1.10:3434"
```

See also:

- [Prevent SSRF using a Tor proxy](../docker#preventing-ssrf-attacks-using-a-tor-proxy)
