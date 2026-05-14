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

The configuration of all calendars is rooted in the [default_specification].
All those values can be changed through a copy of this file hosted on the web
through the calendar parameter `specification_url`.
Each parameter should be documented in [default_specification].

To modify **all calendars** hosted on your instance, use the [OWC_SPECIFICATION] environment variable.
Calendars still override some values for their configuration.
Those which they do not override are affected by the default specification.
Not all values are exposed to the configuration page to be changed.
Those values can still be changed in the `specification_url` and the query parameters.

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
Please refer to the [default_specification].
These values are all documented.
Please use the [OWC_SPECIFICATION] environment variable to change them.

[default_specification]: /assets/default_specification.yml
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

This functionality is provided by [flask-allowed-hosts].

[flask-allowed-hosts]: https://pypi.org/project/flask-allowed-hosts/

### APP_DEBUG

default `false`, values `true` or `false`, always `false` in the Docker container

Set the debug flag for the app.

### CACHE_DIRECTORY

default is a temporary directory (e.g. in `/tmp/`)

The Open Web Calendar caches files needed to display calendars in this directory to speed up loading.
If the directory does not exist, it will be created.


### CACHE_FILE_SIZE

default `20` (MB)

This is the maximum size of one file in the cache.
When the cache is full, the least recently used file is removed.

Examples:

- Allow only small files of 4KB: `CACHE_FILE_SIZE=0.004`
- Allow any size: `CACHE_FILE_SIZE="$CACHE_SIZE"`
- Disable caching: `CACHE_FILE_SIZE=0`

### CACHE_SIZE

default `200` (MB)

This is the maximum cache size in megabytes.
This size is limited to 200MB in order to mitigate the cache filling the file system or in case of `/tmp/` the RAM.

Examples:

- Use 1 GB for caching: `CACHE_SIZE=1024`
- Unlimited cache: `CACHE_SIZE=unlimited`
- Disable caching: `CACHE_SIZE=0`

### CACHE_REQUESTED_URLS_FOR_SECONDS

default `600` (seconds)

Seconds to cache the calendar files that get downloaded to reduce bandwidth and delay.

Examples:

- Refresh fast: `CACHE_REQUESTED_URLS_FOR_SECONDS=10`
- Disable caching: `CACHE_REQUESTED_URLS_FOR_SECONDS=0`

### OWC_ENABLE_JS

default `true`, values `true` or `false`

When set to `false`, user-supplied JavaScript via the `javascript` and `javascript_url`
spec keys is silently dropped from query strings and from the body fetched via
`specification_url`. JavaScript set in `default_specification.yml` or the
`OWC_SPECIFICATION` env var still works (admin-trusted), including absolute
`javascript_url` entries that proxy through `/js/proxy`.

This is a defense-in-depth layer on top of `Content-Security-Policy` for instances
hosted on the **same domain or sub-path** as another service: with JavaScript enabled,
an attacker-controlled URL could execute arbitrary JS in the parent service's origin.
By default OWC assumes it runs on its own subdomain with no shared cookies or state.

Even with `OWC_ENABLE_JS=false`, hosts on shared domains should also set a strict
`Content-Security-Policy` header — this env var prevents OWC from injecting attacker
JS but does not by itself isolate OWC from the parent origin.

### OWC_ENCRYPTION_KEYS

default empty

This is a comma separated list of encryption keys. These can be used to hide sensitive information of URLs.

Examples:

- Disable encryption (default): `OWC_ENCRYPTION_KEYS=`
- Use one key: `OWC_ENCRYPTION_KEYS='Pj...48='`
- Use multiple keys: `OWC_ENCRYPTION_KEYS='Pj...48=,cx...Fw='`  
  If you use multiple keys, only the first one encrypts the data.
  The others are only used to decrypt the data.

You can generate a new key by visiting your instance of the Open Web Calendar on the page [/new-key] or by running this command:

```sh
python3 -m open_web_calendar.new_key
```

See also:

- [Fernet]

[Fernet]: https://cryptography.io/en/latest/fernet/
[/new-key]: {{ link.web }}/new-key

### OWC_MAX_RESPONSE_EVENTS

default `10000` (events)

The maximum number of expanded events returned by `/calendar.events.json`.
Recurring events expand into one entry per occurrence, so a small ICS with
a long RRULE can balloon into millions of events. When the expanded count
exceeds this cap, the request returns HTTP 413.

This is a defense-in-depth check that fires after recurring-event expansion
has already run, so the CPU work of expansion itself is not avoided.
Operators experiencing CPU pressure should lower `OWC_MAX_SOURCE_EVENTS`,
which is the true pre-expansion defense. This addresses pentest finding
CLN-007 (recurring-event denial of service).

### OWC_MAX_RESPONSE_MB

default `10` (MB)

