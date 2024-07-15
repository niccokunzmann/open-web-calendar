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
      - ALLOWED_HOSTS=
    restart: unless-stopped
```

To deploy the Open Web Calendar with `docker compose`, follow these steps:

1. Copy the `docker-compose.yml` file to the directory from where you want to run the container.
2. If needed change the port mapping and [environment variables](../configure).
3. Start the container:

    ```sh
    docker compose up -d
    ```

4. The container will be pulled automatically from [Dockerhub] and then starts.

**Important Note:** If you use this service, consider setting up
[log rotation](https://ishitashah142.medium.com/why-rotating-docker-logs-is-important-how-to-rotate-docker-logs-840520e4c47)
as it is very talkative.

## Update pre-build image with Docker Compose

If you want to update your image with the latest version from [Dockerhub] run this:

```sh
docker compose pull
```

Note: You need to restart the container after pulling in order for the update to apply:

```sh
docker compose up -d
```

## Preventing SSRF attacks using a Tor proxy

The Open Web Calendar can be configured to use a proxy to request `.ics`
and other files. The following example shows the usage of a Tor proxy.
You can try it out at
[tor.open-web-calendar.hosted.quelltext.eu](https://tor.open-web-calendar.hosted.quelltext.eu/).

``` YAML
version: '3'
services:
  tor-open-web-calendar:
    image: niccokunzmann/open-web-calendar:master
    restart: unless-stopped
    environment:
    # use socks5h for *.onion
    # see https://stackoverflow.com/a/42972942/1320237
      - HTTP_PROXY=socks5h://tor-socks-proxy:9150
      - HTTPS_PROXY=socks5h://tor-socks-proxy:9150
      - ALL_PROXY=socks5h://tor-socks-proxy:9150
      - ALLOWED_HOSTS=
    # optional: create a private network so OWC cannot access the Internet directly
    networks:
      - no-internet-only-tor

  # from https://hub.docker.com/r/peterdavehello/tor-socks-proxy/
  tor-socks-proxy:
    image: peterdavehello/tor-socks-proxy # use :test for arm64
    restart: unless-stopped
    # optional: allow access to OWC and the Internet
    networks:
      - default
      - no-internet-only-tor

networks:
  default:
    ipam:
      driver: default
  no-internet-only-tor: # see https://stackoverflow.com/a/51964169/1320237
    driver: bridge
    internal: true

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
