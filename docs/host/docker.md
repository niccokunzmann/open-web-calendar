---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Host the Open Web Calendar using Docker and Docker Compose."
---

# Hosting with Docker

You can use `docker` and `docker compose` to host the Open Web Calendar.

## Build the Image

First, clone the repository:

```sh
git clone https://github.com/niccokunzmann/open-web-calendar
cd open-web-calendar
```

To build the container yourself, run:

```sh
docker build --tag niccokunzmann/open-web-calendar .
```

This will create the image `niccokunzmann/open-web-calendar`.

## Run the Docker Image

You can use the existing image:
[niccokunzmann/open-web-calendar][Dockerhub].

```sh
docker run -d --rm -p 5000:80 --name open-web-calendar niccokunzmann/open-web-calendar
```

Then, you should see your service running at [http://localhost:5000](http://localhost:5000).

This way, you can stop the service:

```shell
docker stop open-web-calendar
```

## Container Tags

The container `niccokunzmann/open-web-calendar:latest` contains the latest release.
Containers are also tagged with the version from the [changelog](../../changelog), e.g.
`niccokunzmann/open-web-calendar:v1.10`.

If you wish to run the latest development version, use `niccokunzmann/open-web-calendar:master`.
This includes unchecked translations.

## Docker Compose

Use the pre-build Dockerhub image with `docker compose`:

``` YAML
version: '3'
services:
  open-web-calendar:
    image: niccokunzmann/open-web-calendar
    ports:
      - '80:80'
    environment:
      - OWC_SPECIFICATION="{'privacy_policy':'http://link-to-my-privacy-policy'}"
      - WORKERS=4
    restart: unless-stopped
    networks:
      - owc-net

networks:
  owc-net: # shield the OWC from accessing other services (SSRF protection)
    ipam:
      driver: default  # give OWC Internet access
```

To deploy the Open Web Calendar with `docker compose`, follow these steps:

1. Copy the `docker-compose.yml` file to the directory from where you want to run the container.
2. If needed change the port mapping and [environment variables](../configure).
3. Start the container:

    ```sh
    docker compose up -d
    ```

4. The container will be pulled automatically from [Dockerhub] and then starts.

!!! note "Growing log files"

    If you use this service, consider setting up
    [log rotation](https://ishitashah142.medium.com/why-rotating-docker-logs-is-important-how-to-rotate-docker-logs-840520e4c47)
    as it is very talkative.

!!! note "IPv6"

    By default, docker only uses IPv4.
    You can [enable IPv6](https://docs.docker.com/engine/daemon/ipv6/).

## Update pre-build image with Docker Compose

If you want to update your image with the latest version from [Dockerhub] run this:

```sh
docker compose pull
```

Note: You need to restart the container after pulling in order for the update to apply:

```sh
docker compose up -d
```

## Preventing SSRF Attacks

The Open Web Calendar by default allows unrestricted access to the local network and Internet.
Adding a proxy to filter the requests is important, especially if you host other services which
should be not accessed by external requests.
Such an attack is called [Server Side Request Forgery](https://en.wikipedia.org/wiki/Server-side_request_forgery).

The Open Web Calendar can be configured to use a **proxy** to request `.ics` and other files.
Filtering traffic is a complicated task and out of scope for this project. Proxies do that well better!

### Preventing SSRF attacks using a Tor proxy

The following example shows the usage of a Tor proxy.
You can try it out at
[tor.open-web-calendar.hosted.quelltext.eu](https://tor.open-web-calendar.hosted.quelltext.eu/).

```yaml
--8<-- "tor/docker-compose.yml"
```

The configuration above prevents access to the internal network as the
requests are sent over the Tor network.
A bonus feature is that calendars can be accessed and hosted as a
Tor Hidden Service using an `.onion` address.
E.g. a calendar file can be served from a Raspberry Pi behind a home
network's firewall.
This [example calendar](https://tor.open-web-calendar.hosted.quelltext.eu/calendar.html?url=http%3A%2F%2F3nbwmxezp5hfdylggjjegrkv5ljuhguyuisgotrjksepeyc2hax2lxyd.onion%2Fone-day-event-repeat-every-day.ics) uses [this onion address](http://3nbwmxezp5hfdylggjjegrkv5ljuhguyuisgotrjksepeyc2hax2lxyd.onion/one-day-event-repeat-every-day.ics).

See also:

- [SSRF Protection with a Proxy Server](../configure#ssrf-protection-with-a-proxy-server)

## Preventing SSRF attacks using a Squid Proxy

The [Squid] proxy is a flexible and highly configurable proxy server.
The Open Web Calendar can be configured to use it to request `.ics` and other files.

Use this as your `docker-compose.yml` file:

```yaml
--8<-- "docker/docker-compose.yml"
```

And add the following `open-web-calendar.conf` file into the same directory.

```sh
--8<-- "docker/open-web-calendar.conf"
```

Then, you can start the service with this command:

```sh
docker compose up -d
```

When you try to access a forbidden calendar with the local `open-web-calendar`,
e.q. `http://172.16.0.1/calendar.ics`, you will see this error message:

> 403 Client Error: Forbidden for url: http://172.16.0.1/calendar.ics

## Automatic Updates

If you have not fixed your version but you use the `latest` or `master` tag,
you can automatically update all the services required.

Create an `update.sh` file next to your `docker-compose.yml` file and add this content:

```sh
#!/bin/bash
#
# update the services
#

cd "`dirname \"$0\"`"

docker compose pull
docker compose create
docker compose up -d --remove-orphans

# clean up
# see https://stackoverflow.com/a/46159681/1320237
docker system prune -a -f
docker rm -v $(docker ps -a -q -f status=exited)
docker rmi -f  $(docker images -f "dangling=true" -q)
  docker volume ls -qf dangling=true | xargs -r docker volume rm
```

Make `update.sh` executable.

```sh
chmod +x update.sh
```

Add a cron job to update everything at 3am daily (when there is an update).
Run this as the user who has access to the `docker` command:

```sh
crontab -e
```

And add this line:

```crontab
3 * * * * /path/to/update.sh 1> /path/to/update.sh.log 2> /path/to/update.sh.log
```

## Further Configuration

After you have set up your own server,
you can [configure the behavior](../configure).


[Dockerhub]: {{link.dockerhub}}
[Squid]: https://www.squid-cache.org/