The maximum byte size of the JSON body returned by `/calendar.events.json`.
When the serialized response exceeds this cap, the request returns HTTP 413.

This addresses pentest finding CLN-007 (recurring-event denial of service).

### OWC_MAX_SOURCE_EVENTS

default `1000` (events)

The maximum number of `VEVENT` components accepted from a single fetched
ICS payload, summed across all `VCALENDAR` blocks in that payload. This is a
pre-expansion cap that rejects abnormally large source calendars before the
recurring-event expansion step runs. When exceeded, the request returns HTTP 413.

This addresses pentest finding CLN-007 (recurring-event denial of service).

### OWC_SPECIFICATION

[OWC_SPECIFICATION]: #owc_specification

`OWC_SPECIFICATION` is an optional environment variable.

- It can be a **path** to a file containing valid YAML or JSON.
- It can be a **string** containing valid YAML or JSON.

Setting `OWC_SPECIFICATION` allows you to replace default values for all calendars.

!!! note

    New versions of the Open Web Calendar can add new configuration parameters.
    Placing your changes in this variable instead of changing the `default_specification` file
    will ensure that you do not break the Open Web Calendar in a future version.

In following example, the title for all calendars that do not set their own title will be changed.

```sh
OWC_SPECIFICATION='{"title": "calendar"}' gunicorn open_web_calendar:app
```

See also:

- [OWC_SPECIFICATION in the API](../../dev/api#owc_specification)

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

## Further Configuration

The Open Web Calendar uses libraries whose behavior can be further customized.

- **Flask** has **[more environment variables](https://flask.palletsprojects.com/en/3.0.x/config/)** available to configure how the application serves content.
- **Requests** is used the get the `.ics` files. You can [configure a proxy](#ssrf-protection-with-a-proxy-server).

The Open Web Calendar relies on proxy servers for these features:

- **Access Control and Users**
  To restrict who can use the Open Web Calendar, you can use `nginx` or `apache` as a reverse proxy in front of it.
  YuNoHost is another self-hosting option to restrict access.
- **HTTPS Encryption**  
  This can be done by `nginx`, `apache` or `caddy`.
- **More Advanced Caching**  
  Basic caching is handled by the Open Web Calendar.
  For more advanced cache configuration, use a proxy server like `squid`.
  Have a look in the documentation below on how to make the Open Web Calendar access the web only through a proxy.
- **Restricting Access to Calendars**
  By default, the Open Web Calendar does not restrict which calendars to show.
  Use the proxy server to filter the calendars.
  If you run the Open Web Calendar behind a firewall with other web services, setting up a proxy is necessary to protect from SSRF attacks.

## SSRF Protection with a Proxy Server

The Open Web Calendar can be used to access the local network behind a firewall,
see [Issue 250](https://github.com/niccokunzmann/open-web-calendar/issues/250).
This free access is intended to show calendars from everywhere.
Since `requests` is used by the Open Web Calendar,
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

## Squid as a Proxy Server

The [Squid] Proxy and Cache is flexible and configurable.
You can use it in front of the Open Web Calendar to configure access and customize caching.

!!! note "Operating System"

    Squid is available for all major platforms.
    For the commands and paths of this tutorial, we assume you run Squid on Debain/Ubuntu.
    The commands might work on other systems, but that is not tested.

After you have installed the [Squid] Proxy, add this file into the  `conf.d` directory.
Squid will load it automatically then.

In Linux, create `/etc/squid/conf.d/open-web-calendar.conf`:

```sh
--8<-- "squid/open-web-calendar.conf"
```

The list above denies the Open Web Calendar access to all known local/internal networks.
If you have your own local network (IPv4 or IPv6), add it to the list above to be sure.

On Linux, you can install the file with this command:

```sh
sudo wget -O /etc/squid/conf.d/open-web-calendar.conf https://raw.githubusercontent.com/niccokunzmann/open-web-calendar/master/docs/snippets/squid/open-web-calendar.conf
```

Then, restart the squid proxy.

```sh
sudo service squid reload
```

Set the environment variables to tell the Open Web Calendar to use the Squid proxy installed on `localhost`.
Setting this variable changes depending on how you run the Open Web Calendar.

If you use the [Python Setup](../pypi), you can set the environment variables for the server like this:

```sh
export HTTP_PROXY="http://localhost:3128"
export HTTPS_PROXY="http://localhost:3128"
export ALL_PROXY="http://localhost:3128"
gunicorn open_web_calendar:app
```

When you try to access a forbidden calendar with the local `open-web-calendar`,
e.q. `http://172.16.0.1/calendar.ics`, you will see this error message:

> 403 Client Error: Forbidden for url: http://172.16.0.1/calendar.ics

[1]: ../pypi
[Squid]: https://www.squid-cache.org/
